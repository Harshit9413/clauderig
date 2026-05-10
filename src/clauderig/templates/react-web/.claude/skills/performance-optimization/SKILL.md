---
name: performance-optimization
description: Advanced React performance — memoization, code splitting, lazy loading, and bundle analysis.
---

# React Performance Optimization

## Memoization

```typescript
// React.memo — skip re-render when props unchanged
const ProductCard = React.memo(function ProductCard({ product }: { product: Product }) {
  return <div>{product.name}</div>;
}, (prev, next) => prev.product.id === next.product.id && prev.product.price === next.product.price);

// useMemo — expensive derived value
const sortedItems = useMemo(
  () => [...items].sort((a, b) => a.price - b.price),
  [items]
);

// useCallback — stable function reference for child props
const handleDelete = useCallback(
  (id: number) => dispatch({ type: "DELETE", id }),
  [dispatch]
);
```

## Code Splitting — Route Level

```typescript
// src/router.tsx
import { lazy, Suspense } from "react";
import { createBrowserRouter } from "react-router-dom";

const Dashboard = lazy(() => import("./pages/Dashboard"));
const Settings  = lazy(() => import("./pages/Settings"));

export const router = createBrowserRouter([
  {
    path: "/dashboard",
    element: (
      <Suspense fallback={<PageSkeleton />}>
        <Dashboard />
      </Suspense>
    ),
  },
  {
    path: "/settings",
    element: (
      <Suspense fallback={<PageSkeleton />}>
        <Settings />
      </Suspense>
    ),
  },
]);
```

## Deferred Non-Urgent Updates

```typescript
import { useDeferredValue, useMemo } from "react";

function SearchResults({ query }: { query: string }) {
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;

  const results = useMemo(
    () => expensiveSearch(deferredQuery),
    [deferredQuery]
  );

  return (
    <div style={{ opacity: isStale ? 0.5 : 1 }}>
      {results.map((r) => <ResultRow key={r.id} item={r} />)}
    </div>
  );
}
```

## Virtualized List (react-window)

```typescript
import { FixedSizeList as List } from "react-window";

function VirtualList({ items }: { items: Item[] }) {
  const Row = ({ index, style }: { index: number; style: React.CSSProperties }) => (
    <div style={style}>
      <ItemCard item={items[index]} />
    </div>
  );

  return (
    <List height={600} itemCount={items.length} itemSize={80} width="100%">
      {Row}
    </List>
  );
}
```

## Image Optimization

```typescript
// Lazy load images
function LazyImage({ src, alt }: { src: string; alt: string }) {
  return <img src={src} alt={alt} loading="lazy" decoding="async" />;
}

// Intersection Observer for custom lazy load
function useInView(ref: React.RefObject<Element>) {
  const [inView, setInView] = useState(false);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        setInView(true);
        observer.disconnect();
      }
    });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [ref]);
  return inView;
}
```

## Bundle Analysis (Vite)

```bash
# vite.config.ts
import { visualizer } from "rollup-plugin-visualizer";

export default defineConfig({
  plugins: [
    react(),
    visualizer({ open: true, gzipSize: true }),  // npm run build → opens report
  ],
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          router: ["react-router-dom"],
        },
      },
    },
  },
});
```
