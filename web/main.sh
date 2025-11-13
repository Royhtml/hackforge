#!/bin/bash

# Hackforge - Termux Web Server Suite
# XAMPP-like solution for Termux with advanced features

# Warna untuk output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
ORANGE='\033[0;33m'
PURPLE='\033[0;95m'
NC='\033[0m' # No Color

# Konfigurasi
HACKFORGE_DIR="$HOME/hackforge"
WEB_ROOT="/data/data/com.termux/files/usr/share/apache2/htdocs"
APACHE_CONF_DIR="/data/data/com.termux/files/usr/etc/apache2"
MARIADB_DATA_DIR="$HACKFORGE_DIR/mysql_data"
BACKUP_DIR="$HACKFORGE_DIR/backups"
LOG_DIR="$HACKFORGE_DIR/logs"

# URL GitHub
GITHUB_REPO="https://github.com/yourusername/hackforge-termux"
GITHUB_RAW_URL="https://raw.githubusercontent.com/yourusername/hackforge-termux/main/hackforge.sh"

# Fungsi animasi loading
show_loading() {
    local pid=$1
    local text=$2
    local delay=0.1
    local spinstr='|/-\'
    
    echo -n -e "${YELLOW}[ ] ${text}... ${NC}"
    
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "\b\b\b\b\b\b"
    echo -e "${GREEN}[✓] ${text} selesai!${NC}"
}

# Fungsi progress bar
progress_bar() {
    local duration=$1
    local text=$2
    local blocks=20
    local progress=0
    
    echo -e "${YELLOW}[ ] ${text}${NC}"
    echo -n "["
    
    for ((i=0; i<=$blocks; i++)); do
        progress=$((i * 5))
        for ((j=0; j<$i; j++)); do
            echo -n "█"
        done
        for ((j=$i; j<$blocks; j++)); do
            echo -n " "
        done
        echo -n "] ${progress}%"
        sleep $(echo "scale=2; $duration/$blocks" | bc)
        echo -ne "\r"
    done
    echo -e "${GREEN}[████████████████████] 100% ${text} selesai!${NC}"
}

# Fungsi cek koneksi internet
check_internet() {
    echo -e "${YELLOW}[+] Mengecek koneksi internet...${NC}"
    if ping -c 1 -W 3 google.com >/dev/null 2>&1; then
        echo -e "${GREEN}[✓] Koneksi internet tersedia${NC}"
        return 0
    else
        echo -e "${RED}[✗] Tidak ada koneksi internet!${NC}"
        return 1
    fi
}

# Fungsi cek dan install dependencies
check_dependencies() {
    echo -e "${CYAN}[+] Mengecek dependencies...${NC}"
    
    local deps=("wget" "curl" "git" "python" "nodejs" "php" "apache2" "mariadb")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if ! command -v $dep &> /dev/null && ! pkg list-installed | grep -q $dep; then
            missing+=($dep)
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${YELLOW}[+] Menginstall dependencies yang diperlukan...${NC}"
        pkg update -y
        for dep in "${missing[@]}"; do
            echo -e "${BLUE}[+] Menginstall $dep...${NC}"
            (pkg install -y $dep 2>/dev/null) &
            show_loading $! "Install $dep"
        done
    else
        echo -e "${GREEN}[✓] Semua dependencies sudah terinstall${NC}"
    fi
}

# Fungsi setup direktori
setup_directories() {
    echo -e "${CYAN}[+] Setup direktori Hackforge...${NC}"
    
    local dirs=("$HACKFORGE_DIR" "$BACKUP_DIR" "$LOG_DIR" "$MARIADB_DATA_DIR" "$WEB_ROOT/projects")
    
    for dir in "${dirs[@]}"; do
        if [ ! -d "$dir" ]; then
            mkdir -p "$dir"
            echo -e "${GREEN}[✓] Direktori $dir dibuat${NC}"
        fi
    done
}

