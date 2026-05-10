---
name: django-signals
description: Django signals patterns for decoupled event handling and post-save actions.
---

# Django Signals Patterns

## Basic Signal

```python
# app/signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Order, Notification


@receiver(post_save, sender=Order)
def notify_on_order_create(sender, instance: Order, created: bool, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Order #{instance.id} placed successfully.",
        )
```

## Connect in AppConfig

```python
# app/apps.py
from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        import orders.signals  # noqa: F401 — registers signal handlers
```

## Custom Signal

```python
# app/signals.py
from django.dispatch import Signal

payment_completed = Signal()  # provides: order, amount
```

```python
# Emit custom signal
payment_completed.send(sender=Payment, order=order, amount=payment.amount)
```

```python
# Listen to custom signal
from app.signals import payment_completed

@receiver(payment_completed)
def fulfill_order(sender, order, amount, **kwargs):
    order.mark_paid()
    order.save()
```

## Disconnect Signal in Tests

```python
# tests/test_orders.py
from django.test import TestCase
from django.db.models.signals import post_save
from orders.signals import notify_on_order_create
from orders.models import Order


class OrderTest(TestCase):
    def setUp(self):
        # Disconnect to avoid side effects in tests
        post_save.disconnect(notify_on_order_create, sender=Order)

    def tearDown(self):
        post_save.connect(notify_on_order_create, sender=Order)

    def test_create_order(self):
        order = Order.objects.create(user_id=1, total=100)
        self.assertEqual(order.total, 100)
```

## Signal for Audit Logging

```python
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    logger.info("User %s logged in from %s", user.email, request.META.get("REMOTE_ADDR"))


@receiver(user_login_failed)
def log_failed_login(sender, credentials, request, **kwargs):
    logger.warning("Failed login for %s from %s", credentials.get("username"), request.META.get("REMOTE_ADDR"))
```
