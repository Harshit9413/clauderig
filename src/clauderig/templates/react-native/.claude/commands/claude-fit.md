---
name: claude-fit
description: Deep-scan this React Native project and rebuild .claude/ to be fully project-specific.
---

# /claude-fit

You are performing a **complete project analysis** to transform this `.claude/` folder from generic templates into a project-specific tool. Work through every phase completely without skipping.

---

## Phase 1: Project Discovery

Read every file below that exists (use the Read tool):

**Package manifests:**
`package.json`, `app.json`, `app.config.js`, `app.config.ts`

**Entry points:**
`App.tsx`, `App.ts`, `index.js`, `src/App.tsx`

**Project structure — list and read up to 3 files from each directory that exists:**
`src/screens/`, `src/components/`, `src/navigation/`, `src/hooks/`, `src/api/`, `src/store/`, `src/context/`, `src/types/`, `src/utils/`, `src/constants/`, `src/services/`

**Config:**
`tsconfig.json`, `.eslintrc.json`, `.eslintrc.js`, `babel.config.js`, `metro.config.js`, `.prettierrc`, `.env.example`, `eas.json`

**Tooling:**
`.github/workflows/`, `Makefile`

**Existing .claude/ content:**
`.claude/CLAUDE.md`, list all files in `.claude/skills/`, `.claude/commands/`, `.claude/rules/`, `.claude/memory/`

---

## Phase 2: Extract Project Context

- **PROJECT_NAME** — from `app.json` name or `package.json` name
- **PURPOSE** — 1–2 sentences from README or app.json description
- **EXPO_SDK** — Expo SDK version from `package.json` (or bare React Native version)
- **IS_EXPO** — yes/no (expo in dependencies)
- **IS_EAS** — yes/no (eas.json exists)
- **LANGUAGE** — TypeScript / JavaScript
- **TEST_CMD** — from `package.json` scripts.test
- **LINT_CMD** — from `package.json` scripts.lint
- **DEV_CMD** — `npx expo start` or `npx react-native run-ios` etc.
- **SCREENS_PATH** — actual path (e.g. `src/screens/` or `screens/`)
- **COMPONENTS_PATH** — actual path
- **NAVIGATION_PATH** — actual path
- **HOOKS_PATH** — actual path
- **API_PATH** — actual path
- **STATE_MANAGER** — Zustand / Redux Toolkit / Context / None
- **DATA_FETCHING** — React Query / SWR / axios / fetch / None
- **NAV_LIB** — React Navigation v5/v6 / Expo Router
- **NAV_STRUCTURE** — Stack / Tab / Drawer / Mixed (from navigation files)
- **SCREEN_NAMES** — actual screen component names found
- **AUTH_FLOW** — yes/no + library (expo-auth-session / react-native-app-auth / custom)
- **STORAGE** — AsyncStorage / SecureStore / MMKV / None
- **NOTIFICATIONS** — expo-notifications / react-native-push-notification / None
- **EXTRA_LIBS** — other notable dependencies

---

## Phase 3: Fully Rewrite .claude/CLAUDE.md

**Replace** the entire contents of `.claude/CLAUDE.md`:

```
# Project Rules — [PROJECT_NAME]

## Stack
React Native, [EXPO_SDK or bare], [LANGUAGE], [NAV_LIB] navigation, [STATE_MANAGER] state

## Dev Commands
- Start:       [DEV_CMD]
- iOS:         [npx expo run:ios or npx react-native run-ios]
- Android:     [npx expo run:android or npx react-native run-android]
- Test:        [TEST_CMD]
- Lint:        [LINT_CMD]
- [EAS build if IS_EAS]: eas build --platform all

## Project Structure
[Actual layout — only paths that exist]
- [SCREENS_PATH] — screen components
- [COMPONENTS_PATH] — reusable UI components
- [NAVIGATION_PATH] — navigation configuration
- [HOOKS_PATH] — custom hooks
- [API_PATH] — API client functions
- src/constants/ — colors, spacing, config

## Navigation ([NAV_LIB])
[NAV_STRUCTURE. Root navigator type. Auth flow vs main flow separation if found.]

## Screens
[SCREEN_NAMES — one per line with what it shows]

## State Management ([STATE_MANAGER])
[Store file locations. How state is organized.]

## Data Fetching ([DATA_FETCHING])
[API client setup. Base URL env var or config constant. Auth token injection.]

## Storage ([STORAGE])
[What is stored. Key naming convention. Secure vs non-secure split.]

## Code Style
[ESLint + Prettier. StyleSheet.create for all styles. No inline style objects.]

## Always Do
[Derive from actual codebase: safe-area handling, platform checks, permission patterns]

## Never Do
[Derive from codebase conventions]

## Testing
[TEST_CMD]. Test file location. Mocking patterns used.

## MCP Servers
[GitHub MCP; Filesystem MCP]
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
- Dev:      [DEV_CMD]
- Test:     [TEST_CMD]
- Stack:    Expo [EXPO_SDK], [STATE_MANAGER], [DATA_FETCHING]
- Nav:      [NAV_LIB] — [NAV_STRUCTURE]
- Storage:  [STORAGE]

## Screens
[SCREEN_NAMES — name and what it shows]

## Navigation Structure
[Describe the full nav tree: root navigator → auth/main split → individual stacks/tabs]

## Key Files
[App entry point, navigation root file, auth flow, global providers, env config]
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

## Navigation ([NAV_LIB])
[Navigator types used. How screens are registered. Deep linking config if found.]

## Auth Flow
[If present: how login state is persisted, how nav reacts to auth state, token storage]

## State ([STATE_MANAGER])
[Store files. How to add new state. Async state handling.]

## API Layer ([DATA_FETCHING])
[Client file. Base URL source. Request interceptors. Error handling pattern.]

## Push Notifications ([NOTIFICATIONS or "none"])
[Setup, permission request, handler registration, deep link from notification]

## Environment Variables
[All env vars from .env.example with their purpose and how they are loaded]
```

