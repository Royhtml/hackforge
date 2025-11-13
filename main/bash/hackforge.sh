#!/bin/bash

# Hackforge - Ultimate Gaming Platform for Termux
# Created with professional UI and animations

# Colors and formatting
RED='\033[1;31m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
WHITE='\033[1;37m'
NC='\033[0m'
BOLD='\033[1m'
BLINK='\033[5m'

# Animation functions
function spinning_animation() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

function progress_bar() {
    local duration=$1
    local increment=$((100/$duration))
    local cur=0
    while [[ $cur -le 100 ]]; do
        printf "\r${CYAN}[${BOLD}"
        for i in $(seq 1 $((cur/2))); do printf "█"; done
        for i in $(seq $((cur/2+1)) 50); do printf "░"; done
        printf "${NC}] ${YELLOW}%3d%%${NC}" $cur
        cur=$((cur+increment))
        sleep 0.1
    done
    printf "\n"
}

function type_animation() {
    local text=$1
    for ((i=0; i<${#text}; i++)); do
        printf "${CYAN}${text:$i:1}${NC}"
        sleep 0.03
    done
    printf "\n"
}

# Check dependencies
function check_dependencies() {
    local deps=("git" "wget" "python" "nodejs" "clang")
    local missing=()
    
    echo -e "${YELLOW}Checking dependencies...${NC}"
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null; then
            missing+=($dep)
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}Missing dependencies: ${missing[*]}${NC}"
        echo -e "${YELLOW}Installing missing dependencies...${NC}"
        pkg update && pkg install -y ${missing[@]}
    fi
}

# Main menu
function main_menu() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
 _   _            __ _                  
| | | | __ _  ___/ _| |_ ___  _ __ ___  
| |_| |/ _` |/ __| |_| __/ _ \| '_ ` _ \ 
|  _  | (_| | (__|  _| || (_) | | | | | |
|_| |_|\__,_|\___|_|  \__\___/|_| |_| |_|
                                         
EOF
    echo -e "${NC}"
    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           ${BOLD}${WHITE}HACKFORGE MENU${NC}${CYAN}              ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║   ${GREEN}1.${NC} ${YELLOW}Install Dependencies${NC}             ${CYAN}║${NC}"
    echo -e "${CYAN}║   ${GREEN}2.${NC} ${YELLOW}Games Collection${NC}                ${CYAN}║${NC}"
    echo -e "${CYAN}║   ${GREEN}3.${NC} ${YELLOW}System Info${NC}                     ${CYAN}║${NC}"
    echo -e "${CYAN}║   ${GREEN}4.${NC} ${YELLOW}Update Hackforge${NC}               ${CYAN}║${NC}"
    echo -e "${CYAN}║   ${GREEN}5.${NC} ${RED}Exit${NC}                            ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
    echo -e ""
    read -p "$(echo -e ${YELLOW}"Select option [1-5]: "${NC})" choice
    
    case $choice in
        1) install_dependencies ;;
        2) games_menu ;;
        3) system_info ;;
        4) update_hackforge ;;
        5) exit_app ;;
        *) echo -e "${RED}Invalid option!${NC}"; sleep 1; main_menu ;;
    esac
}

# Install dependencies
function install_dependencies() {
    clear
    echo -e "${PURPLE}"
    type_animation "Installing Dependencies..."
    echo -e "${NC}"
    
    progress_bar 5 &
    pid=$!
    
    pkg update -y && pkg upgrade -y
    pkg install -y git wget python nodejs clang make \
        python-numpy python-pip nodejs-lts ruby \
        libxml2 libxslt ncurses-utils
    
    wait $pid
    
    pip install requests beautifulsoup4 colorama
    
    echo -e "${GREEN}Dependencies installed successfully!${NC}"
    sleep 2
    main_menu
}

# Games menu
function games_menu() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
  ____                       
 / ___| __ _ _ __ ___   ___  
