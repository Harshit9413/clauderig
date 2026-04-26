---
name: add-test
description: Write a PHPUnit test for an existing controller endpoint or service method.
---

# /add-test

Ask:
1. What to test? (endpoint URL or class::method)
2. What behavior to verify?
3. Feature test (HTTP) or unit test?

Then:
- Feature tests use `$this->getJson()`, `$this->postJson()` etc.
- Mock external deps with `$this->mock(ServiceClass::class)`
- Use factories: `User::factory()->create()`
- Name: `test_<what>_<outcome>` (e.g., `test_create_product_returns_201`)

Run `php artisan test --filter=<test_name>` and show output.
