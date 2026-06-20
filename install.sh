#!/bin/bash
set -e

echo -e "\033[1;35m"
echo "               ▄▄               "
echo "              ████              "
echo "             ██████             "
echo "            ████████            "
echo "           ██████████           "
echo "▄▄▄▄▄▄▄▄▄▄████████████▄▄▄▄▄▄▄▄▄▄"
echo "████████████████████████████████"
echo "▀▀▀▀▀▀▀▀▀██████████████▀▀▀▀▀▀▀▀▀"
echo "              ████              "
echo "             ██████             "
echo "              ████              "
echo "               ▀▀               "
echo -e "\033[0m"
echo -e "\033[1;36mInstalling IRIS OSINT Platform...\033[0m"

INSTALL_DIR="$HOME/.local/share/iris"
BIN_DIR="$HOME/.local/bin"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Clone or pull the latest code
if [ -d "$INSTALL_DIR" ]; then
    echo -e "\n[*] Updating existing installation in $INSTALL_DIR..."
    cd "$INSTALL_DIR"
    git pull origin master --quiet
else
    echo -e "\n[*] Cloning repository..."
    git clone https://github.com/malrobust/iris.git "$INSTALL_DIR" --quiet
    cd "$INSTALL_DIR"
fi

# Setup Virtual Environment to avoid system package conflicts (PEP 668)
echo "[*] Setting up isolated Python environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo "[*] Installing dependencies (this may take a moment)..."
pip install --upgrade pip --quiet
pip install -e . --quiet

# Create a global symlink
echo "[*] Creating global executable..."
ln -sf "$INSTALL_DIR/.venv/bin/iris" "$BIN_DIR/iris"

echo -e "\n\033[1;32m✓ IRIS successfully installed!\033[0m"
echo -e "You can now run IRIS from anywhere simply by typing: \033[1;36miris\033[0m\n"

# Verify PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "\033[1;33m⚠️  Warning: $BIN_DIR is not in your PATH.\033[0m"
    echo "To fix this, add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo "Then run: source ~/.bashrc"
fi
