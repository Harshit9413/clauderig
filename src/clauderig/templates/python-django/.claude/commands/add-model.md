---
name: add-model
description: Add a new Django model with migration.
---

# /add-model

Ask:
1. Model name?
2. Fields? (name, type, constraints for each)
3. Relationships? (ForeignKey, M2M?)

Then:
1. Add model to `app/models.py`
2. Add `__str__` method
3. `python manage.py makemigrations`
4. Show migration file — ask to confirm
5. `python manage.py migrate`
6. Register in `app/admin.py`
