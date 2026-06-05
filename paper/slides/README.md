# Paper Zoom Briefing

This directory contains a paper-only presentation package for explaining the article in an 8-10 minute Zoom meeting.

## Files

| File | Role |
|:--|:--|
| `paper-zoom-briefing.md` | Editable Marp slide deck. |
| `paper-zoom-script.md` | Separate slide-by-slide live presentation script. |
| `paper-zoom-presentation-checklist.md` | Practical delivery checklist for a simple supervisor-facing presentation. |
| `themes/paper-zoom.css` | Custom academic presentation theme. |
| `dist/` | Local generated HTML output, ignored by Git. |

The shareable PDF is generated at:

```bash
paper/share/paper-zoom-briefing.pdf
```

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

Use the PDF for Zoom screen sharing and keep `paper-zoom-script.md` open on a second screen. The live route is 10 main slides; appendix slides are only for questions. Before presenting, run through `paper-zoom-presentation-checklist.md` to keep the explanation simple, direct, and supervisor-friendly.
