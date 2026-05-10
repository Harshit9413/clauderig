---
name: django-celery
description: Django + Celery patterns for async tasks, periodic jobs, retries, and task chaining.
---

# Django Celery Patterns

## Setup

```python
# config/celery.py
import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("myproject")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
```

```python
# config/__init__.py
from .celery import app as celery_app
__all__ = ["celery_app"]
```

```python
# settings.py
CELERY_BROKER_URL  = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
```

## Define Tasks

```python
# orders/tasks.py
from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name="orders.send_confirmation",
)
def send_order_confirmation(self, order_id: int) -> str:
    from orders.models import Order
    try:
        order = Order.objects.select_related("user").get(pk=order_id)
        send_mail(
            subject=f"Order #{order.id} Confirmed",
            message=f"Hi {order.user.first_name}, your order is confirmed.",
            from_email="no-reply@shop.com",
            recipient_list=[order.user.email],
        )
        logger.info("Sent confirmation for order %s", order_id)
        return f"sent:{order_id}"
    except Order.DoesNotExist:
        logger.error("Order %s not found", order_id)
        return f"not_found:{order_id}"
    except Exception as exc:
        raise self.retry(exc=exc)
```

## Dispatch from Views / Services

```python
from orders.tasks import send_order_confirmation

# Fire-and-forget
send_order_confirmation.delay(order.id)

# With options
send_order_confirmation.apply_async(
    args=[order.id],
    countdown=10,          # delay 10s
    expires=3600,          # discard if not run within 1 hour
)
```

## Periodic Tasks (Celery Beat)

```python
# settings.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "cleanup-old-sessions": {
        "task": "users.tasks.cleanup_expired_sessions",
        "schedule": crontab(hour=2, minute=0),  # daily 2am
    },
    "send-weekly-digest": {
        "task": "emails.tasks.weekly_digest",
        "schedule": crontab(day_of_week="monday", hour=8),
    },
}
```

## Task Chaining & Groups

```python
from celery import chain, group

# Chain — sequential
pipeline = chain(
    validate_order.s(order_id),
    charge_payment.s(),
    send_order_confirmation.s(),
)
pipeline.delay()

# Group — parallel
report_tasks = group(
    generate_sales_report.s(month),
    generate_user_report.s(month),
    generate_inventory_report.s(month),
)
report_tasks.apply_async()
```

## Run Workers

```bash
# Worker
celery -A config worker --loglevel=info -Q default,priority

# Beat scheduler
celery -A config beat --loglevel=info

# Both together (dev only)
celery -A config worker --beat --loglevel=info
```
