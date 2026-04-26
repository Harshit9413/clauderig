---
name: claude-fit
description: Scan this PHP project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — PHP Project Scanner

## Step 1: Inventory Dependencies

Read `composer.json` and `composer.lock`. Note:
- `laravel/sanctum` or `laravel/passport` → propose `api-auth` skill
- `predis/predis` → propose `redis-caching` skill + Redis MCP note
- `league/flysystem-aws-s3-v3` → propose `s3-storage` skill
- `spatie/laravel-permission` → propose `rbac-permissions` skill
- `stripe/stripe-php` → propose `stripe-integration` skill

## Step 2: Inventory Project Structure

List `app/Http/Controllers/`, `app/Models/`, `routes/`. Read `routes/api.php`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with test command, route structure, auth approach.
