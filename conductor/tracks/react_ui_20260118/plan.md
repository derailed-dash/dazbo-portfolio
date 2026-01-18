# Implementation Plan - React UI Implementation

This plan outlines the steps to implement the React-based frontend for the Dazbo Portfolio, featuring carousels for content and a shell for the conversational agent.

## Phase 1: Environment Setup & Scaffolding [checkpoint: e84015f]
- [x] Task: Initialize Vite React Application [commit: 9c52753]
    - [x] Run Vite initialization in `frontend/` directory with TypeScript template
    - [x] Install core dependencies: `react-bootstrap`, `bootstrap`, `react-router-dom`, `lucide-react`, `axios`
    - [x] Configure `vite.config.ts` for proxying API requests to FastAPI backend
- [x] Task: Define Base Project Structure [commit: ceee1eb]
    - [x] Organize directories: `src/components`, `src/pages`, `src/services`, `src/styles`, `src/hooks`
    - [x] Setup global CSS variables for Material Design (colors, shadows, spacing)
- [x] Task: Conductor - User Manual Verification 'Phase 1: Setup' (Protocol in workflow.md) [commit: e84015f]

## Phase 2: Core Layout & Styling
- [ ] Task: Create Base Layout Components
    - [ ] Implement Responsive Navbar (Material Design style)
    - [ ] Implement Footer with social links
    - [ ] Create `MainLayout` wrapper component
- [ ] Task: Implement Material Design Theme
    - [ ] Customize Bootstrap SCSS/CSS to match elevations and typography
    - [ ] Create shared UI components (Buttons, Cards) with Material attributes
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Layout' (Protocol in workflow.md)

## Phase 3: Content Carousels
- [ ] Task: Create Generic Carousel Component
    - [ ] Write unit tests for Carousel rendering and responsiveness
    - [ ] Implement `ShowcaseCarousel` using React Bootstrap `Carousel`
- [ ] Task: Implement Content Services
    - [ ] Create API service for fetching Blogs, Projects, and Experience
    - [ ] Write tests for data fetching and error handling
- [ ] Task: Build Specific Carousels
    - [ ] Implement `BlogCarousel` with card-based items
    - [ ] Implement `ProjectCarousel` for GitHub repositories
    - [ ] Implement `AppsCarousel` for featured applications
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Carousels' (Protocol in workflow.md)

## Phase 4: Navigation & Chat Widget
- [ ] Task: Configure Routing
    - [ ] Setup `BrowserRouter` in `App.tsx`
    - [ ] Create `HomePage` (Landing Page)
    - [ ] Create `DetailPlaceholderPage` for item deep-dives
- [ ] Task: Implement Chat Widget Shell
    - [ ] Write tests for Chat Widget toggle behavior
    - [ ] Implement `ChatWidget` fixed floating button
    - [ ] Create `ChatWindow` UI shell with message area and input field (visuals only)
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Navigation' (Protocol in workflow.md)

## Phase 5: Verification & Polishing
- [ ] Task: End-to-End Visual Review
    - [ ] Verify responsiveness on mobile, tablet, and desktop
    - [ ] Check accessibility (aria-labels, color contrast)
    - [ ] Ensure consistent Material Design styling across all components
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Verification' (Protocol in workflow.md)
