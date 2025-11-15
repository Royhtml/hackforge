#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import subprocess
import threading
import socket
import platform
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

class AnimasiLoading:
    def __init__(self):
        self.animasi = [
            "⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"
        ]
        self.running = False
        self.thread = None
    
    def _animate(self, pesan="Loading"):
        i = 0
        while self.running:
            print(f"\r{Colors.CYAN}{self.animasi[i % len(self.animasi)]} {pesan}...{Colors.END}", end="", flush=True)
            time.sleep(0.1)
            i += 1
    
    def start(self, pesan="Loading"):
        self.running = True
        self.thread = threading.Thread(target=self._animate, args=(pesan,))
        self.thread.daemon = True
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("\r" + " " * 50 + "\r", end="", flush=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Mendapatkan ukuran terminal"""
    try:
        if os.name == 'nt':  # Windows
            from ctypes import windll, create_string_buffer
            h = windll.kernel32.GetStdHandle(-12)
            csbi = create_string_buffer(22)
            windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
            cols = csbi.raw[10] - csbi.raw[8] + 1
            rows = csbi.raw[12] - csbi.raw[6] + 1
            return cols, rows
        else:  # Unix/Linux
            cols, rows = os.get_terminal_size()
            return cols, rows
    except:
        return 80, 24  # Default size

def tampilkan_ascii_art():
    """Menampilkan ASCII art yang menyesuaikan ukuran terminal"""
    cols, rows = get_terminal_size()
    
    # ASCII art yang responsif
    if cols >= 80:
        ascii_art = f"""
{Colors.CYAN}
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
╚══════════════════════════════════════════════════╝
{Colors.END}
"""
    elif cols >= 60:
        ascii_art = f"""
{Colors.CYAN}
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
╚══════════════════════════════════════════════════╝
{Colors.END}
"""
    else:
        ascii_art = f"""
{Colors.CYAN}
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
╚══════════════════════════════════════════════════╝
{Colors.END}
"""
    print(ascii_art)

def cek_koneksi_internet():
    """Cek koneksi internet"""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def install_packages():
    """Install package Python yang diperlukan"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                   INSTALL PACKAGES                           ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    packages = [
        "requests", "colorama", "flask", "django", "numpy", "pandas"
    ]
    
    print(f"{Colors.CYAN}Package yang akan diinstall:{Colors.END}")
    for i, package in enumerate(packages, 1):
        print(f"  {Colors.YELLOW}[{i}]{Colors.END} {package}")
    
    print(f"  {Colors.YELLOW}[A]{Colors.END} Install semua package")
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    pilihan = input(f"{Colors.GREEN}Pilih package (nomor/A/0): {Colors.END}").strip().upper()
    
    if pilihan == "0":
        return
    elif pilihan == "A":
        packages_to_install = packages
    else:
        try:
            index = int(pilihan) - 1
            if 0 <= index < len(packages):
                packages_to_install = [packages[index]]
            else:
                print(f"{Colors.RED}Pilihan tidak valid!{Colors.END}")
                time.sleep(1)
                return
        except ValueError:
            print(f"{Colors.RED}Input tidak valid!{Colors.END}")
            time.sleep(1)
            return
    
    loading = AnimasiLoading()
    
    for package in packages_to_install:
        loading.start(f"Installing {package}")
        try:
            # Gunakan pip yang sesuai
            pip_cmd = "pip" if os.name == 'nt' else "pip3"
            
            result = subprocess.run(
                [pip_cmd, "install", package], 
                capture_output=True, 
                text=True, 
                timeout=60
            )
            
            loading.stop()
            
            if result.returncode == 0:
                print(f"{Colors.GREEN}✓ {package} berhasil diinstall{Colors.END}")
            else:
                print(f"{Colors.RED}✗ Gagal install {package}: {result.stderr}{Colors.END}")
                
        except subprocess.TimeoutExpired:
            loading.stop()
            print(f"{Colors.RED}✗ Timeout saat install {package}{Colors.END}")
        except Exception as e:
            loading.stop()
            print(f"{Colors.RED}✗ Error install {package}: {str(e)}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def update_pip():
    """Update pip ke versi terbaru"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                     UPDATE PIP                               ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    print(f"{Colors.YELLOW}Memperbarui pip...{Colors.END}")
    
    loading = AnimasiLoading()
    loading.start("Updating pip")
    
    try:
        pip_cmd = "pip" if os.name == 'nt' else "pip3"
        python_cmd = "python" if os.name == 'nt' else "python3"
        
        # Update pip
        result = subprocess.run(
            [python_cmd, "-m", "pip", "install", "--upgrade", "pip"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        loading.stop()
        
        if result.returncode == 0:
            print(f"{Colors.GREEN}✓ Pip berhasil diupdate{Colors.END}")
        else:
            print(f"{Colors.RED}✗ Gagal update pip: {result.stderr}{Colors.END}")
            
    except subprocess.TimeoutExpired:
        loading.stop()
        print(f"{Colors.RED}✗ Timeout saat update pip{Colors.END}")
    except Exception as e:
        loading.stop()
        print(f"{Colors.RED}✗ Error update pip: {str(e)}{Colors.END}")
    
    input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def jalankan_python_script():
    """Menjalankan script Python"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║   JALANKAN SCRIPT PYTHON   ║{Colors.END}")
    print(f"{Colors.GREEN}╚════════════════════════════╝{Colors.END}")
    print()
    
    # Cari semua file tes.py di direktori dan subfolder
    files_python = []
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f == 'tes.py':
                files_python.append(os.path.join(root, f))
    
    if not files_python:
        print(f"{Colors.RED}Tidak ada file 'tes.py' ditemukan di direktori ini.{Colors.END}")
        input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")
        return
    
    print(f"{Colors.CYAN}Pilih script Python yang ingin dijalankan:{Colors.END}")
    for i, file in enumerate(files_python, 1):
        print(f"  {Colors.YELLOW}[{i}]{Colors.END} {file}")
    
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    try:
        pilihan = int(input(f"{Colors.GREEN}Pilih nomor: {Colors.END}"))
        
        if pilihan == 0:
            return
        
        if 1 <= pilihan <= len(files_python):
            file_terpilih = files_python[pilihan-1]
            
            loading = AnimasiLoading()
            loading.start(f"Menjalankan {file_terpilih}")
            
            try:
                time.sleep(2)
                loading.stop()
                
                print(f"\n{Colors.GREEN}Menjalankan: {file_terpilih}{Colors.END}")
                print(f"{Colors.CYAN}" + "="*50 + f"{Colors.END}")
                
                # Jalankan script Python dengan command yang sesuai
                python_cmd = "python" if os.name == 'nt' else "python3"
                os.system(f'{python_cmd} "{file_terpilih}"')
                
            except Exception as e:
                loading.stop()
                print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
            
            input(f"\n{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")
        else:
            print(f"{Colors.RED}Pilihan tidak valid!{Colors.END}")
            time.sleep(1)
    
    except ValueError:
        print(f"{Colors.RED}Input harus berupa angka!{Colors.END}")
        time.sleep(1)


