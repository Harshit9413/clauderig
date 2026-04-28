---
name: claude-fit
description: Deep-scan this React project and rebuild .claude/ to be fully project-specific.
---

# /claude-fit

You are performing a **complete project analysis** to transform this `.claude/` folder from generic templates into a project-specific tool. Work through every phase completely without skipping.

---

## Phase 1: Project Discovery

Read every file below that exists (use the Read tool):

**Package manifest:**
`package.json`, `package-lock.json` (scripts section only)

**App entry points:**
`src/main.tsx`, `src/main.ts`, `src/index.tsx`, `src/App.tsx`, `src/App.ts`, `next.config.js`, `next.config.ts`, `vite.config.ts`, `vite.config.js`

**Project structure — list and read up to 3 files from each directory that exists:**
`src/components/`, `src/pages/`, `src/app/` (Next.js), `src/hooks/`, `src/api/`, `src/store/`, `src/context/`, `src/types/`, `src/utils/`, `src/lib/`

**Config files:**
`tsconfig.json`, `.eslintrc.json`, `.eslintrc.js`, `eslint.config.js`, `.prettierrc`, `tailwind.config.ts`, `tailwind.config.js`, `vitest.config.ts`, `jest.config.ts`, `.env.example`

**Tooling:**
`Makefile`, `.github/workflows/`

**Existing .claude/ content:**
`.claude/CLAUDE.md`, list all files in `.claude/skills/`, `.claude/commands/`, `.claude/rules/`, `.claude/memory/`

---

## Phase 2: Extract Project Context

- **PROJECT_NAME** — from `package.json` name field
- **PURPOSE** — 1–2 sentences from README or `package.json` description
- **FRAMEWORK** — Next.js / Vite / CRA / Remix (from package.json dependencies)
- **LANGUAGE** — TypeScript / JavaScript (from tsconfig.json existence)
- **NODE_VERSION** — from `.nvmrc`, `.node-version`, or `package.json` engines
- **DEV_CMD** — from `package.json` scripts.dev or scripts.start
- **BUILD_CMD** — from `package.json` scripts.build
- **TEST_CMD** — from `package.json` scripts.test (vitest / jest / playwright)
- **LINT_CMD** — from `package.json` scripts.lint
- **COMPONENTS_PATH** — actual path (e.g. `src/components/` or `components/`)
- **PAGES_PATH** — actual path (e.g. `src/pages/` or `src/app/` for Next.js)
- **HOOKS_PATH** — actual path (e.g. `src/hooks/`)
- **API_PATH** — actual path (e.g. `src/api/` or `src/services/`)
- **STATE_MANAGER** — Zustand / Redux Toolkit / Recoil / Jotai / Context only / None
- **DATA_FETCHING** — React Query / SWR / RTK Query / axios / fetch / None
- **ROUTER** — React Router / Next.js App Router / Next.js Pages Router / TanStack Router
- **CSS** — Tailwind / CSS Modules / styled-components / Emotion / plain CSS
- **UI_LIB** — shadcn/ui / Radix / MUI / Chakra / Headless UI / None
- **E2E** — Playwright / Cypress / None
- **EXTRA_LIBS** — other notable dependencies detected

---

## Phase 3: Fully Rewrite .claude/CLAUDE.md

**Replace** the entire contents of `.claude/CLAUDE.md`:

```
# Project Rules — [PROJECT_NAME]

## Stack
React, [FRAMEWORK], [LANGUAGE], [CSS], [STATE_MANAGER] state, [DATA_FETCHING] data fetching

## Dev Commands
- Start:  [DEV_CMD]
- Build:  [BUILD_CMD]
- Test:   [TEST_CMD]
- Lint:   [LINT_CMD]

## Project Structure
[Actual layout — only paths that exist]
- [COMPONENTS_PATH] — reusable UI components
- [PAGES_PATH] — [route-based pages / Next.js app dir / etc]
- [HOOKS_PATH] — custom React hooks
- [API_PATH] — API client functions
- [store/ or context/ path] — [STATE_MANAGER] state
- src/types/ — TypeScript interfaces/types

## State Management ([STATE_MANAGER])
[How state is organized: stores, slices, or context files found. Actual store file paths.]

## Data Fetching ([DATA_FETCHING])
[How API calls are made. Base URL source (env var name). Auth header pattern if detected.]

## Routing ([ROUTER])
[Route organization found: file-based / manual. Route patterns detected in codebase.]

## Styling ([CSS])
[How CSS is applied. Config file path. Design tokens or theme file if found.]

## TypeScript Config
[Strict mode: yes/no. Path aliases from tsconfig.json. Notable compiler options.]

## Code Style
[ESLint config file. Prettier config. Key rules detected.]

## Always Do
[Derive from actual codebase patterns: e.g. "all API calls in src/api/", "hooks return typed objects"]

## Never Do
[Derive from codebase conventions]

## Testing
[TEST_CMD]. [Unit/Integration/E2E breakdown]. Test file location convention found.

## MCP Servers
[Playwright MCP if E2E detected; GitHub MCP; Filesystem MCP]
```

