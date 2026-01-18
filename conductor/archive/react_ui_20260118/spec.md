# Track Specification: React UI Implementation (Initial)

## Overview
This track focuses on building the initial React frontend for the Dazbo Portfolio. The goal is to create a visually appealing, responsive landing page that consolidates Dazbo's blogs, GitHub repositories, and applications into a central showcase, while providing the foundation for an interactive chat experience.

## Functional Requirements
- **Build System**: Initialize a React application using **Vite** in a `frontend/` directory.
- **Styling**: Implement UI using **React Bootstrap**, styled with **Material Design** principles (elevations, shadows, typography).
- **Navigation**: Use **React Router** to support a hybrid single-page structure.
    - Landing page (Home) containing carousels for Blogs, Projects, and Applications.
    - Placeholder/Structure for detailed views of individual items.
- **Content Showcases (Carousels)**:
    - **Blogs Carousel**: Display blog posts fetched from the backend (`/blogs`).
    - **Projects Carousel**: Display GitHub repositories fetched from the backend (`/projects`).
    - **Apps Carousel**: Display manual/featured applications.
- **Chat Widget Shell**:
    - Implement a **Fixed Floating Button** (bottom-right) for the conversational agent.
    - Create the visual chat overlay/window shell (to be wired to the agent in a later track).
- **Data Fetching**: Integrate with the existing FastAPI backend to retrieve content.

## Non-Functional Requirements
- **Responsive Design**: Mobile-first approach; carousels and UI must work seamlessly on mobile (per `workflow.md`).
- **Modern UI/UX**: Clean, professional aesthetic consistent with "Dazbo" style (innovation-focused, friendly).

## Acceptance Criteria
- [ ] React application successfully initialized with Vite and running.
- [ ] Landing page displays three distinct carousels (Blogs, Repos, Apps).
- [ ] Carousels are responsive and populated with dummy/initial data from backend.
- [ ] Navigation between landing page and a placeholder detail page works correctly.
- [ ] Chat button is persistent and toggles a visible (empty) chat window shell.
- [ ] UI adheres to Material Design aesthetics (shadows, spacing, color palette).

## Out of Scope
- Full conversational agent logic (streaming, session persistence).
- Production-ready SEO optimization.
- Image scraping/automation for carousels (manual URLs/placeholders only).