def jalankan_server_web():
    """Menjalankan server web localhost menggunakan Python"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                   JALANKAN SERVER WEB                        ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    # Cek apakah direktori web dan file index.html ada
    web_dir = "web"
    index_file = os.path.join(web_dir, "index.html")
    
    if not os.path.exists(web_dir):
        print(f"{Colors.YELLOW}Membuat direktori 'web'...{Colors.END}")
        os.makedirs(web_dir)
    
    if not os.path.exists(index_file):
        print(f"{Colors.YELLOW}Membuat file index.html...{Colors.END}")
        buat_file_index_html()
    
    print(f"{Colors.CYAN}Pilih port untuk server web:{Colors.END}")
    print(f"  {Colors.YELLOW}[1]{Colors.END} Port 8080 (Default)")
    print(f"  {Colors.YELLOW}[2]{Colors.END} Port 8000")
    print(f"  {Colors.YELLOW}[3]{Colors.END} Custom port")
    print(f"  {Colors.YELLOW}[0]{Colors.END} Kembali")
    print()
    
    try:
        pilihan_port = int(input(f"{Colors.GREEN}Pilih nomor: {Colors.END}"))
        
        if pilihan_port == 0:
            return
        
        port = 8080  # Default
        
        if pilihan_port == 1:
            port = 8080
        elif pilihan_port == 2:
            port = 8000
        elif pilihan_port == 3:
            try:
                port = int(input(f"{Colors.CYAN}Masukkan port: {Colors.END}"))
                if port < 1 or port > 65535:
                    raise ValueError
            except ValueError:
                print(f"{Colors.RED}Port tidak valid! Menggunakan port 8080{Colors.END}")
                port = 8080
        else:
            print(f"{Colors.RED}Pilihan tidak valid! Menggunakan port 8080{Colors.END}")
        
        loading = AnimasiLoading()
        loading.start(f"Menjalankan server web di port {port}")
        
        try:
            time.sleep(2)
            loading.stop()
            
            print(f"\n{Colors.GREEN}Server web berhasil dijalankan!{Colors.END}")
            print(f"{Colors.CYAN}URL: http://localhost:{port}{Colors.END}")
            print(f"{Colors.CYAN}Direktori: {os.path.abspath(web_dir)}{Colors.END}")
            print(f"\n{Colors.YELLOW}Tekan Ctrl+C untuk menghentikan server{Colors.END}")
            print(f"{Colors.CYAN}" + "="*50 + f"{Colors.END}")
            
            # Simpan direktori saat ini
            current_dir = os.getcwd()
            
            # Pastikan kita di direktori yang benar
            if os.path.exists(web_dir):
                os.chdir(web_dir)
            
            try:
                # Jalankan server web menggunakan Python
                python_cmd = "python" if os.name == 'nt' else "python3"
                
                if os.name == 'nt':  # Windows
                    os.system(f'{python_cmd} -m http.server {port}')
                else:  # Unix/Linux
                    os.system(f'{python_cmd} -m http.server {port}')
                    
            except KeyboardInterrupt:
                print(f"\n{Colors.YELLOW}Server dihentikan.{Colors.END}")
            except Exception as e:
                print(f"\n{Colors.RED}Error menjalankan server: {str(e)}{Colors.END}")
            finally:
                # Kembali ke direktori semula
                os.chdir(current_dir)
            
        except Exception as e:
            loading.stop()
            print(f"\n{Colors.RED}Error: {str(e)}{Colors.END}")
    
    except ValueError:
        print(f"{Colors.RED}Input harus berupa angka!{Colors.END}")
        time.sleep(1)

def buat_file_index_html():
    """Membuat file index.html default"""
    content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LionCix - Cyber Security Platform</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel = "stylesheet" href = "css/cs.css">
      <link rel="icon" type="image/x-icon" href="https://cdn-icons-png.freepik.com/512/6783/6783360.png">
</head>
<body>
    <!-- Header -->
    <header>
        <div class="container">
            <div class="header-content">
                <div class="logo">
                    <i class="fas fa-shield-alt"></i>
                    <h1>LionCix</h1>
                </div>
                <nav class="desktop-nav">
                    <ul>
                        <li><a href="index2.html">esy:(Home)</a></li>
                        <li><a href="mudah.html">error:{Easy}</a></li>
                        <li><a href="level.html">syntax:{Medium}</a></li>
                        <li><a href="#">Community</a></li>
                        <li><a href="#">About</a></li>
                    </ul>
                </nav>
                <div class="auth-buttons">
                    <button class="btn btn-outline">Print("Prosess")</button>
                    <button class="btn btn-primary">helloword("print")</button>
                </div>
            </div>
        </div>
    </header>

    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h2>Advanced Cyber Security Platform</h2>
            <p>LionCix provides cutting-edge tools and resources for cybersecurity professionals, ethical hackers, and developers to test, learn, and secure digital systems.</p>
            <button class="btn btn-primary">./Get Started</button>
        </div>
    </section>

    <!-- VS Code Editor Section -->
    <section class="editor-section">
        <div class="container">
            <h2 class="section-title">VS Code Editor & Preview</h2>
            <div class="editor-container">
                <div class="editor-header">
                    <div class="editor-title">
                        <i class="fas fa-code"></i>
                        <span>LionCix Editor</span>
                    </div>
                    <div class="editor-controls">
                        <div class="control close"></div>
                        <div class="control minimize"></div>
                        <div class="control maximize"></div>
                    </div>
                </div>
                <div class="editor-body">
                    <div class="editor-sidebar">
                        <div class="sidebar-icon active">
                            <i class="fas fa-file-code"></i>
                        </div>
                        <div class="sidebar-icon">
                            <i class="fas fa-search"></i>
                        </div>
                        <div class="sidebar-icon">
                            <i class="fas fa-code-branch"></i>
                        </div>
                        <div class="sidebar-icon">
                            <i class="fas fa-bug"></i>
                        </div>
                        <div class="sidebar-icon">
                            <i class="fas fa-cog"></i>
                        </div>
                    </div>
                    <div class="editor-content">
                        <div class="editor-tabs">
                            <div class="editor-tab active">index.html</div>
                            <div class="editor-tab">style.css</div>
                            <div class="editor-tab">script.js</div>
                        </div>
                        <div class="editor-code">
                            <div class="code-line">
                                <span class="line-number">1</span>
                                <span class="line-content"><span class="keyword">&lt;!DOCTYPE</span> html&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">2</span>
                                <span class="line-content"><span class="keyword">&lt;html</span> lang=<span class="string">"en"</span>&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">3</span>
                                <span class="line-content"><span class="keyword">&lt;head&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">4</span>
                                <span class="line-content">  <span class="keyword">&lt;meta</span> charset=<span class="string">"UTF-8"</span>&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">5</span>
                                <span class="line-content">  <span class="keyword">&lt;meta</span> name=<span class="string">"viewport"</span> content=<span class="string">"width=device-width, initial-scale=1.0"</span>&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">6</span>
                                <span class="line-content">  <span class="keyword">&lt;title&gt;</span>LionCix - Cyber Security Platform<span class="keyword">&lt;/title&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">7</span>
                                <span class="line-content">  <span class="keyword">&lt;link</span> rel=<span class="string">"stylesheet"</span> href=<span class="string">"style.css"</span>&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">8</span>
                                <span class="line-content"><span class="keyword">&lt;/head&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">9</span>
                                <span class="line-content"><span class="keyword">&lt;body&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">10</span>
                                <span class="line-content">  <span class="keyword">&lt;header&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">11</span>
                                <span class="line-content">    <span class="keyword">&lt;h1&gt;</span>Welcome to LionCix<span class="keyword">&lt;/h1&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">12</span>
                                <span class="line-content">    <span class="keyword">&lt;p&gt;</span>Advanced Cyber Security Platform<span class="keyword">&lt;/p&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">13</span>
                                <span class="line-content">  <span class="keyword">&lt;/header&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">14</span>
                                <span class="line-content">  <span class="keyword">&lt;main&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">15</span>
                                <span class="line-content">    <span class="keyword">&lt;section</span> id=<span class="string">"features"</span>&gt;</span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">16</span>
                                <span class="line-content">      <span class="comment">&lt;!-- Features content here --&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">17</span>
                                <span class="line-content">    <span class="keyword">&lt;/section&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">18</span>
                                <span class="line-content">  <span class="keyword">&lt;/main&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">19</span>
                                <span class="line-content">  <span class="keyword">&lt;script</span> src=<span class="string">"script.js"</span>&gt;<span class="keyword">&lt;/script&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">20</span>
                                <span class="line-content"><span class="keyword">&lt;/body&gt;</span></span>
                            </div>
                            <div class="code-line">
                                <span class="line-number">21</span>
                                <span class="line-content"><span class="keyword">&lt;/html&gt;</span></span>
                            </div>
                        </div>
                    </div>
                    <div class="editor-preview">
                        <div class="preview-header">
                            <div class="preview-title">Preview: index.html</div>
                            <div class="preview-actions">
                                <button class="preview-action"><i class="fas fa-expand"></i></button>
                                <button class="preview-action"><i class="fas fa-sync-alt"></i></button>
                            </div>
                        </div>
                        <div class="preview-content">
                            <iframe src="about:blank" class="preview-website" id="preview-frame"></iframe>
                        </div>
                    </div>
                </div>
                <div class="editor-footer">
                    <div class="footer-status">
                        <div class="status-item">
                            <i class="fas fa-code-branch"></i>
                            <span>main</span>
                        </div>
                        <div class="status-item">
                            <i class="fas fa-check-circle"></i>
                            <span>Prettier</span>
                        </div>
                    </div>
                    <div class="footer-position">
                        <span>Ln 1, Col 1</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section class="features">
        <div class="container">
            <h2 class="section-title">Our Features</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-code"></i>
                    </div>
                    <h3>VS Code Editor</h3>
                    <p>Code directly in our browser-based VS Code editor with syntax highlighting, IntelliSense, and Git integration.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-eye"></i>
                    </div>
                    <h3>Live Preview</h3>
                    <p>See your changes in real-time with our integrated live preview feature that updates as you code.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3>Security Testing</h3>
                    <p>Test your code for vulnerabilities with our integrated security scanning tools and penetration testing.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Additional Features Section -->
    <section class="additional-features">
        <div class="container">
            <h2 class="section-title">Additional Features</h2>
            <div class="features-list">
                <div class="feature-item">
                    <i class="fas fa-terminal"></i>
                    <div class="feature-item-content">
                        <h4>Integrated Terminal</h4>
                        <p>Access a powerful terminal directly within the editor for running commands and scripts.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-puzzle-piece"></i>
                    <div class="feature-item-content">
                        <h4>Extensions Marketplace</h4>
                        <p>Enhance your editor with extensions from our marketplace tailored for security professionals.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-cloud"></i>
                    <div class="feature-item-content">
                        <h4>Cloud Storage</h4>
                        <p>Save your projects securely in the cloud and access them from anywhere.</p>
                    </div>
                </div>
                <div class="feature-item">
                    <i class="fas fa-users"></i>
                    <div class="feature-item-content">
                        <h4>Collaboration Tools</h4>
                        <p>Work together with your team in real-time with shared editing and commenting features.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-column">
                    <h3>LionCix</h3>
                    <p>Advanced cybersecurity platform for professionals and enthusiasts.</p>
                    <div class="social-links">
                        <a href="#"><i class="fab fa-github"></i></a>
                        <a href="#"><i class="fab fa-twitter"></i></a>
                        <a href="#"><i class="fab fa-discord"></i></a>
                        <a href="#"><i class="fab fa-linkedin"></i></a>
                    </div>
                </div>
                <div class="footer-column">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Tools</a></li>
                        <li><a href="#">Documentation</a></li>
                        <li><a href="#">Blog</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Resources</h3>
                    <ul>
                        <li><a href="#">Tutorials</a></li>
                        <li><a href="#">Cheat Sheets</a></li>
                        <li><a href="#">Community</a></li>
                        <li><a href="#">Support</a></li>
                    </ul>
                </div>
                <div class="footer-column">
                    <h3>Legal</h3>
                    <ul>
                        <li><a href="#">Terms of Service</a></li>
                        <li><a href="#">Privacy Policy</a></li>
                        <li><a href="#">Responsible Disclosure</a></li>
                        <li><a href="#">Code of Conduct</a></li>
                    </ul>
                </div>
            </div>
            <div class="copyright">
                <p>&copy; 2025 LionCix. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- Mobile Navbar -->
    <nav class="mobile-navbar">
        <ul class="mobile-nav-items">
            <li>
                <a href="index2.html" class="mobile-nav-item active">
                    <i class="fas fa-home"></i>
                    <span>esy:(Home)</span>
                </a>
            </li>
            <li>
                <a href="mudah.html" class="mobile-nav-item">
                    <i class="fas fa-code"></i>
                    <span>error:{Easy}</span>
                </a>
            </li>
            <li>
                <a href="level.html" class="mobile-nav-item">
                    <i class="fas fa-tools"></i>
                    <span>syntax:{Medium}</span>
                </a>
            </li>
            <li>
                <a href="#" class="mobile-nav-item">
                    <i class="fas fa-book"></i>
                    <span>Learn</span>
                </a>
            </li>
            <li>
                <a href="#" class="mobile-nav-item">
                    <i class="fas fa-user"></i>
                    <span>Account</span>
                </a>
            </li>
        </ul>
    </nav>
    <script src= "js/jsjs.js"></script>
</body>
</html>"""
    
    with open(os.path.join("web", "index.html"), "w", encoding="utf-8") as f:
        f.write(content)

