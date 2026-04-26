---
name: psr-standards
description: PSR-1, PSR-4, PSR-7, and PSR-12 standards for PHP projects.
---

# PSR Standards

## PSR-12: Code Style

```php
<?php

declare(strict_types=1);

namespace App\Services;

class UserService
{
    public function __construct(
        private readonly UserRepository $repository,
    ) {}

    public function findById(int $id): ?User
    {
        return $this->repository->find($id);
    }

    public function create(array $data): User
    {
        return $this->repository->create($data);
    }
}
```

Key rules:
- 4-space indentation (no tabs)
- Opening brace on same line for classes and methods
- One blank line between methods
- `declare(strict_types=1)` after opening `<?php`

## PSR-4: Autoloading

```json
{
    "autoload": {
        "psr-4": {
            "App\\": "app/"
        }
    }
}
```

Run `composer dump-autoload` after adding new namespaces.

## Return Types

Always declare return types:

```php
public function getUser(int $id): User {}
public function findAll(): Collection {}
public function save(User $user): void {}
public function exists(string $email): bool {}
```

## Type Declarations

```php
// Property types (PHP 7.4+)
private string $name;
private ?int $age = null;
private readonly string $email;

// Constructor promotion (PHP 8.0+)
public function __construct(
    private string $name,
    private readonly int $id,
) {}
```

## Nullable vs Union Types

```php
// Nullable (can be null)
public function find(int $id): ?User { ... }

// Union (PHP 8.0+)
public function parse(string|int $input): string { ... }
```
