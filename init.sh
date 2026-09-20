#!/bin/bash

NETWORK_NAME="external-fcdk"

# 1. Create the Docker network if it doesn't already exist
if sudo docker network inspect "$NETWORK_NAME" >/dev/null 2>&1; then
    echo "Network '$NETWORK_NAME' already exists."
else
    echo "Creating Docker network '$NETWORK_NAME'..."
    sudo docker network create "$NETWORK_NAME"
fi

# 2. Navigate to the db directory and start Docker Compose
echo "Starting db services..."
cd db
sudo docker compose up -d

# 3. Navigate to the API directory and start Docker Compose
echo "Starting API services..."
cd ../API
sudo docker compose up -d

echo "All services started successfully!"