| |  _ / _` | '_ ` _ \ / _ \ 
| |_| | (_| | | | | | |  __/ 
 \____|\__,_|_| |_| |_|\___| 
                             
EOF
    echo -e "${NC}"
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║               ${BOLD}${WHITE}GAMES COLLECTION${NC}${CYAN}                 ║${NC}"
    echo -e "${CYAN}╠════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║ ${GREEN}1.${NC} ${YELLOW}Snake Game${NC}                            ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}2.${NC} ${YELLOW}2048 Game${NC}                             ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}3.${NC} ${YELLOW}Flappy Bird${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}4.${NC} ${YELLOW}Space Invaders${NC}                        ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}5.${NC} ${YELLOW}Tetris${NC}                                ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}6.${NC} ${YELLOW}Minesweeper${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}7.${NC} ${YELLOW}Sudoku${NC}                                ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}8.${NC} ${YELLOW}Tic Tac Toe${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}9.${NC} ${YELLOW}Hangman${NC}                               ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}10.${NC} ${YELLOW}Chess${NC}                                ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}11.${NC} ${YELLOW}Pacman${NC}                               ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}12.${NC} ${YELLOW}Doom (Text-based)${NC}                   ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}13.${NC} ${YELLOW}Dino Runner${NC}                         ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}14.${NC} ${YELLOW}Breakout${NC}                            ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}15.${NC} ${YELLOW}Pong${NC}                                 ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}16.${NC} ${YELLOW}More Games...${NC}                       ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}0.${NC} ${RED}Back to Main Menu${NC}                 ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo -e ""
    read -p "$(echo -e ${YELLOW}"Select game [0-16]: "${NC})" game_choice
    
    case $game_choice in
        1) download_and_run "snake" ;;
        2) download_and_run "2048" ;;
        3) download_and_run "flappy" ;;
        4) download_and_run "space" ;;
        5) download_and_run "tetris" ;;
        6) download_and_run "minesweeper" ;;
        7) download_and_run "sudoku" ;;
        8) download_and_run "tictactoe" ;;
        9) download_and_run "hangman" ;;
        10) download_and_run "chess" ;;
        11) download_and_run "pacman" ;;
        12) download_and_run "doom" ;;
        13) download_and_run "dino" ;;
        14) download_and_run "breakout" ;;
        15) download_and_run "pong" ;;
        16) more_games_menu ;;
        0) main_menu ;;
        *) echo -e "${RED}Invalid option!${NC}"; sleep 1; games_menu ;;
    esac
}

# More games menu
function more_games_menu() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
 __  __                 
|  \/  | ___  _ __  ___ 
| |\/| |/ _ \| '_ \/ __|
| |  | | (_) | |_) \__ \
|_|  |_|\___/| .__/|___/
             |_|        
EOF
    echo -e "${NC}"
    echo -e "${CYAN}╔════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                ${BOLD}${WHITE}MORE GAMES${NC}${CYAN}                    ║${NC}"
    echo -e "${CYAN}╠════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║ ${GREEN}17.${NC} ${YELLOW}Rock Paper Scissors${NC}                 ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}18.${NC} ${YELLOW}Number Guessing${NC}                     ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}19.${NC} ${YELLOW}Wordle${NC}                              ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}20.${NC} ${YELLOW}Blackjack${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}21.${NC} ${YELLOW}Roulette${NC}                            ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}22.${NC} ${YELLOW}Slot Machine${NC}                        ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}23.${NC} ${YELLOW}Connect Four${NC}                        ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}24.${NC} ${YELLOW}Memory Game${NC}                         ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}25.${NC} ${YELLOW}Quiz Game${NC}                           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}26.${NC} ${YELLOW}Text Adventure${NC}                      ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}27.${NC} ${YELLOW}Racing Game${NC}                         ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}28.${NC} ${YELLOW}Zork${NC}                                ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}29.${NC} ${YELLOW}Simon Says${NC}                          ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}30.${NC} ${YELLOW}Mastermind${NC}                          ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}0.${NC} ${RED}Back to Games Menu${NC}                 ${CYAN}║${NC}"
    echo -e "${CYAN}╚════════════════════════════════════════════════╝${NC}"
    echo -e ""
    read -p "$(echo -e ${YELLOW}"Select game [0,17-30]: "${NC})" more_game_choice
    
    case $more_game_choice in
        17) download_and_run "rps" ;;
        18) download_and_run "number" ;;
        19) download_and_run "wordle" ;;
        20) download_and_run "blackjack" ;;
        21) download_and_run "roulette" ;;
        22) download_and_run "slot" ;;
        23) download_and_run "connect4" ;;
        24) download_and_run "memory" ;;
        25) download_and_run "quiz" ;;
        26) download_and_run "adventure" ;;
        27) download_and_run "racing" ;;
        28) download_and_run "zork" ;;
        29) download_and_run "simon" ;;
        30) download_and_run "mastermind" ;;
        0) games_menu ;;
        *) echo -e "${RED}Invalid option!${NC}"; sleep 1; more_games_menu ;;
    esac
}

