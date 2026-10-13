# AI Accelerator Architecture Atlas

Hosted as a standalone static application under `/tools/accelerator-atlas/`, linked from the Jekyll `/tools/` navigation page.

- `chips.json`: canonical, source-linked accelerator dataset.
- `index.template.html`: presentation template with `__JSON__` placeholder.
- `build.py`: validates data and regenerates `index.html` and `chips.csv`.
- `index.html`: self-contained page; no external runtime dependencies.
- `chips.csv`: tabular export.

Update procedure: verify specs against primary sources; edit `chips.json`; update `last_verified` and `snapshot_date`; run `python tools/accelerator-atlas/build.py` from the repository root; test locally and commit the regenerated artifacts.

The 3D design-space coordinates are editorial/qualitative, **not benchmark scores**. No automatic deployment or source syncing is provided by this change.
