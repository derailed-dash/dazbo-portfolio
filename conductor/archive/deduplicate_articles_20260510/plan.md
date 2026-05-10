# Implementation Plan: `deduplicate_articles`

## Phase 1: Research and Frontend Preparation [checkpoint: b02482d]
- [x] Task: Analyze current blog rendering logic in `frontend/src/pages/BlogsPage.tsx` (or equivalent). b02482d
- [x] Task: Update `Blog` interface in `frontend/src/types.ts` to support an array of platform links (e.g., `platforms: { name: string, url: string }[]`). b02482d
- [x] Task: Conductor - User Manual Verification 'Research and Frontend Preparation' (Protocol in workflow.md) b02482d

## Phase 2: Deduplication Logic (TDD) [checkpoint: 668da21]
- [x] Task: Write failing unit tests for a new utility function `mergeDuplicateArticles` in `frontend/src/utils/blogUtils.test.ts`. 668da21
    - [x] Test that articles with identical titles are merged. 668da21
    - [x] Test that dev.to metadata is preserved over Medium when both exist. 668da21
    - [x] Test that the merged object contains links to all original platforms. 668da21
- [x] Task: Implement `mergeDuplicateArticles` in `frontend/src/utils/blogUtils.ts`. 668da21
- [x] Task: Refactor and verify all unit tests pass. 668da21
- [x] Task: Integrate `mergeDuplicateArticles` into the data fetching hook or component logic. 668da21
- [x] Task: Conductor - User Manual Verification 'Deduplication Logic' (Protocol in workflow.md) 668da21

## Phase 3: UI Component Updates [checkpoint: 64d6ad0]
- [x] Task: Update `BlogCard` component to render multiple platform icons. 64d6ad0
    - [x] Update `ShowcaseCard` to render icons in the right corner. 64d6ad0
    - [x] Add "Read ->" indicator pointing to the icons. 64d6ad0
- [x] Add dev.to and Medium icons (using `lucide-react` or existing assets). 64d6ad0
- [x] Update CSS/Styles to place icons at the bottom of the card, ensuring they match the Glassmorphism aesthetic. 64d6ad0
- [x] Conductor - User Manual Verification 'UI Component Updates' (Protocol in workflow.md) 64d6ad0

## Phase 4: Matching Logic Refinement (TDD) [checkpoint: 64d6ad0]
- [x] Task: Update `mergeDuplicateArticles` to handle similar titles (whitespace/dash normalization). 64d6ad0
- [x] Task: Add test cases for "Extremely Similar" titles in `blogUtils.test.ts`. 64d6ad0
- [x] Task: Verify all tests pass. 64d6ad0
- [x] Conductor - User Manual Verification 'Matching Logic Refinement' (Protocol in workflow.md) 64d6ad0

## Phase 6: Post-Review Refinements (TDD) [checkpoint: b64590a]
- [x] Task: Update `mergeDuplicateArticles` to preserve technical characters (TDD). b64590a
    - [x] Update tests to include "C# vs C" and "Node.js vs Nodejs" scenarios. b64590a
    - [x] Remove aggressive regex in `normalizeTitle`. b64590a
- [x] Task: Ensure platform icon order matches metadata precedence. b64590a
    - [x] Update logic to map `platforms` from the `sorted` duplicates array. b64590a
- [x] Task: Refactor `ShowcaseCard` for better performance and maintainability. b64590a
    - [x] Use `src.url` as key instead of `src.platform`. b64590a
    - [x] Move hover effects from inline styles to CSS class `hover-scale-sm`. b64590a
- [x] Conductor - User Manual Verification 'Post-Review Refinements' (Protocol in workflow.md) b64590a

## Phase 7: Re-Finalization
