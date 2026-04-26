#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for React (Web) projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @playwright/mcp
echo ""
echo "Set: GITHUB_TOKEN environment variable"
echo "Playwright MCP is ready — no extra config needed"
