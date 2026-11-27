# Signed Four-Port Equality–Balance Networks (27 November 2026)

**Status:** Mathematical model and canonical research framework; universal aggregate contraction and P versus NP remain open.

The exact LaTeX source and bibliography of the locally compiled 21-page manuscript are published here. Both Git blob hashes match the source package.

| File | Purpose | SHA-256 |
| --- | --- | --- |
| [eb4_model.tex](eb4_model.tex) | Standalone manuscript | `8d15b6f1a4815cfb851414544f49af1a32ff5be635fe998642e7a816c166fd25` |
| [references.bib](references.bib) | Bibliography | `0defb47a000998b2f20ce8485f3ccf6edd868ba89a8d32a4caa4ec4363b1d47e` |

The original compiled PDF has SHA-256 `a1550135fad80350a975c2a1125bd3e86b473270fd1a6ef2ad280e31b91d3c97`. Binary upload is pending; the PDF is not yet available in this repository. A locally rebuilt PDF may differ in bytes because of TeX versions or metadata.

## Build

Use a standard TeX Live distribution with AMS packages, Latin Modern, TikZ, biblatex, Biber, booktabs, xurl and hyperref. From this directory:

```sh
pdflatex -interaction=nonstopmode -halt-on-error eb4_model.tex
biber eb4_model
pdflatex -interaction=nonstopmode -halt-on-error eb4_model.tex
pdflatex -interaction=nonstopmode -halt-on-error eb4_model.tex
```

Alternatively upload the two source files to Overleaf and select `eb4_model.tex` as the main document.

## Pinned reproducibility resources

- [Shared E/B research directive](https://github.com/j15marti/pnp/blob/869007811cfe4a6b703e7f111111b820f3afcb03/research/coordination/shared-eb-2026-11-27/DIRECTIVE.md)
- [Deterministic E/B compiler](https://github.com/j15marti/pnp/blob/21b9d53fb8166c819b24e708656c742cd3c24f10/research/coordination/shared-eb-2026-11-27/compile.js)
- [Setup verification data](https://github.com/j15marti/pnp/blob/e33b46e88cab91df6169785bf98540c3d8936061/research/coordination/shared-eb-2026-11-27/setup-results.json)
- [Exact instance registry](https://github.com/j15marti/pnp/blob/0c14cdc57925788cf7a451dcd5aa171dce860f2c/research/coordination/shared-eb-2026-11-27/instance-registry-v1.json)
- [Original UNSAT corpus](https://github.com/j15marti/pnp/blob/e315349cd6c1fe3fa696504859f28312f6aab69a/research/coordination/shared-unsat-2026-11-27/benchmarks.json)
- [Reference certificate checker](https://github.com/j15marti/pnp/blob/1c4f25dabf9b6e2c715f9f2eaf71ebab397f5717/research/coordination/shared-unsat-2026-11-27/verify.js)

No full native solve or independent formal-kernel verification is claimed for the manuscript.
