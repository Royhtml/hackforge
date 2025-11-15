<!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>LionCox - Lioncix Security</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
                color: #00ff00;
                min-height: 100vh;
                overflow-x: hidden;
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                padding: 40px 0;
                border-bottom: 2px solid #00ff00;
                margin-bottom: 40px;
            }
            
            .logo {
                font-size: 3.5em;
                font-weight: bold;
                color: #00ff00;
                text-shadow: 0 0 10px #00ff00, 0 0 20px #00ff00;
                margin-bottom: 10px;
                letter-spacing: 3px;
            }
            
            .subtitle {
                font-size: 1.2em;
                color: #00ff00;
                opacity: 0.8;
                margin-bottom: 20px;
            }
            
            .cyber-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
                margin-bottom: 50px;
            }
            
            .cyber-card {
                background: rgba(0, 255, 0, 0.05);
                border: 1px solid #00ff00;
                border-radius: 8px;
                padding: 30px;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .cyber-card::before {
                content: '';
                position: absolute;
                top: -2px;
                left: -2px;
                right: -2px;
                bottom: -2px;
                background: linear-gradient(45deg, #00ff00, #008000, #00ff00);
                z-index: -1;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .cyber-card:hover::before {
                opacity: 1;
            }
            
            .cyber-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 255, 0, 0.2);
            }
            
            .card-title {
                font-size: 1.5em;
                color: #00ff00;
                margin-bottom: 15px;
                font-weight: bold;
            }
            
            .card-content {
                color: #00ff00;
                opacity: 0.9;
                line-height: 1.6;
            }
            
            .terminal {
                background: #000000;
                border: 2px solid #00ff00;
                border-radius: 8px;
                padding: 20px;
                margin: 30px 0;
                font-family: 'Courier New', monospace;
            }
            
            .terminal-header {
                color: #00ff00;
                margin-bottom: 15px;
                font-weight: bold;
            }
            
            .terminal-output {
                color: #00ff00;
                line-height: 1.5;
            }
            
            .command {
                color: #ffff00;
            }
            
            .footer {
                text-align: center;
                padding: 30px 0;
                border-top: 1px solid #00ff00;
                margin-top: 50px;
                color: #00ff00;
                opacity: 0.7;
            }
            
            .scanning-animation {
                animation: scan 2s linear infinite;
            }
            
            @keyframes scan {
                0% { background-position: -100% 0; }
                100% { background-position: 200% 0; }
            }
            
            .security-badge {
                display: inline-block;
                background: #00ff00;
                color: #000;
                padding: 5px 15px;
                border-radius: 20px;
                font-weight: bold;
                margin: 10px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">LIONCIX</div>
                <div class="subtitle">CYBERSECURITY SOLUTIONS</div>
                <div class="security-badge">SECURE • RELIABLE • TRUSTED</div>
            </div>
            
            <div class="cyber-grid">
                <div class="cyber-card">
                    <div class="card-title">🔒 Security Monitoring</div>
                    <div class="card-content">
                        Real-time monitoring and threat detection to protect your digital assets from potential cyber threats.
                    </div>
                </div>
                
                <div class="cyber-card">
                    <div class="card-title">🛡️ Vulnerability Assessment</div>
                    <div class="card-content">
                        Comprehensive security assessments to identify and mitigate vulnerabilities in your systems.
                    </div>
                </div>
                
                <div class="cyber-card">
                    <div class="card-title">⚡ Incident Response</div>
                    <div class="card-content">
                        Rapid response team ready to handle security incidents and minimize impact on your operations.
                    </div>
                </div>
            </div>
            
            <div class="terminal">
                <div class="terminal-header">SYSTEM STATUS - SECURE</div>
                <div class="terminal-output">
                    <span class="command">$</span> system_check --security<br>
                    ✅ Firewall: ACTIVE<br>
                    ✅ Encryption: ENABLED<br>
                    ✅ Monitoring: RUNNING<br>
                    ✅ Updates: CURRENT<br>
                    <br>
                    <span class="command">$</span> threat_level<br>
                    🔒 CURRENT THREAT LEVEL: LOW<br>
                </div>
            </div>
            
            <div class="footer">
                &copy; 2024 LionCox - Lioncix Cybersecurity. All systems secure.
            </div>
        </div>
    </body>
    </html>
    