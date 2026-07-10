# Paper Zoom Briefing

This directory contains the professor-facing presentation package for the canonical manuscript, `paper/manuscript/paper.md`. The live route has 18 audience-facing slides and is designed for a 16-18 minute Zoom discussion.

## Files

| File | Role |
|:--|:--|
| `paper-zoom-briefing.md` | Editable Marp deck using the existing `paper-zoom` theme and Figures 1-4. |
| `paper-zoom-script.md` | Full synchronized slide-by-slide speaking script. |
| `paper-zoom-presentation-checklist.md` | Delivery, number-checking, and Q&A checklist. |
| `themes/paper-zoom.css` | Custom academic presentation theme. |
| `dist/` | Generated local HTML output; do not edit by hand. |

The shareable PDF is generated at `paper/share/paper-zoom-briefing.pdf`. Generated `dist/` and `share/` files are outputs, not synchronization sources.

## Canonical Inputs

Before revising the briefing, reconcile it against:

- `paper/manuscript/paper.md` for claims, definitions, sample frames, inference, and limitations.
- `paper/figures/figure1_two_part_framework.png` through `figure4_post_entry_trajectories.png` for audience-facing results.
- `paper/tables/table1_sample_frames.md`, `table2_adoption_results.md`, and `table3_generator_components.md` for compact numerical checks.

The source deck and script currently use the paper's three-estimand structure: fleet coverage, sparse first installed-capacity entry, and engineering components of gross MWh/t. Keep the official FY2024 415/991=41.9% context distinct from the analytical 417/1,014=41.1% measure.

## Export

Install Node dependencies once if needed:

```bash
npm install
```

Export HTML:

```bash
npm run slides:paper
```

Export the shareable PDF:

```bash
npm run slides:paper:pdf
```

## Presentation Use

Use the PDF for Zoom screen sharing and keep `paper-zoom-script.md` open on a second screen. The slides remain streamlined; the script carries the Firth definition, identity construction, model detail, inference hierarchy, pathway denominators, and noncausal limitations.
