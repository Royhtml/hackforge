#!/usr/bin/env python3
"""
Hackforge - Termux Web Server Suite
XAMPP-like solution for Termux dengan path yang benar
"""

import os
import sys
import time
import signal
import subprocess
import threading
import webbrowser
import urllib.request
import tarfile
import json
from pathlib import Path
import socket
import shutil
from datetime import datetime

# Konfigurasi Termux
HOME_DIR = str(Path.home())
USERNAME = os.path.basename(HOME_DIR)
HACKFORGE_DIR = os.path.join(HOME_DIR, "hackforge")
WEB_ROOT = os.path.join(HOME_DIR, "htdocs")
APACHE_CONF_DIR = "/data/data/com.termux/files/usr/etc/apache2"
PHP_CONFIG_DIR = "/data/data/com.termux/files/usr/etc/php"
MARIADB_DATA_DIR = os.path.join(HACKFORGE_DIR, "mysql_data")
BACKUP_DIR = os.path.join(HACKFORGE_DIR, "backups")
LOG_DIR = os.path.join(HACKFORGE_DIR, "logs")
PROJECTS_DIR = os.path.join(HACKFORGE_DIR, "projects")

# Warna untuk output
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    MAGENTA = '\033[0;35m'
    NC = '\033[0m'

class Hackforge:
    def __init__(self):
        self.setup_directories()
        self.services = {
            'apache': False,
            'mariadb': False
        }
        
    def print_banner(self):
        """Menampilkan banner Hackforge"""
        banner = f"""
{Colors.MAGENTA}
╔══════════════════════════════════════════════════╗
║                              ▒░░░                ║
║                             ░▒▒░░                ║
║                            ▒▒▒▒░░                ║
║              ▒▒░░▒   ▒░░░░▒▒▒▒▒░▒                ║
║            ░░░░░░▒▒░░░░░░░░░▒▒▒▒                 ║
║        ▒░░░░▒▒▒▒▒░░░░░░░░░░░░░▒▒▒                ║
║          ▒▒▓   ▒░▒░░▓▓▓▓▓▒░░░░░░▒▒               ║
║               ▓░░░▓▓▓▓▒▓▓▓▓▓░░░░░▒               ║
║               ▒░▒▓▓▒▓▓▓▓▓▒▓▓▓▒░░░░▒              ║
║               ░░▓▓▒░▒▓▒▒▒▒▒▒▓▓▒░░░▒              ║
║              ▒░▒▓▒▓░█░░░░▒█▓▓▓▓░░░▒▒             ║
║              ▒░▒▓▓▒░░░░░░░░▒▓▓▓▓░░▒▒             ║
║              ▒░▓▓▓▓░░░░░░░░▒▓▓▓░▒▒▒▓             ║
║               ▒▓▓▓▓▒▒▒▒░░▒▓▓▓▓▒▒░░░▒             ║         
║                                                  ║
║                                                  ║
║              █░░ █ █▀█ █▄░█ █▀▀ █ ▀▄▀            ║
║              █▄▄ █ █▄█ █░▀█ █▄▄ █ █░█            ║
║                                                  ║
║        █░█ ▄▀█ █▀▀ █▄▀ █▀▀ █▀█ █▀█ █▀▀ █▀▀       ║
║        █▀█ █▀█ █▄▄ █░█ █▀░ █▄█ █▀▄ █▄█ ██▄       ║
║                                                  ║
║            PROFESSIONAL Hacker V2.8.7            ║
║            Created by Dwi Bakti N Dev            ║
║                User: {USERNAME:<15}             ║
╚══════════════════════════════════════════════════╝
{Colors.NC}
"""
        print(banner)
    
    def print_status(self, message, status="info"):
        """Print status dengan warna"""
        colors = {
            "info": Colors.BLUE,
            "success": Colors.GREEN,
            "warning": Colors.YELLOW,
            "error": Colors.RED
        }
        prefix = {
            "info": "[INFO]",
            "success": "[SUCCESS]",
            "warning": "[WARNING]",
            "error": "[ERROR]"
        }
        color = colors.get(status, Colors.BLUE)
        print(f"{color}{prefix[status]} {message}{Colors.NC}")
    
    def run_command(self, command, shell=True):
        """Menjalankan command dan return output"""
        try:
            result = subprocess.run(command, shell=shell, capture_output=True, text=True)
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return -1, "", str(e)
    
    def check_internet(self):
        """Cek koneksi internet"""
        self.print_status("Mengecek koneksi internet...", "info")
        try:
            urllib.request.urlopen('http://google.com', timeout=5)
            self.print_status("Koneksi internet tersedia", "success")
            return True
        except:
            self.print_status("Tidak ada koneksi internet!", "warning")
            return False
    
    def setup_directories(self):
        """Setup direktori Hackforge"""
        self.print_status("Setup direktori Hackforge...", "info")
        
        directories = [
            HACKFORGE_DIR,
            BACKUP_DIR,
            LOG_DIR,
            MARIADB_DATA_DIR,
            WEB_ROOT,
            os.path.join(WEB_ROOT, "phpmyadmin"),
            PROJECTS_DIR
        ]
        
        for directory in directories:
            try:
                os.makedirs(directory, exist_ok=True)
                self.print_status(f"Direktori {directory} siap", "success")
            except Exception as e:
                self.print_status(f"Gagal buat {directory}: {e}", "error")
    
    def install_dependencies(self):
        """Install dependencies yang diperlukan"""
        self.print_status("Mengecek dan menginstall dependencies...", "info")
        
        packages = [
            "wget", "curl", "git", "python", "nodejs", 
            "apache2", "php", "php-apache", "php-mysqli",
            "mariadb"
        ]
        
        for pkg in packages:
            # Cek apakah package sudah terinstall
            code, stdout, stderr = self.run_command(f"pkg list-installed | grep {pkg}")
            if code != 0:
                self.print_status(f"Menginstall {pkg}...", "warning")
                code, stdout, stderr = self.run_command(f"pkg install -y {pkg}")
                if code == 0:
                    self.print_status(f"{pkg} berhasil diinstall", "success")
                else:
                    self.print_status(f"Gagal install {pkg}: {stderr}", "error")
            else:
                self.print_status(f"{pkg} sudah terinstall", "success")
    
    def configure_apache(self):
        """Konfigurasi Apache untuk Termux"""
        self.print_status("Mengkonfigurasi Apache...", "info")
        
        # Backup config asli
        httpd_conf = os.path.join(APACHE_CONF_DIR, "httpd.conf")
        if os.path.exists(httpd_conf):
            shutil.copy2(httpd_conf, httpd_conf + ".backup")
        
        # Buat konfigurasi custom
        config_content = f'''# Hackforge Apache Configuration
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

User {USERNAME}
Group {USERNAME}

ServerAdmin webmaster@localhost
ServerName localhost:8080

DocumentRoot "{WEB_ROOT}"

<Directory "{WEB_ROOT}">
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

<Files ".ht*">
    Require all denied
</Files>

ErrorLog "{LOG_DIR}/apache_error.log"
CustomLog "{LOG_DIR}/apache_access.log" common

<IfModule mime_module>
    TypesConfig /data/data/com.termux/files/usr/etc/apache2/mime.types
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz
    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps
</IfModule>

<FilesMatch \\.php$>
    SetHandler application/x-httpd-php
</FilesMatch>

DirectoryIndex index.html index.php
'''
        
        try:
            with open(httpd_conf, 'w') as f:
                f.write(config_content)
            self.print_status("Apache configured successfully", "success")
        except Exception as e:
            self.print_status(f"Gagal konfigurasi Apache: {e}", "error")
    
    def configure_php(self):
        """Konfigurasi PHP"""
        self.print_status("Mengkonfigurasi PHP...", "info")
        
        php_ini_path = os.path.join(PHP_CONFIG_DIR, "php.ini")
        
        if os.path.exists(php_ini_path):
            with open(php_ini_path, 'r') as f:
                content = f.read()
            
            # Enable extensions dan setting penting
            replacements = {
                ';extension=curl': 'extension=curl',
                ';extension=gd': 'extension=gd',
                ';extension=mysqli': 'extension=mysqli',
                ';extension=pdo_mysql': 'extension=pdo_mysql',
                'display_errors = Off': 'display_errors = On',
                'upload_max_filesize = 2M': 'upload_max_filesize = 64M',
                'post_max_size = 8M': 'post_max_size = 64M',
                'memory_limit = 128M': 'memory_limit = 256M'
            }
            
            for old, new in replacements.items():
                content = content.replace(old, new)
            
            with open(php_ini_path, 'w') as f:
                f.write(content)
            
            self.print_status("PHP configured successfully", "success")
    
    def setup_mariadb(self):
        """Setup MariaDB database"""
        self.print_status("Setup MariaDB...", "info")
        
        # Inisialisasi database jika belum ada
        if not os.path.exists(os.path.join(MARIADB_DATA_DIR, "mysql")):
            self.print_status("Inisialisasi database MariaDB...", "warning")
            code, stdout, stderr = self.run_command(
                f"mysql_install_db --datadir={MARIADB_DATA_DIR}"
            )
            if code == 0:
                self.print_status("Database initialized", "success")
            else:
                self.print_status(f"Gagal inisialisasi database: {stderr}", "error")
                return False
        
        # Buat konfigurasi custom
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        config_content = f'''
[mysqld]
datadir={MARIADB_DATA_DIR}
socket={HACKFORGE_DIR}/mysql.sock
user={USERNAME}
port=3306

[mysqld_safe]
log-error={LOG_DIR}/mysql.log
pid-file={HACKFORGE_DIR}/mysql.pid

[client]
socket={HACKFORGE_DIR}/mysql.sock
'''
        
        with open(my_cnf, 'w') as f:
            f.write(config_content)
        
        self.print_status("MariaDB configured", "success")
        return True
    
    def download_phpmyadmin(self):
        """Download dan install phpMyAdmin"""
        self.print_status("Downloading phpMyAdmin...", "info")
        
        pma_dir = os.path.join(WEB_ROOT, "phpmyadmin")
        
        # Hapus direktori lama jika ada
        if os.path.exists(pma_dir):
            shutil.rmtree(pma_dir)
        
        os.makedirs(pma_dir, exist_ok=True)
        
        try:
            # Download phpMyAdmin
            pma_version = "5.2.1"
            pma_url = f"https://files.phpmyadmin.net/phpMyAdmin/{pma_version}/phpMyAdmin-{pma_version}-all-languages.tar.gz"
            tar_path = os.path.join(HACKFORGE_DIR, "phpmyadmin.tar.gz")
            
            self.print_status(f"Download dari: {pma_url}", "info")
            urllib.request.urlretrieve(pma_url, tar_path)
            
            # Extract
            self.print_status("Extracting phpMyAdmin...", "info")
            with tarfile.open(tar_path, 'r:gz') as tar:
                tar.extractall("/tmp/")
            
            # Pindahkan ke web directory
            extracted_dir = f"/tmp/phpMyAdmin-{pma_version}-all-languages"
            if os.path.exists(extracted_dir):
                for item in os.listdir(extracted_dir):
                    src = os.path.join(extracted_dir, item)
                    dst = os.path.join(pma_dir, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)
                
                # Buat config
                config_content = '''<?php
$cfg['blowfish_secret'] = 'hackforge_termux_secret_2024';
$i = 0;
$i++;
$cfg['Servers'][$i]['auth_type'] = 'cookie';
$cfg['Servers'][$i]['host'] = '127.0.0.1';
$cfg['Servers'][$i]['connect_type'] = 'tcp';
$cfg['Servers'][$i]['compress'] = false;
$cfg['Servers'][$i]['AllowNoPassword'] = true;
?>
'''
                config_file = os.path.join(pma_dir, "config.inc.php")
                with open(config_file, 'w') as f:
                    f.write(config_content)
                
                # Cleanup
                shutil.rmtree(extracted_dir)
                os.remove(tar_path)
                
                self.print_status("phpMyAdmin installed successfully", "success")
                return True
                
        except Exception as e:
            self.print_status(f"Gagal install phpMyAdmin: {e}", "error")
            # Buat fallback simple phpmyadmin
            self.create_fallback_phpmyadmin(pma_dir)
            return False
    
    def create_fallback_phpmyadmin(self, pma_dir):
        """Buat fallback phpMyAdmin sederhana"""
        self.print_status("Membuat fallback phpMyAdmin...", "warning")
        
        simple_pma = '''<!DOCTYPE html>
<html>
<head>
    <title>phpMyAdmin - Hackforge</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f0f0f0; }
        .container { background: white; padding: 20px; border-radius: 10px; }
        .btn { background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>phpMyAdmin - Hackforge</h1>
        <p>phpMyAdmin is being installed. Please wait or refresh the page.</p>
        <p>You can also manage MySQL manually via command line:</p>
        <code>mysql -u root</code>
        <p><a href="/" class="btn">Back to Home</a></p>
    </div>
</body>
</html>'''
        
        index_file = os.path.join(pma_dir, "index.html")
        with open(index_file, 'w') as f:
            f.write(simple_pma)
    
    def create_sample_files(self):
        """Buat file sample untuk testing"""
        self.print_status("Membuat sample files...", "info")
        
        # File index.html utama
        index_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Hackforge - {USERNAME}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .container {{ max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }}
        .btn {{ background: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin: 5px; display: inline-block; }}
        .status {{ padding: 10px; margin: 10px 0; border-radius: 5px; }}
        .success {{ background: #4CAF50; }}
        .error {{ background: #f44336; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Hackforge Server - {USERNAME}</h1>
        <p>Your personal web development environment on Termux</p>
        
        <div class="status success">
            <h3>✅ Services Status</h3>
            <p>Apache: Running on port 8080</p>
            <p>PHP: Active</p>
            <p>MariaDB: Ready</p>
        </div>
        
        <h3>Quick Links:</h3>
        <a href="/phpmyadmin" class="btn">📊 phpMyAdmin</a>
        <a href="/info.php" class="btn">ℹ️ PHP Info</a>
        <a href="/test.php" class="btn">🧪 Test PHP</a>
        <a href="/demo.html" class="btn">🎯 Demo Page</a>
        
        <h3>Server Information:</h3>
        <ul>
            <li><strong>Web Root:</strong> {WEB_ROOT}</li>
            <li><strong>User:</strong> {USERNAME}</li>
            <li><strong>Hackforge Dir:</strong> {HACKFORGE_DIR}</li>
        </ul>
    </div>
</body>
</html>'''
        
        with open(os.path.join(WEB_ROOT, "index.html"), 'w') as f:
            f.write(index_content)
        
        # File info.php
        with open(os.path.join(WEB_ROOT, "info.php"), 'w') as f:
            f.write("<?php phpinfo(); ?>")
        
        # File test.php
        test_php = '''<?php
echo "<h1>PHP Test Page</h1>";
echo "<p>PHP Version: " . PHP_VERSION . "</p>";

// Test MySQL connection
$socket = '/data/data/com.termux/files/home/hackforge/mysql.sock';
try {
    $conn = new mysqli('localhost', 'root', '', '', 0, $socket);
    if ($conn->connect_error) {
        echo "<p style='color: red;'>MySQL Connection Failed: " . $conn->connect_error . "</p>";
    } else {
        echo "<p style='color: green;'>✅ MySQL Connection Successful!</p>";
        echo "<p>MySQL Version: " . $conn->server_version . "</p>";
        $conn->close();
    }
} catch (Exception $e) {
    echo "<p style='color: red;'>MySQL Error: " . $e->getMessage() . "</p>";
}

// Test PHP extensions
$extensions = ['mysqli', 'pdo_mysql', 'curl', 'gd', 'mbstring'];
echo "<h3>PHP Extensions:</h3>";
foreach ($extensions as $ext) {
    if (extension_loaded($ext)) {
        echo "<p>✅ $ext</p>";
    } else {
        echo "<p>❌ $ext</p>";
    }
}
?>'''
        
        with open(os.path.join(WEB_ROOT, "test.php"), 'w') as f:
            f.write(test_php)
        
        # Demo page
        demo_html = '''<!DOCTYPE html>
<html>
<head>
    <title>Demo - Hackforge</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .demo-box { border: 2px solid #4CAF50; padding: 20px; margin: 20px 0; border-radius: 10px; }
    </style>
</head>
<body>
    <h1>Hackforge Demo Page</h1>
    <div class="demo-box">
        <h2>🎯 Server Environment</h2>
        <p>This page demonstrates that your server is working correctly.</p>
        <p>All services are properly configured and running.</p>
    </div>
    <a href="/">Back to Home</a>
</body>
</html>'''
        
        with open(os.path.join(WEB_ROOT, "demo.html"), 'w') as f:
            f.write(demo_html)
        
        self.print_status("Sample files created", "success")
    
    def start_apache(self):
        """Start Apache server"""
        self.print_status("Starting Apache...", "info")
        
        # Stop Apache jika sedang running
        self.run_command("pkill -f apache")
        time.sleep(2)
        
        # Start Apache
        code, stdout, stderr = self.run_command("apachectl -k start")
        if code == 0:
            self.print_status("Apache started successfully", "success")
            self.services['apache'] = True
            return True
        else:
            self.print_status(f"Failed to start Apache: {stderr}", "error")
            return False
    
    def start_mariadb(self):
        """Start MariaDB server"""
        self.print_status("Starting MariaDB...", "info")
        
        # Stop MariaDB jika sedang running
        self.run_command("pkill -f mysql")
        time.sleep(2)
        
        # Start MariaDB dengan config custom
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        cmd = f"mysqld_safe --defaults-file={my_cnf} --datadir={MARIADB_DATA_DIR} &"
        code, stdout, stderr = self.run_command(cmd)
        time.sleep(5)  # Beri waktu untuk startup
        
        # Test connection
        for i in range(10):
            code, stdout, stderr = self.run_command(
                f"mysqladmin --defaults-file={my_cnf} ping"
            )
            if code == 0:
                self.print_status("MariaDB started successfully", "success")
                
                # First time setup
                mysql_configured = os.path.join(HACKFORGE_DIR, ".mysql_configured")
                if not os.path.exists(mysql_configured):
                    self.print_status("First-time MySQL setup...", "info")
                    self.run_command(
                        f"mysql --defaults-file={my_cnf} -e \"ALTER USER 'root'@'localhost' IDENTIFIED BY ''; FLUSH PRIVILEGES;\""
                    )
                    with open(mysql_configured, 'w') as f:
                        f.write("configured")
                
                self.services['mariadb'] = True
                return True
            time.sleep(2)
        
        self.print_status("Failed to start MariaDB - timeout", "error")
        return False
    
    def stop_apache(self):
        """Stop Apache server"""
        self.print_status("Stopping Apache...", "info")
        code, stdout, stderr = self.run_command("apachectl -k stop")
        if code == 0:
            self.print_status("Apache stopped", "success")
            self.services['apache'] = False
        else:
            self.run_command("pkill -f apache")
            self.print_status("Apache stopped (force)", "warning")
            self.services['apache'] = False
    
    def stop_mariadb(self):
        """Stop MariaDB server"""
        self.print_status("Stopping MariaDB...", "info")
        my_cnf = os.path.join(HACKFORGE_DIR, "my.cnf")
        code, stdout, stderr = self.run_command(f"mysqladmin --defaults-file={my_cnf} shutdown")
        if code == 0:
            self.print_status("MariaDB stopped", "success")
            self.services['mariadb'] = False
        else:
            self.run_command("pkill -f mysql")
            self.print_status("MariaDB stopped (force)", "warning")
            self.services['mariadb'] = False
    
    def check_services_status(self):
        """Cek status services"""
        # Cek Apache
        code, stdout, stderr = self.run_command("pgrep -f apache")
        apache_running = code == 0
        
        # Cek MariaDB
        code, stdout, stderr = self.run_command("pgrep -f mysqld")
        mariadb_running = code == 0
        
        return apache_running, mariadb_running
    
    def install_complete(self):
        """Installasi lengkap"""
        self.print_banner()
        
        if not self.check_internet():
            self.print_status("Installation requires internet", "error")
            return False
        
        try:
            self.print_status("Starting complete installation...", "info")
            
            # Step-by-step installation
            self.install_dependencies()
            self.configure_apache()
            self.configure_php()
            self.setup_mariadb()
            self.download_phpmyadmin()
            self.create_sample_files()
            
            # Mark as installed
            with open(os.path.join(HACKFORGE_DIR, ".installed"), 'w') as f:
                f.write(f"Installed: {datetime.now()}\nUser: {USERNAME}")
            
            self.print_status("Installation completed successfully!", "success")
            
            # Start services
            self.start_services()
            
            return True
            
        except Exception as e:
            self.print_status(f"Installation failed: {e}", "error")
            return False
    
    def start_services(self):
        """Start semua services"""
        self.print_status("Starting all services...", "info")
        self.start_apache()
        self.start_mariadb()
        
        # Tampilkan status akhir
        apache_status, mariadb_status = self.check_services_status()
        if apache_status and mariadb_status:
            self.print_status("All services running successfully!", "success")
        else:
            self.print_status("Some services may not be running properly", "warning")
    
    def stop_services(self):
        """Stop semua services"""
        self.print_status("Stopping all services...", "info")
        self.stop_apache()
        self.stop_mariadb()
        self.print_status("All services stopped", "success")
    
    def show_status(self):
        """Tampilkan status system"""
        apache_status, mariadb_status = self.check_services_status()
        
        print(f"\n{Colors.CYAN}=== HACKFORGE STATUS ==={Colors.NC}")
        print(f"User: {USERNAME}")
        print(f"Web Root: {WEB_ROOT}")
        print(f"Hackforge Dir: {HACKFORGE_DIR}")
        print("─" * 50)
        print(f"Apache:   {'🟢 RUNNING' if apache_status else '🔴 STOPPED'}")
        print(f"MariaDB:  {'🟢 RUNNING' if mariadb_status else '🔴 STOPPED'}")
        print("─" * 50)
        print(f"{Colors.GREEN}Web Interface: http://localhost:8080{Colors.NC}")
        print(f"{Colors.GREEN}phpMyAdmin:     http://localhost:8080/phpmyadmin{Colors.NC}")
        print(f"{Colors.GREEN}PHP Info:       http://localhost:8080/info.php{Colors.NC}")
        print(f"{Colors.GREEN}Test Page:      http://localhost:8080/test.php{Colors.NC}")
    
    def open_browser(self, path=""):
        """Buka browser dengan path tertentu"""
        url = f"http://localhost:8080{path}"
        self.print_status(f"Opening: {url}", "info")
        try:
            webbrowser.open(url)
        except:
            self.print_status(f"Buka manual: {Colors.GREEN}{url}{Colors.NC}", "warning")

def main():
    """Main function"""
    hackforge = Hackforge()
    
    while True:
        hackforge.print_banner()
        hackforge.show_status()
        
        print(f"\n{Colors.CYAN}=== MAIN MENU ==={Colors.NC}")
        print("1. 🚀 INSTALL Hackforge (Full Setup)")
        print("2. ⚡ START Services")
        print("3. 🛑 STOP Services")
        print("4. 🔄 RESTART Services")
        print("5. 🌐 Open Web Interface")
        print("6. 📊 Open phpMyAdmin")
        print("7. ℹ️  System Info")
        print("0. ❌ Exit")
        
        choice = input(f"\n{Colors.YELLOW}Pilih opsi [0-7]: {Colors.NC}").strip()
        
        if choice == "1":
            if hackforge.install_complete():
                input(f"\n{Colors.GREEN}Installasi selesai! Tekan Enter...{Colors.NC}")
            else:
                input(f"\n{Colors.RED}Installasi gagal! Tekan Enter...{Colors.NC}")
        
        elif choice == "2":
            hackforge.start_services()
            input(f"\n{Colors.YELLOW}Tekan Enter...{Colors.NC}")
        
        elif choice == "3":
            hackforge.stop_services()
            input(f"\n{Colors.YELLOW}Tekan Enter...{Colors.NC}")
        
        elif choice == "4":
            hackforge.stop_services()
            time.sleep(3)
            hackforge.start_services()
            input(f"\n{Colors.YELLOW}Tekan Enter...{Colors.NC}")
        
        elif choice == "5":
            hackforge.open_browser()
        
        elif choice == "6":
            hackforge.open_browser("/phpmyadmin")
        
        elif choice == "7":
            print(f"\n{Colors.CYAN}=== SYSTEM INFO ==={Colors.NC}")
            print(f"OS: {os.uname().sysname}")
            print(f"User: {USERNAME}")
            print(f"Home: {HOME_DIR}")
            print(f"Web Root: {WEB_ROOT}")
            input(f"\n{Colors.YELLOW}Tekan Enter...{Colors.NC}")
        
        elif choice == "0":
            hackforge.print_status("Menghentikan services...", "info")
            hackforge.stop_services()
            hackforge.print_status("Terima kasih menggunakan LionCix Hackforge! 👋", "success")
            break
        
        else:
            hackforge.print_status("Pilihan tidak valid!", "error")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Interrupted by user{Colors.NC}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.NC}")