### .claude/memory/conventions.md
```
---
type: reference
updated: [today YYYY-MM-DD]
---
# Conventions — [PROJECT_NAME]

## Screen Structure
[How screen components are organized: single file? Separate styles? Header config?]

## Component Pattern
[Props interface naming. StyleSheet placement. Platform-specific variants.]

## Navigation Pattern
[How to navigate between screens. How to pass params. useNavigation vs prop drilling.]

## Style Convention
[Colors from constants. Spacing scale. Platform.select usage patterns found.]

## Test Pattern
[Test file naming. Mock patterns. renderWithProviders if custom render found.]
```

---

## Phase 5: Rewrite Existing Skills with Project-Specific Code

For each file in `.claude/skills/*/SKILL.md`:
1. Read current content
2. Replace examples with this project's actual:
   - Screen names from SCREEN_NAMES
   - Navigation types matching NAV_STRUCTURE
   - Import paths matching SCREENS_PATH, COMPONENTS_PATH, NAVIGATION_PATH
   - State manager syntax matching STATE_MANAGER
3. Keep structure, replace all generic placeholders

---

## Phase 6: Add New Skills for Detected Libraries

Create `.claude/skills/<name>/SKILL.md` for each detected lib not already present:

**@tanstack/react-query → react-query-patterns:**
Cover: QueryClient in App.tsx, useQuery/useMutation, query key conventions, offline handling. Use actual API path.

**zustand → zustand-store:**
Cover: store creation, persist middleware with AsyncStorage/MMKV, typed selectors. Reference actual stores.

**expo-notifications → push-notifications:**
Cover: permission request, token registration, notification handler, background handler, deep link from tap.

**react-native-maps → maps-integration:**
Cover: MapView setup, marker rendering, region control, permission handling.

**expo-auth-session / react-native-app-auth → oauth-auth:**
Cover: provider config, token exchange, secure storage, refresh flow.

**react-native-reanimated → animation-patterns:**
Cover: useSharedValue, useAnimatedStyle, withTiming/withSpring, gesture integration.

**@react-native-async-storage → storage-patterns:**
Cover: get/set/remove, typed wrappers, migration patterns, SecureStore for sensitive data.

**eas → eas-build:**
Cover: build profiles, env vars in EAS, submit config, OTA updates with expo-updates.

---

## Phase 7: Update Commands with Project Paths

Update each `.claude/commands/` file:
- Replace `src/screens/` with [SCREENS_PATH]
- Replace `src/components/` with [COMPONENTS_PATH]
- Replace `src/navigation/` with [NAVIGATION_PATH]
- Replace `npm test` with [TEST_CMD]
- Replace `npx expo start` with [DEV_CMD]
- Replace generic screen examples with first name from SCREEN_NAMES
- Update navigation import to match actual nav file structure

---

## Phase 8: Update .claude/rules/

Rewrite `.claude/rules/coding-standards.md` with:
- TypeScript strictness from tsconfig.json
- ESLint rules from config
- Prettier settings
- StyleSheet requirements (create vs inline)
- Platform-specific code conventions from codebase
- Expo SDK constraints (managed vs bare workflow)

---

## Phase 9: Report

```
✓ Rewrote .claude/CLAUDE.md — [PROJECT_NAME] ([EXPO_SDK], [NAV_STRUCTURE] nav)
✓ Created .claude/memory/project.md
✓ Created .claude/memory/stack.md
✓ Created .claude/memory/conventions.md
✓ Updated N skills with project-specific code examples
✓ Added new skills: [list or "none"]
✓ Updated N commands with actual paths
✓ Rewrote .claude/rules/coding-standards.md

.claude/ is now tuned for [PROJECT_NAME].
Run /claude-fit again after adding major new packages or screens.
```