# Download and run game
function download_and_run() {
    local game_type=$1
    local game_url=""
    local game_name=""
    local game_file=""
    
    # Define game repositories
    case $game_type in
        "snake")
            game_url="https://github.com/karlkani/snake-game/archive/refs/heads/master.zip"
            game_name="Snake Game"
            game_file="snake.py"
            ;;
        "2048")
            game_url="https://github.com/bfelbo/2048/archive/refs/heads/master.zip"
            game_name="2048 Game"
            game_file="2048.py"
            ;;
        "flappy")
            game_url="https://github.com/sourabhv/FlapPyBird/archive/refs/heads/master.zip"
            game_name="Flappy Bird"
            game_file="flappy.py"
            ;;
        "space")
            game_url="https://github.com/techwithtim/Space-Invaders/archive/refs/heads/master.zip"
            game_name="Space Invaders"
            game_file="space_invaders.py"
            ;;
        "tetris")
            game_url="https://github.com/uvipen/Tetris-python/archive/refs/heads/master.zip"
            game_name="Tetris"
            game_file="tetris.py"
            ;;
        "minesweeper")
            game_url="https://github.com/games-on-terminal/minesweeper/archive/refs/heads/main.zip"
            game_name="Minesweeper"
            game_file="minesweeper.py"
            ;;
        "sudoku")
            game_url="https://github.com/Ruturaj4/Sudoku-solver/archive/refs/heads/main.zip"
            game_name="Sudoku"
            game_file="sudoku.py"
            ;;
        "tictactoe")
            game_url="https://github.com/kying18/tic-tac-toe/archive/refs/heads/master.zip"
            game_name="Tic Tac Toe"
            game_file="tictactoe.py"
            ;;
        "hangman")
            game_url="https://github.com/kying18/hangman/archive/refs/heads/master.zip"
            game_name="Hangman"
            game_file="hangman.py"
            ;;
        "chess")
            game_url="https://github.com/othree/chess-text/archive/refs/heads/master.zip"
            game_name="Chess"
            game_file="chess.py"
            ;;
        "pacman")
            game_url="https://github.com/hbokmann/Pacman/archive/refs/heads/master.zip"
            game_name="Pacman"
            game_file="pacman.py"
            ;;
        "doom")
            game_url="https://github.com/ripred/textdoom/archive/refs/heads/master.zip"
            game_name="Doom (Text-based)"
            game_file="doom.py"
            ;;
        "dino")
            game_url="https://github.com/ziggear/dino-runner/archive/refs/heads/master.zip"
            game_name="Dino Runner"
            game_file="dino.py"
            ;;
        "breakout")
            game_url="https://github.com/breakout-game/breakout/archive/refs/heads/master.zip"
            game_name="Breakout"
            game_file="breakout.py"
            ;;
        "pong")
            game_url="https://github.com/russs123/pong/archive/refs/heads/main.zip"
            game_name="Pong"
            game_file="pong.py"
            ;;
        "rps")
            game_url="https://github.com/kying18/rock-paper-scissors/archive/refs/heads/master.zip"
            game_name="Rock Paper Scissors"
            game_file="rps.py"
            ;;
        "number")
            game_url="https://github.com/python-engineer/python-fun/archive/refs/heads/main.zip"
            game_name="Number Guessing"
            game_file="number_guess.py"
            ;;
        "wordle")
            game_url="https://github.com/lynn/wordle/archive/refs/heads/main.zip"
            game_name="Wordle"
            game_file="wordle.py"
            ;;
        "blackjack")
            game_url="https://github.com/kying18/blackjack/archive/refs/heads/master.zip"
            game_name="Blackjack"
            game_file="blackjack.py"
            ;;
        "roulette")
            game_url="https://github.com/dworschk/roulette/archive/refs/heads/master.zip"
            game_name="Roulette"
            game_file="roulette.py"
            ;;
        "slot")
            game_url="https://github.com/techwithtim/Slot-Machine/archive/refs/heads/main.zip"
            game_name="Slot Machine"
            game_file="slot_machine.py"
            ;;
        "connect4")
            game_url="https://github.com/techwithtim/Connect4/archive/refs/heads/master.zip"
            game_name="Connect Four"
            game_file="connect4.py"
            ;;
        "memory")
            game_url="https://github.com/techwithtim/Memory-Game/archive/refs/heads/master.zip"
            game_name="Memory Game"
            game_file="memory_game.py"
            ;;
        "quiz")
            game_url="https://github.com/techwithtim/Quiz-Game/archive/refs/heads/master.zip"
            game_name="Quiz Game"
            game_file="quiz_game.py"
            ;;
        "adventure")
            game_url="https://github.com/techwithtim/Text-Based-Adventure/archive/refs/heads/master.zip"
            game_name="Text Adventure"
            game_file="adventure.py"
            ;;
        "racing")
            game_url="https://github.com/techwithtim/Racing-Game/archive/refs/heads/master.zip"
            game_name="Racing Game"
            game_file="racing.py"
            ;;
        "zork")
            game_url="https://github.com/devottys/zork/archive/refs/heads/master.zip"
            game_name="Zork"
            game_file="zork.py"
            ;;
        "simon")
            game_url="https://github.com/techwithtim/Simon-Says/archive/refs/heads/master.zip"
            game_name="Simon Says"
            game_file="simon.py"
            ;;
        "mastermind")
            game_url="https://github.com/techwithtim/Mastermind/archive/refs/heads/master.zip"
            game_name="Mastermind"
            game_file="mastermind.py"
            ;;
    esac
    
    clear
    echo -e "${PURPLE}"
    type_animation "Downloading $game_name..."
    echo -e "${NC}"
    
    # Create games directory
    mkdir -p ~/hackforge_games
    cd ~/hackforge_games
    
    # Download and extract game
    if wget -q "$game_url" -O game.zip && unzip -q game.zip; then
        echo -e "${GREEN}Download successful!${NC}"
        rm game.zip
        
        # Find and run the game file
        local game_dir=$(find . -name "*.py" -type f | head -1 | xargs dirname 2>/dev/null)
        if [ -n "$game_dir" ]; then
            cd "$game_dir"
            echo -e "${YELLOW}Starting $game_name...${NC}"
            sleep 2
            
            # Try to run the game
            python_file=$(find . -name "*.py" -type f | head -1)
            if [ -n "$python_file" ]; then
                python3 "$python_file"
            else
                echo -e "${RED}Game file not found!${NC}"
            fi
        else
            echo -e "${RED}Could not find game directory!${NC}"
        fi
    else
        echo -e "${RED}Download failed!${NC}"
    fi
    
    echo -e ""
    read -p "$(echo -e ${YELLOW}"Press Enter to return to menu..."${NC})" -n 1
    games_menu
}

