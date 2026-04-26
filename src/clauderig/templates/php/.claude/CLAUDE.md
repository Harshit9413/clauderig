# Project Rules — PHP / Laravel

## Stack
PHP 8.1+, Laravel 10+, Eloquent ORM, PHPUnit.

## Code Style
- PSR-12 coding style. Run `php-cs-fixer fix` before commits.
- `declare(strict_types=1)` at top of every file.
- Use camelCase for methods/variables, PascalCase for classes.
- Return type declarations on all methods.

## File/Folder Conventions (Laravel)
- Controllers → `app/Http/Controllers/<Resource>Controller.php`
- Models → `app/Models/<Resource>.php`
- Migrations → `database/migrations/`
- Routes → `routes/api.php` for API, `routes/web.php` for web
- Services → `app/Services/<Resource>Service.php`
- Form Requests → `app/Http/Requests/<Resource>Request.php`

## Always Do
- Use Form Requests for validation (`php artisan make:request`)
- Use Eloquent models, never raw SQL
- Use Laravel CSRF protection in web routes
- Return JSON from API controllers: `response()->json($data, $status)`

## Never Do
- No logic in controllers — use service classes
- No `DB::statement()` unless absolutely necessary
- No user input directly in queries
- No secrets in code — use `.env` + `config/`

## Testing
- PHPUnit feature tests in `tests/Feature/`
- Unit tests in `tests/Unit/`
- Run: `php artisan test` or `./vendor/bin/phpunit`
- Use factories: `User::factory()->create()`

## Recommended MCP Servers
- **Postgres MCP** — query DB directly. Set `DATABASE_URL`.
- **GitHub MCP** — browse issues/PRs. Set `GITHUB_TOKEN`.
- **Filesystem MCP** — pre-configured.
