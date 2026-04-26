# Project Rules — React (Web)

## Stack
React 18+, TypeScript, Vite or Next.js, Tailwind CSS.

## Code Style
- ESLint + Prettier. Run `npx eslint --fix` before commits.
- Use TypeScript strictly — no `any` without justification.
- Functional components only. No class components.
- File naming: `ComponentName.tsx`, hooks as `useHookName.ts`.

## File/Folder Conventions
- Components → `src/components/<ComponentName>/index.tsx`
- Pages/Views → `src/pages/` or `src/app/` (Next.js)
- Hooks → `src/hooks/use<Name>.ts`
- API calls → `src/api/<resource>.ts`
- Types → `src/types/<resource>.ts`
- Utils → `src/utils/<name>.ts`

## Always Do
- Use TypeScript interfaces for all props
- Extract data fetching logic into custom hooks
- Use Tailwind for styling — no inline styles
- Colocate component tests with the component

## Never Do
- No direct DOM manipulation (`document.getElementById`)
- No `useEffect` for derived state — use `useMemo`
- No prop drilling deeper than 2 levels — use context or state manager
- No API calls directly in components

## Testing
- Vitest + React Testing Library
- Run: `npm test`

## Recommended MCP Servers
- **Playwright MCP** — browser automation for testing. Pre-configured.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
