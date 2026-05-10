---
name: django-caching
description: Django caching patterns using Redis, cache decorators, and low-level cache API.
---

# Django Caching Patterns

## Redis Setup (settings.py)

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 300,  # 5 minutes default
    }
}
```

## View Caching Decorator

```python
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View

# Function-based view
@cache_page(60 * 15)  # 15 minutes
def product_list(request):
    products = Product.objects.all()
    return JsonResponse({"products": list(products.values())})


# Class-based view
@method_decorator(cache_page(60 * 15), name="dispatch")
class ProductListView(View):
    def get(self, request):
        ...
```

## Low-Level Cache API

```python
from django.core.cache import cache


def get_user_profile(user_id: int) -> dict:
    cache_key = f"user_profile:{user_id}"
    data = cache.get(cache_key)
    if data is None:
        user = User.objects.select_related("profile").get(pk=user_id)
        data = {"id": user.id, "email": user.email, "bio": user.profile.bio}
        cache.set(cache_key, data, timeout=300)
    return data


def invalidate_user_profile(user_id: int) -> None:
    cache.delete(f"user_profile:{user_id}")
```

## Cache Invalidation via Signal

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from .models import User


@receiver(post_save, sender=User)
def clear_user_cache(sender, instance: User, **kwargs):
    cache.delete(f"user_profile:{instance.pk}")
```

## Per-User Cache Key

```python
from django.core.cache import cache
from functools import wraps


def user_cache(timeout=300):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return view_func(request, *args, **kwargs)
            key = f"view:{view_func.__name__}:user:{request.user.pk}"
            cached = cache.get(key)
            if cached:
                return cached
            response = view_func(request, *args, **kwargs)
            cache.set(key, response, timeout)
            return response
        return wrapper
    return decorator
```

## Cache Many Keys at Once

```python
keys = [f"user_profile:{uid}" for uid in user_ids]
results = cache.get_many(keys)           # dict of found keys
missing = [k for k in keys if k not in results]
# fetch missing from DB, then:
cache.set_many({k: data[k] for k in missing}, timeout=300)
```
