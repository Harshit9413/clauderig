---
name: advanced-typescript
description: Advanced TypeScript patterns for React — generics, discriminated unions, branded types, and utility types.
---

# Advanced TypeScript for React

## Generic Components

```typescript
interface SelectProps<T> {
  options: T[];
  value: T | null;
  onChange: (value: T) => void;
  getLabel: (option: T) => string;
  getValue: (option: T) => string | number;
}

function Select<T>({ options, value, onChange, getLabel, getValue }: SelectProps<T>) {
  return (
    <select
      value={value ? String(getValue(value)) : ""}
      onChange={(e) => {
        const found = options.find((o) => String(getValue(o)) === e.target.value);
        if (found) onChange(found);
      }}
    >
      {options.map((o) => (
        <option key={String(getValue(o))} value={String(getValue(o))}>
          {getLabel(o)}
        </option>
      ))}
    </select>
  );
}

// Usage — fully typed, no any
<Select
  options={users}
  value={selectedUser}
  onChange={setSelectedUser}
  getLabel={(u) => u.name}
  getValue={(u) => u.id}
/>
```

## Discriminated Unions for State

```typescript
type AsyncState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; error: Error };

function useAsync<T>(fn: () => Promise<T>) {
  const [state, setState] = useState<AsyncState<T>>({ status: "idle" });

  const run = async () => {
    setState({ status: "loading" });
    try {
      const data = await fn();
      setState({ status: "success", data });
    } catch (error) {
      setState({ status: "error", error: error as Error });
    }
  };

  return { state, run };
}

// Exhaustive switch — TS errors if a case is missed
function renderState<T>(state: AsyncState<T>, render: (data: T) => React.ReactNode) {
  switch (state.status) {
    case "idle":    return null;
    case "loading": return <Spinner />;
    case "success": return render(state.data);
    case "error":   return <ErrorMessage error={state.error} />;
  }
}
```

## Branded Types

```typescript
// Prevent mixing up IDs of different entities
type UserId    = number & { readonly __brand: "UserId" };
type ProductId = number & { readonly __brand: "ProductId" };

const toUserId    = (id: number): UserId    => id as UserId;
const toProductId = (id: number): ProductId => id as ProductId;

function getUser(id: UserId): Promise<User> { ... }

getUser(toProductId(1)); // TS error — wrong brand
getUser(toUserId(1));    // OK
```

## Conditional & Mapped Types

```typescript
// Make specific keys optional
type PartialBy<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>;

type CreateUserInput = PartialBy<User, "id" | "createdAt">;

// Deep readonly
type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends object ? DeepReadonly<T[K]> : T[K];
};

// Extract event handler prop names
type EventHandlers<T> = {
  [K in keyof T as K extends `on${string}` ? K : never]: T[K];
};
```

## Template Literal Types

```typescript
type HttpMethod = "GET" | "POST" | "PUT" | "DELETE";
type ApiEndpoint = `/api/${string}`;

type EventName = `on${"Click" | "Focus" | "Blur"}`;
// "onClick" | "onFocus" | "onBlur"

// Typed CSS class builder
type Size = "sm" | "md" | "lg";
type Variant = "primary" | "secondary";
type ButtonClass = `btn-${Size}-${Variant}`;
// "btn-sm-primary" | "btn-sm-secondary" | "btn-md-primary" | ...
```

## useReducer with Typed Actions

```typescript
type Action =
  | { type: "INCREMENT"; by?: number }
  | { type: "DECREMENT"; by?: number }
  | { type: "RESET" };

interface State { count: number }

function reducer(state: State, action: Action): State {
  switch (action.type) {
    case "INCREMENT": return { count: state.count + (action.by ?? 1) };
    case "DECREMENT": return { count: state.count - (action.by ?? 1) };
    case "RESET":     return { count: 0 };
  }
}
```
