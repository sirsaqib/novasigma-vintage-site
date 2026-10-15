# Speed optimization — WebP conversion (2026-10-14 ~17:30 PDT)

## Why
User demands 100% mobile PageSpeed. Live measurement (pagespeed.web.dev, mobile,
2026-10-14 17:16 PDT) showed **89** — top issue: "Improve image delivery"
(est. 2,624 KiB savings). Images were 3,350 KB total as JPG/PNG.

## What changed (in ~/workspace/deploys/novasigma-vintage/)
1. Converted 38 images to WebP (photos q76, alpha graphics q82, method=6):
   - logo-badge.png 1215px → 480px WebP (215 KB → 29 KB)
   - hero-warehouse.jpg → WebP (198 KB → 130 KB)
   - logos/*.png (1920px originals) → max 500px WebP
   - retail/ + wholesale/ photos → WebP
   - logo-sm.png → WebP
2. Kept as-is: favicon.png, apple-touch-icon.png (browser requirements),
   logo.png (unreferenced), r6-levis-trucker.jpg + w-b-levis-3.jpg
   (WebP made them BIGGER — originals were already optimal).
3. Updated all references in 16 HTML files + data/*.json (products, categories,
   posts, settings) — including the CSS background url() for hero-rack.
4. Updated generator templates (gen_brands.py, gen_retail.py) so re-runs emit
   .webp paths.
5. Added explicit width/height to 124 <img> tags (silences the PageSpeed
   "explicit width and height" diagnostic; CLS was already 0).

## Result
- images/: 3,350 KB → 2,099 KB (−37%)
- Zero missing image references (verified by script)
- Backup of originals: ~/workspace/deploys/novasigma-vintage-backup-20261014-speed/

## NOT done (needs main agent)
- **Deploy**: gh/vercel CLIs are not authenticated in this environment.
  Push this directory to github.com/sirsaqib/novasigma-vintage-site and let
  Vercel redeploy.
- **Re-measure**: run PageSpeed mobile again after deploy (API quota was
  exhausted today; use pagespeed.web.dev in browser).
- Expected: high-90s. Remaining PageSpeed notes were "forced reflow"
  (TBT already 0 ms — cosmetic) and field data "No Data" (needs real traffic).
