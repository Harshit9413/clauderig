---
name: composer-deps
description: Managing Composer dependencies, semantic versioning, and package security.
---

# Composer Dependency Management

## Version Constraints

```json
{
    "require": {
        "php": "^8.1",
        "laravel/framework": "^10.0",
        "guzzlehttp/guzzle": "^7.5"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.0",
        "laravel/pint": "^1.0"
    }
}
```

- `^1.2.3` — compatible with 1.x, no breaking changes (recommended)
- `~1.2.3` — patch updates only (1.2.x)
- `1.2.3` — exact version (avoid unless necessary)

## Useful Commands

```bash
composer install              # install from lock file
composer require vendor/pkg   # add a package
composer require --dev vendor/pkg  # add dev package
composer update vendor/pkg    # update specific package
composer audit                # check for security advisories
composer install --optimize-autoloader --no-dev  # production
```

## Lock File

Always commit `composer.lock`. It guarantees reproducible installs.
Never edit it manually.

## Checking for Outdated Packages

```bash
composer outdated
composer outdated --direct    # only direct dependencies
```
