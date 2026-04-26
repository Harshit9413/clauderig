#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for Django projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
npm install -g @modelcontextprotocol/server-postgres
echo ""
echo "Set: GITHUB_TOKEN and DATABASE_URL environment variables"
