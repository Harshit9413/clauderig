---
name: add-view
description: Add a new DRF API view with serializer, URL routing, and test.
---

# /add-view

Ask the user:
1. Resource name? (e.g., products)
2. View type? (APIView / ModelViewSet / GenericAPIView)
3. Which HTTP methods?
4. Auth required?

Create:
- View in `app/views.py` or `app/views/<resource>.py`
- Serializer in `app/serializers.py`
- URL pattern in `app/urls.py`
- Test in `tests/test_<resource>.py` using `APIClient`

Run `python manage.py test tests.test_<resource>` and show output.
