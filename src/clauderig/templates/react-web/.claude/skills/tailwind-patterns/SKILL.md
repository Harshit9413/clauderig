---
name: tailwind-patterns
description: Tailwind CSS patterns for layout, responsive design, and component styling.
---

# Tailwind CSS Patterns

## Responsive Layout

```tsx
<div className="flex flex-col md:flex-row gap-4">
  <aside className="w-full md:w-64 shrink-0">...</aside>
  <main className="flex-1 min-w-0">...</main>
</div>
```

## Card Component

```tsx
<div className="rounded-xl border border-gray-200 bg-white p-6 shadow-sm hover:shadow-md transition-shadow">
  <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
  <p className="mt-2 text-sm text-gray-500">{description}</p>
</div>
```

## Button Variants

```tsx
const base = "rounded-lg px-4 py-2 font-medium text-sm transition-colors focus-visible:outline-none focus-visible:ring-2";
const variants = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-100 text-gray-700 hover:bg-gray-200",
  danger: "bg-red-600 text-white hover:bg-red-700",
};
```

## Form Inputs

```tsx
<input
  className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm
             placeholder:text-gray-400 focus:border-blue-500 focus:outline-none
             focus:ring-1 focus:ring-blue-500"
/>
```

## Conditional Classes (use clsx)

```typescript
import clsx from "clsx";
const className = clsx("base", isActive && "active", isDisabled && "opacity-50 cursor-not-allowed");
```

## Dark Mode

```tsx
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100">
```
