---
name: expo-patterns
description: Expo SDK patterns for config, assets, environment, and build.
---

# Expo Patterns

## app.config.js (dynamic config)

```javascript
export default {
  expo: {
    name: "MyApp",
    slug: "my-app",
    version: "1.0.0",
    orientation: "portrait",
    icon: "./assets/icon.png",
    ios: { bundleIdentifier: "com.yourco.myapp", supportsTablet: false },
    android: { package: "com.yourco.myapp" },
    extra: {
      apiUrl: process.env.API_URL,
      eas: { projectId: "your-project-id" },
    },
  },
};
```

## Environment Variables

```typescript
import Constants from "expo-constants";
export const API_URL = Constants.expoConfig?.extra?.apiUrl as string;
```

Never put secrets in `app.config.js`. Use EAS Secrets for production.

## SecureStore (sensitive data)

```typescript
import * as SecureStore from "expo-secure-store";

await SecureStore.setItemAsync("authToken", token);
const token = await SecureStore.getItemAsync("authToken");
```

Never use AsyncStorage for tokens — use SecureStore.

## EAS Build

```bash
eas build --profile development --platform ios   # dev build
eas build --profile production --platform all    # production
```
