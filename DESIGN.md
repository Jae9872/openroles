# DESIGN SYSTEM — openroles

> Source of truth for all UI. Applies the `frontend-taste` pack rules:
> hierarchy first, spacing 4/8/16/24/40, contrast ≥4.5:1, state by ≥2 cues,
> visible focus, motion ≤200ms for state changes only, empty/loading/error
> states designed, verbs for buttons, nouns for labels.

## 1. Color tokens

### Surfaces (dark default — Linear palette)
| Token | Hex | Use |
|---|---|---|
| `--bg` | `#09090b` | Page background |
| `--surf` | `#18181b` | Cards, panels, table rows hover |
| `--surf-2` | `#1f1f23` | Nested surfaces, hover |
| `--border` | `#27272a` | Borders, dividers |
| `--border-strong` | `#3f3f46` | Hover borders, focus rings |

### Text
| Token | Hex | Contrast on --bg | Use |
|---|---|---|---|
| `--text` | `#f4f4f5` | 18.5:1 | Primary text, headings |
| `--muted` | `#a1a1aa` | 8.2:1 | Secondary text, descriptions |
| `--dim` | `#71717a` | 4.6:1 | Tertiary, stamps, meta (minimum body contrast) |

### Signal colors (neon, tinted)
| Token | Hex | Tint bg | Border | Use |
|---|---|---|---|---|
| `--blue` | `#60a5fa` | `#60a5fa10` | `#60a5fa40` | Remote, links, focus ring |
| `--emerald` | `#34d399` | `#34d39910` | `#34d39940` | Visa, success, apply |
| `--violet` | `#a78bfa` | `#a78bfa10` | `#a78bfa40` | Equity, accent |
| `--amber` | `#fbbf24` | `#fbbf2410` | `#fbbf2440` | Salary, warning |
| `--red` | `#f87171` | `#f8717110` | `#f8717140` | Error, reject |

### Light mode (optional, v2)
Invert surfaces: `--bg #fafafa`, `--surf #ffffff`, `--border #e4e4e7`,
`--text #09090b`, `--muted #52525b`, `--dim #71717a`. Signal colors
darken by 10% (e.g. `--blue #2563eb`).

## 2. Typography

### Font stack
- **Primary:** `system-ui, -apple-system, "Segoe UI", Roboto, sans-serif`
- **Monospace:** `ui-monospace, "SF Mono", "Cascadia Code", monospace`
- **Future:** Geist Sans / Inter (when self-hosted; for now system stack = 0ms load)

### Scale (px)
| Name | Size | Weight | Line-height | Letter-spacing | Use |
|---|---|---|---|---|---|
| `display` | 22 | 600 | 1.2 | -0.02em | Page title (h1) |
| `title` | 16 | 600 | 1.3 | -0.01em | Section headings |
| `body` | 15 | 400 | 1.5 | 0 | Default text |
| `small` | 13 | 400 | 1.5 | 0 | Table cells, descriptions |
| `caption` | 11 | 500 | 1.4 | 0.06em | Labels, stamps, counts (uppercase) |
| `mono` | 11 | 400 | 1.4 | 0 | Provenance stamps, IDs |

### Rules
- One typeface family. No mixing serif/sans.
- Headings: weight 600, tight tracking. Body: weight 400.
- Never below 11px. Never above 22px for page titles (hierarchy, not decoration).

## 3. Spacing scale

Base unit: **4px**. Allowed values only: `4, 8, 16, 24, 40, 64`.

| Token | Value | Use |
|---|---|---|
| `xs` | 4px | Inline gaps, badge padding |
| `sm` | 8px | Component internal padding |
| `md` | 16px | Section gaps, card padding |
| `lg` | 24px | Page padding, section separation |
| `xl` | 40px | Major section breaks |
| `xxl` | 64px | Page-level vertical rhythm |

No arbitrary pixels. If a value isn't on this scale, it's a bug.

## 4. Radius & borders

| Token | Value | Use |
|---|---|---|
| `radius-sm` | 4px | Badges, inputs, kbd |
| `radius-md` | 6px | Buttons, cards, panels (default) |
| `radius-lg` | 8px | Banners, modals |
| `radius-full` | 999px | Pills, filter buttons, avatars |

- Border width: 1px default, 2px for focus rings.
- Border color: `--border` default, `--border-strong` on hover.

## 5. Motion

- **Duration:** 150ms for state changes, 200ms max. Never longer.
- **Easing:** `ease-out` for entrances, `ease-in` for exits, `ease-in-out` for toggles.
- **Allowed:** hover lifts (translateY -1px), filter fade, focus ring appear, row highlight.
- **Forbidden:** decorative animation, parallax, auto-playing carousels, loading spinners >200ms (use skeleton instead).
- **Reduced motion:** respect `prefers-reduced-motion: reduce` — disable all transitions.

