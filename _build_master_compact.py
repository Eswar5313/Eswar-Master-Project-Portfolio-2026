#!/usr/bin/env python3
"""Compact rebuild of Eswar-Master-Project-Portfolio-2026: one dashboard page (hash-routed track/project views),
projects.json registry (103 projects), README with full index. ≤ 8 files so it uploads via GitHub web in one go."""
import json, re, html, os, shutil
E = html.escape
HANDLE = "Eswar5313"; REPO = "Eswar-Master-Project-Portfolio-2026"; CODEC = "Codec-Technologies-Internship-Portfolio-2026"; LENS = "Eswar-Portfolio-Lens-Index-2026"
OWNER = "Eswar Mahalingam"; GH = f"https://github.com/{HANDLE}"; PAGES = f"https://{HANDLE.lower()}.github.io/{REPO}"; CODEC_PAGES = f"https://{HANDLE.lower()}.github.io/{CODEC}"
OUT = "/home/claude/work/master"; shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
reg = json.load(open("/root/.claude/uploads/4ad55d60-1b47-5ed5-8770-d68a3d79de72/6d7077da-projects.json"))
tracks_codec = {t["id"]: t for t in json.load(open("/tmp/tracks.json"))}

# ---- refresh tracks
for t in reg["tracks"]:
    if t["key"] == "hexa": t["role"] = "Data Analyst (Internship, Jun–Sep 2026)"
    if t["key"] == "codec":
        t["slug"] = "04-Codec-Technologies-Internship"; t["title"] = "Codec Technologies — 4 Internship Tracks (50)"
        t["tagline"] = "EV 10 · Cyber Security 20 · Digital Electronics & VLSI 10 · Robotics & Automation 10 — 595+ automated tests, one engineering-report PDF per project; unavailable tools declared as substitutions"
        t["role"] = "Intern — Electric Vehicle · Cyber Security · Digital Electronics & VLSI · Robotics & Automation (Aug 2026–Present)"
        t["evidence_repo"] = f"{GH}/{CODEC}"
        newp = []
        for tid, prefix, folder in (("ev", "EV", "Electric-Vehicle"), ("cyber", "Cyber", "Cyber-Security"), ("vlsi", "VLSI", "Digital-Electronics-VLSI"), ("robo", "Robotics", "Robotics-Automation")):
            for c in tracks_codec[tid]["cards"]:
                newp.append(dict(slug=f"{prefix.upper()}-{c['num']}-{c['folder'][3:]}", title=f"{prefix} {c['num']} — {c['title']}", summary=c["desc"],
                    results=[f"{k}: {v}" for k, v in c["metrics"]], tools=c["chips"][:5], files=[f"reports/{c['folder']}.pdf", "source zip → " + c["folder"] + "/"],
                    tags=[{"ev": "EV", "cyber": "Cyber", "vlsi": "VLSI", "robo": "Robotics"}[tid], "Codec"] + c["chips"][:2],
                    evidence=f"{GH}/{CODEC}/blob/main/{folder}/reports/{c['folder']}.pdf", page=f"{CODEC_PAGES}/#{tid}-{c['num']}", new=tid in ("vlsi", "robo")))
        t["projects"] = newp
for t in reg["tracks"]:
    for p in t["projects"]:
        p.setdefault("evidence", ""); p.setdefault("new", False)
reg["total"] = sum(len(t["projects"]) for t in reg["tracks"]); N = reg["total"]; assert N == 103, N
reg["handle"] = HANDLE; reg["pages"] = PAGES
json.dump(reg, open(f"{OUT}/projects.json", "w"), indent=1, ensure_ascii=False)

