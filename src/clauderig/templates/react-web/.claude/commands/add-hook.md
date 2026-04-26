---
name: add-hook
description: Add a custom React hook for data fetching, state, or side effects.
---

# /add-hook

Ask:
1. Hook name? (use<Name>)
2. What does it do?
3. What does it return?

Create `src/hooks/use<Name>.ts` with:
- TypeScript return type
- Loading, error states for data-fetching hooks
- Cleanup in `useEffect` where applicable

Write a test in `src/hooks/use<Name>.test.ts` using `renderHook`.

Run `npm test -- --run use<Name>` and show output.
