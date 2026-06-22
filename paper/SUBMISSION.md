# How to publish this on bioRxiv — the steps only you can do

Everything below is prepared and **local**; nothing has been pushed or posted. Posting a preprint is
a permanent public act under your name, so each public step is yours. Estimated time: Zenodo ~15 min,
bioRxiv ~30–45 min. All free. **Do these in order.**

## Gate status (machine-checked, 2026-06-22)
- `pubkit readiness` → **mechanizable bar CLEAR** (attestation ✓, manuscript ✓, AUDIT.md ✓, honest-framing ✓)
- `pubkit guard` → **clean** (no secrets / no transcript leak)
- `claims.yaml` attested → **24/24 checks reproduced** (`attestation.json`, `all_passed: true`)
- Adversarial audit re-run → **no scientific overclaim**; novelty re-checked against 61 papers (two S2 sweeps)

## 0. Prerequisites (already done from the HIV submission)
- [x] **ORCID** `0009-0000-5520-915X` (Seth Cope) — in `CITATION.cff`, `.zenodo.json`, `MANUSCRIPT.md`.
- [x] **Real name, "Independent researcher"** in all metadata. **Do not list an institution you aren't part of.**
- [x] **bioRxiv account** exists (from the HIV preprint).

## 1. Zenodo — citable DOI for the code (NOT done yet)
- [ ] Make the GitHub repo **public**, turn on the **Zenodo ↔ GitHub** toggle, cut release **v1.0.0**.
      `.zenodo.json` is ready (title/abstract/keywords/ORCID). Or run `pubkit zenodo <repo>` for the click-path.
- [ ] Paste the minted DOI into `paper/MANUSCRIPT.md` (Data availability), `CITATION.cff`, `ABSTRACT.md`.

## 2. Manuscript PDF (DONE — generated on-box, no pandoc/LaTeX needed)
- [x] `docs/index.html` — self-contained, **figure-embedded** render (all 5 figures base64-embedded,
      full Google-Scholar/Dublin-Core/JSON-LD metadata). Built with `pubkit pages` (local only).
- [x] **`paper/manuscript.pdf` generated** (8 pages, all 5 figures, 394 KB, PDF-1.4) via headless
      Chromium — and copied to `docs/manuscript.pdf` for the Pages download link. Regenerate with:
      ```
      chromium --headless=new --no-pdf-header-footer \
        --print-to-pdf="$PWD/paper/manuscript.pdf" "file://$PWD/docs/index.html"
      ```
- [ ] **Re-read the whole PDF in your own voice.** Keep every caveat — the honesty is the credibility.

## 3. bioRxiv — post the preprint
- [ ] New submission. Suggested fields:
  - **Subject category:** *Systems Biology* (within-host ODE modeling; the HIV preprint used the same).
    Alt: *Immunology* if you prefer the disease framing.
  - **Type:** "Research article with data". **License:** CC-BY. **Author:** Seth Cope (corresponding) + ORCID.
    **Funding:** none. **Competing interests:** none. **AI assistance:** disclosed (it's in the manuscript).
  - Upload `paper/manuscript.pdf`; if asked for figures separately, upload the five `analysis/t1d_*.png`.
- [ ] ⚠️ **The web Abstract field may reject non-ASCII.** When you paste the abstract, replace em-dashes
      `—` with `--`, `≥`/`≤` with `>=`/`<=`, `→` with `->`, `β`→`beta`, `ρ`→`rho`, `φ`→`phi`, `𝒜`→`A`.
      (The PDF keeps the nice typography; only the web abstract box is fussy — this bit us on HIV.)
- [ ] After submit you get an **MS ID, "in screening"** (~24–72 h). To edit before it posts: author area →
      "Manuscripts Undergoing Screening" → "Request Return of Manuscript". Do NOT resubmit (dup).

## 4. After it's live
- [ ] Put the bioRxiv link + DOI in the GitHub `README.md`.
- [ ] Consider holding outreach until it has posted; lead with the **falsifiable NOD experiment** (the
      tolerance-first sequencing test), not a claim.

## Hard rules (protect yourself)
- **Frame it as a modeling hypothesis, never a finding or a "cure."** It generates a testable
  sequencing rule; it demonstrates nothing in a patient. Overclaiming is the fastest way to be dismissed.
- **Foster et al. 2025 is a conference abstract** (ADA 2136-LB) — cite it as such; the manuscript does.
- **Keep the disclosed caveats** (Hill n=2 dependence; "100%" is 5-yr-horizon-specific; the model
  under-produces the teplizumab monotherapy delay). They are in the manuscript's Limitations — leave them in.
- **Never pay a "publisher" that emails offering to publish your work.** bioRxiv and Zenodo are free; that
  solicitation is the predatory-journal trap.
- **Sequencing:** your `~/dev/diseases/METHOD.md` says publish one at a time, strongest first — the HIV
  preprint is already in screening; consider letting it land before posting this one.
