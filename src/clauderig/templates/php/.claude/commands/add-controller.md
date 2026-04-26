---
name: add-controller
description: Add a new Laravel API controller with routes, form request, and test.
---

# /add-controller

Ask:
1. Resource name? (e.g., Product)
2. Which methods? (index / show / store / update / destroy)
3. Auth required?

Then:
1. `php artisan make:controller <Resource>Controller --api`
2. `php artisan make:request Store<Resource>Request`
3. Add validation rules to the Form Request
4. Implement controller methods — each calls a service method
5. Register routes in `routes/api.php`
6. `php artisan make:test <Resource>ControllerTest`
7. Write feature tests using `$this->actingAs($user)->postJson(...)`

Run `php artisan test tests/Feature/<Resource>ControllerTest.php` and show output.
