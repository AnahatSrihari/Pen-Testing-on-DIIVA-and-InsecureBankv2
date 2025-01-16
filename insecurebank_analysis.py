#!/usr/bin/env python3

import subprocess
import json
import os
from datetime import datetime
from android_pentest import AndroidPentestFramework

# Add ADB path constant
ADB_PATH = "C:\\Program Files\\platform-tools\\adb.exe"

class InsecureBankAnalyzer(AndroidPentestFramework):
    def __init__(self):
        super().__init__()
        self.package_name = "com.android.insecurebankv2"
        self.report_data['app_name'] = "Android InsecureBankv2"
        self.report_data['analysis_modules'] = []

    def check_root_detection(self):
        """Check for root detection mechanisms"""
        try:
            result = subprocess.run(
                [ADB_PATH, 'shell', 'strings', '/data/app/' + self.package_name + '*/base.apk'],
                capture_output=True,
                text=True
            )
            root_indicators = [
                'su',
                'busybox',
                'superuser',
                'SuperSU',
                'RootChecker'
            ]
            findings = []
            
            for line in result.stdout.split('\n'):
                for indicator in root_indicators:
                    if indicator.lower() in line.lower():
                        findings.append(line.strip())
            
            self.report_data['analysis_modules'].append({
                'module': 'root_detection',
                'findings': findings,
                'risk_level': 'Medium' if not findings else 'Low'
            })
            return findings
        except Exception as e:
            print(f"Error checking root detection: {e}")
            return []

    def analyze_network_security(self):
        """Analyze network security configurations"""
        try:
            result = subprocess.run(
                [ADB_PATH, 'shell', 'strings', '/data/app/' + self.package_name + '*/base.apk'],
                capture_output=True,
                text=True
            )
            security_issues = []
            
            # Check for HTTP URLs
            if 'http://' in result.stdout:
                security_issues.append('Uses insecure HTTP connections')
            
            # Check for hardcoded endpoints
            if 'api.' in result.stdout or 'www.' in result.stdout:
                security_issues.append('Contains hardcoded API endpoints')
            
            # Check for certificate validation
            cert_checks = [
                'X509TrustManager',
                'HostnameVerifier',
                'SSLSocketFactory'
            ]
            for check in cert_checks:
                if check in result.stdout:
                    security_issues.append(f'Custom {check} implementation found - potential SSL bypass')
            
            self.report_data['analysis_modules'].append({
                'module': 'network_security',
                'findings': security_issues,
                'risk_level': 'High' if security_issues else 'Low'
            })
            return security_issues
        except Exception as e:
            print(f"Error analyzing network security: {e}")
            return []

    def check_data_storage(self):
        """Analyze data storage security"""
        try:
            result = subprocess.run(
                [ADB_PATH, 'shell', 'run-as', self.package_name, 'ls', '/data/data/' + self.package_name],
                capture_output=True,
                text=True
            )
            storage_issues = []
            
            # Check for sensitive directories
            sensitive_dirs = ['shared_prefs', 'databases', 'files']
            for dir_name in sensitive_dirs:
                if dir_name in result.stdout:
                    storage_issues.append(f'Found {dir_name} directory - potential sensitive data storage')
            
            # Check shared preferences
            if 'shared_prefs' in result.stdout:
                prefs_result = subprocess.run(
                    [ADB_PATH, 'shell', 'run-as', self.package_name, 'ls', '/data/data/' + self.package_name + '/shared_prefs'],
                    capture_output=True,
                    text=True
                )
                if prefs_result.stdout:
                    storage_issues.append('Shared preferences files found - check for sensitive data storage')
            
            self.report_data['analysis_modules'].append({
                'module': 'data_storage',
                'findings': storage_issues,
                'risk_level': 'High' if storage_issues else 'Low'
            })
            return storage_issues
        except Exception as e:
            print(f"Error checking data storage: {e}")
            return []

    def analyze_exported_components(self):
        """Analyze exported components in the application"""
        try:
            result = subprocess.run(
                [ADB_PATH, 'shell', 'dumpsys', 'package', self.package_name],
                capture_output=True,
                text=True
            )
            
            exported_components = []
            current_component = None
            
            for line in result.stdout.split('\n'):
                if 'Activity' in line or 'Service' in line or 'Receiver' in line:
                    current_component = line.strip()
                elif 'android.intent.action' in line and current_component:
                    exported_components.append({
                        'component': current_component,
                        'intent_filter': line.strip()
                    })
            
            self.report_data['analysis_modules'].append({
                'module': 'exported_components',
                'findings': exported_components,
                'risk_level': 'High' if exported_components else 'Low'
            })
            return exported_components
        except Exception as e:
            print(f"Error analyzing exported components: {e}")
            return []

    def generate_detailed_report(self, output_file='insecurebank_report.json'):
        """Generate a detailed JSON report with all findings"""
        try:
            self.report_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.report_data['summary'] = {
                'total_issues': sum(len(module['findings']) for module in self.report_data['analysis_modules']),
                'risk_levels': {
                    'High': len([m for m in self.report_data['analysis_modules'] if m['risk_level'] == 'High']),
                    'Medium': len([m for m in self.report_data['analysis_modules'] if m['risk_level'] == 'Medium']),
                    'Low': len([m for m in self.report_data['analysis_modules'] if m['risk_level'] == 'Low'])
                }
            }
            
            with open(output_file, 'w') as f:
                json.dump(self.report_data, f, indent=4)
            print(f"Detailed report generated successfully: {output_file}")
            
            # Generate markdown report
            self.generate_markdown_report()
        except Exception as e:
            print(f"Error generating report: {e}")

    def generate_markdown_report(self):
        """Generate a markdown report for better readability"""
        try:
            markdown_content = f"""# Security Analysis Report: Android InsecureBankv2
            
## Overview
- **Application**: {self.report_data['app_name']}
- **Analysis Date**: {self.report_data['timestamp']}
- **Package Name**: {self.package_name}

## Executive Summary
- Total Issues Found: {self.report_data['summary']['total_issues']}
- Risk Level Distribution:
  - High: {self.report_data['summary']['risk_levels']['High']}
  - Medium: {self.report_data['summary']['risk_levels']['Medium']}
  - Low: {self.report_data['summary']['risk_levels']['Low']}

## Detailed Findings

"""
            for module in self.report_data['analysis_modules']:
                markdown_content += f"""### {module['module'].replace('_', ' ').title()}
- **Risk Level**: {module['risk_level']}
- **Findings**:
"""
                if isinstance(module['findings'], list):
                    for finding in module['findings']:
                        if isinstance(finding, dict):
                            for key, value in finding.items():
                                markdown_content += f"  - {key}: {value}\n"
                        else:
                            markdown_content += f"  - {finding}\n"
                markdown_content += "\n"

            markdown_content += """
## Recommendations

1. Implement proper SSL/TLS certificate validation
2. Remove any hardcoded sensitive information
3. Implement proper root detection mechanisms
4. Secure data storage using encryption
5. Review and secure exported components
6. Implement proper authentication mechanisms
7. Add proper input validation

## Conclusion
This security analysis has identified several critical security issues that need to be addressed. The application shows multiple vulnerabilities that could be exploited by malicious actors.

"""
            
            with open('insecurebank_report.md', 'w') as f:
                f.write(markdown_content)
            print("Markdown report generated successfully: insecurebank_report.md")
        except Exception as e:
            print(f"Error generating markdown report: {e}")

