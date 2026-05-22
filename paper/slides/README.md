# Paper Zoom Briefing

This directory contains a paper-only presentation package for explaining the article in a 10-15 minute Zoom meeting.

## Files

| File | Role |
|:--|:--|
| `paper-zoom-briefing.md` | Editable Marp slide deck. |
| `paper-zoom-script.md` | Full slide-by-slide speaker script and Zoom run sheet. |
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

Use the PDF for Zoom screen sharing and keep `paper-zoom-script.md` open on a second screen. The main deck is designed for a mixed academic/non-expert audience: plain-language framing comes first, while model details and claim boundaries are placed later or in the appendix.

