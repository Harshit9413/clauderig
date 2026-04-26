---
name: add-screen
description: Add a new React Native screen with navigation registration and test.
---

# /add-screen

Ask:
1. Screen name? (e.g., ProfileScreen)
2. What does it display?
3. What navigator? (Stack / Tab / Drawer)
4. Route params it receives?

Create:
- `src/screens/<Name>Screen.tsx` — typed params, StyleSheet.create
- Register in the navigator in `src/navigation/`
- `src/screens/<Name>Screen.test.tsx` — renders without crash

Use `useSafeAreaInsets` if needed.
Run `npm test -- --testPathPattern=<Name>Screen` and show output.
