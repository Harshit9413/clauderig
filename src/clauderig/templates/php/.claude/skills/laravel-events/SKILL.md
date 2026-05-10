---
name: laravel-events
description: Laravel Events and Listeners — sync/async listeners, broadcasting, and Laravel Echo.
---

# Laravel Events & Broadcasting

## Define an Event

```php
<?php

declare(strict_types=1);

namespace App\Events;

use App\Models\Order;
use Illuminate\Foundation\Events\Dispatchable;
use Illuminate\Queue\SerializesModels;
use Illuminate\Broadcasting\InteractsWithSockets;
use Illuminate\Contracts\Broadcasting\ShouldBroadcast;
use Illuminate\Broadcasting\PrivateChannel;

class OrderPlaced implements ShouldBroadcast
{
    use Dispatchable, InteractsWithSockets, SerializesModels;

    public function __construct(public readonly Order $order) {}

    public function broadcastOn(): array
    {
        return [new PrivateChannel("orders.{$this->order->user_id}")];
    }

    public function broadcastAs(): string
    {
        return 'order.placed';
    }

    public function broadcastWith(): array
    {
        return [
            'order_id' => $this->order->id,
            'total'    => $this->order->total,
            'status'   => $this->order->status,
        ];
    }
}
```

## Define a Listener

```php
<?php

declare(strict_types=1);

namespace App\Listeners;

use App\Events\OrderPlaced;
use App\Services\EmailService;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Queue\InteractsWithQueue;

class SendOrderNotification implements ShouldQueue
{
    use InteractsWithQueue;

    public int $tries = 3;
    public string $queue = 'emails';

    public function __construct(private readonly EmailService $email) {}

    public function handle(OrderPlaced $event): void
    {
        $this->email->sendOrderConfirmation($event->order);
    }

    public function failed(OrderPlaced $event, \Throwable $exception): void
    {
        \Log::error("Notification failed for order #{$event->order->id}");
    }
}
```

## Register Events (EventServiceProvider)

```php
protected $listen = [
    OrderPlaced::class => [
        SendOrderNotification::class,
        UpdateInventory::class,
        TrackAnalytics::class,
    ],
];
```

## Dispatch Events

```php
use App\Events\OrderPlaced;

// In a service / controller
OrderPlaced::dispatch($order);

// Or via event() helper
event(new OrderPlaced($order));

// After DB transaction (prevents duplicate events on rollback)
\DB::transaction(function () use ($order) {
    $order->save();
    OrderPlaced::dispatch($order);
});
```

## Broadcasting Setup (Pusher / Soketi)

```php
// .env
BROADCAST_DRIVER=pusher
PUSHER_APP_ID=your_app_id
PUSHER_APP_KEY=your_app_key
PUSHER_APP_SECRET=your_app_secret
PUSHER_HOST=localhost   # soketi self-hosted
PUSHER_PORT=6001
PUSHER_SCHEME=http
```

## Channel Authorization

```php
// routes/channels.php
Broadcast::channel('orders.{userId}', function ($user, int $userId): bool {
    return $user->id === $userId;
});

// Admin can listen to all
Broadcast::channel('orders.{userId}', function ($user, int $userId): bool {
    return $user->id === $userId || $user->is_admin;
});
```

## Laravel Echo (Frontend)

```typescript
import Echo from "laravel-echo";
import Pusher from "pusher-js";

window.Pusher = Pusher;

const echo = new Echo({
  broadcaster: "pusher",
  key: import.meta.env.VITE_PUSHER_APP_KEY,
  cluster: "mt1",
  forceTLS: false,
});

// Listen on private channel
echo.private(`orders.${userId}`)
  .listen(".order.placed", (data: { order_id: number; total: number }) => {
    console.log("New order:", data);
  });
```
