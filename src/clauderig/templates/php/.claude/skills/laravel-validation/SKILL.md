---
name: laravel-validation
description: Laravel Form Request validation patterns, custom rules, and error responses.
---

# Laravel Validation Patterns

## Form Request

```php
<?php

declare(strict_types=1);

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return $this->user()->can('create', Post::class);
    }

    public function rules(): array
    {
        return [
            'title'        => ['required', 'string', 'min:5', 'max:255'],
            'body'         => ['required', 'string', 'min:10'],
            'category_id'  => ['required', 'integer', Rule::exists('categories', 'id')],
            'tags'         => ['nullable', 'array', 'max:5'],
            'tags.*'       => ['string', 'max:50'],
            'published_at' => ['nullable', 'date', 'after_or_equal:today'],
        ];
    }

    public function messages(): array
    {
        return [
            'title.min'   => 'Title must be at least 5 characters.',
            'body.min'    => 'Body must be at least 10 characters.',
            'tags.max'    => 'Maximum 5 tags allowed.',
        ];
    }
}
```

## Controller Usage

```php
public function store(StorePostRequest $request): JsonResponse
{
    // $request->validated() contains only validated data
    $post = $this->postService->create($request->validated());
    return response()->json($post, 201);
}
```

## Custom Validation Rule

```php
<?php

declare(strict_types=1);

namespace App\Rules;

use Closure;
use Illuminate\Contracts\Validation\ValidationRule;

class UniqueSlug implements ValidationRule
{
    public function validate(string $attribute, mixed $value, Closure $fail): void
    {
        $exists = Post::where('slug', $value)->exists();
        if ($exists) {
            $fail("The :attribute has already been taken.");
        }
    }
}
```

Usage in rules:
```php
'slug' => ['required', 'string', new UniqueSlug()],
```

## Conditional Validation

```php
public function rules(): array
{
    return [
        'type'   => ['required', Rule::in(['free', 'paid'])],
        'price'  => [
            Rule::when($this->input('type') === 'paid', ['required', 'numeric', 'min:0.01']),
        ],
        'coupon' => [
            Rule::unless($this->user()->isAdmin(), ['prohibited']),
        ],
    ];
}
```

## API Error Response (422)

```php
// Automatic for Form Requests — Laravel returns:
{
    "message": "The given data was invalid.",
    "errors": {
        "title": ["The title field is required."],
        "category_id": ["The selected category id is invalid."]
    }
}
```

## Manual Validation in Service

```php
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\ValidationException;

$validator = Validator::make($data, [
    'email' => ['required', 'email'],
]);

if ($validator->fails()) {
    throw new ValidationException($validator);
}
```
