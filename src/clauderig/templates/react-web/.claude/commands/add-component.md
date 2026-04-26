---
name: add-component
description: Add a new React component with TypeScript props, styling, and test.
---

# /add-component

Ask:
1. Component name? (PascalCase)
2. What does it render?
3. What props does it accept?
4. Does it fetch data or receive it via props?

Create:
- `src/components/<Name>/index.tsx` — typed props interface, component
- `src/components/<Name>/<Name>.test.tsx` — renders without crash + key behavior

Use Tailwind for styling. If it fetches data, extract into `src/hooks/use<Name>.ts`.

Run `npm test -- --run <Name>` and show output.
