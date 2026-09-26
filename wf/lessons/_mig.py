import os,re,sys,json
M='/home/lorkhan/.claude/projects/-home-lorkhan-repo-moddings-skyrim/memory'
OUT='/home/lorkhan/repo/moddings/skyrim/wf/lessons'
T={
'user-preferences':('使用者偏好與邊界','reply-in-traditional-chinese top-level-explain-in-plain-words dont-inflate-light-preferences answer-should-we-with-a-threshold investigate-all-then-install-once send-screenshots-to-session notes-agent-minimal-contact dont-clutter-home-with-agent-output check-clock-dont-estimate-time artifact-republish-needs-read-first'),
'dispatch-and-agents':('調度、模型分級與交接書','im-dispatcher-codex-implements dispatcher-must-use-own-assistants fable-top-handles-only-hardest fable-top-opus-middle-management model-tiers-and-headcount prefer-gpt-sol-for-all-tasks delegate-simple-work-to-sonnet trust-gpt-sol-more rush-mode-parallel-opus-agent-lines leads-manage-subordinate-context leads-must-not-end-turn-to-wait handoff-scope-words-expand handoff-must-split-no-evidence-from-negative-evidence verify-waituser-against-logs driving-other-cli-agents codex-tmux-operational-notes codex-tmux-enter-must-be-verified tmux-working-text-is-not-liveness throttle-by-tree-not-by-name'),
'locks-screen-and-game':('鎖、螢幕與開遊戲','user-present-screen-is-still-usable gd-libs-session-coexistence launch-skyrim-via-steam skyrim-no-appmanifest-steam-safe verify-game-alive-via-qa-not-ps alt-tab-during-loading-deadlocks agent-driven-nexus-download'),
'git-and-repos':('版控、repo 佈局與文件整理','workspace-not-a-git-repo workspace-layout-and-duties push-and-remote-actions profiles-repo-has-remote gitlink-is-a-commit-not-a-branch commit-explicit-paths-only pathspec-commit-drops-untrack profile-promote-switches-worktree handoffs-junk-not-tracked-periodic-hygiene user-facing-pages-go-in-wf-user run-tests-in-worktree-not-main-tree archive-obsolete-and-unlink kernel-tools-not-mcp-not-skill wf-kernel-upstream-and-upgrade'),
'mo2-profiles':('MO2 與 profile','profile-restore-order-and-flags mo2-first-launch-drops-new-plugin-star mo2-auto-adds-stray-mods-dirs mo2-phantom-profile-workflows-dir dsport-dev-profile-drift rs-children-missing-esp fomod-install-tooling cc-download-lands-in-cwd-data rule-out-a-concept-scan-same-batch-siblings dyndolod-esp-masters-pin-content-mods'),
'housecarl-and-tools':('houseCARL、xEdit、DynDOLOD 等工具坑','housecarl-setfield-cjk-byte-drop housecarl-cannot-point-real-mo2-instance housecarl-merge-facegen-backslash-filename missing-master-scan-mast-not-housecarl bsa-voice-index-false-negative nexus-api-version-is-not-proof xedit-linux-needs-ascii-data-root dyndolod-runtime-and-traps vanilla-masters-cleaned-in-data'),
'faces-followers-bodies':('臉、隨從、身體與動畫','voiced-follower-makeover-project look-transplant-workflow-and-picker hide-donor-after-look-transplant facegen-verify-size-md5-not-existence look-layer-must-carry-hdpt-flst-clfm hdpt-edid-must-match-facegen-shape-names facegen-headpart-count-mismatch-discards-facegen custom-race-blocks-facegen-load face-bugs-check-real-actor-and-upstream-fomod outfit-hair-slot-hides-headparts bodyslide-wine-preset-empty-nam7-weight daegon-2212-midsave-upgrade oar-copy-folder-bypasses-gates oar-non-ascii-animation-dir-kills-cache oar-root-disabled-misses-subfolder-variants'),
'crash-triage':('CTD 真因與判法','upstream-skse-dll-fix-via-fork-ci le-collision-nif-precision-crash pepe-tls-end-crash-is-payloadinterpreter-dangling-listener doomperk-advanceobject-block-ctd spid-outfit-manager-live-inventory-reset-ctd daegon-itemfinding-script-ctd custom-navm-combat-pathing-ctd achr-base-must-be-npc-not-lvln gltf2nif-effect-shader-ctd'),
'translation-and-zh':('翻譯與中文層','translation-layer-cost-threshold no-cht-chs-preference chinese-diff-ok-but-no-tofu slanguage-english-chinese-in-english-slot zh-layer-gate-base-mod-must-be-enabled zhport-editorid-fallback-and-hdpt-untranslatable apocalypse-rebuild-waits-new-playthrough'),
'project-decisions':('專案裁示與地圖／內容限制','dsport-render-constraints stat-zero-obnd-culls-large-statics bloodchill-inigo-land-dirty-edit avif-perktree-overridden-by-non-overhaul-mods'),
}
MACHINE='interactive-grep-is-ugrep pgrep-self-match-beyond-brackets'.split()
STALE='overnight-agent-fleet-2026-08-20 aetheria-agent-coexistence'.split()
allf=sorted(f[:-3] for f in os.listdir(M) if f.endswith('.md') and f not in('MEMORY.md','this-machine.md'))
mapped={s:t for t,(_,l) in T.items() for s in l.split()}
for s in MACHINE+STALE: mapped[s]='-'
miss=[f for f in allf if f not in mapped]; extra=[s for s in mapped if s not in allf]
print('files',len(allf),'miss',miss,'extra',extra)
if miss or extra: sys.exit(1)
def parse(slug):
    t=open(f'{M}/{slug}.md').read()
    m=re.match(r'---\n(.*?)\n---\n(.*)',t,re.S)
    fm,body=m.group(1),m.group(2).strip()
    d=re.search(r'^description:\s*(.*)$',fm,re.M).group(1).strip()
    ty=re.search(r'type:\s*(\w+)',fm).group(1)
    body=re.sub(r'^(#+) ',lambda x:'#'+x.group(1)+' ',body,flags=re.M)
    body=re.sub(r'^(#{2}) ','### ',body,flags=re.M)
    body=re.sub(r'\[([^\]]*)\]\(([a-z0-9-]+)\.md\)',lambda x:f'{x.group(1)}（條目 `{x.group(2)}`）',body)
    return d,ty,body
