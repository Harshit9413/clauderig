---
name: rn-offline
description: React Native offline-first patterns — NetInfo, optimistic updates, background sync, and queue.
---

# React Native Offline-First Patterns

## Network State Detection

```typescript
import NetInfo, { NetInfoState } from "@react-native-community/netinfo";
import { useEffect, useState } from "react";

export function useNetworkStatus() {
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    const unsubscribe = NetInfo.addEventListener((state: NetInfoState) => {
      setIsOnline(state.isConnected ?? false);
    });
    return unsubscribe;
  }, []);

  return isOnline;
}
```

## Offline Banner

```typescript
export function OfflineBanner() {
  const isOnline = useNetworkStatus();
  if (isOnline) return null;

  return (
    <View style={styles.banner}>
      <Text style={styles.text}>You are offline. Changes will sync when reconnected.</Text>
    </View>
  );
}
```

## Optimistic Updates with Rollback

```typescript
import { useAuthStore } from "@/stores/auth";
import { MMKV } from "react-native-mmkv";

const storage = new MMKV({ id: "pending-ops" });

interface PendingOperation {
  id: string;
  type: "CREATE" | "UPDATE" | "DELETE";
  payload: unknown;
  timestamp: number;
}

function useMutationWithOptimistic<T>(
  mutationFn: (payload: T) => Promise<void>,
  onOptimistic: (payload: T) => void,
  onRollback: (payload: T) => void,
) {
  const isOnline = useNetworkStatus();

  return async (payload: T) => {
    onOptimistic(payload);                        // update UI immediately

    if (!isOnline) {
      queueOperation({ type: "UPDATE", payload }); // defer
      return;
    }

    try {
      await mutationFn(payload);
    } catch {
      onRollback(payload);                         // revert on failure
    }
  };
}
```

## Operation Queue with Sync

```typescript
import NetInfo from "@react-native-community/netinfo";
import { storage } from "./storage";

const QUEUE_KEY = "op_queue";

function queueOperation(op: Omit<PendingOperation, "id" | "timestamp">) {
  const existing: PendingOperation[] = JSON.parse(storage.getString(QUEUE_KEY) ?? "[]");
  existing.push({ ...op, id: Date.now().toString(), timestamp: Date.now() });
  storage.set(QUEUE_KEY, JSON.stringify(existing));
}

async function flushQueue(api: ApiClient) {
  const ops: PendingOperation[] = JSON.parse(storage.getString(QUEUE_KEY) ?? "[]");
  if (!ops.length) return;

  const failed: PendingOperation[] = [];
  for (const op of ops) {
    try {
      await api.execute(op);
    } catch {
      failed.push(op);
    }
  }
  storage.set(QUEUE_KEY, JSON.stringify(failed));
}

// Listen for reconnection → flush
NetInfo.addEventListener((state) => {
  if (state.isConnected) flushQueue(apiClient);
});
```

## React Query Offline Persistence

```typescript
import { QueryClient } from "@tanstack/react-query";
import { createAsyncStoragePersister } from "@tanstack/query-async-storage-persister";
import { persistQueryClient } from "@tanstack/react-query-persist-client";
import AsyncStorage from "@react-native-async-storage/async-storage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5,        // 5 min
      gcTime:    1000 * 60 * 60 * 24,  // 24 hr persist
      retry: (failureCount, error: any) =>
        error?.status !== 404 && failureCount < 2,
    },
  },
});

const persister = createAsyncStoragePersister({ storage: AsyncStorage });

persistQueryClient({
  queryClient,
  persister,
  maxAge: 1000 * 60 * 60 * 24, // restore cache up to 24 hours old
});
```

## Background Fetch (Expo)

```typescript
import * as BackgroundFetch from "expo-background-fetch";
import * as TaskManager from "expo-task-manager";

const SYNC_TASK = "background-sync";

TaskManager.defineTask(SYNC_TASK, async () => {
  try {
    await flushQueue(apiClient);
    return BackgroundFetch.BackgroundFetchResult.NewData;
  } catch {
    return BackgroundFetch.BackgroundFetchResult.Failed;
  }
});

await BackgroundFetch.registerTaskAsync(SYNC_TASK, {
  minimumInterval: 15 * 60, // every 15 minutes
  stopOnTerminate: false,
  startOnBoot: true,
});
```
