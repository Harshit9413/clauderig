# PHP / Laravel Coding Standards

## Do
- `declare(strict_types=1)` at top of every file
- Use Form Requests for all validation
- Service classes for business logic; controllers only delegate
- Return type declarations on every method
- Use factories in tests, never hand-craft models

## Don't
- No `DB::raw()` with user input (SQL injection risk)
- No business logic in controllers or models
- No hard-coded credentials or `.env` values in code
- No `@` error suppression operator
- No skipping CSRF on web routes
