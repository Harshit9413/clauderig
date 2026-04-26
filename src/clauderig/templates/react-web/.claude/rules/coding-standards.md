# React Web Coding Standards

## Do
- TypeScript for every file (.tsx / .ts)
- Props interfaces for every component
- Custom hooks for data fetching and complex state
- Tailwind for all styling
- Colocate tests with components

## Don't
- No `any` type without a comment explaining why
- No direct DOM manipulation
- No API calls inside JSX
- No useEffect for derived state (use useMemo)
- No prop drilling past 2 levels
