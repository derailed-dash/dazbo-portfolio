---
version: "1.0"
name: "Dazbo Portfolio"
description: "High-contrast, premium 'Midnight' theme with glassmorphic accents, following a refined Material 3-inspired aesthetic."
colors:
  primary: "#6200EE"
  secondary: "#03DAC6"
  tertiary: "#BB86FC"
  surface: "#FFFFFF"
  background: "#000000"
  error: "#B3261E"
  on-primary: "#FFFFFF"
  on-surface: "#000000"
typography:
  display-lg:
    fontFamily: "Inter"
    fontSize: "57px"
    fontWeight: 700
    lineHeight: "64px"
    letterSpacing: "-0.25px"
  body-md:
    fontFamily: "Inter"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: "24px"
    letterSpacing: "0.5px"
rounded:
  sm: "4px"
  md: "8px"
  lg: "16px"
  full: "9999px"
spacing:
  sm: "8px"
  md: "16px"
  lg: "24px"
components:
  card:
    background: "rgba(255, 255, 255, 0.05)"
    backdropFilter: "blur(10px)"
  button:
    borderRadius: "8px"
---

# Visual Design and UX Guidelines

This document serves as the single source of truth for the visual identity and user experience of the **Dazbo Portfolio** application.

## Overview

The portfolio follows a high-contrast, premium aesthetic branded as the **"Midnight" Theme**, a refined Material 3-inspired design. It is designed to showcase professional content (blogs, projects) with a focus on legibility, smooth interactions, and a "glassmorphic" feel.

## Colours

The colour palette prioritises deep blacks for the background with vibrant Material accents for interactions and branding.

| Token | Value | Description |
| :--- | :--- | :--- |
| `background` | `#000000` | Pure Black background for high contrast. |
| `surface` | `#FFFFFF` | White surface used for primary cards and text containers. |
| `primary` | `#6200EE` | Deep Purple accent for primary actions and branding. |
| `secondary` | `#03DAC6` | Teal accent for secondary actions and success states. |
| `tertiary` | `#BB86FC` | Light Purple accent for secondary branding and highlights. |

## Typography

The design uses a clean, modern sans-serif stack to ensure clarity across all devices.

*   **Main stack**: `'Inter'`, `'Roboto'`, sans-serif. 
*   **Weights**: 400 (Regular), 500 (Medium/Active Links), 600 (Semi-Bold), 700 (Bold/Titles).
*   **Rendering**: Optimised legibility with `-webkit-font-smoothing: antialiased`.

## Layout

The application uses a responsive grid system that adapts from mobile to desktop.

*   **Grid**: Fluid layout with a maximum content width of `1200px`.
*   **Margins**: Consistent use of the `spacing.md` (16px) token for mobile gutters, scaling to `spacing.lg` (24px) for desktop.
*   **Alignment**: Content is generally centred with left-aligned text blocks for readability.

## Elevation & Depth

Three distinct shadow levels (Material 3 elevations) provide depth and interaction feedback for surfaces.

*   **Level 1**: Subtle shadows for base cards.
*   **Level 2**: Mid-level depth for active or hovered elements.
*   **Level 3**: High depth for overlays, modals, and the `ChatWidget`.

Material cards use a 0.3s ease-in-out transition for elevation shifts and a `translateY(-4px)` lift on hover.

## Shapes

The design language uses rounded corners consistently to soften the high-contrast aesthetic.

*   **Cards & Buttons**: Use the `rounded.md` (8px) token.
*   **Tags & Labels**: Use the `rounded.full` (9999px) token for a pill-shaped appearance.

## Components

### Glassmorphism
A core design pattern using `backdrop-filter: blur(10px)` and semi-transparent backgrounds:
*   **`.btn-glass`**: Transparent buttons with white borders and subtle hover glows.
*   **`.glass-card`**: Low-opacity containers for markdown content and background elements.
*   **`.glass-tag`**: High-contrast, blurred labels used for technology tags.

### Key Frontend Components

*   **`MainLayout`**: The top-level wrapper including `AppNavbar`, `Footer`, and `ChatWidget`.
*   **`ShowcaseCarousel`**: Reusable component displaying collections. Scales from 1 item (mobile) to 3 items (desktop).
*   **`ProjectCarousel`**: Specifically configured to sort GitHub projects, prioritising active work (updated <45 days, >0 stars).
*   **`AboutPage`**: Professional profile rendering Markdown from Firestore with a glassmorphic UI.

### Markdown Rendering

*   **Premium Blockquotes**: Features a left-border accent (`primary`), glassmorphic background, and semi-bold attribution.
*   **Glass Tags**: Inline code rendered as high-readability glassmorphic tags.

## Do's and Don't's

### Do's

- Use glassmorphism for overlays to maintain context with the background.
- Prioritise readability by using the `on-surface` colour for all primary text.
- Maintain a clear hierarchy using the Material elevation system.

### Don't's

- Avoid using pure red or green for anything other than errors/success; use the theme's secondary (Teal) for positive actions.
- Do not use more than two font families; stick to the Inter/Roboto stack.

## Development CLI UX

The CLI tools are designed for immediate visual feedback and clarity when managing content.

### Console UX with Rich

The application uses the `rich` library to enhance the CLI experience with spinners, progress bars, and thread-safe logging. This ensures a clean and readable output during long-running ingestion tasks.

#### Local Development Access

1.  **Process Mode**: `http://localhost:5173` (via `make react-ui` + `make local-backend`).
2.  **Container Mode**: `http://localhost:8080` (via `make docker-build` + `make docker-run`).
