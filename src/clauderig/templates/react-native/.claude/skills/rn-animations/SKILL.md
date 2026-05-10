---
name: rn-animations
description: React Native Reanimated 3 patterns for smooth animations and gestures.
---

# React Native Animations

## Fade In with Reanimated

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
  withSpring,
  runOnJS,
} from "react-native-reanimated";
import { useEffect } from "react";

export function FadeIn({ children }: { children: React.ReactNode }) {
  const opacity = useSharedValue(0);

  useEffect(() => {
    opacity.value = withTiming(1, { duration: 300 });
  }, []);

  const style = useAnimatedStyle(() => ({ opacity: opacity.value }));

  return <Animated.View style={style}>{children}</Animated.View>;
}
```

## Slide Up Sheet

```typescript
import { Dimensions } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";
import { Gesture, GestureDetector } from "react-native-gesture-handler";

const SCREEN_HEIGHT = Dimensions.get("window").height;
const SHEET_HEIGHT = SCREEN_HEIGHT * 0.5;

export function BottomSheet({ visible }: { visible: boolean }) {
  const translateY = useSharedValue(SHEET_HEIGHT);

  useEffect(() => {
    translateY.value = withSpring(visible ? 0 : SHEET_HEIGHT, {
      damping: 20,
      stiffness: 150,
    });
  }, [visible]);

  const style = useAnimatedStyle(() => ({
    transform: [{ translateY: translateY.value }],
  }));

  return (
    <Animated.View style={[{ height: SHEET_HEIGHT, position: "absolute", bottom: 0, width: "100%" }, style]}>
      {/* sheet content */}
    </Animated.View>
  );
}
```

## Press Scale Animation

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from "react-native-reanimated";
import { Pressable } from "react-native";

export function AnimatedButton({ onPress, children }: { onPress: () => void; children: React.ReactNode }) {
  const scale = useSharedValue(1);

  const style = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Pressable
      onPressIn={() => { scale.value = withSpring(0.95); }}
      onPressOut={() => { scale.value = withSpring(1); }}
      onPress={onPress}
    >
      <Animated.View style={style}>{children}</Animated.View>
    </Pressable>
  );
}
```

## Layout Animation

```typescript
import Animated, { Layout, FadeIn, FadeOut } from "react-native-reanimated";

// Items animate when added/removed from list
export function AnimatedList({ items }: { items: string[] }) {
  return (
    <>
      {items.map((item) => (
        <Animated.View
          key={item}
          entering={FadeIn.duration(200)}
          exiting={FadeOut.duration(150)}
          layout={Layout.springify()}
        >
          <Text>{item}</Text>
        </Animated.View>
      ))}
    </>
  );
}
```