def informasi_sistem():
    """Menampilkan informasi sistem"""
    clear_screen()
    tampilkan_ascii_art()
    
    print(f"{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.GREEN}║                     INFORMASI SISTEM                        ║{Colors.END}")
    print(f"{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}")
    print()
    
    # Informasi sistem yang lebih lengkap
    system_info = [
        ("Sistem Operasi", platform.system()),
        ("Versi OS", platform.release()),
        ("Arsitektur", platform.architecture()[0]),
        ("Processor", platform.processor() or "Tidak diketahui"),
        ("Python Version", platform.python_version()),
        ("Direktori Saat Ini", os.getcwd()),
        ("Koneksi Internet", "✅ Terhubung" if cek_koneksi_internet() else "❌ Terputus"),
        ("Platform", sys.platform),
        ("Terminal Size", f"{get_terminal_size()[0]}x{get_terminal_size()[1]}"),
    ]
    
    for label, value in system_info:
        print(f"{Colors.CYAN}{label:<20}:{Colors.END} {Colors.YELLOW}{value}{Colors.END}")
    
    print()
    input(f"{Colors.YELLOW}Tekan Enter untuk kembali...{Colors.END}")

def main():
    # Cek Python version
    if sys.version_info < (3, 6):
        print(f"{Colors.RED}Python 3.6 atau lebih tinggi diperlukan!{Colors.END}")
        sys.exit(1)
    
    while True:
        clear_screen()
        tampilkan_ascii_art()
        
        # Header dengan informasi
        cols, rows = get_terminal_size()
        header_width = min(cols - 4, 76)
        
        print(f"{Colors.GREEN}╔{'═' * header_width}╗{Colors.END}")
        print(f"{Colors.GREEN}║{'MENU UTAMA - TERMUX & WINDOWS TOOL'.center(header_width)}║{Colors.END}")
        print(f"{Colors.GREEN}╚{'═' * header_width}╝{Colors.END}")
        print()
        
        # Menu options yang diperbarui
        menu_options = [
            ("1", "Jalankan Script Python", "🐍"),
            ("2", "Jalankan Server Web", "🌐"),
            ("3", "Install Packages", "📦"),
            ("4", "Update Pip", "🔄"),
            ("5", "Informasi Sistem", "💻"),
            ("0", "Keluar", "🚪")
        ]
        
        for option, description, icon in menu_options:
            print(f"  {Colors.YELLOW}[{option}]{Colors.END} {icon} {description}")
        
        print()
        print(f"{Colors.CYAN}{'═' * header_width}{Colors.END}")
        
        # Informasi platform
        platform_info = "Windows" if os.name == 'nt' else "Termux/Linux"
        print(f"{Colors.MAGENTA}Platform: {platform_info} | Terminal: {cols}x{rows}{Colors.END}")
        print()
        
        try:
            pilihan = input(f"{Colors.GREEN}Pilih menu [{Colors.YELLOW}0-5{Colors.GREEN}]: {Colors.END}").strip()
            
            if pilihan == "1":
                jalankan_python_script()
            elif pilihan == "2":
                jalankan_server_web()
            elif pilihan == "3":
                install_packages()
            elif pilihan == "4":
                update_pip()
            elif pilihan == "5":
                informasi_sistem()
            elif pilihan == "0":
                print(f"\n{Colors.GREEN}Terima kasih telah menggunakan Termux Multi-Tool! 👋{Colors.END}")
                print(f"{Colors.CYAN}Sampai jumpa! 😊{Colors.END}")
                time.sleep(1)
                break
            else:
                print(f"{Colors.RED}Pilihan tidak valid! Silakan pilih 0-5.{Colors.END}")
                time.sleep(1)
        
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}Program dihentikan oleh pengguna.{Colors.END}")
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"{Colors.RED}Error: {str(e)}{Colors.END}")
        sys.exit(1)