def main():
    analyzer = InsecureBankAnalyzer()
    
    print("Starting Android InsecureBankv2 Security Analysis...")
    
    print("\n1. Checking ADB Connection...")
    if not analyzer.check_adb_connection():
        print("No Android device connected. Please connect a device and try again.")
        return
    
    print("\n2. Analyzing App Permissions...")
    analyzer.analyze_app_permissions(analyzer.package_name)
    
    print("\n3. Checking Root Detection...")
    analyzer.check_root_detection()
    
    print("\n4. Analyzing Network Security...")
    analyzer.analyze_network_security()
    
    print("\n5. Checking Data Storage...")
    analyzer.check_data_storage()
    
    print("\n6. Analyzing Exported Components...")
    analyzer.analyze_exported_components()
    
    print("\n7. Checking Debug Status...")
    analyzer.check_debug_enabled(analyzer.package_name)
    
    print("\n8. Scanning for Sensitive Data...")
    analyzer.scan_for_sensitive_data(analyzer.package_name)
    
    print("\n9. Checking SSL Pinning Implementation...")
    analyzer.check_ssl_pinning(analyzer.package_name)
    
    # Generate final reports
    analyzer.generate_detailed_report()
    
    print("\nAnalysis completed. Check insecurebank_report.json and insecurebank_report.md for detailed results.")

if __name__ == "__main__":
    main()
