---
name: add-component
description: Add a new React Native component with typed props and test.
---

# /add-component

Ask:
1. Component name?
2. What does it render?
3. What props?

Create:
- `src/components/<Name>.tsx` — typed props, `StyleSheet.create`
- `src/components/<Name>.test.tsx` — render test

Avoid inline styles, extract platform-specific logic to constants.
Run `npm test -- --testPathPattern=<Name>` and show output.
