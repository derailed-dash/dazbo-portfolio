# Implementation Plan - SEO, UI Refinement, and Header Updates

This plan outlines the steps to implement SEO improvements, update UI text, and document the design decisions.

## Phase 1: UI Wording Tweaks & Robots.txt
*Quick wins and static assets.*

- [x] Task: Update Header tagline text in the frontend. c92bb77
- [x] Task: Update Footer copyright and links in the frontend. fb9489d
- [x] Task: Create `robots.txt` in `frontend/public/` to guide search crawlers. 4a6d226
- [x] Task: Conductor - User Manual Verification 'Phase 1: UI Wording Tweaks & Robots.txt' (Protocol in workflow.md) [checkpoint: c92fbef]

## Phase 2: Frontend SEO Infrastructure
*Integrating head management and structured data.*

- [x] Task: Install `react-helmet-async` in the frontend. fe340f2
- [x] Task: Configure `HelmetProvider` in the main application entry point. e1f0b7c
- [x] Task: Create a reusable `SEO` component to manage meta tags, OG tags, and JSON-LD. 2c751b5
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Frontend SEO Infrastructure' (Protocol in workflow.md)

## Phase 3: Dynamic SEO Implementation
*Applying SEO to home, blog, and project pages.*

- [ ] Task: Apply `SEO` component to the Home page with default keywords.
- [ ] Task: Apply `SEO` component to the Blog Detail page using dynamic data.
- [ ] Task: Apply `SEO` component to the Project Detail page using dynamic data.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Dynamic SEO Implementation' (Protocol in workflow.md)

## Phase 4: Backend Sitemap
*Dynamic sitemap generation for indexing.*

- [ ] Task: Implement dynamic XML sitemap generation in the backend.
- [ ] Task: Update `BlogService` and `ProjectService` if necessary to facilitate URL list retrieval.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Backend Sitemap' (Protocol in workflow.md)

## Phase 5: Documentation
*Recording design decisions.*

- [ ] Task: Update `docs/design-and-walkthrough.md` with SEO architecture and configuration details.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Documentation' (Protocol in workflow.md)
