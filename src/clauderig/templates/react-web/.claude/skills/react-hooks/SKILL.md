---
name: react-hooks
description: React hook patterns for state, effects, data fetching, and performance.
---

# React Hook Patterns

## Data Fetching Hook

```typescript
// src/hooks/useUser.ts
import { useState, useEffect } from "react";

interface User {
  id: number;
  name: string;
  email: string;
}

export function useUser(userId: number) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/users/${userId}`)
      .then((r) => r.json())
      .then((data) => { if (!cancelled) setUser(data); })
      .catch((err) => { if (!cancelled) setError(err); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [userId]);

  return { user, loading, error };
}
```

## useMemo — Derived State

```typescript
const total = useMemo(
  () => items.reduce((sum, item) => sum + item.price, 0),
  [items]
);
```

## useCallback — Stable References

```typescript
const handleSubmit = useCallback(
  (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit(formData);
  },
  [formData, onSubmit]
);
```

## useRef — DOM + Mutable Values

```typescript
// Focus on mount
const inputRef = useRef<HTMLInputElement>(null);
useEffect(() => { inputRef.current?.focus(); }, []);
```

## Custom Form Hook

```typescript
export function useForm<T extends Record<string, unknown>>(initial: T) {
  const [values, setValues] = useState(initial);
  const onChange = (e: React.ChangeEvent<HTMLInputElement>) =>
    setValues((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  const reset = () => setValues(initial);
  return { values, onChange, reset };
}
```
