# React Native Coding Standards

## Do
- TypeScript for every file
- `StyleSheet.create` for all styles (enables optimization)
- `Platform.OS` / `Platform.select` for platform differences
- Handle permissions with graceful degradation
- Test on both iOS and Android

## Don't
- No inline style objects (create new object each render)
- No AsyncStorage for sensitive data (use SecureStore)
- No hard-coded colors or spacing — use constants
- No navigation outside screen components
- No `any` type