# Fungsi install Apache
install_apache() {
    echo -e "${CYAN}[+] Setup Apache Web Server...${NC}"
    
    if ! command -v apachectl &> /dev/null; then
        (pkg install -y apache2 2>/dev/null) &
        show_loading $! "Install Apache"
    fi
    
    # Backup config original
    if [ ! -f "$APACHE_CONF_DIR/httpd.conf.bak" ]; then
        cp "$APACHE_CONF_DIR/httpd.conf" "$APACHE_CONF_DIR/httpd.conf.bak"
    fi
    
    # Buat config custom untuk Hackforge
    cat > "$APACHE_CONF_DIR/httpd.conf" << 'EOF'
ServerRoot "/data/data/com.termux/files/usr"

LoadModule mpm_worker_module libexec/apache2/mod_mpm_worker.so
LoadModule authn_file_module libexec/apache2/mod_authn_file.so
LoadModule authn_core_module libexec/apache2/mod_authn_core.so
LoadModule authz_host_module libexec/apache2/mod_authz_host.so
LoadModule authz_groupfile_module libexec/apache2/mod_authz_groupfile.so
LoadModule authz_user_module libexec/apache2/mod_authz_user.so
LoadModule authz_core_module libexec/apache2/mod_authz_core.so
LoadModule access_compat_module libexec/apache2/mod_access_compat.so
LoadModule auth_basic_module libexec/apache2/mod_auth_basic.so
LoadModule reqtimeout_module libexec/apache2/mod_reqtimeout.so
LoadModule filter_module libexec/apache2/mod_filter.so
LoadModule mime_module libexec/apache2/mod_mime.so
LoadModule log_config_module libexec/apache2/mod_log_config.so
LoadModule env_module libexec/apache2/mod_env.so
LoadModule headers_module libexec/apache2/mod_headers.so
LoadModule setenvif_module libexec/apache2/mod_setenvif.so
LoadModule version_module libexec/apache2/mod_version.so
LoadModule unixd_module libexec/apache2/mod_unixd.so
LoadModule status_module libexec/apache2/mod_status.so
LoadModule autoindex_module libexec/apache2/mod_autoindex.so
LoadModule dir_module libexec/apache2/mod_dir.so
LoadModule alias_module libexec/apache2/mod_alias.so
LoadModule php_module libexec/apache2/libphp.so

Listen 8080

LoadModule mpm_worker_module libexec/apache2/mod_mpm_worker.so

User $(whoami)
Group $(whoami)

ServerAdmin admin@hackforge.local
ServerName localhost:8080

<Directory />
    AllowOverride none
    Require all denied
</Directory>

DocumentRoot "/data/data/com.termux/files/usr/share/apache2/htdocs"

<Directory "/data/data/com.termux/files/usr/share/apache2/htdocs">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

<IfModule dir_module>
    DirectoryIndex index.html index.php
</IfModule>

<Files ".ht*">
    Require all denied
</Files>

ErrorLog "/data/data/com.termux/files/usr/var/log/apache2/error.log"
LogLevel warn

<IfModule log_config_module>
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common

    <IfModule logio_module>
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>

    CustomLog "/data/data/com.termux/files/usr/var/log/apache2/access.log" common
</IfModule>

<IfModule mime_module>
    TypesConfig /data/data/com.termux/files/usr/etc/apache2/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps
</IfModule>

Include /data/data/com.termux/files/usr/etc/apache2/extra/httpd-vhosts.conf

# PHP configuration
<FilesMatch \.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

PHPIniDir "/data/data/com.termux/files/usr/etc/php"
EOF

    # Buat virtual hosts
    cat > "$APACHE_CONF_DIR/extra/httpd-vhosts.conf" << 'EOF'
# Virtual Hosts for Hackforge

<VirtualHost *:8080>
    DocumentRoot "/data/data/com.termux/files/usr/share/apache2/htdocs"
    ServerName localhost
    ErrorLog "/data/data/com.termux/files/usr/var/log/apache2/localhost-error_log"
    CustomLog "/data/data/com.termux/files/usr/var/log/apache2/localhost-access_log" common
</VirtualHost>

<VirtualHost *:8080>
    DocumentRoot "/data/data/com.termux/files/usr/share/apache2/htdocs/phpmyadmin"
    ServerName phpmyadmin.local
    ErrorLog "/data/data/com.termux/files/usr/var/log/apache2/phpmyadmin-error_log"
    CustomLog "/data/data/com.termux/files/usr/var/log/apache2/phpmyadmin-access_log" common
</VirtualHost>
EOF

    echo -e "${GREEN}[✓] Apache configured${NC}"
}

