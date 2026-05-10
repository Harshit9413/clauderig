---
name: django-permissions
description: Django custom permissions, object-level permissions, and DRF permission classes.
---

# Django Permissions Patterns

## Model-Level Permissions

```python
# orders/models.py
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)

    class Meta:
        permissions = [
            ("can_cancel_order", "Can cancel any order"),
            ("can_refund_order", "Can issue refunds"),
            ("view_order_report", "Can view order analytics"),
        ]
```

```python
# Assign in code
from django.contrib.auth.models import Permission

perm = Permission.objects.get(codename="can_cancel_order")
user.user_permissions.add(perm)

# Check
user.has_perm("orders.can_cancel_order")   # → True/False
```

## DRF Custom Permission Class

```python
# orders/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrAdmin(BasePermission):
    """Object-level: owner can read/write, admin can do anything."""

    def has_permission(self, request, view) -> bool:
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj) -> bool:
        if request.user.is_staff:
            return True
        return obj.user_id == request.user.pk


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff
```

## Applying Permissions to Views

```python
# orders/views.py
from rest_framework.viewsets import ModelViewSet
from .permissions import IsOwnerOrAdmin

class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=self.request.user)
```

## Role-Based Access with Groups

```python
from django.contrib.auth.models import Group, Permission

# Create roles once (e.g., in a management command or migration)
def setup_roles():
    manager_group, _ = Group.objects.get_or_create(name="Manager")
    perms = Permission.objects.filter(codename__in=[
        "can_cancel_order", "view_order_report"
    ])
    manager_group.permissions.set(perms)

# Assign user to role
user.groups.add(Group.objects.get(name="Manager"))

# Check role
user.groups.filter(name="Manager").exists()
```

## DRF Permission Combining

```python
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsOwnerOrAdmin

# AND — both must pass
permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

# OR (DRF 3.9+)
from rest_framework.permissions import OR

permission_classes = [IsAdminUser | IsOwnerOrAdmin]
```

## Row-Level Permissions via django-guardian

```bash
pip install django-guardian
```

```python
# settings.py
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]
INSTALLED_APPS += ["guardian"]
```

```python
from guardian.shortcuts import assign_perm, get_objects_for_user

# Grant object-level perm
assign_perm("orders.can_cancel_order", user, order_instance)

# Revoke
from guardian.shortcuts import remove_perm
remove_perm("orders.can_cancel_order", user, order_instance)

# Query objects user has perm on
my_cancellable_orders = get_objects_for_user(user, "orders.can_cancel_order", Order)
```
