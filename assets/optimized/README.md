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