## 6. Component specs

### Buttons
| Variant | Background | Text | Border | Use |
|---|---|---|---|---|
| Primary | `--text` (#f4f4f5) | `--bg` (#09090b) | none | One per screen max (Apply, Submit) |
| Secondary | `--surf` | `--text` | `--border` | Filters, toggles |
| Ghost | transparent | `--muted` | none | Links, nav |
| Danger | `--red` tint | `--red` | `--red` border | Reject, delete |

- Padding: `6px 12px` (sm/md). Radius: 6px.
- Hover: `translateY(-1px)` + border darken. Focus: 2px `--blue` ring, 2px offset.
- Labels: verbs ("Apply", "Filter", "Reject"). Never "Submit" or "OK".

### Badges (signal pills)
- Padding: `2px 7px`. Radius: 999px. Font: 10px, weight 600.
- Always: color + icon + text (≥2 cues). Never color alone.
- Variants: visa (emerald), remote (blue), equity (violet), salary (amber).

### Filter bar
- Horizontal flex, gap 8px, wraps on mobile.
- Active state: `--text` border + `--surf-2` background.
- Inactive: `--border` + `--surf`.
- Count in `--dim` 11px next to label.

### Table / feed rows
- Row padding: 10px 8px. Border-bottom: 1px `--border` (or `#18181b`).
- Hover: `--surf` background, 150ms transition.
- Focus: 2px `--blue` outline, inset.
- Columns: company (16%), role (30%), location (16%), signals (38%).

### Cards / panels
- Background: `--surf`. Border: 1px `--border`. Radius: 6px.
- Padding: 16px. Gap between: 8px.

### Empty state
- Centered, `--muted` text, 13px, with a one-line explanation and a primary action.
- Never blank. Never "No data." — say "No roles match these filters. Try removing a filter."

### Loading state
- Skeleton rows (3-5) with `--surf` background and subtle pulse (150ms, respects reduced-motion).
- Never a spinner for >200ms.

### Error state
- `--red` text, 13px, with retry button. Show what failed and why.

### Map markers
- Cluster: circle, size by count (14/20/28px), color step blue→violet→emerald.
- Individual: 5px white circle with 1px dark stroke.
- Popup: `--surf` background, 12px text, company name bold, role count, source.

## 7. Layout

### Grid
- Max width: 1120px, centered, 24px horizontal padding.
- Map page: 2-column grid (1fr + 360px panel).
- Mobile (<720px): single column, hide company+location columns, filters wrap.

### Breakpoints
| Name | Width | Behavior |
|---|---|---|
| Mobile | <720px | Single column, compact |
| Tablet | 720-1024px | Reduced padding, 2-col where possible |
| Desktop | >1024px | Full layout |

### Z-index
| Layer | Value |
|---|---|
| Base | 0 |
| Sticky header | 10 |
| Dropdown/popover | 20 |
| Modal/overlay | 30 |
| Toast | 40 |

## 8. Accessibility

- **Contrast:** body text ≥4.5:1 (verified: `--dim` on `--bg` = 4.6:1, minimum).
- **Focus:** always visible, 2px `--blue` ring, 2px offset. Never `outline: none` without replacement.
- **Keyboard:** every flow completable via keyboard. J/K navigate, Enter activates, Esc closes.
- **State:** ≥2 cues (color + text or icon). Never color alone.
- **Screen reader:** semantic HTML (`<table>`, `<button>`, `role="toolbar"`, `aria-label`).
- **Reduced motion:** `@media (prefers-reduced-motion: reduce)` disables all transitions.

## 9. Content rules

- **Buttons:** verbs ("Apply", "Filter", "Reject", "Save"). Never "Submit", "OK", "Click here".
- **Labels:** nouns ("Visa", "Remote", "Equity", "Company", "Role").
- **Stamps:** lowercase, dim, mono. e.g. "via greenhouse · 2026-11-03".
- **Empty states:** explain + action. "No roles match. Try removing a filter."
- **Errors:** what failed + why + retry. "Failed to load companies.geojson. Retry."
- **Numbers:** real or absent. Never "500+" or "thousands" without backing data.
- **No jargon:** "provenance" → "source", "ingest" → "fetch", "dedupe" → "remove duplicates".

## 10. Iconography

- Emoji as status icons (🛂 🌐 📈 💰) — zero asset cost, renders everywhere.
- No icon font, no SVG sprite sheet. If an icon isn't an emoji, use a 14px inline SVG.
- Arrows: `↗` for external links, `←` for back navigation.

## 11. Dark mode default, light mode optional

Dark is the default (Linear palette). Light mode is a v2 feature — only add when
there's user demand. When added, swap `--bg`/`--surf`/`--text` tokens via
`@media (prefers-color-scheme: light)` or a toggle class on `<html>`.
