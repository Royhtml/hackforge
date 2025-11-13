#!/bin/bash

# Hackforge Installer
# Professional gaming platform for Termux

echo -e "\033[1;35m"
cat << "EOF"
 _   _            __ _                  
| | | | __ _  ___/ _| |_ ___  _ __ ___  
| |_| |/ _` |/ __| |_| __/ _ \| '_ ` _ \ 
|  _  | (_| | (__|  _| || (_) | | | | | |
|_| |_|\__,_|\___|_|  \__\___/|_| |_| |_|
                                         
EOF
echo -e "\033[0m"

echo -e "\033[1;36mInstalling Hackforge...\033[0m"

# Update packages
pkg update -y && pkg upgrade -y

# Install dependencies
pkg install -y git wget python nodejs clang make \
    python-numpy python-pip nodejs-lts ruby \
    libxml2 libxslt ncurses-utils

# Install Python packages
pip install requests beautifulsoup4 colorama

# Create Hackforge directory
mkdir -p ~/hackforge
cd ~/hackforge

# Download main script
wget -q https://github.com/Royhtml/main/bash/hackforge.sh -O hackforge.sh
chmod +x hackforge.sh

# Create games directory
mkdir -p ~/hackforge_games

# Create desktop entry
cat > ~/.shortcuts/Hackforge << EOF
#!/bin/bash
cd ~/hackforge
./hackforge.sh
EOF

chmod +x ~/.shortcuts/Hackforge

echo -e "\033[1;32mInstallation complete!\033[0m"
echo -e "\033[1;33mRun Hackforge with: ./hackforge.sh\033[0m"
echo -e "\033[1;36mOr use the shortcut in Termux widget!\033[0m"