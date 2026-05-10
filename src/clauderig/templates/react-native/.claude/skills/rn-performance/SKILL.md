---
name: rn-performance
description: React Native performance — FlatList optimization, Hermes, JS thread offloading, and memory profiling.
---

# React Native Performance

## FlatList Optimization

```typescript
import { FlatList, ViewToken } from "react-native";
import { useCallback, memo } from "react";

interface Item { id: string; title: string }

const ItemRow = memo(function ItemRow({ item }: { item: Item }) {
  return <Text>{item.title}</Text>;
});

export function OptimizedList({ data }: { data: Item[] }) {
  const renderItem = useCallback(
    ({ item }: { item: Item }) => <ItemRow item={item} />,
    []
  );

  const keyExtractor = useCallback((item: Item) => item.id, []);

  const onViewableItemsChanged = useCallback(
    ({ viewableItems }: { viewableItems: ViewToken[] }) => {
      // prefetch next batch based on visible items
    },
    []
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      maxToRenderPerBatch={10}       // items per JS batch
      updateCellsBatchingPeriod={50} // ms between batches
      windowSize={5}                 // render 5x viewport
      initialNumToRender={10}
      removeClippedSubviews          // unmount off-screen items
      getItemLayout={(_, index) => ({ length: 80, offset: 80 * index, index })}
      onViewableItemsChanged={onViewableItemsChanged}
    />
  );
}
```

## Hermes Engine (app.json / metro.config.js)

```json
// app.json — enable Hermes
{
  "expo": {
    "jsEngine": "hermes"
  }
}
```

```javascript
// Check Hermes at runtime
if (global.HermesInternal) {
  console.log("Hermes is enabled");
}
```

## Move Work Off JS Thread

```typescript
// react-native-fast-image for image caching
import FastImage from "react-native-fast-image";

<FastImage
  style={{ width: 200, height: 200 }}
  source={{ uri: imageUrl, priority: FastImage.priority.normal }}
  resizeMode={FastImage.resizeMode.cover}
/>

// Worklets for heavy computation (Reanimated)
import { runOnUI, runOnJS } from "react-native-reanimated";

const processOnUI = () => {
  "worklet";
  const result = heavyComputation();
  runOnJS(setResult)(result);
};
```

## InteractionManager — Defer Heavy Work

```typescript
import { InteractionManager } from "react-native";
import { useEffect } from "react";

export function ExpensiveScreen() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    // Wait for navigation animation to finish
    const task = InteractionManager.runAfterInteractions(() => {
      setReady(true);
    });
    return () => task.cancel();
  }, []);

  if (!ready) return <LoadingSkeleton />;
  return <HeavyComponent />;
}
```

## Memory — Avoid Leaks

```typescript
// Cancel async operations on unmount
useEffect(() => {
  let cancelled = false;
  fetchData().then((data) => {
    if (!cancelled) setData(data);
  });
  return () => { cancelled = true; };
}, []);

// Clear timers
useEffect(() => {
  const id = setInterval(poll, 5000);
  return () => clearInterval(id);
}, []);

// Remove event listeners
useEffect(() => {
  const sub = AppState.addEventListener("change", handleAppState);
  return () => sub.remove();
}, []);
```

## Flipper Performance Profiling

```bash
# Install Flipper plugins for RN
# - Hermes Debugger
# - React DevTools
# - Network Inspector

# Profile JS thread in Flipper:
# Open app → Flipper → React Native → Profiler → Record
```
