# Track Specification: SEO, UI Refinement, and Header Updates

## Overview
This track focuses on improving the discoverability and search engine ranking of the Dazbo Portfolio application while making minor wording refinements to the user interface (Footer and Header). The goal is to ensure that searching for "Darren Lester", "Dazbo", or professional roles like "Google Cloud Architect" leads users to this portfolio. Additionally, we will document the SEO configuration and design decisions in the project documentation.

## Functional Requirements

### 1. SEO & Searchability
- **Document Head Management:** Integrate `react-helmet-async` into the React frontend to dynamically manage `<title>`, `<meta name="description">`, and other head tags.
- **Keyword Targeting:** Define default meta tags including:
    - **Title Template:** `[Page Title] | Darren "Dazbo" Lester - Solutions Architect`
    - **Meta Description:** A professional summary including keywords: "Darren Lester", "Dazbo", "Solutions Architect", "Google Cloud", "AI Agent Developer".
- **Dynamic Meta Tags:**
    - **Blog Detail Pages:** Use the blog title and AI-generated summary for meta tags.
    - **Project Detail Pages:** Use the project title and description for meta tags.
- **Open Graph (Social Sharing):** Implement OG tags (`og:title`, `og:description`, `og:image`, `og:url`) to ensure professional-looking cards when links are shared on LinkedIn, Twitter, etc.
- **Sitemap Generation:**
    - Implement a FastAPI endpoint `/api/sitemap.xml` that dynamically generates a valid XML sitemap.
    - The sitemap must include the home page and all dynamic paths for Blogs and Projects fetched from Firestore.
- **Robots.txt:** Add a static `robots.txt` file to the frontend `public/` directory allowing all crawlers to index the site and pointing to the sitemap.
- **Structured Data (JSON-LD):** Inject JSON-LD snippets for the "Person" (Home) and "Article" (Blogs) to provide search engines with explicit metadata.

### 2. UI Wording Tweaks
- **Header Updates:**
    - Change the tagline text from "Powered by Python, React, and Gemini AI" to "**Built with Python, React, and Gemini AI**".
- **Footer Updates:**
    - Update copyright text (e.g., "© 2026 Darren Lester").
    - Ensure clear links to LinkedIn, GitHub, and Medium/Dev.to are present and accurately labeled.
    - Refine any "About" or "Disclaimer" text in the footer for a professional tone.

### 3. Documentation
- **Design Decisions:** Update `docs/design-and-walkthrough.md` to record the decision to use `react-helmet-async` for SEO and the implementation of the sitemap endpoint.

## Technical Requirements
- **Frontend:** Install and configure `react-helmet-async`.
- **Backend:** Update `fast_api_app.py` to serve a dynamic sitemap.
- **Data:** Ensure `Blog` and `Project` models provide sufficient metadata for SEO (handled by existing ingestion logic).

## Acceptance Criteria
- [ ] Searching for "site:dazbo.com" (or the specific domain) shows descriptive titles and snippets.
- [ ] Sharing a blog post link on LinkedIn displays a card with the correct title and image.
- [ ] `/api/sitemap.xml` returns valid XML listing all available portfolio items.
- [ ] `robots.txt` is accessible at the root.
- [ ] Header tagline reads "Built with Python, React, and Gemini AI".
- [ ] Footer text is updated and professional.
- [ ] `docs/design-and-walkthrough.md` reflects the new SEO architecture.

## Out of Scope
- Advanced SEO analytics integration (e.g., Google Analytics 4).
- Backlink building or off-page SEO strategies.
- Large-scale UI redesign.
