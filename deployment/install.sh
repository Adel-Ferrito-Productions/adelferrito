#!/bin/bash

# Malta Lightning Monitor - Installation Script
# This script sets up the monitoring system as a systemd service

set -e

echo "=========================================="
echo "Malta Lightning Monitor - Installation"
echo "=========================================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Error: Please run as root (use sudo)"
    exit 1
fi

# Installation directory
INSTALL_DIR="/opt/malta-lightning-monitor"

# Create lightning user if it doesn't exist
if ! id -u lightning > /dev/null 2>&1; then
    echo "Creating lightning user..."
    useradd -r -s /bin/false -d $INSTALL_DIR lightning
fi

# Create installation directory
echo "Creating installation directory: $INSTALL_DIR"
mkdir -p $INSTALL_DIR
cd $INSTALL_DIR

# Copy files
echo "Copying application files..."
cp -r /path/to/source/* $INSTALL_DIR/

# Create Python virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create data directories
echo "Creating data directories..."
mkdir -p lightning_monitor/data/cache
mkdir -p lightning_monitor/data/logs

# Set permissions
echo "Setting permissions..."
chown -R lightning:lightning $INSTALL_DIR
chmod -R 755 $INSTALL_DIR
chmod 600 $INSTALL_DIR/.env

# Copy environment file if it doesn't exist
if [ ! -f "$INSTALL_DIR/.env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo
    echo "⚠️  IMPORTANT: Edit $INSTALL_DIR/.env with your API keys"
    echo
fi

# Install systemd service
echo "Installing systemd service..."
cp deployment/malta-lightning-monitor.service /etc/systemd/system/
systemctl daemon-reload

# Enable but don't start yet
systemctl enable malta-lightning-monitor

echo
echo "=========================================="
echo "Installation complete!"
echo "=========================================="
echo
echo "Next steps:"
echo "1. Edit configuration: $INSTALL_DIR/.env"
echo "2. Edit config file: $INSTALL_DIR/config/config.yaml"
echo "3. Test the system: sudo -u lightning $INSTALL_DIR/venv/bin/python $INSTALL_DIR/main.py --test"
echo "4. Start the service: sudo systemctl start malta-lightning-monitor"
echo "5. Check status: sudo systemctl status malta-lightning-monitor"
echo "6. View logs: sudo journalctl -u malta-lightning-monitor -f"
echo
echo "For documentation, see: $INSTALL_DIR/README.md"
echo