CSS = open("/tmp/lens_css.txt").read() + """
.trk{margin:26px 0;scroll-margin-top:90px}.trk h2{font-size:22px;color:var(--navy);border-left:5px solid var(--gold);padding-left:12px}.trk .sub{color:var(--muted);font-size:13.5px;margin:6px 0 12px 17px}
.card .links{display:flex;gap:6px;margin-top:8px;flex-wrap:wrap}.card .links a{font-size:11.5px;font-weight:600;padding:4px 9px;border-radius:5px;background:var(--navy);color:#fff}.card .links a.alt{background:#fff;color:var(--navy);border:1px solid var(--navy)}.card .links a.dis{background:#eee;color:#888;border:1px solid #ddd;pointer-events:none}
.new{display:inline-block;background:var(--gold);color:var(--navy);font-size:10px;font-weight:700;border-radius:4px;padding:1px 6px;margin-left:6px;vertical-align:middle}
.detail{display:block;background:#fff;border-radius:12px;padding:22px;border-top:5px solid var(--gold);box-shadow:0 1px 4px rgba(10,31,68,.1)}.detail h2{font-size:24px;color:var(--navy);margin:10px 0 4px}.detail .crumb{font-size:12px;letter-spacing:.08em;text-transform:uppercase}.detail .crumb a{color:var(--gold)}.detail table{border-collapse:collapse;width:100%;margin-top:12px;font-size:13.5px}.detail td{border-bottom:1px solid var(--line);padding:8px 6px;vertical-align:top}.detail td:first-child{width:160px;color:var(--muted);font-weight:600}
.tt{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:14px 0}.tt a{background:#fff;border-radius:10px;border-top:4px solid var(--gold);padding:12px 14px;box-shadow:0 1px 4px rgba(10,31,68,.1)}.tt b{display:block;color:var(--navy);font-size:15px}.tt span{font-size:12.5px;color:var(--muted)}"""
FONTS = '<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">'
chips = "".join(f'<button class="chip" data-t="{t["slug"]}">{E(t["title"].split(" — ")[0])} <b>{len(t["projects"])}</b></button>' for t in reg["tracks"])
page = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{OWNER} — Master Project Portfolio 2026</title>{FONTS}<style>{CSS}</style></head><body>
<header class="top"><div class="wrap"><div class="crumb">Master Project Portfolio · 2026</div><h1>{OWNER} — every project, one dashboard</h1>
<p class="lead">{N} projects across {len(reg['tracks'])} tracks. Filter by track or tag, search by tool, open any card for its full record and evidence link. <span class="new">NEW</span> 20 Digital Electronics &amp; VLSI and Robotics &amp; Automation projects added Sep 2026.</p>
<div class="kpis"><div class="kpi"><b>{N}</b><span>Projects</span></div><div class="kpi"><b>{len(reg['tracks'])}</b><span>Tracks</span></div><div class="kpi"><b>50</b><span>Engineering projects with report PDFs</span></div><div class="kpi"><b>595+</b><span>Automated tests (Codec)</span></div><div class="kpi"><b>20k+</b><span>Live Excel formulas</span></div><div class="kpi"><b>0</b><span>Unverified figures printed</span></div></div>
<div class="btnrow"><a class="btn" href="{GH}/{CODEC}">Codec portfolio (files)</a><a class="btn" href="https://{HANDLE.lower()}.github.io/{LENS}/">Lens index (by skill · tool · sector · role)</a><a class="btn ghost" href="README.md">README</a><a class="btn ghost" href="projects.json">projects.json</a></div></div></header>
<div class="bar"><div class="wrap"><input id="q" type="search" placeholder="Search projects, tools, tags…"><div class="lens"><button class="chip on" data-t="">All tracks</button>{chips}</div><span style="font-size:13px;color:var(--muted)">Showing <b id="count"></b></span></div></div>
<main><div class="wrap" id="root"></div></main>
<div class="foot"><div class="wrap">© 2026 {OWNER} · Evidence for the 50 Codec projects is in <a href="{GH}/{CODEC}">{CODEC}</a>; data, product and Internship Studio deliverables are attached per project as they are published (see each card's Evidence button).</div></div>
<script>const R={json.dumps(reg, ensure_ascii=False)};const q=document.getElementById('q');let trk='';
const slug=s=>s.replace(/[^A-Za-z0-9]+/g,'-').replace(/^-|-$/g,'');
function card(t,p){{const ev=p.evidence?`<a href="${{p.evidence}}">Evidence</a>`:`<a class="dis">Evidence — to be attached</a>`;return `<article class="card"><div class="id">${{t.title.split(' — ')[0]}}${{p.new?'<span class="new">NEW</span>':''}}</div><h3>${{p.title}}</h3><p>${{p.summary}}</p>${{p.results&&p.results.length?`<div class="res">▸ ${{p.results[0]}}</div>`:''}}<div class="tags">${{p.tools.slice(0,5).map(x=>`<span>${{x}}</span>`).join('')}}</div><div class="links"><a class="alt" href="#${{t.slug}}/${{p.slug}}">Details</a>${{ev}}${{p.page?`<a class="alt" href="${{p.page}}">Page</a>`:''}}</div></article>`}}
function home(){{const s=q.value.trim().toLowerCase();let shown=0;const parts=[];
if(!trk&&!s)parts.push(`<div class="tt">${{R.tracks.map(t=>`<a href="#${{t.slug}}"><b>${{t.title}}</b><span>${{t.projects.length}} projects · ${{t.tagline}}</span></a>`).join('')}}</div>`);
R.tracks.forEach(t=>{{if(trk&&t.slug!==trk)return;const ps=t.projects.filter(p=>!s||(p.title+' '+p.summary+' '+p.tools.join(' ')+' '+p.tags.join(' ')+' '+(p.results||[]).join(' ')).toLowerCase().includes(s));if(!ps.length)return;shown+=ps.length;
parts.push(`<section class="trk" id="t-${{t.slug}}"><h2>${{t.title}} <span class="n" style="font-size:13px;color:var(--muted);font-weight:400">${{ps.length}} project${{ps.length>1?'s':''}}</span></h2><div class="sub">${{t.tagline}} · <i>${{t.role}}</i>${{t.evidence_repo?` · <a href="${{t.evidence_repo}}">evidence repo</a>`:''}}</div><div class="grid">${{ps.map(p=>card(t,p)).join('')}}</div></section>`)}});
document.getElementById('root').innerHTML=parts.join('')||'<div class="empty">No projects match.</div>';document.getElementById('count').textContent=shown;
document.querySelectorAll('.chip').forEach(x=>x.classList.toggle('on',x.dataset.t===trk));}}
function detail(t,p){{const rows=[['Track',t.title],['Role / programme',t.role+' · '+t.org],['Summary',p.summary],['Results',(p.results||[]).map(r=>'▸ '+r).join('<br>')],['Tools',p.tools.join(' · ')],['Tags',p.tags.join(' · ')],['Files',(p.files||[]).join('<br>')],['Evidence',p.evidence?`<a href="${{p.evidence}}">${{p.evidence}}</a>`:'To be attached — see README §Evidence']];
document.getElementById('root').innerHTML=`<div class="detail"><div class="crumb"><a href="#">← All tracks</a> / <a href="#${{t.slug}}">${{t.title.split(' — ')[0]}}</a></div><h2>${{p.title}}${{p.new?'<span class="new">NEW</span>':''}}</h2><table>${{rows.map(([k,v])=>`<tr><td>${{k}}</td><td>${{v}}</td></tr>`).join('')}}</table>${{p.page?`<p style="margin-top:14px"><a class="btn" href="${{p.page}}">Open project page</a></p>`:''}}</div>`;document.getElementById('count').textContent=1;}}
function route(){{const h=decodeURIComponent(location.hash.slice(1));const [ts,ps]=h.split('/');const t=R.tracks.find(x=>x.slug===ts);trk=t?ts:'';if(t&&ps){{const p=t.projects.find(x=>x.slug===ps);if(p){{detail(t,p);return}}}}home();window.scrollTo(0,0);}}
document.querySelectorAll('.chip').forEach(b=>b.onclick=()=>{{location.hash=b.dataset.t?'#'+b.dataset.t:'#'}});q.oninput=home;addEventListener('hashchange',route);route();</script></body></html>"""
open(f"{OUT}/index.html", "w").write(page); open(f"{OUT}/.nojekyll", "w").write("")

# ---- README
R = [f"""<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0A1F44,100:C9A227&height=170&section=header&text=Eswar%20Mahalingam&fontSize=42&fontColor=ffffff&desc=Master%20Project%20Portfolio%20%C2%B7%202026&descAlignY=72&descSize=18" width="100%"/>

**{N} projects · {len(reg['tracks'])} tracks · one navigable dashboard**

[![Dashboard](https://img.shields.io/badge/Open-Live%20Dashboard-C9A227?style=for-the-badge&logo=githubpages&logoColor=0A1F44)]({PAGES}/)
[![Projects](https://img.shields.io/badge/Projects-{N}-0A1F44?style=for-the-badge)](#tracks)
[![Codec](https://img.shields.io/badge/Codec%20engineering%20projects-50%20·%20595%2B%20tests-138808?style=for-the-badge)]({GH}/{CODEC})
[![Lens](https://img.shields.io/badge/Lens%20index-by%20skill%20·%20tool%20·%20sector-0A1F44?style=for-the-badge)]({GH}/{LENS})
[![LinkedIn](https://img.shields.io/badge/LinkedIn-eswar--mahalingam-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/eswar-mahalingam)

</div>

> **Start here → [the dashboard]({PAGES}/).** Filter by track, search by tool, open any card for the full record. Project pages are URL routes on the one dashboard (`#track/project`), so this repository stays small enough to upload in a single step and never breaks a link.

## 🆕 Recent additions (September 2026)

| Added | Scale | Where |
|---|:-:|---|
| Digital Electronics & VLSI track — Verilog/VHDL RTL, Yosys + nextpnr place-and-route, own RTL-to-GDSII flow | 10 projects | [Codec portfolio]({GH}/{CODEC}/tree/main/Digital-Electronics-VLSI) |
| Robotics & Automation track — A*/SLAM/PID/Kalman/IK simulations with OpenCV, 143 tests | 10 projects | [Codec portfolio]({GH}/{CODEC}/tree/main/Robotics-Automation) |
| Engineering-report PDFs for all 50 Codec projects; Cyber titles filled in | 50 PDFs | [Codec dashboard]({CODEC_PAGES}/) |

## Why this repository exists
Hiring managers see a CV line; they rarely see the work. This repository puts every project I delivered in 2026 in one place, in one structure — dashboard → track → project → evidence — so the proof behind any CV claim is two clicks away.

## Tracks

| # | Track | Projects | Scope | Open |
|---|-------|:-:|-------|------|"""]
for t in reg["tracks"]:
    R.append(f"| {t['slug'][:2]} | **{t['title']}** | {len(t['projects'])} | {t['tagline']} | [dashboard]({PAGES}/#{t['slug']}) |")
R.append(f"""
```mermaid
pie showData
    title Projects by track
""" + "\n".join(f"    {t['title'].split(' — ')[0]} : {len(t['projects'])}" for t in reg["tracks"]) + "\n```\n")
R.append("## Full project index\n")
for t in reg["tracks"]:
    R.append(f"<details{' open' if t['key']=='codec' else ''}>\n<summary><b>{E(t['title'])}</b> — {len(t['projects'])} projects · <i>{E(t['role'])}</i></summary>\n\n| # | Project | Headline result | Tools | Evidence |\n|---|---|---|---|---|")
    for i, p in enumerate(t["projects"], 1):
        ev = f"[report]({p['evidence']})" if p["evidence"] else "to be attached"
        R.append(f"| {i} | [{p['title']}]({PAGES}/#{t['slug']}/{p['slug']}){' 🆕' if p['new'] else ''} | {(p['results'] or [''])[0]} | {' · '.join(p['tools'][:4])} | {ev} |")
    R.append("\n</details>\n")
R.append(f"""## Evidence
- **Codec Technologies (50 projects)** — every card links to its engineering-report PDF in [{CODEC}]({GH}/{CODEC}); the complete source trees are the `*_source.zip` archives in that repo (unzip → each project runs with `run_all.sh`).
- **HEXA, Product Management, Internship Studio, Excel Module, Personal builds (53 projects)** — the deliverables (PDF reports, workbooks, decks, code) are being attached as GitHub Releases / linked drives; until a card shows an Evidence button, the `projects.json` record lists the file names that exist for it. Nothing is claimed here that does not exist as a file.
- Machine-readable registry: [`projects.json`](projects.json). The Lens Index repo re-indexes the same {N} projects by skill, tool, sector, target role and method: [{LENS}]({GH}/{LENS}).

## Standards that run through every project
Verified figures only · declared substitutions wherever a real dataset or a named tool could not be used · AI partnership disclosed (Claude for structuring, drafting and code review; analysis, decisions, interviews and submissions are mine) · zero-white-space documents, measured not eyeballed · defensive security only.

## Contact
**{OWNER}** · Ghaziabad, NCR, India · eswarmba05313@gmail.com · +91-9360548243 · [LinkedIn](https://linkedin.com/in/eswar-mahalingam) · [GitHub]({GH})

<div align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:C9A227,100:0A1F44&height=90&section=footer" width="100%"/></div>
""")
open(f"{OUT}/README.md", "w").write("\n".join(R))
DESC = (f"Master portfolio of {N} delivered projects in one navigable dashboard — 13 HEXA data-analytics builds, 8 PM case studies, 16 Internship Studio packs, "
        "50 Codec engineering & security projects (EV, cyber, VLSI, robotics — 595+ tests, report PDF each), Excel mastery module and self-built tools. Dashboard → track → project → evidence.")
assert len(DESC) <= 350, len(DESC)
open(f"{OUT}/REPO_NAME_AND_DESCRIPTION.txt", "w").write(f"REPOSITORY NAME\n{REPO}\n\nDESCRIPTION ({len(DESC)}/350 characters)\n{DESC}\n\nTOPICS\nportfolio data-analytics product-management excel python machine-learning cyber-security electric-vehicles vlsi robotics dashboards case-studies internship-projects\n\nWEBSITE (after enabling GitHub Pages)\n{PAGES}/\n")
open(f"{OUT}/PUSH_TO_GITHUB.md", "w").write(f"""# Upload (GitHub web, one drag-and-drop — {len(os.listdir(OUT)) + 1} files)
1. github.com → New repository → `{REPO}` → paste description from REPO_NAME_AND_DESCRIPTION.txt → Public → "Add a README" UNTICKED → Create.
   If the old 83-folder version was partly uploaded: Settings → Delete this repository first, then recreate.
2. "uploading an existing file" → drag ALL files in this folder (include `.nojekyll`) → Commit changes.
3. Settings → Pages → Deploy from a branch → main / (root) → Save → dashboard live at {PAGES}/ in ~2 minutes.
4. To attach a deliverable later: upload the file to a GitHub Release of this repo (Releases → Draft a new release → attach files), copy its URL into that project's `"evidence"` field in projects.json, commit — the dashboard and README pick it up on the next regenerate (`python3 _build_master_compact.py`) or just edit the README row by hand.
""")
shutil.copy(__file__, f"{OUT}/_build_master_compact.py")
print(N, sorted(os.listdir(OUT)))
