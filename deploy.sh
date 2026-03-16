#!/bin/bash
# Quick deploy script for gopalsankhala.in
# Run on your server: bash deploy.sh

set -e

APP_DIR="/var/www/penny-drop"
REPO="https://github.com/vikramsankhala/UPI-Penny-Drop-Verification.git"

echo "=== UPI Penny Drop Deployment ==="

if [ ! -d "$APP_DIR" ]; then
    echo "Cloning repo..."
    sudo mkdir -p /var/www
    sudo git clone "$REPO" "$APP_DIR"
    cd "$APP_DIR"
    echo "Create .env with Razorpay credentials before running:"
    echo "  RAZORPAY_KEY_ID=rzp_live_xxx"
    echo "  RAZORPAY_KEY_SECRET=xxx"
    echo "  RAZORPAY_SOURCE_ACCOUNT=xxx"
    echo ""
    echo "Then run: sudo bash deploy.sh"
    exit 0
fi

cd "$APP_DIR"
echo "Pulling latest..."
sudo git pull origin main

echo "Installing dependencies..."
sudo python3 -m venv venv 2>/dev/null || true
sudo ./venv/bin/pip install -r requirements.txt -q

echo "Restarting service..."
sudo systemctl restart penny-drop 2>/dev/null || echo "Run: sudo systemctl start penny-drop"

echo "Done. Check: curl https://gopalsankhala.in"
