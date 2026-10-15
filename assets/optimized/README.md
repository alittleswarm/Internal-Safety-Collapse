# README display images

The README loads these smaller WebP images and links each scientific figure to its original PNG. Keep the original PNGs: they are the full-resolution source files.

All WebP outputs use lossless encoding. The mechanism and overview previews are resized to 2000 pixels wide for the README. The framework diagram and example panel retain their original dimensions and decoded pixels.

Regenerate an output when its source changes, using `cwebp`:

```sh
cwebp -lossless -z 9 -exact -metadata all -resize 2000 0 -mt assets/tvd_mechanism.png -o assets/optimized/tvd_mechanism.webp
cwebp -lossless -z 9 -exact -metadata all -resize 2000 0 -mt assets/fig1_bench_overview.png -o assets/optimized/fig1_bench_overview.webp
cwebp -lossless -z 9 -exact -metadata all -mt assets/fig2_tvd_framework.png -o assets/optimized/fig2_tvd_framework.webp
cwebp -lossless -z 9 -exact -metadata all -mt assets/trigger_example/cross_domain_panel.png -o assets/optimized/cross_domain_panel.webp
```

The banner is a 2000-pixel-wide JPEG at quality 90. Model icons shared by the README and project website live in `docs/static/img/favicons/`; `sources.json` records their original URLs.

The current README mechanism figure is `tvd-execution-modes.webp`, exported from `../tvd-execution-modes.drawio.png`. The PNG embeds an editable draw.io diagram. The older `tvd_mechanism` files remain available for historical reference.


The README's workspace illustrations use the same editable draw.io format:

- `tvd-execution-modes.webp`: LlamaGuard task, data file, and label-matching checks.
- `tvd-workspace-trajectory.webp`: an illustrative sequence of edits and checks, not an experimental trace.
- `tvd-template-workspaces.webp`: real repository folders and context-file variants.

Each preview links to `../<name>.drawio.png`, which embeds the editable XML. After editing and exporting that PNG in draw.io, rebuild its preview with:

```sh
cwebp -lossless -z 9 -exact -metadata all -resize 2000 0 -mt assets/<name>.drawio.png -o assets/optimized/<name>.webp
```

The paper's `fig1_bench_overview.png` and `fig2_tvd_framework.png` remain unchanged and linked from the README. The LlamaGuard illustrations show the label-matching task; the executable `my_favorite` template uses Qwen3Guard.
