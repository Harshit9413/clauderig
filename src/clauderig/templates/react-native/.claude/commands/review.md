---
name: review
description: Review current branch for RN code quality and test coverage.
---

# /review

1. `git diff main...HEAD`
2. For each changed file: typed props, StyleSheet.create, no `any`, safe-area handled
3. Cross-platform: any iOS/Android specific code without `Platform.OS` guard?
4. `npm test` — report results
5. `npx eslint .` — report issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