# Fungsi install PHP dengan extensions
install_php() {
    echo -e "${CYAN}[+] Setup PHP dengan extensions...${NC}"
    
    local php_extensions=("php-apache" "php-mysqli" "php-pdo_mysql" "php-curl" "php-gd" "php-mbstring" "php-xml" "php-zip" "php-json")
    
    for ext in "${php_extensions[@]}"; do
        if ! pkg list-installed | grep -q $ext; then
            (pkg install -y $ext 2>/dev/null) &
            show_loading $! "Install $ext"
        fi
    done
    
    # Configure PHP
    local php_ini="/data/data/com.termux/files/usr/etc/php.ini"
    if [ -f "$php_ini" ]; then
        sed -i 's/;extension=mysqli/extension=mysqli/g' "$php_ini"
        sed -i 's/;extension=pdo_mysql/extension=pdo_mysql/g' "$php_ini"
        sed -i 's/;extension=curl/extension=curl/g' "$php_ini"
        sed -i 's/;extension=gd/extension=gd/g' "$php_ini"
        sed -i 's/display_errors = Off/display_errors = On/g' "$php_ini"
        sed -i 's/upload_max_filesize = 2M/upload_max_filesize = 64M/g' "$php_ini"
        sed -i 's/post_max_size = 8M/post_max_size = 64M/g' "$php_ini"
    fi
    
    echo -e "${GREEN}[✓] PHP configured${NC}"
}

# Fungsi install dan setup MariaDB
install_mariadb() {
    echo -e "${CYAN}[+] Setup MariaDB Database...${NC}"
    
    if ! command -v mysql &> /dev/null; then
        (pkg install -y mariadb 2>/dev/null) &
        show_loading $! "Install MariaDB"
    fi
    
    # Setup data directory
    if [ ! -d "$MARIADB_DATA_DIR/mysql" ]; then
        echo -e "${YELLOW}[+] Initialize MariaDB data directory...${NC}"
        mysql_install_db --datadir="$MARIADB_DATA_DIR"
    fi
    
    # Buat config MariaDB untuk Termux
    cat > "$HACKFORGE_DIR/my.cnf" << EOF
[mysqld]
datadir=$MARIADB_DATA_DIR
socket=$HACKFORGE_DIR/mysql.sock
user=$(whoami)
port=3306

# Security
skip-networking
bind-address=127.0.0.1

# Performance
key_buffer_size=16M
max_allowed_packet=16M
thread_stack=192K
thread_cache_size=8

[mysqld_safe]
log-error=$LOG_DIR/mariadb.log
pid-file=$HACKFORGE_DIR/mysqld.pid

[mysql]
socket=$HACKFORGE_DIR/mysql.sock

[client]
socket=$HACKFORGE_DIR/mysql.sock
EOF

    echo -e "${GREEN}[✓] MariaDB configured${NC}"
}

