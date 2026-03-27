# Visual Design and UX Guidelines

This document serves as the single source of truth for the visual identity, UI components, frontend aesthetics, and CLI user experience of the **Dazbo Portfolio** application.

## Visual Identity

The portfolio uses a sleek, modern aesthetic heavily influenced by the Material Design system, adapted into a personalized "Dazbo Dark" theme.

*   **Typography**: `Inter` is the primary font family, falling back to system-ui and sans-serif for optimal cross-device legibility.
*   **Color Palette**: Controlled dynamically via CSS variables (`--md-sys-color-background`, `--md-sys-color-primary`, etc.) to enforce a strong dark theme presentation.
*   **Aesthetics**: Glassmorphism is used extensively to create depth and a premium feel.

## Visual Effects and Glassmorphism

Glassmorphism effects are implemented centrally in `index.css` to provide a consistent translucent, blurred overlay appearance.

*   **Glass Controls (`.btn-glass`)**: Buttons use a lightweight blur (`backdrop-filter: blur(4px)`) and a semi-transparent white background with a solid white border. On hover, these elements brighten and emit a soft glowing box-shadow.
*   **Glass Panels (`.glass-card`)**: Content cards utilize a stronger blur (`blur(10px)`) and subtle borders. Hover interactions lift the cards (`translateY(-5px)`) and intensify the drop shadow to create a sophisticated layered depth.
*   **Inline Code Tags (`code.glass-tag`)**: Code snippets within markdown blocks are styled as glass pills, offering a compact, distinct visual contrast against standard text without overpowering the paragraph layout.

## Premium Content Styling

Careful attention is paid to how ingested Markdown content is presented:

*   **Blockquotes**: Styled as premium callouts featuring a primary color left-border, a gentle blur backdrop, and subtle shadowing. Text is italicized (`font-style: italic`), and attribution elements (`<strong>`) are rendered as professional, uppercase metadata labels to cleanly separate quotes from their authors.
*   **Custom Scrollbars**: Webkit scrollbars are styled with a dark track and a refined `#333` thumb layout to match the application's overall dark mode seamlessly.

## Key Frontend Components

The React/Vite SPA relies on several core architectural components to drive its UI:

*   **`MainLayout`**: The top-level wrapper for all pages. It structurally guarantees the display of the `AppNavbar` (top), `Footer` (bottom), and the `ChatWidget` across all user sessions.
*   **`ShowcaseCarousel`**: A highly reusable component for displaying dynamic collections of items (like blogs and projects).
    *   *Responsiveness*: On mobile devices, it snaps to display 1 item per slide. On desktop resolutions, it intelligently expands to a grid of 3 items per slide.
    *   *Navigation*: Includes bespoke, custom-styled "Previous" and "Next" controls and positional indicators.
*   **`ChatWidget`**: A floating action button (FAB) that persistently rests on the screen and expands into the conversational AI chat interface. 
*   **`AboutPage`**: A dedicated profile page rendering Markdown content straight from Firestore, framed within a large glassmorphic UI overlay.

## Development Workflow UX

### Development CLI Environment
When developing locally using the `setup-env.sh` and Vite server workflow, developers experience instant Hot Module Replacement to instantly observe CSS and glassmorphic changes.

### Ingestion Experience (CLI)
The visual experience extends beyond the DOM into the backend scripts. The python CLI ingestion tool (`app/tools/ingest.py`) provides a premium, rich console UX:

*   **Progress Indicators:** Powered by the Python `rich.progress` library, offering animated spinners, progress bars, and real-time status reporting (e.g., "Reading", "Enriching", "Saving") for lengthy ingestion tasks like Dev.to and Medium scraping.
*   **Summary Stats:** At the conclusion of a run, a detailed, cleanly formatted console report visually breaks down counts for New, Updated, Enriched, Skipped, and Filtered items per platform.
