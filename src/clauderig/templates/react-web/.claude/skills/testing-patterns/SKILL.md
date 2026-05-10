---
name: testing-patterns
description: React Testing Library and Vitest patterns for component and hook testing.
---

# React Testing Patterns

## Component Test

```typescript
// src/components/Button/Button.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("renders label and calls onClick", () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Save</Button>);
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    expect(onClick).toHaveBeenCalledOnce();
  });

  it("is disabled when loading", () => {
    render(<Button loading>Save</Button>);
    expect(screen.getByRole("button")).toBeDisabled();
  });
});
```

## Async Component Test

```typescript
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { server } from "@/mocks/server";
import { http, HttpResponse } from "msw";
import { UserProfile } from "./UserProfile";

it("shows user name after load", async () => {
  server.use(
    http.get("/api/users/1", () =>
      HttpResponse.json({ id: 1, name: "Alice" })
    )
  );
  render(<UserProfile userId={1} />);
  expect(screen.getByText(/loading/i)).toBeInTheDocument();
  await screen.findByText("Alice");
});
```

## Custom Hook Test

```typescript
import { renderHook, act } from "@testing-library/react";
import { useCounter } from "./useCounter";

it("increments counter", () => {
  const { result } = renderHook(() => useCounter(0));
  act(() => result.current.increment());
  expect(result.current.count).toBe(1);
});
```

## Form Interaction Test

```typescript
import userEvent from "@testing-library/user-event";

it("submits form with user input", async () => {
  const user = userEvent.setup();
  const onSubmit = vi.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  await user.type(screen.getByLabelText("Email"), "alice@example.com");
  await user.type(screen.getByLabelText("Password"), "secret");
  await user.click(screen.getByRole("button", { name: /login/i }));

  expect(onSubmit).toHaveBeenCalledWith({
    email: "alice@example.com",
    password: "secret",
  });
});
```

## MSW Setup (vitest.setup.ts)

```typescript
import { beforeAll, afterEach, afterAll } from "vitest";
import { server } from "@/mocks/server";

beforeAll(() => server.listen({ onUnhandledRequest: "error" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```