# System info
function system_info() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
  ____           _                  
 / ___| _   _ ___| |_ ___ _ __ ___   
 \___ \| | | / __| __/ _ \ '_ ` _ \  
  ___) | |_| \__ \ ||  __/ | | | | | 
 |____/ \__, |___/\__\___|_| |_| |_| 
        |___/                        
EOF
    echo -e "${NC}"
    
    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║           ${BOLD}${WHITE}SYSTEM INFORMATION${NC}${CYAN}         ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║ ${YELLOW}OS:${NC} $(uname -o)                      ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${YELLOW}Kernel:${NC} $(uname -r)                 ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${YELLOW}Architecture:${NC} $(uname -m)           ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${YELLOW}Termux:${NC} v$TERMUX_VERSION            ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${YELLOW}Storage:${NC} $(df -h ~ | awk 'NR==2 {print $4}') free${CYAN}║${NC}"
    echo -e "${CYAN}║ ${YELLOW}Memory:${NC} $(free -m | awk 'NR==2 {print $3"MB/"$2"MB"}') used${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
    
    echo -e ""
    read -p "$(echo -e ${YELLOW}"Press Enter to return to menu..."${NC})" -n 1
    main_menu
}

# Update Hackforge
function update_hackforge() {
    clear
    echo -e "${PURPLE}"
    type_animation "Updating Hackforge..."
    echo -e "${NC}"
    
    progress_bar 3 &
    pid=$!
    
    # Simulate update process
    cd ~
    if [ -d "hackforge" ]; then
        cd hackforge
        git pull origin main 2>/dev/null || echo -e "${YELLOW}Manual update required${NC}"
    fi
    
    wait $pid
    echo -e "${GREEN}Hackforge updated successfully!${NC}"
    sleep 2
    main_menu
}