# Fungsi install phpMyAdmin
install_phpmyadmin() {
    echo -e "${CYAN}[+] Setup phpMyAdmin...${NC}"
    
    local pma_dir="$WEB_ROOT/phpmyadmin"
    local pma_version="5.2.1"
    local pma_url="https://files.phpmyadmin.net/phpMyAdmin/$pma_version/phpMyAdmin-$pma_version-all-languages.tar.gz"
    
    if [ ! -d "$pma_dir" ]; then
        mkdir -p "$pma_dir"
        echo -e "${BLUE}[+] Downloading phpMyAdmin...${NC}"
        (wget -q -O "/tmp/phpmyadmin.tar.gz" "$pma_url" && \
         tar -xzf "/tmp/phpmyadmin.tar.gz" -C "$pma_dir" --strip-components=1 && \
         rm "/tmp/phpmyadmin.tar.gz") &
        show_loading $! "Install phpMyAdmin"
        
        # Buat config phpMyAdmin
        cat > "$pma_dir/config.inc.php" << 'EOF'
<?php
$cfg['blowfish_secret'] = 'hackforge_termux_secret_key_2024';
$i = 0;
$i++;
$cfg['Servers'][$i]['auth_type'] = 'cookie';
$cfg['Servers'][$i]['host'] = '127.0.0.1';
$cfg['Servers'][$i]['connect_type'] = 'tcp';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = true;
$cfg['UploadDir'] = '';
$cfg['SaveDir'] = '';
$cfg['TempDir'] = '/tmp';
?>
EOF
    fi
    
    echo -e "${GREEN}[✓] phpMyAdmin installed${NC}"
}

