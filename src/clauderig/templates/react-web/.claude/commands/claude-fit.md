---
name: claude-fit
description: Scan this React project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — React Project Scanner

## Step 1: Inventory Dependencies

Read `package.json`. Note:
- `zustand` or `@reduxjs/toolkit` → propose matching state-management skill update
- `react-query` or `@tanstack/react-query` → propose `react-query-patterns` skill
- `react-router-dom` → propose `routing-patterns` skill
- `axios` → propose `api-client` skill
- `@playwright/test` → propose E2E test command
- `framer-motion` → propose `animation-patterns` skill
- `next` → propose Next.js-specific skills

## Step 2: Inventory Project Structure

List `src/`. Check: components, hooks, pages, api, types folders. Read `src/App.tsx` or `src/main.tsx`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with: test command, folder structure, state management in use, API base URL pattern.