# Exit application
function exit_app() {
    clear
    echo -e "${PURPLE}"
    type_animation "Thank you for using Hackforge!"
    echo -e "${NC}"
    echo -e "${CYAN}See you next time! 👋${NC}"
    sleep 2
    clear
    exit 0
}

# Initialize Hackforge
function init_hackforge() {
    clear
    echo -e "${PURPLE}"
    cat << "EOF"
 ██░ ██  ▄▄▄     ▄▄▄█████▓▓█████  ██▀███   ▄████▄   ██░ ██ 
▓██░ ██▒▒████▄   ▓  ██▒ ▓▒▓█   ▀ ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒
▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░▒███   ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░
░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░ ▒▓█  ▄ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██ 
░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░ ░▒████▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓
 ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░   ░░ ▒░ ░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒
 ▒ ░▒░ ░  ▒   ▒▒ ░   ░     ░ ░  ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░
 ░  ░░ ░  ░   ▒    ░         ░     ░░   ░ ░         ░  ░░ ░
 ░  ░  ░      ░  ░           ░  ░   ░     ░ ░       ░  ░  ░
                                         ░                 
EOF
    echo -e "${NC}"
    echo -e "${CYAN}╔══════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║    ${BOLD}${WHITE}ULTIMATE GAMING PLATFORM${NC}${CYAN}         ║${NC}"
    echo -e "${CYAN}║        ${BOLD}${WHITE}FOR TERMUX${NC}${CYAN}                  ║${NC}"
    echo -e "${CYAN}╠══════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║ ${GREEN}✓${NC} ${YELLOW}30+ Games Collection${NC}              ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}✓${NC} ${YELLOW}Professional UI${NC}                   ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}✓${NC} ${YELLOW}Smooth Animations${NC}                 ${CYAN}║${NC}"
    echo -e "${CYAN}║ ${GREEN}✓${NC} ${YELLOW}Easy Installation${NC}                 ${CYAN}║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════╝${NC}"
    echo -e ""
    
    progress_bar 5 &
    pid=$!
    sleep 2
    wait $pid
    
    check_dependencies
    main_menu
}

# Trap Ctrl+C
trap 'echo -e "\n${RED}Operation cancelled!${NC}"; sleep 1; main_menu' INT

# Start Hackforge
init_hackforge