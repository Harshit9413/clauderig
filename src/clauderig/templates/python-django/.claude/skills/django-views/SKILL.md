---
name: django-views
description: DRF ViewSet, APIView, and permission patterns.
---

# DRF View Patterns

## ModelViewSet (most common)

```python
from rest_framework import viewsets, permissions
from app.models import Product
from app.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)
```

Register in `urls.py`:
```python
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("products", ProductViewSet)
urlpatterns = [path("api/v1/", include(router.urls))]
```

## APIView (more control)

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data["new_password"])
        request.user.save()
        return Response({"detail": "Password updated"}, status=status.HTTP_200_OK)
```

## Custom Permissions

```python
from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

## Pagination

```python
# settings.py
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}
```
