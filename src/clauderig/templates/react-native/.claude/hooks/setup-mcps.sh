#!/usr/bin/env bash
set -euo pipefail
echo "Installing MCP prerequisites for React Native projects..."
npm install -g @modelcontextprotocol/server-github
npm install -g @modelcontextprotocol/server-filesystem
echo ""
echo "Set: GITHUB_TOKEN environment variable"
