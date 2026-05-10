---
name: laravel-eloquent
description: Laravel Eloquent ORM patterns for relationships, scopes, and query optimization.
---

# Laravel Eloquent Patterns

## Model with Relationships

```php
<?php

declare(strict_types=1);

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use HasFactory, SoftDeletes;

    protected $fillable = ['title', 'body', 'user_id', 'published_at'];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

## Local Scopes

```php
public function scopePublished(Builder $query): Builder
{
    return $query->whereNotNull('published_at')->where('published_at', '<=', now());
}

public function scopeByUser(Builder $query, int $userId): Builder
{
    return $query->where('user_id', $userId);
}

// Usage:
Post::published()->byUser(1)->latest()->get();
```

## Eager Loading (avoid N+1)

```php
// Bad — N+1
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // query per post
}

// Good — eager load
$posts = Post::with(['user', 'comments.author'])->published()->paginate(20);
```

## Accessors & Mutators (PHP 8.x)

```php
use Illuminate\Database\Eloquent\Casts\Attribute;

protected function fullName(): Attribute
{
    return Attribute::make(
        get: fn () => "{$this->first_name} {$this->last_name}",
    );
}

protected function password(): Attribute
{
    return Attribute::make(
        set: fn (string $value) => bcrypt($value),
    );
}
```

## Repository Pattern

```php
// app/Repositories/PostRepository.php
class PostRepository
{
    public function findPublished(int $perPage = 15): LengthAwarePaginator
    {
        return Post::with('user')
            ->published()
            ->latest()
            ->paginate($perPage);
    }

    public function create(array $data): Post
    {
        return Post::create($data);
    }

    public function findOrFail(int $id): Post
    {
        return Post::findOrFail($id);
    }
}
```

## Factory

```php
// database/factories/PostFactory.php
class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title'        => $this->faker->sentence(),
            'body'         => $this->faker->paragraphs(3, true),
            'user_id'      => User::factory(),
            'published_at' => $this->faker->optional()->dateTime(),
        ];
    }

    public function published(): static
    {
        return $this->state(['published_at' => now()]);
    }
}
```
