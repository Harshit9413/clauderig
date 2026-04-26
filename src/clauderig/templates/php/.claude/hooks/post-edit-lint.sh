#!/usr/bin/env bash
php-cs-fixer fix "$CLAUDE_FILE_PATH" 2>/dev/null || true
