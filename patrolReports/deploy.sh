#!/bin/bash
# Deploy USS Cod Patrol Reports to production
# Usage: ./deploy.sh [-f|--force]
#   -f, --force    Force copy all files regardless of modification time

set -e

PROD_DIR="/var/www/html/codpatrols"
DEV_DIR="/home/jmknapp/cod/patrolReports"

# Parse arguments
FORCE_FLAG=""
while [[ $# -gt 0 ]]; do
    case $1 in
        -f|--force)
            FORCE_FLAG="--ignore-times"
            echo "Force mode: copying all files regardless of modification time"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: ./deploy.sh [-f|--force]"
            exit 1
            ;;
    esac
done

echo "=== Deploying USS Cod Patrol Reports ==="

# Ensure log directory exists
sudo mkdir -p /var/log/codpatrols
sudo chown www-data:www-data /var/log/codpatrols

# Sync files (excluding dev-only files)
echo "Syncing files to $PROD_DIR..."
sudo rsync -av --delete $FORCE_FLAG \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.env' \
    --exclude='venv' \
    --exclude='temp_*' \
    --exclude='*.xlsx' \
    --exclude='corrections/' \
    "$DEV_DIR/" "$PROD_DIR/"

# Copy .env separately (contains secrets)
if [ -f "$DEV_DIR/.env" ]; then
    sudo cp "$DEV_DIR/.env" "$PROD_DIR/.env"
    sudo chmod 600 "$PROD_DIR/.env"
fi

# Set ownership
sudo chown -R www-data:www-data "$PROD_DIR"

# Restart the service
echo "Restarting codpatrols service..."
sudo systemctl restart codpatrols || echo "Note: codpatrols service not yet configured"

echo "=== Deployment complete ==="
