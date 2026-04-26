# Project Rules — React Native

## Stack
React Native 0.73+, Expo SDK 50+, TypeScript, React Navigation v6.

## Code Style
- ESLint + Prettier. Run `npx eslint --fix` before commits.
- TypeScript strictly — no `any`.
- Functional components, hooks only.
- File naming: `ScreenName.tsx`, components as `ComponentName.tsx`.

## File/Folder Conventions
- Screens → `src/screens/<Name>Screen.tsx`
- Components → `src/components/<Name>.tsx`
- Navigation → `src/navigation/`
- Hooks → `src/hooks/use<Name>.ts`
- API calls → `src/api/<resource>.ts`
- Constants → `src/constants/`

## Always Do
- Use React Navigation for all navigation
- Handle safe-area insets via `SafeAreaView` or `useSafeAreaInsets`
- Use `StyleSheet.create` for all styles
- Test on both iOS and Android simulators
- Use `Platform.OS` for platform-specific behavior

## Never Do
- No hard-coded colors — use a theme/constants file
- No inline style objects (create new object each render)
- No navigation calls outside screen components
- No bare `fetch` — wrap in a typed API client
- No `any` type

## Testing
- Jest + React Native Testing Library
- Run: `npm test`

## Recommended MCP Servers
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
