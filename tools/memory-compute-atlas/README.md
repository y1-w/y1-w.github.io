# Memory Compute Atlas — offline review edition

An independent, evidence-linked and **fully offline-capable** atlas of physical compute-in-memory (CIM/IMC), processing-in-memory (PIM), near-memory compute (NMC/PNM) and related enabling memory technologies.

## Open it now

1. Unzip the archive.
2. Double-click **`index.html`**. No installation or local server required.
3. Use **Product atlas** for sorting/searching/filtering and selecting up to four products to compare. Company and product titles link to detailed profiles; **Insights** contains six technical essays.

Everything the site needs is local. Source links to manufacturers and papers are external and require an internet connection only if you click them.

## GitHub Pages integration

Place the folder contents in:

`tools/memory-compute-atlas/`

Update `_pages/tools.md` to present both atlases together in the responsive tools directory.

Published URL:

`https://y1-w.github.io/tools/memory-compute-atlas/`

The website is designed to coexist with `tools/accelerator-atlas/` and to be linked as a second resource under `/tools/`.

## Dataset and updates

- `data.json`: human-readable source snapshot; includes 30 product records and 21 company profiles, source URLs, caveats and clearly distinguished product maturity.
- `data.js`: an inlined JavaScript copy of the same snapshot, necessary for `file://` access in browsers without CORS restrictions.
- `products.csv`: downloadable tabular product list.
- `build_data.py`: reproducibly converts the research workbook at its declared path into the three source exports. If the workbook is moved, edit the `SRC=` line; in production use your own evidence-reviewed inputs.
- `app.js` and `styles.css`: plain JavaScript and CSS, no framework/CDN/runtime dependency.

To update a record without Python, edit **both** the JSON and its equivalent object in `data.js`. Do not alter underlying vendor claims without verifying their sources and scope.

## Method and limitations

Snapshot: 23 October 2026. Coverage is a curated research atlas, not a census, performance ranking or investment report. Numbers reflect published disclosures and are not independently measured. Product status can change. Memory devices without demonstrated in-memory MAC are labeled as **Memory enabler**, not CIM accelerators. Companies that are only software operators, or whose relevant hardware is not established by public evidence, are excluded. Academic lab spin-off status is distinguished from co-development partnerships and founder education. City lists include reported offices/R&D locations but should not be interpreted as certified R&D-site audits.

No geopolitical analysis is included. No cookies, analytics, third-party scripts or external font calls are used.