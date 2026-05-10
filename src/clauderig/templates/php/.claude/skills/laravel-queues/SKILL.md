---
name: laravel-queues
description: Laravel Queue jobs — dispatching, retries, failed jobs, batches, and Horizon.
---

# Laravel Queue Patterns

## Create a Job

```php
<?php

declare(strict_types=1);

namespace App\Jobs;

use App\Models\Order;
use App\Services\EmailService;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;

class SendOrderConfirmation implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public int $tries = 3;
    public int $backoff = 60;          // seconds between retries
    public int $timeout = 30;          // max execution time

    public function __construct(private readonly Order $order) {}

    public function handle(EmailService $email): void
    {
        $email->sendOrderConfirmation($this->order);
    }

    public function failed(\Throwable $exception): void
    {
        \Log::error("Order confirmation failed for #{$this->order->id}", [
            'error' => $exception->getMessage(),
        ]);
    }
}
```

## Dispatch Jobs

```php
use App\Jobs\SendOrderConfirmation;

// Immediately to queue
SendOrderConfirmation::dispatch($order);

// With delay
SendOrderConfirmation::dispatch($order)->delay(now()->addMinutes(5));

// On specific queue
SendOrderConfirmation::dispatch($order)->onQueue('emails');

// After DB transaction commits
SendOrderConfirmation::dispatchAfterResponse($order);
```

## Job Batching

```php
use Illuminate\Bus\Batch;
use Illuminate\Support\Facades\Bus;

$batch = Bus::batch([
    new GenerateSalesReport($month),
    new GenerateUserReport($month),
    new GenerateInventoryReport($month),
])->then(function (Batch $batch) {
    \Log::info('All reports generated for batch ' . $batch->id);
})->catch(function (Batch $batch, \Throwable $e) {
    \Log::error('Batch failed: ' . $e->getMessage());
})->onQueue('reports')->dispatch();

// Check status later
$batch = Bus::findBatch($batchId);
$batch->totalJobs;
$batch->failedJobs;
$batch->progress();   // 0–100
```

## Chaining Jobs

```php
use Illuminate\Support\Facades\Bus;

Bus::chain([
    new ValidateOrder($order),
    new ChargePayment($order),
    new SendOrderConfirmation($order),
])->dispatch();
```

## Failed Jobs

```php
# Retry all failed jobs
php artisan queue:retry all

# Retry specific job
php artisan queue:retry <uuid>

# Flush failed jobs
php artisan queue:flush
```

```php
// config/queue.php — store failed jobs in DB
'failed' => [
    'driver'   => env('QUEUE_FAILED_DRIVER', 'database-uuids'),
    'database' => env('DB_CONNECTION', 'mysql'),
    'table'    => 'failed_jobs',
],
```

## Laravel Horizon (Redis)

```bash
composer require laravel/horizon
php artisan horizon:install
php artisan horizon
```

```php
// config/horizon.php
'environments' => [
    'production' => [
        'supervisor-1' => [
            'maxProcesses' => 10,
            'balanceMaxShift' => 1,
            'balanceCooldown' => 3,
            'queue' => ['emails', 'default'],
        ],
    ],
],
```

## Run Worker

```bash
# Single worker
php artisan queue:work redis --queue=emails,default --tries=3 --timeout=60

# With Horizon (recommended for Redis)
php artisan horizon
```
