---
name: django-orm
description: Django ORM patterns for queries, relationships, and avoiding N+1 problems.
---

# Django ORM Patterns

## Basic Queries

```python
from django.shortcuts import get_object_or_404

# Get or 404
user = get_object_or_404(User, pk=user_id)

# Filter
users = User.objects.filter(is_active=True).order_by("-created_at")

# Exists check (cheaper than count)
if User.objects.filter(email=email).exists():
    raise ValidationError("Email taken")
```

## Relationships

```python
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

## Avoid N+1

```python
# Bad — hits DB once per post
posts = Post.objects.all()
for post in posts:
    print(post.author.name)  # N queries

# Good — 2 queries total
posts = Post.objects.select_related("author").all()

# For M2M
posts = Post.objects.prefetch_related("tags").all()
```

## Custom Manager

```python
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class User(models.Model):
    objects = models.Manager()
    active = ActiveManager()
```

## Transactions

```python
from django.db import transaction

@transaction.atomic
def transfer(from_user, to_user, amount):
    from_user.balance -= amount
    to_user.balance += amount
    from_user.save()
    to_user.save()
```

## Bulk Operations

```python
# Bulk create (single query)
User.objects.bulk_create([User(email=e) for e in emails])

# Bulk update
User.objects.filter(is_trial=True).update(plan="free")
```
