# AI Accelerator Architecture Atlas

Hosted as a standalone static application under `/tools/accelerator-atlas/`, linked from the Jekyll `/tools/` navigation page.

- `chips.json`: canonical, source-linked accelerator dataset.
- `index.template.html`: presentation template with `__JSON__` placeholder.
- `build.py`: validates data and regenerates `index.html` and `chips.csv`.
- `index.html`: self-contained page; no external runtime dependencies.
- `chips.csv`: tabular export.
- `details/<id>.json`: per-processor architecture record (summary, highlight tiles, analysis sections, figure specs, memory hierarchy, caveats, extra references). One file is required for every chip in `chips.json`.
- `figures.py`: dependency-free SVG block-diagram engine used to draw the architecture figures from the `figures` specs (flex-style boxes, cell grids, trees, die-to-die links).
- `chip.template.html`: shell for the generated detail pages.
- `chips/<id>/index.html`: generated detail page for each processor, linked from the database table, quick view, comparison panel and design-space map.

Update procedure: verify specs against primary sources; edit `chips.json`; update `last_verified` and `snapshot_date`; add or update `details/<id>.json`; run `python tools/accelerator-atlas/build.py` from the repository root; test locally and commit the regenerated artifacts.

The 3D design-space coordinates are editorial/qualitative, **not benchmark scores**. No automatic deployment or source syncing is provided by this change.

Architecture figures are original schematics redrawn from the cited public disclosures — not vendor artwork and not to scale. Grid cell counts are exact only where a figure caption says so; undisclosed blocks are drawn dashed.
