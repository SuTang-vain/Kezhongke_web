#!/bin/bash

# Configuration
REMOTE_HOST="ecs-server"
REMOTE_DIR="/var/www/kezhongke"
LOCAL_DIR="./"

echo "🚀 Starting deployment to $REMOTE_HOST..."

# Sync files (excluding git and OS junk)
rsync -avz --exclude '.git*' --exclude '.DS_Store' --exclude '.claude' \
    "$LOCAL_DIR" "$REMOTE_HOST:$REMOTE_DIR"

# Set permissions on remote
ssh "$REMOTE_HOST" "chown -R nginx:nginx $REMOTE_DIR && chmod -R 755 $REMOTE_DIR"

echo "✅ Deployment complete! Visit http://39.105.42.19"