---

## Phase 4: Create .claude/memory/ Files

### .claude/memory/project.md
```
---
type: project
updated: [today YYYY-MM-DD]
---
# [PROJECT_NAME]

[PURPOSE]

## Quick Reference
- Dev:    [DEV_CMD]
- Test:   [TEST_CMD]
- Stack:  [FRAMEWORK], [STATE_MANAGER], [DATA_FETCHING]
- CSS:    [CSS]
- Router: [ROUTER]

## Key Components
[List notable components found: name — what it renders]

## State Stores
[List store/context files found: file — what state it manages]

## API Layer
[List API files found: file — what endpoints it calls. Base URL env var name.]

## Key Files
[Entry point, router config, global providers setup, env variables needed]
```

### .claude/memory/stack.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Stack Details — [PROJECT_NAME]

## NPM Dependencies and Their Role
[Each non-obvious package: name — what it does in this project]

## State Management ([STATE_MANAGER])
[Store file locations. How to add new state. Selector patterns used.]

## Data Fetching ([DATA_FETCHING])
[Client setup. Query key conventions if React Query. Base URL config. Auth token injection.]

## Routing ([ROUTER])
[Route definitions location. Protected route pattern. Navigation patterns used.]

## UI Library ([UI_LIB or CSS])
[Component naming. Theme config. How dark mode works if configured.]

## Environment Variables
[All VITE_* / NEXT_PUBLIC_* vars from .env.example with their purpose]
```

### .claude/memory/conventions.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Conventions — [PROJECT_NAME]

## Component Structure
[File structure for components: index.tsx + types.ts? Single file? With test colocation?]

## Hook Pattern
[How custom hooks are structured — include a real example from the codebase]

## API Call Pattern
[How API functions are written — include a real example]

## Type Conventions
[How types/interfaces are named and organized]

## Test Pattern
[Test file naming, setup pattern, assertion style from actual tests]
```

---

## Phase 5: Rewrite Existing Skills with Project-Specific Code

For each file in `.claude/skills/*/SKILL.md`:
1. Read current content
2. Replace examples with this project's actual:
   - Import paths matching COMPONENTS_PATH, HOOKS_PATH, API_PATH
   - State manager syntax (Zustand store / Redux slice / Context) matching STATE_MANAGER
   - CSS approach matching CSS (Tailwind classes / CSS modules / styled)
   - TypeScript types matching LANGUAGE and tsconfig strict setting
3. Keep structure, replace all generic placeholders

---

## Phase 6: Add New Skills for Detected Libraries

Create `.claude/skills/<name>/SKILL.md` for each detected lib not already present:

**@tanstack/react-query → react-query-patterns:**
Cover: QueryClient setup, useQuery, useMutation, query key conventions, optimistic updates, error handling. Use actual API path pattern.

**zustand → zustand-store:**
Cover: store creation, slices if used, devtools, persistence, typed selectors. Use actual store files as reference.

**@reduxjs/toolkit → redux-patterns:**
Cover: createSlice, createAsyncThunk, RTK Query if used, typed hooks. Use actual slice files.

**react-router-dom → routing-patterns:**
Cover: route definition, protected routes, navigation hooks, URL params. Use actual route structure.

**axios → api-client:**
Cover: instance setup, interceptors for auth, request/response typing. Use actual baseURL env var.

**framer-motion → animation-patterns:**
Cover: variants, page transitions, layout animations, gestures.

**shadcn/ui → shadcn-components:**
Cover: component usage, theming, extending components, dark mode.

**@playwright/test → e2e-testing:**
Cover: test file structure, page object model, fixture setup, CI config.

---

## Phase 7: Update Commands with Project Paths

Update each `.claude/commands/` file:
- Replace `src/components/` with [COMPONENTS_PATH]
- Replace `src/pages/` with [PAGES_PATH]
- Replace `src/hooks/` with [HOOKS_PATH]
- Replace `npm test` with [TEST_CMD]
- Replace `npm run dev` with [DEV_CMD]
- Replace generic component examples with actual component style from codebase
- Update import path examples to match tsconfig aliases if configured

---

## Phase 8: Update .claude/rules/

Rewrite `.claude/rules/coding-standards.md` with:
- Actual ESLint rules from config file
- Prettier config (print width, quotes, semi)
- TypeScript strict settings from tsconfig.json
- CSS approach rules (Tailwind ordering, CSS module naming)
- Framework-specific rules (Next.js server/client components if applicable)

---

## Phase 9: Report

```
✓ Rewrote .claude/CLAUDE.md — [PROJECT_NAME] ([FRAMEWORK], [STATE_MANAGER])
✓ Created .claude/memory/project.md
✓ Created .claude/memory/stack.md
✓ Created .claude/memory/conventions.md
✓ Updated N skills with project-specific code examples
✓ Added new skills: [list or "none"]
✓ Updated N commands with actual paths
✓ Rewrote .claude/rules/coding-standards.md

.claude/ is now tuned for [PROJECT_NAME].
Run /claude-fit again after major dependency changes.
```
