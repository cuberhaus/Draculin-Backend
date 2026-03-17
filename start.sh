#!/usr/bin/env bash
# Run Draculin (backend + frontend) via Docker.
# Only prerequisite: Docker

set -e
cd "$(dirname "$0")"

echo "Starting Draculin (backend + frontend)..."
echo "  Backend API:        http://localhost:8889"
echo "  Flutter web app:    http://localhost:8890"
echo ""
docker compose up --build
