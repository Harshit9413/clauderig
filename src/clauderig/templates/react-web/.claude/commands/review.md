---
name: review
description: Review current branch for code quality, accessibility, and test coverage.
---

# /review

Run in order:
1. `git diff main...HEAD` — changed files
2. TypeScript check: `npx tsc --noEmit`
3. For each component: are props typed? any `any`? any direct DOM manipulation?
4. Check: do changed components have test updates?
5. `npm test` — report results
6. `npx eslint .` — report issues

Summary: ✓ good / ✗ fix before merge / ⚠ suggestions
