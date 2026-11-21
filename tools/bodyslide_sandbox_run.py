#!/usr/bin/env python3
"""Run one headless BodySlide batch build inside a bwrap sandbox (Xvfb, private Wine prefix).

Layout of a run directory (RUN, must be ASCII and outside every live MO2 root):
  RUN/tool/            merged BodySlide tool + resources (bodyslide_stage.py --out RUN/tool)
  RUN/prefix/          private WINEPREFIX (created on first build)
  RUN/home/            HOME inside the sandbox
  RUN/safe-fallback/   Config OutputDataPath; must stay empty
  RUN/rounds/<label>/  output/ (the -t target) and evidence/ (argv, logs, result.json)

Isolation: bwrap mounts / read-only, a private /tmp, /dev and /proc, unshares
network/PID/IPC/UTS and binds exactly one writable path, RUN. Inside RUN the tool
resources (SliderSets, ShapeData, presets, groups, exe, res, Config.xml) are bound
read-only again, so only Log_BS.txt, the prefix, HOME and the round can change.
Wine's Z: drive still maps /, but the whole host tree outside RUN is read-only.
Before anything runs, realpaths of RUN are checked against mods/, overwrite/,
profiles/, game Data and instance/ (bodyslide_guard.py); any overlap is refused.

On timeout the inner supervisor runs `wineserver -k` for this run's WINEPREFIX only,
then the outer process kills the bwrap session; the PID namespace takes every
remaining child with it. Nothing outside this process tree is signalled.

Example (from the parent repo root):
  python tools/bodyslide_sandbox_run.py build --run-dir /disk/bs-run --label a \
    --group 'Exact Group' --preset 'Exact Preset' --tri --mo2-dir /path/to/MO2 \
    --game-data /path/to/Skyrim/Data

Exit: 0 build verified (wine exit 0, no timeout, this round's log has the completion
line, output non-empty, safe-fallback empty, --expect-file all present);
1 build ran but a check failed (see result.json `failures`); 2 refused before running
(guard, missing tool, bad label, existing round, non-ASCII path, missing bwrap/Xvfb/wine).
Upstream completion strings: BodySlideApp.cpp (commit 033016464d31761bfaf6966db3ea9c3c3cb6105a)
CommandLineBuild 'All command-line build sets processed successfully!'; older builds
'All group build sets processed successfully!'.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bodyslide_guard as guard  # noqa: E402

COMPLETION = ('All command-line build sets processed successfully!',
              'All group build sets processed successfully!')
RO_ITEMS = ('SliderSets', 'ShapeData', 'SliderPresets', 'SliderGroups', 'SliderCategories',
            'ConversionSets', 'RefTemplates', 'res', 'lang', 'BodySlide.exe', 'Config.xml',
            'BuildSelection.xml')
LABEL = re.compile(r'^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$')
CONFIG = '''<Config>
  <TargetGame>4</TargetGame>
  <WarnMissingGamePath>false</WarnMissingGamePath>
  <BSATextureScan>false</BSATextureScan>
  <GameDataPath>.</GameDataPath>
  <OutputDataPath>{fallback}</OutputDataPath>
  <ProjectPath>.</ProjectPath>
  <GameRegKey/><GameRegVal/>
  <LogLevel>3</LogLevel>
  <Language>-1</Language>
</Config>
'''


def win_path(path: Path) -> str:
    """POSIX absolute path -> Wine Z: path with a trailing backslash."""
    return 'Z:' + str(path).replace('/', '\\').rstrip('\\') + '\\'


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def listing(root: Path):
    return [dict(path=p.relative_to(root).as_posix(), size=p.stat().st_size, sha256=sha256(p))
            for p in sorted(root.rglob('*')) if p.is_file()]


def bwrap_argv(run: Path, inner: list[str], env: dict[str, str]) -> list[str]:
    tool = run / 'tool'
    argv = ['bwrap', '--ro-bind', '/', '/', '--dev', '/dev', '--proc', '/proc',
            '--tmpfs', '/tmp', '--bind', str(run), str(run)]
    for item in RO_ITEMS:
        if (tool / item).exists():
            argv += ['--ro-bind', str(tool / item), str(tool / item)]
    argv += ['--unshare-net', '--unshare-pid', '--unshare-ipc', '--unshare-uts',
             '--die-with-parent', '--new-session', '--clearenv']
    for key, value in sorted(env.items()):
        argv += ['--setenv', key, value]
    return argv + ['--chdir', str(tool), '--'] + inner


def sandbox_env(run: Path) -> dict[str, str]:
    return {'PATH': os.environ.get('PATH', '/usr/bin:/bin'), 'HOME': str(run / 'home'),
            'WINEPREFIX': str(run / 'prefix'), 'WINEDEBUG': '-all',
            'WINEDLLOVERRIDES': 'mscoree,mshtml=', 'LIBGL_ALWAYS_SOFTWARE': '1',
            'LANG': 'C.UTF-8', 'XDG_CACHE_HOME': str(run / 'home' / '.cache')}


def wine_argv(args, output: Path) -> list[str]:
    argv = ['wine', 'BodySlide.exe', '-gbuild', args.group]
    if args.preset is not None:
        argv += ['-p', args.preset]
    if args.tri:
        argv.append('-tri')
    return argv + ['-t', win_path(output)]


def preflight(args):
    errors = []
    run = guard.real(args.run_dir)
    if guard.non_ascii(run):
        errors.append(f'run dir must be ASCII: {run}')
    if not LABEL.match(args.label):
        errors.append(f'label must match {LABEL.pattern}: {args.label!r}')
    roots, missing = guard.live_roots(args.mo2_dir, args.mods_dir, args.overwrite_dir,
                                      args.game_data, args.instance_dir, args.forbid)
    if missing:
        errors.append('live roots unknown (pass flags or env): ' + ', '.join(missing))
    errors += guard.check_isolated({'run-dir': run}, roots)
    if not (run / 'tool' / 'BodySlide.exe').is_file():
        errors.append(f'missing {run / "tool" / "BodySlide.exe"} (stage the tool into RUN/tool)')
    if (run / 'tool').is_symlink() or any((run / 'tool' / i).is_symlink() for i in RO_ITEMS):
        errors.append('tool dir items must be real copies, not symlinks')
    if (run / 'rounds' / args.label).exists():
        errors.append(f'round already exists (use a new label): {run / "rounds" / args.label}')
    fallback = run / 'safe-fallback'
    if fallback.exists() and any(fallback.iterdir()):
        errors.append(f'safe-fallback is not empty: {fallback}')
    for exe in ('bwrap', 'Xvfb', 'wine', 'wineserver'):
        if shutil.which(exe) is None:
            errors.append(f'{exe} not found on PATH')
    return run, roots, errors


def log_slice(log: Path, before: bytes):
    """Return (this round's bytes, mode).

    The local 5.8.2 build keeps a rolling Log_BS.txt: each session starts with a
    `[#Log <date>]` header and old sessions are trimmed (observed 2026-11-21), so a
    byte offset is not enough. Mode 'last-session' = bytes from the last header, which
    must not already be in the pre-run log ('stale' -> empty). Without headers, a
    byte-exact prefix means 'append'; otherwise the whole file is this round ('rewritten').
    """
    if not log.is_file():
        return b'', 'missing'
    data = log.read_bytes()
    start = data.rfind(b'[#Log ')
    if start >= 0:
        session = data[start:]
        return (b'', 'stale') if session in before else (session, 'last-session')
    if before and data.startswith(before):
        return data[len(before):], 'append'
    return data, 'rewritten' if before else 'new'


def evaluate(inner: dict, slice_text: str, outputs: list, fallback_files: list, expect: list):
    failures = []
    if inner.get('timed_out'):
        failures.append('wine timed out')
    if inner.get('wine_returncode') != 0:
        failures.append(f'wine exit {inner.get("wine_returncode")}')
    if not any(c in slice_text for c in COMPLETION):
        failures.append('completion line missing from this round of Log_BS.txt')
    if not outputs:
        failures.append('output directory is empty')
    if fallback_files:
        failures.append(f'safe-fallback received files: {fallback_files[:5]}')
    have = {o['path'].casefold() for o in outputs}
    failures += [f'expected output missing: {e}' for e in expect if e.replace('\\', '/').casefold() not in have]
    return failures


def build(args) -> int:
    run, roots, errors = preflight(args)
    if errors:
        print(json.dumps({'ok': False, 'stage': 'preflight', 'errors': errors}, indent=2))
        return 2
    tool, rnd = run / 'tool', run / 'rounds' / args.label
    output, evidence, fallback = rnd / 'output', rnd / 'evidence', run / 'safe-fallback'
    env = sandbox_env(run)
    inner_spec = dict(wine=None, timeout=args.timeout, init_timeout=args.init_timeout,
                      evidence=str(evidence), prefix=env['WINEPREFIX'])
    inner_cmd = [sys.executable, '-I', str(Path(__file__).resolve()), '_inner']
    plan = dict(run=str(run), live_roots={k: str(v) for k, v in roots.items()},
                wine_argv=wine_argv(args, output), bwrap_argv=None, cwd=str(tool))
    plan['bwrap_argv'] = bwrap_argv(run, inner_cmd + ['<spec.json>'], env)
    if args.dry_run:
        print(json.dumps(dict(ok=True, dry_run=True, **plan), ensure_ascii=False, indent=2))
        return 0
    for d in (run / 'home', run / 'prefix', fallback, run / 'rounds'):
        d.mkdir(parents=True, exist_ok=True)
    rnd.mkdir()
    output.mkdir()
    evidence.mkdir()
    staged = tool / 'Config.staged.xml'
    if (tool / 'Config.xml').is_file() and not staged.exists():
        shutil.copy2(tool / 'Config.xml', staged)
    (tool / 'Config.xml').write_text(CONFIG.format(fallback=win_path(fallback)), encoding='utf-8')
    log = tool / 'Log_BS.txt'
    before = log.read_bytes() if log.is_file() else b''
    offset = len(before)
    inner_spec['wine'] = plan['wine_argv']
    spec_path = evidence / 'inner-spec.json'
    spec_path.write_text(json.dumps(inner_spec, ensure_ascii=False, indent=2), encoding='utf-8')
    argv = bwrap_argv(run, inner_cmd + [str(spec_path)], env)
    plan.update(bwrap_argv=argv, log_offset=offset, started=time.strftime('%Y-%m-%dT%H:%M:%S%z'))
    (evidence / 'command.json').write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding='utf-8')
    outer_timeout = args.init_timeout + args.timeout + 90
    proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    outer = dict(pid=proc.pid, timed_out=False)
    try:
        out, err = proc.communicate(timeout=outer_timeout)
    except subprocess.TimeoutExpired:
        outer['timed_out'] = True
        os.killpg(proc.pid, signal.SIGKILL)  # our own session only; PID namespace reaps the rest
        out, err = proc.communicate()
    outer['returncode'] = proc.returncode
    (evidence / 'sandbox.stdout').write_bytes(out)
    (evidence / 'sandbox.stderr').write_bytes(err)
    inner_path = evidence / 'inner-result.json'
    inner = json.loads(inner_path.read_text()) if inner_path.is_file() else {'missing': True}
    data, log_mode = log_slice(log, before)
    offset = len(log.read_bytes()) - len(data) if log.is_file() else 0
    (evidence / 'log-slice.txt').write_bytes(data)
    text = data.decode('utf-8', 'replace')
    outputs = listing(output)
    fallback_files = [p.relative_to(fallback).as_posix() for p in fallback.rglob('*')]
    failures = evaluate(inner, text, outputs, fallback_files, args.expect_file or [])
    if outer['timed_out']:
        failures.append('outer sandbox timeout')
    result = dict(ok=not failures, label=args.label, failures=failures, outer=outer, inner=inner,
                  log_byte_range=[offset, offset + len(data)], log_mode=log_mode,
                  processed=re.findall(r"Processing '([^']*)'", text),
                  outputs=outputs, safe_fallback_files=fallback_files)
    (evidence / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: result[k] for k in ('ok', 'label', 'failures', 'processed')}
                     | {'outputs': len(outputs), 'evidence': str(evidence)}, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


def _run_logged(argv, evidence: Path, name: str, timeout: int, env=None):
    with open(evidence / f'{name}.stdout', 'wb') as o, open(evidence / f'{name}.stderr', 'wb') as e:
        p = subprocess.Popen(argv, stdout=o, stderr=e, env=env, start_new_session=True)
        try:
            return p.wait(timeout=timeout), False
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            return p.returncode, True


def inner(spec_path: str) -> int:
    """Runs inside the sandbox: own Xvfb, optional prefix init, one BodySlide build."""
    spec = json.loads(Path(spec_path).read_text(encoding='utf-8'))
    evidence = Path(spec['evidence'])
    res = dict(started=time.time())
    r, w = os.pipe()
    xvfb = subprocess.Popen(['Xvfb', '-displayfd', str(w), '-screen', '0', '1280x1024x24',
                             '-nolisten', 'tcp', '-extension', 'GLX'], pass_fds=(w,),
                            stdout=subprocess.DEVNULL, stderr=open(evidence / 'xvfb.stderr', 'wb'))
    os.close(w)
    display = b''
    deadline = time.time() + 30
    os.set_blocking(r, False)
    while time.time() < deadline and not display.endswith(b'\n'):
        try:
            display += os.read(r, 64)
        except BlockingIOError:
            time.sleep(0.1)
    os.close(r)
    try:
        if not display.strip():
            res['error'] = 'Xvfb did not report a display'
            return 1
        env = dict(os.environ, DISPLAY=':' + display.decode().strip())
        res['display'] = env['DISPLAY']
        if not (Path(spec['prefix']) / 'system.reg').exists():
            res['wineboot_returncode'], res['wineboot_timed_out'] = _run_logged(
                ['wineboot', '-i'], evidence, 'wineboot', spec['init_timeout'], env)
            _run_logged(['wineserver', '-w'], evidence, 'wineserver-init', 60, env)
        res['wine_argv'] = spec['wine']
        t0 = time.time()
        res['wine_returncode'], res['timed_out'] = _run_logged(spec['wine'], evidence, 'wine', spec['timeout'], env)
        res['wine_seconds'] = round(time.time() - t0, 1)
        if res['timed_out']:
            res['wineserver_kill'] = _run_logged(['wineserver', '-k'], evidence, 'wineserver-kill', 30, env)[0]
        res['wineserver_wait'], wait_timeout = _run_logged(['wineserver', '-w'], evidence, 'wineserver-wait', 60, env)
        if wait_timeout:
            res['wineserver_kill_after_wait'] = _run_logged(['wineserver', '-k'], evidence, 'wineserver-kill2', 30, env)[0]
        return 0
    finally:
        xvfb.terminate()
        try:
            res['xvfb_returncode'] = xvfb.wait(timeout=10)
        except subprocess.TimeoutExpired:
            xvfb.kill()
            res['xvfb_returncode'] = xvfb.wait()
        res['finished'] = time.time()
        (evidence / 'inner-result.json').write_text(json.dumps(res, indent=2), encoding='utf-8')


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if argv[:1] == ['_inner']:
        return inner(argv[1])
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='cmd', required=True)
    b = sub.add_parser('build', help='one sandboxed BodySlide -gbuild round')
    b.add_argument('--run-dir', required=True, type=Path)
    b.add_argument('--label', required=True, help='new round name (a, b, b-repeat ...)')
    b.add_argument('--group', required=True, help='exact SliderGroups group name')
    b.add_argument('--preset', help='exact preset name for -p (omit for OSP defaults route)')
    b.add_argument('--tri', action='store_true', help='pass -tri')
    b.add_argument('--timeout', type=int, default=120, help='seconds for BodySlide itself')
    b.add_argument('--init-timeout', type=int, default=300, help='seconds for first wineboot')
    b.add_argument('--expect-file', action='append', help='relative output path that must exist')
    for flag in ('--mo2-dir', '--mods-dir', '--overwrite-dir', '--game-data', '--instance-dir'):
        b.add_argument(flag, type=Path)
    b.add_argument('--forbid', action='append', type=Path, default=[], help='extra live root to refuse')
    b.add_argument('--dry-run', action='store_true', help='check and print argv only')
    args = parser.parse_args(argv)
    return build(args)


if __name__ == '__main__':
    sys.exit(main())
