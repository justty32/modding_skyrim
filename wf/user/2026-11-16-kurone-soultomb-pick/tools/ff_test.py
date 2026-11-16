#!/usr/bin/env python3
"""Headless Firefox (Marionette) smoke test of the pick page. Fresh profile, records its own pid.

Usage: python3 -I ff_test.py PAGE.html OUTDIR
"""
import base64, json, os, socket, subprocess, sys, time
from pathlib import Path

page, outdir = Path(sys.argv[1]).resolve(), Path(sys.argv[2])
outdir.mkdir(parents=True, exist_ok=True)
prof = outdir / "ffprofile"
prof.mkdir(exist_ok=True)
(prof / "user.js").write_text('user_pref("marionette.port", 28311);\nuser_pref("browser.shell.checkDefaultBrowser", false);\n'
                              'user_pref("datareporting.policy.dataSubmissionEnabled", false);\n'
                              'user_pref("toolkit.telemetry.reportingpolicy.firstRun", false);\n')
proc = subprocess.Popen(["firefox", "--headless", "--marionette", "--no-remote", "--profile", str(prof),
                         "--window-size=1600,1100"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
(outdir / "firefox.pid").write_text(str(proc.pid))


class M:
    def __init__(self):
        for _ in range(60):
            try:
                self.s = socket.create_connection(("127.0.0.1", 28311), timeout=60)
                break
            except OSError:
                time.sleep(0.5)
        self.buf = b""
        self.mid = 0
        self.read()

    def read(self):
        while b":" not in self.buf:
            self.buf += self.s.recv(65536)
        n, rest = self.buf.split(b":", 1)
        n = int(n)
        while len(rest) < n:
            rest += self.s.recv(1 << 20)
        self.buf = rest[n:]
        return json.loads(rest[:n])

    def cmd(self, name, params=None):
        self.mid += 1
        msg = json.dumps([0, self.mid, name, params or {}]).encode()
        self.s.sendall(str(len(msg)).encode() + b":" + msg)
        r = self.read()
        if r[2]:
            raise RuntimeError(r[2])
        return r[3]


TEST = r"""
const done = arguments[arguments.length - 1];
(async () => {
  const out = {errors: window.__errs || []};
  const $ = id => document.getElementById(id);
  const rows = [...document.querySelectorAll('#target-rows tr')];
  out.rows = rows.length;
  out.visible_default = rows.filter(r => !r.hidden).length;
  out.counts_text = $('visible-count').textContent;
  out.fatal_hidden = $('fatal').hidden;
  const fem = rows.filter(r => !r.hidden);
  const dsel = r => r.querySelector('select[data-part=donor]');
  const bsel = r => r.querySelector('select[data-part=body]');
  out.female_row0_donor_options = dsel(fem[0]).options.length;
  // pick same donor for two female rows
  const did = [...dsel(fem[0]).options].find(o => o.value).value;
  for (const r of [fem[0], fem[1]]) { dsel(r).value = did; dsel(r).dispatchEvent(new Event('change', {bubbles: true})); }
  out.dup_rows = rows.filter(r => r.classList.contains('duplicate')).length;
  out.dup_badge = fem[0].querySelector('.badge.red') ? fem[0].querySelector('.badge.red').textContent : null;
  // male row: body rimlydia
  $('sex-filter').value = '男'; $('sex-filter').dispatchEvent(new Event('change'));
  const male = rows.filter(r => !r.hidden);
  out.visible_male = male.length;
  bsel(male[0]).value = 'rimlydia'; bsel(male[0]).dispatchEvent(new Event('change', {bubbles: true}));
  out.male_badges = [...male[0].querySelectorAll('.badge')].map(b => b.textContent);
  out.male_donor_options_default = dsel(male[0]).options.length;
  $('donor-all-sexes').checked = true; $('donor-all-sexes').dispatchEvent(new Event('change'));
  out.male_donor_options_all = dsel(male[0]).options.length;
  // cross-sex pick, then turn toggle off: selection must remain
  const femDonor = [...dsel(male[0]).options].find(o => o.parentNode.label === '主要角色・女').value;
  dsel(male[0]).value = femDonor; dsel(male[0]).dispatchEvent(new Event('change', {bubbles: true}));
  $('donor-all-sexes').checked = false; $('donor-all-sexes').dispatchEvent(new Event('change'));
  out.cross_sex_kept = dsel(male[0]).value === femDonor;
  out.cross_badges = [...male[0].querySelectorAll('.badge')].map(b => b.textContent);
  // export
  const exp = JSON.parse($('export-json').value);
  out.export_keys = Object.keys(exp);
  out.export_picks = exp.picks.length;
  out.export_pick0_keys = Object.keys(exp.picks[0]);
  out.export_sample = exp.picks.slice(0, 2);
  out.storage = localStorage.getItem('kurone-soultomb-pick/v1');
  // clear then import
  window.confirm = () => true;
  $('clear').click();
  out.after_clear = JSON.parse($('export-json').value).picks.length;
  const dt = new DataTransfer();
  dt.items.add(new File([JSON.stringify(exp)], 'x.json', {type: 'application/json'}));
  $('import-file').files = dt.files;
  $('import-file').dispatchEvent(new Event('change'));
  await new Promise(r => setTimeout(r, 800));
  const back = JSON.parse($('export-json').value);
  const strip = o => JSON.stringify(o.picks);
  out.import_roundtrip_equal = strip(back) === strip(exp);
  out.import_status = $('action-status').textContent;
  $('sex-filter').value = '女'; $('sex-filter').dispatchEvent(new Event('change'));
  out.errors = window.__errs || [];
  done(out);
})().catch(e => done({fatal: String(e), stack: e.stack}));
"""

m = None
try:
    m = M()
    m.cmd("WebDriver:NewSession", {"capabilities": {"alwaysMatch": {"acceptInsecureCerts": True}}})
    m.cmd("WebDriver:Navigate", {"url": page.as_uri()})
    time.sleep(1.5)
    shot = m.cmd("WebDriver:TakeScreenshot", {"full": False})
    (outdir / "default.png").write_bytes(base64.b64decode(shot["value"]))
    res = m.cmd("WebDriver:ExecuteAsyncScript", {"script": TEST, "args": [], "scriptTimeout": 30000})
    (outdir / "result.json").write_text(json.dumps(res["value"], ensure_ascii=False, indent=1))
    shot = m.cmd("WebDriver:TakeScreenshot", {"full": False})
    (outdir / "after.png").write_bytes(base64.b64decode(shot["value"]))
    print(json.dumps(res["value"], ensure_ascii=False, indent=1))
    try:
        m.cmd("Marionette:Quit", {"flags": ["eForceQuit"]})
    except Exception:
        pass
finally:
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.terminate()  # our own recorded child pid only
        proc.wait(timeout=10)
