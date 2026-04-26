---
name: claude-fit
description: Scan this React Native project and enhance .claude/ with project-specific skills and context.
---

# /claude-fit — React Native Project Scanner

## Step 1: Inventory Dependencies

Read `package.json`. Note:
- `@react-native-async-storage/async-storage` → propose `storage-patterns` skill
- `react-native-reanimated` → propose `animation-patterns` skill
- `@tanstack/react-query` → propose `react-query-patterns` skill
- `zustand` → propose `state-management` skill
- `expo-notifications` → propose `push-notifications` skill
- `react-native-maps` → propose `maps-integration` skill

## Step 2: Inventory Project Structure

Read `app.json` or `app.config.js`. List `src/screens/`, `src/components/`, `src/navigation/`.

## Step 3: Check Existing .claude/ Contents

List `.claude/commands/` and `.claude/skills/`.

## Step 4: Present Checklist

Numbered proposals with reasons. Wait for user selection.

## Step 5: Create Approved Files

YAML frontmatter conventions from shipped templates.

## Step 6: Update CLAUDE.md

Append `## Project-Specific Context` with: Expo SDK version, navigation structure, state management, test command.
