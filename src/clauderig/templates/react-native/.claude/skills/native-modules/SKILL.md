---
name: native-modules
description: Patterns for using native device APIs via Expo modules.
---

# Native Module Patterns

## Camera (expo-camera)

```typescript
import { CameraView, useCameraPermissions } from "expo-camera";

export function CameraScreen() {
  const [permission, requestPermission] = useCameraPermissions();

  if (!permission?.granted) {
    return <Button title="Grant Camera Access" onPress={requestPermission} />;
  }

  return <CameraView style={{ flex: 1 }} facing="back" />;
}
```

## Location (expo-location)

```typescript
import * as Location from "expo-location";

async function getCurrentLocation() {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== "granted") return null;
  return Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.Balanced });
}
```

## Image Picker (expo-image-picker)

```typescript
import * as ImagePicker from "expo-image-picker";

async function pickImage() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ImagePicker.MediaTypeOptions.Images,
    allowsEditing: true,
    quality: 0.8,
  });
  if (!result.canceled) return result.assets[0].uri;
  return null;
}
```

## Platform-Specific Styles

```typescript
import { Platform, StyleSheet } from "react-native";

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === "ios" ? 44 : 24,
    ...Platform.select({
      ios: { shadowColor: "#000", shadowOpacity: 0.1 },
      android: { elevation: 4 },
    }),
  },
});
```

## Permissions Pattern

Always: check → request → handle denial gracefully. Never assume granted.
