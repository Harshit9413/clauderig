---
name: run-migration
description: Create and apply a Django database migration.
---

# /run-migration

Ask: what schema change are you making?

Then:
1. Make the model change
2. `python manage.py makemigrations --name <description>`
3. Show generated migration — ask to confirm
4. `python manage.py migrate`
5. If data migration needed: warn and propose a `RunPython` step