# Fungsi buat sample project
create_sample_project() {
    echo -e "${CYAN}[+] Membuat sample project...${NC}"
    
    local project_dir="$WEB_ROOT/projects/hackforge_demo"
    mkdir -p "$project_dir"
    
    # Buat index.php
    cat > "$project_dir/index.php" << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hackforge Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Courier New', monospace;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            background: rgba(0,0,0,0.7);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 0 30px rgba(255,255,255,0.3);
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .status-card {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .status-card.good { border-color: #00b894; }
        .status-card.warning { border-color: #fdcb6e; }
        .status-card.error { border-color: #e17055; }
        .tech-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            margin: 2px;
            border-radius: 20px;
            font-size: 0.8em;
        }
        .terminal {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
            font-family: 'Courier New', monospace;
            color: #00ff00;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Hackforge</h1>
            <p>Your XAMPP-like Solution for Termux</p>
        </div>

        <div class="status-grid">
            <div class="status-card good">
                <h3>PHP Version</h3>
                <p><?php echo phpversion(); ?></p>
            </div>
            <div class="status-card good">
                <h3>Server Software</h3>
                <p><?php echo $_SERVER['SERVER_SOFTWARE']; ?></p>
            </div>
            <div class="status-card good">
                <h3>Database</h3>
                <p>MariaDB Ready</p>
            </div>
            <div class="status-card good">
                <h3>phpMyAdmin</h3>
                <p>Available</p>
            </div>
        </div>

        <div class="terminal">
            <div>$ system status</div>
            <div>> Web Server: <span style="color:#00ff00">RUNNING</span></div>
            <div>> Database: <span style="color:#00ff00">ONLINE</span></div>
            <div>> phpMyAdmin: <span style="color:#00ff00">ACCESSIBLE</span></div>
            <div>> Security: <span style="color:#fdcb6e">DEVELOPMENT MODE</span></div>
        </div>

        <div style="text-align: center; margin-top: 20px;">
            <h3>Supported Technologies</h3>
            <div>
                <span class="tech-badge">PHP <?php echo phpversion(); ?></span>
                <span class="tech-badge">MariaDB</span>
                <span class="tech-badge">Apache</span>
                <span class="tech-badge">HTML5</span>
                <span class="tech-badge">CSS3</span>
                <span class="tech-badge">JavaScript</span>
                <span class="tech-badge">phpMyAdmin</span>
            </div>
        </div>

        <div style="margin-top: 30px; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 8px;">
            <h3>Quick Links</h3>
            <ul style="list-style: none; margin-top: 10px;">
                <li><a href="/" style="color: #48dbfb;">Home Directory</a></li>
                <li><a href="/phpmyadmin" style="color: #48dbfb;">phpMyAdmin</a></li>
                <li><a href="/projects" style="color: #48dbfb;">Projects Directory</a></li>
                <li><a href="/projects/hackforge_demo" style="color: #48dbfb;">This Demo</a></li>
            </ul>
        </div>

        <?php
        // Test database connection
        try {
            $conn = new mysqli('127.0.0.1', 'root', '', '', 3306);
            if ($conn->connect_error) {
                echo '<div style="margin-top: 20px; padding: 10px; background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; border-radius: 5px;">';
                echo '<strong>Database Status:</strong> <span style="color:#e74c3c">Disconnected</span>';
                echo '</div>';
            } else {
                echo '<div style="margin-top: 20px; padding: 10px; background: rgba(46, 204, 113, 0.2); border: 1px solid #2ecc71; border-radius: 5px;">';
                echo '<strong>Database Status:</strong> <span style="color:#2ecc71">Connected</span>';
                echo '</div>';
                $conn->close();
            }
        } catch (Exception $e) {
            echo '<div style="margin-top: 20px; padding: 10px; background: rgba(231, 76, 60, 0.2); border: 1px solid #e74c3c; border-radius: 5px;">';
            echo '<strong>Database Error:</strong> ' . $e->getMessage();
            echo '</div>';
        }
        ?>
    </div>
</body>
</html>
EOF

    # Buat info.php
    cat > "$WEB_ROOT/info.php" << 'EOF'
<?php
phpinfo();
?>
EOF

    echo -e "${GREEN}[✓] Sample project created${NC}"
}

# Fungsi start services
start_services() {
    echo -e "${CYAN}[+] Starting Hackforge Services...${NC}"
    
    # Start Apache
    if ! pgrep -x "httpd" > /dev/null; then
        apachectl -k start
        echo -e "${GREEN}[✓] Apache started${NC}"
    else
        echo -e "${YELLOW}[!] Apache already running${NC}"
    fi
    
    # Start MariaDB
    if ! pgrep -x "mysqld" > /dev/null; then
        mysqld_safe --defaults-file="$HACKFORGE_DIR/my.cnf" &
        sleep 5
        echo -e "${GREEN}[✓] MariaDB started${NC}"
        
        # Setup root password jika pertama kali
        if [ ! -f "$HACKFORGE_DIR/mysql_configured" ]; then
            echo -e "${YELLOW}[+] Configuring MariaDB...${NC}"
            mysqladmin -u root password "" 2>/dev/null || true
            touch "$HACKFORGE_DIR/mysql_configured"
        fi
    else
        echo -e "${YELLOW}[!] MariaDB already running${NC}"
    fi
}

# Fungsi stop services
stop_services() {
    echo -e "${CYAN}[+] Stopping Hackforge Services...${NC}"
    
    # Stop Apache
    if pgrep -x "httpd" > /dev/null; then
        apachectl -k stop
        echo -e "${GREEN}[✓] Apache stopped${NC}"
    fi
    
    # Stop MariaDB
    if pgrep -x "mysqld" > /dev/null; then
        killall mysqld 2>/dev/null
        echo -e "${GREEN}[✓] MariaDB stopped${NC}"
    fi
}

# Fungsi status services
status_services() {
    echo -e "${CYAN}[+] Hackforge Services Status${NC}"
    echo -e "─────────────────────────────"
    
    # Check Apache
    if pgrep -x "httpd" > /dev/null; then
        echo -e "Apache:    ${GREEN}● RUNNING${NC}"
    else
        echo -e "Apache:    ${RED}● STOPPED${NC}"
    fi
    
    # Check MariaDB
    if pgrep -x "mysqld" > /dev/null; then
        echo -e "MariaDB:   ${GREEN}● RUNNING${NC}"
    else
        echo -e "MariaDB:   ${RED}● STOPPED${NC}"
    fi
    
    # Check PHP
    if command -v php &> /dev/null; then
        echo -e "PHP:       ${GREEN}● INSTALLED${NC}"
    else
        echo -e "PHP:       ${RED}● NOT INSTALLED${NC}"
    fi
    
    echo -e "─────────────────────────────"
    echo -e "Web Server: ${BLUE}http://localhost:8080${NC}"
    echo -e "phpMyAdmin: ${BLUE}http://localhost:8080/phpmyadmin${NC}"
    echo -e "Demo Page:  ${BLUE}http://localhost:8080/projects/hackforge_demo${NC}"
}

# Fungsi backup database
backup_database() {
    local backup_file="$BACKUP_DIR/db_backup_$(date +%Y%m%d_%H%M%S).sql"
    
    echo -e "${CYAN}[+] Creating database backup...${NC}"
    
    if mysqldump -u root --all-databases > "$backup_file" 2>/dev/null; then
        echo -e "${GREEN}[✓] Backup created: $(basename $backup_file)${NC}"
    else
        echo -e "${RED}[✗] Backup failed${NC}"
    fi
}

# Fungsi restore database
restore_database() {
    local backup_files=($(ls -1t "$BACKUP_DIR"/*.sql 2>/dev/null))
    
    if [ ${#backup_files[@]} -eq 0 ]; then
        echo -e "${RED}[!] No backup files found${NC}"
        return
    fi
    
    echo -e "${CYAN}[+] Available backups:${NC}"
    for i in "${!backup_files[@]}"; do
        echo -e "  $((i+1)). $(basename ${backup_files[$i]})"
    done
    
    echo -e -n "${YELLOW}Select backup to restore [1-${#backup_files[@]}]: ${NC}"
    read choice
    
    if [[ $choice =~ ^[0-9]+$ ]] && [ $choice -ge 1 ] && [ $choice -le ${#backup_files[@]} ]; then
        local selected_file="${backup_files[$((choice-1))]}"
        echo -e "${YELLOW}[+] Restoring from $selected_file...${NC}"
        
        if mysql -u root < "$selected_file" 2>/dev/null; then
            echo -e "${GREEN}[✓] Database restored${NC}"
        else
            echo -e "${RED}[✗] Restore failed${NC}"
        fi
    else
        echo -e "${RED}[!] Invalid selection${NC}"
    fi
}

# Fungsi create new project
create_new_project() {
    echo -e -n "${YELLOW}Enter project name: ${NC}"
    read project_name
    
    if [ -z "$project_name" ]; then
        echo -e "${RED}[!] Project name cannot be empty${NC}"
        return
    fi
    
    local project_dir="$WEB_ROOT/projects/$project_name"
    
    if [ -d "$project_dir" ]; then
        echo -e "${RED}[!] Project already exists${NC}"
        return
    fi
    
    mkdir -p "$project_dir"
    
    # Buat file index.php sederhana
    cat > "$project_dir/index.php" << EOF
<!DOCTYPE html>
<html>
<head>
    <title>$project_name - Hackforge</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px;
            background: #f4f4f4;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Welcome to $project_name</h1>
        <p>This project is running on Hackforge</p>
        <p><strong>PHP Version:</strong> <?php echo phpversion(); ?></p>
        <p><strong>Server:</strong> <?php echo \$_SERVER['SERVER_SOFTWARE']; ?></p>
        
        <h3>Database Connection Test:</h3>
        <?php
        \$conn = new mysqli('127.0.0.1', 'root', '');
        if (\$conn->connect_error) {
            echo '<p style="color: red;">Database connection failed</p>';
        } else {
            echo '<p style="color: green;">Database connection successful!</p>';
            \$conn->close();
        }
        ?>
    </div>
</body>
</html>
EOF

    # Buat database dengan nama yang sama (opsional)
    echo -e -n "${YELLOW}Create database with same name? [y/N]: ${NC}"
    read create_db
    
    if [[ $create_db =~ ^[Yy]$ ]]; then
        mysql -u root -e "CREATE DATABASE IF NOT EXISTS \`$project_name\`;" 2>/dev/null
        echo -e "${GREEN}[✓] Database '$project_name' created${NC}"
    fi
    
    echo -e "${GREEN}[✓] Project '$project_name' created at: $project_dir${NC}"
    echo -e "${BLUE}[+] Access URL: http://localhost:8080/projects/$project_name${NC}"
}

# Fungsi install Hackforge
install_hackforge() {
    clear
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║             HACKFORGE INSTALLER              ║"
    echo "║            XAMPP for Termux - Pro            ║"
    echo "║                                              ║"
    echo "║            Installing Components...          ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    if ! check_internet; then
        echo -e "${RED}[!] Installation requires internet connection${NC}"
        return 1
    fi
    
    progress_bar 3 "Preparing installation"
    
    # Eksekusi installasi
    check_dependencies
    setup_directories
    install_apache
    install_php
    install_mariadb
    install_phpmyadmin
    create_sample_project
    
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║           INSTALLATION COMPLETE!             ║"
    echo "║                                              ║"
    echo "║        Hackforge is ready to use!            ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    start_services
    status_services
    
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Fungsi main menu
main_menu() {
    while true; do
        clear
        echo -e "${MAGENTA}"
        echo "╔══════════════════════════════════════════════╗"
        echo "║                   HACKFORGE                  ║"
        echo "║           XAMPP for Termux - Pro             ║"
        echo "║                                              ║"
        echo "║     Complete Web Development Environment     ║"
        echo "╚══════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        echo -e "${CYAN}MAIN MENU:${NC}"
        echo -e "1. 🚀 INSTALL Hackforge (Full Setup)"
        echo -e "2. ⚡ START All Services"
        echo -e "3. 🛑 STOP All Services"
        echo -e "4. 📊 STATUS Services"
        echo -e "5. 🗃️  DATABASE Backup"
        echo -e "6. 🔄 DATABASE Restore"
        echo -e "7. 📁 NEW Project"
        echo -e "8. 🛠️  MANAGE Services"
        echo -e "9. ℹ️  SYSTEM Info"
        echo -e "0. ❌ EXIT"
        echo -e ""
        echo -e "${YELLOW}Choose option [0-9]: ${NC}"
        read choice
        
        case $choice in
            1)
                install_hackforge
                ;;
            2)
                start_services
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            3)
                stop_services
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            4)
                status_services
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            5)
                backup_database
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            6)
                restore_database
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            7)
                create_new_project
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            8)
                manage_services_menu
                ;;
            9)
                show_system_info
                ;;
            0)
                echo -e "${GREEN}Thank you for using Hackforge! 👋${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                sleep 2
                ;;
        esac
    done
}

# Fungsi manage services menu
manage_services_menu() {
    while true; do
        clear
        echo -e "${CYAN}"
        echo "╔══════════════════════════════════════════════╗"
        echo "║              MANAGE SERVICES                 ║"
        echo "╚══════════════════════════════════════════════╝"
        echo -e "${NC}"
        
        status_services
        echo -e ""
        echo -e "${YELLOW}MANAGEMENT OPTIONS:${NC}"
        echo -e "1. 🔄 RESTART Apache"
        echo -e "2. 🔄 RESTART MariaDB"
        echo -e "3. 📝 VIEW Apache Logs"
        echo -e "4. 📝 VIEW MariaDB Logs"
        echo -e "5. 🧹 CLEAR Logs"
        echo -e "6. 🏠 BACK to Main Menu"
        echo -e ""
        echo -e "${YELLOW}Choose option [1-6]: ${NC}"
        read choice
        
        case $choice in
            1)
                echo -e "${YELLOW}[+] Restarting Apache...${NC}"
                apachectl -k restart
                echo -e "${GREEN}[✓] Apache restarted${NC}"
                sleep 2
                ;;
            2)
                echo -e "${YELLOW}[+] Restarting MariaDB...${NC}"
                stop_services
                sleep 2
                start_services
                echo -e "${GREEN}[✓] MariaDB restarted${NC}"
                sleep 2
                ;;
            3)
                echo -e "${CYAN}[+] Apache Error Log:${NC}"
                tail -20 "/data/data/com.termux/files/usr/var/log/apache2/error.log"
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            4)
                echo -e "${CYAN}[+] MariaDB Error Log:${NC}"
                tail -20 "$LOG_DIR/mariadb.log"
                echo -e "\n${YELLOW}Press Enter to continue...${NC}"
                read
                ;;
            5)
                echo -e "${YELLOW}[+] Clearing logs...${NC}"
                > "/data/data/com.termux/files/usr/var/log/apache2/error.log"
                > "/data/data/com.termux/files/usr/var/log/apache2/access.log"
                > "$LOG_DIR/mariadb.log"
                echo -e "${GREEN}[✓] Logs cleared${NC}"
                sleep 2
                ;;
            6)
                return
                ;;
            *)
                echo -e "${RED}Invalid choice!${NC}"
                sleep 2
                ;;
        esac
    done
}

# Fungsi show system info
show_system_info() {
    clear
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║               SYSTEM INFORMATION             ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    echo -e "${YELLOW}System Info:${NC}"
    echo -e "  OS: $(uname -o)"
    echo -e "  Kernel: $(uname -r)"
    echo -e "  Architecture: $(uname -m)"
    
    echo -e "\n${YELLOW}Hackforge Info:${NC}"
    echo -e "  Version: 2.0.0"
    echo -e "  Install Directory: $HACKFORGE_DIR"
    echo -e "  Web Root: $WEB_ROOT"
    echo -e "  Backups: $BACKUP_DIR"
    
    echo -e "\n${YELLOW}Installed Components:${NC}"
    echo -e "  Apache: $(apachectl -v 2>/dev/null | head -1 | cut -d' ' -f3) ✓"
    echo -e "  PHP: $(php -v 2>/dev/null | head -1 | cut -d' ' -f2) ✓"
    echo -e "  MariaDB: $(mysql --version 2>/dev/null | cut -d' ' -f5 | sed 's/,//') ✓"
    echo -e "  Node.js: $(node --version 2>/dev/null) ✓"
    echo -e "  Python: $(python --version 2>/dev/null) ✓"
    
    echo -e "\n${YELLOW}Disk Usage:${NC}"
    df -h $HOME | tail -1
    
    echo -e "\n${YELLOW}Access URLs:${NC}"
    echo -e "  Main Site: ${BLUE}http://localhost:8080${NC}"
    echo -e "  phpMyAdmin: ${BLUE}http://localhost:8080/phpmyadmin${NC}"
    echo -e "  PHP Info: ${BLUE}http://localhost:8080/info.php${NC}"
    echo -e "  Projects: ${BLUE}http://localhost:8080/projects${NC}"
    
    echo -e "\n${GREEN}Press Enter to continue...${NC}"
    read
}

# Initialize Hackforge
initialize_hackforge() {
    clear
    echo -e "${MAGENTA}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║                   HACKFORGE                  ║"
    echo "║           XAMPP for Termux - Pro             ║"
    echo "║                                              ║"
    echo "║                 Initializing...              ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
    
    # Buat direktori utama
    mkdir -p "$HACKFORGE_DIR" "$BACKUP_DIR" "$LOG_DIR"
    
    # Check jika sudah terinstall
    if [ -f "$HACKFORGE_DIR/installed" ]; then
        echo -e "${GREEN}[✓] Hackforge detected, starting services...${NC}"
        start_services
    fi
    
    progress_bar 2 "Loading Hackforge"
}

# Main execution
initialize_hackforge
main_menu