LIMIT=7900
os.makedirs(OUT,exist_ok=True)
files={}
for topic,(title,l) in T.items():
    chunks=[[]];
    for slug in l.split():
        d,ty,body=parse(slug)
        sec=f'## {slug}\n\n> {d}（原 type: {ty}）\n\n{body}\n'
        cur=chunks[-1]
        if cur and sum(len(x.encode()) for x in cur)+len(sec.encode())+300>LIMIT: chunks.append([]); cur=chunks[-1]
        cur.append(sec)
    n=len(chunks)
    for i,c in enumerate(chunks):
        name=topic+('' if i==0 else f'-{i+1}')
        hdr=f'# {title}'+(f'（{i+1}/{n}）' if n>1 else '')+'\n\n[lessons 索引](README.md)'
        if n>1: hdr+='｜同主題：'+'、'.join(f'[{topic+("" if j==0 else f"-{j+1}")}]({topic+("" if j==0 else f"-{j+1}")}.md)' for j in range(n) if j!=i)
        hdr+='\n\n'
        open(f'{OUT}/{name}.md','w').write(hdr+'\n'.join(c))
        files[name]=(title,[s.split('\n')[0][3:] for s in c])
json.dump(files,open('/tmp/claude-1000/-home-lorkhan-repo-moddings-skyrim/6c153478-99cc-4767-a691-ef13c5e4f465/scratchpad/files.json','w'),ensure_ascii=False,indent=1)
print(sum(len(v[1]) for v in files.values()))
for k,v in files.items(): print(k,len(v[1]),os.path.getsize(f'{OUT}/{k}.md'))
