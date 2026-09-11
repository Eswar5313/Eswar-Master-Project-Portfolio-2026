# Upload (GitHub web, one drag-and-drop — 7 files)
1. github.com → New repository → `Eswar-Master-Project-Portfolio-2026` → paste description from REPO_NAME_AND_DESCRIPTION.txt → Public → "Add a README" UNTICKED → Create.
   If the old 83-folder version was partly uploaded: Settings → Delete this repository first, then recreate.
2. "uploading an existing file" → drag ALL files in this folder (include `.nojekyll`) → Commit changes.
3. Settings → Pages → Deploy from a branch → main / (root) → Save → dashboard live at https://eswar5313.github.io/Eswar-Master-Project-Portfolio-2026/ in ~2 minutes.
4. To attach a deliverable later: upload the file to a GitHub Release of this repo (Releases → Draft a new release → attach files), copy its URL into that project's `"evidence"` field in projects.json, commit — the dashboard and README pick it up on the next regenerate (`python3 _build_master_compact.py`) or just edit the README row by hand.
