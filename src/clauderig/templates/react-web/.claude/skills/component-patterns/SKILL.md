---
name: component-patterns
description: React component composition patterns — compound components, render props, and HOCs.
---

# React Component Patterns

## Compound Components

```typescript
// src/components/Tabs/index.tsx
import { createContext, useContext, useState } from "react";

interface TabsContextValue {
  active: string;
  setActive: (id: string) => void;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabs() {
  const ctx = useContext(TabsContext);
  if (!ctx) throw new Error("Must be used inside <Tabs>");
  return ctx;
}

export function Tabs({ children, defaultTab }: { children: React.ReactNode; defaultTab: string }) {
  const [active, setActive] = useState(defaultTab);
  return <TabsContext.Provider value={{ active, setActive }}>{children}</TabsContext.Provider>;
}

Tabs.Tab = function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { active, setActive } = useTabs();
  return (
    <button
      className={active === id ? "border-b-2 border-blue-500" : ""}
      onClick={() => setActive(id)}
    >
      {children}
    </button>
  );
};

Tabs.Panel = function Panel({ id, children }: { id: string; children: React.ReactNode }) {
  const { active } = useTabs();
  return active === id ? <div>{children}</div> : null;
};
```

Usage:
```tsx
<Tabs defaultTab="profile">
  <Tabs.Tab id="profile">Profile</Tabs.Tab>
  <Tabs.Tab id="settings">Settings</Tabs.Tab>
  <Tabs.Panel id="profile"><ProfileForm /></Tabs.Panel>
  <Tabs.Panel id="settings"><SettingsForm /></Tabs.Panel>
</Tabs>
```

## Controlled vs Uncontrolled

```typescript
interface InputProps {
  value?: string;           // controlled
  defaultValue?: string;    // uncontrolled
  onChange?: (value: string) => void;
}

export function Input({ value, defaultValue, onChange }: InputProps) {
  const [internal, setInternal] = useState(defaultValue ?? "");
  const current = value ?? internal;
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (value === undefined) setInternal(e.target.value);
    onChange?.(e.target.value);
  };
  return <input value={current} onChange={handleChange} />;
}
```

## Polymorphic Component

```typescript
type AsProp<C extends React.ElementType> = { as?: C };
type PropsOf<C extends React.ElementType, P = {}> = P &
  AsProp<C> &
  Omit<React.ComponentPropsWithoutRef<C>, keyof (P & AsProp<C>)>;

export function Text<C extends React.ElementType = "p">({
  as,
  children,
  ...props
}: PropsOf<C, { children: React.ReactNode }>) {
  const Tag = as ?? "p";
  return <Tag {...props}>{children}</Tag>;
}
// <Text as="h1">Title</Text>
// <Text as="span">Inline</Text>
```
