---
name: rn-storage
description: React Native local storage patterns using AsyncStorage and MMKV.
---

# React Native Storage Patterns

## AsyncStorage — Simple Key/Value

```typescript
import AsyncStorage from "@react-native-async-storage/async-storage";

// Store
export async function saveUser(user: User): Promise<void> {
  await AsyncStorage.setItem("@user", JSON.stringify(user));
}

// Retrieve
export async function getUser(): Promise<User | null> {
  const raw = await AsyncStorage.getItem("@user");
  return raw ? (JSON.parse(raw) as User) : null;
}

// Remove
export async function clearUser(): Promise<void> {
  await AsyncStorage.removeItem("@user");
}
```

## MMKV — Fast Synchronous Storage

```typescript
import { MMKV } from "react-native-mmkv";

export const storage = new MMKV({ id: "app-storage" });

// Write (synchronous)
storage.set("token", "Bearer abc123");
storage.set("userId", 42);
storage.set("settings", JSON.stringify({ theme: "dark" }));

// Read (synchronous)
const token = storage.getString("token");
const userId = storage.getNumber("userId");
const settings = JSON.parse(storage.getString("settings") ?? "{}");

// Delete
storage.delete("token");
```

## Storage Hook

```typescript
import { useState, useEffect } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";

export function useStorage<T>(key: string, defaultValue: T) {
  const [value, setValue] = useState<T>(defaultValue);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem(key)
      .then((raw) => {
        if (raw !== null) setValue(JSON.parse(raw) as T);
      })
      .finally(() => setLoading(false));
  }, [key]);

  const update = async (next: T) => {
    setValue(next);
    await AsyncStorage.setItem(key, JSON.stringify(next));
  };

  const remove = async () => {
    setValue(defaultValue);
    await AsyncStorage.removeItem(key);
  };

  return { value, loading, update, remove };
}
```

Usage:
```typescript
const { value: theme, update: setTheme } = useStorage("theme", "light");
```

## Zustand + MMKV Persist

```typescript
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { storage } from "./storage";

const mmkvStorage = {
  getItem: (key: string) => storage.getString(key) ?? null,
  setItem: (key: string, value: string) => storage.set(key, value),
  removeItem: (key: string) => storage.delete(key),
};

interface AuthStore {
  token: string | null;
  setToken: (token: string | null) => void;
}

export const useAuthStore = create<AuthStore>()(
  persist(
    (set) => ({
      token: null,
      setToken: (token) => set({ token }),
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => mmkvStorage),
    }
  )
);
```
