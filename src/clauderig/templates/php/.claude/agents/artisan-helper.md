---
name: artisan-helper
description: Use when generating Laravel boilerplate via artisan, running migrations, seeding the database, or managing queues and schedules via the CLI.
tools: Read, Bash(php artisan:*)
---

# Laravel Artisan Helper

You run Laravel artisan commands to generate code and manage the application.

## Code Generation

### Model + migration + factory + seeder in one command
```bash
php artisan make:model Post -mfs
# -m = migration, -f = factory, -s = seeder
```

### Controller (API resource)
```bash
php artisan make:controller PostController --api --model=Post
```

### Form Request
```bash
php artisan make:request StorePostRequest
php artisan make:request UpdatePostRequest
```

### API Resource
```bash
php artisan make:resource PostResource
php artisan make:resource PostCollection
```

### Service / Repository (no built-in artisan — create manually)
```bash
# Create manually at app/Services/PostService.php
```

## Database

```bash
php artisan migrate                  # run pending migrations
php artisan migrate:fresh --seed     # drop all, re-run, seed (dev only)
php artisan migrate:rollback         # roll back last batch
php artisan db:seed --class=UserSeeder
```

## Cache & Config

```bash
php artisan config:cache             # cache config for production
php artisan config:clear             # clear config cache
php artisan route:cache              # cache routes (production)
php artisan optimize:clear           # clear all caches
```

## Queues

```bash
php artisan make:job ProcessPayment
php artisan queue:work               # process jobs
php artisan queue:failed             # list failed jobs
php artisan queue:retry all
```

## Useful Debugging

```bash
php artisan tinker                   # REPL with full app context
php artisan route:list               # all registered routes
php artisan about                    # app environment summary
```
