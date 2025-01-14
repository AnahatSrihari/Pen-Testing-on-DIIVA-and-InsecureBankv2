from fpdf import FPDF
import datetime

class SecurityReport(FPDF):
    def header(self):
        # Logo - You can add your logo here
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'DIVA Android Security Assessment Report', 0, 1, 'C')
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

def generate_report():
    pdf = SecurityReport()
    pdf.add_page()
    
    # Title Page
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(0, 60, 'DIVA Android App', 0, 1, 'C')
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'Security Assessment Report', 0, 1, 'C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Date: {datetime.datetime.now().strftime("%Y-%m-%d")}', 0, 1, 'C')
    pdf.add_page()

    # Executive Summary
    pdf.chapter_title('Executive Summary')
    summary = """This report presents the findings of a security assessment conducted on the DIVA (Damn Insecure and Vulnerable App) Android application. DIVA is deliberately built to be vulnerable for learning and testing purposes. The assessment identified multiple high-risk vulnerabilities that could compromise user data and system security."""
    pdf.chapter_body(summary)

    # Vulnerability 1: Insecure Logging
    pdf.chapter_title('1. Insecure Logging')
    insecure_logging = """Severity: High
Risk: The application logs sensitive user credentials in plain text to the Android system log.

Technical Details:
- Location: Insecure Logging Activity
- Issue: User credentials (username and password) are logged using Android's Log.d()
- Impact: Any application with READ_LOGS permission can access user credentials
- Proof of Concept:
  1. Enter credentials in the login form
  2. Check logcat output using 'adb logcat'
  3. Credentials appear in plain text

Recommendation:
1. Remove all debug logging in production builds
2. Never log sensitive information
3. Implement proper logging levels (ERROR, WARN, INFO, DEBUG)"""
    pdf.chapter_body(insecure_logging)

    # Vulnerability 2: Hardcoding Issues
    pdf.chapter_title('2. Hardcoding Issues')
    hardcoding = """Severity: High
Risk: Critical secrets and API keys are hardcoded in the application code.

Technical Details:
- Location: Hardcoding Issues Activity
- Issue: API keys and credentials stored directly in source code
- Impact: Reverse engineering can easily expose sensitive credentials
- Proof of Concept:
  1. Decompile APK using tools like jadx
  2. Search for hardcoded strings
  3. Extract sensitive information

Recommendation:
1. Use Android Keystore System for storing sensitive keys
2. Implement proper key management systems
3. Use encryption for storing sensitive data
4. Consider using remote configuration for API endpoints"""
    pdf.chapter_body(hardcoding)

    # Vulnerability 3: Insecure Data Storage
    pdf.chapter_title('3. Insecure Data Storage')
    data_storage = """Severity: High
Risk: Sensitive user data stored without encryption in shared preferences and SQLite database.

Technical Details:
- Location: Insecure Data Storage Activities
- Issues Found:
  a) Plain text storage in SharedPreferences
  b) Unencrypted SQLite database
  c) External storage without proper permissions
- Impact: Local attacks can extract sensitive user data
- Proof of Concept:
  1. Access app's data directory using adb
  2. Extract shared_prefs and databases
  3. Read data without requiring decryption

Recommendation:
1. Use EncryptedSharedPreferences
2. Implement SQLCipher for database encryption
3. Use Android Keystore for key management
4. Avoid storing sensitive data in external storage"""
    pdf.chapter_body(data_storage)

    # Vulnerability 4: Access Control Issues
    pdf.chapter_title('4. Access Control Issues')
    access_control = """Severity: High
Risk: Insufficient access controls allow unauthorized access to protected functionality.

Technical Details:
- Location: Access Control Issue Activities
- Issues Found:
  a) Missing permission checks
  b) Implicit intents exposing sensitive activities
  c) Weak activity access controls
- Impact: Unauthorized users can access restricted features
- Proof of Concept:
  1. Launch activities directly using adb
  2. Bypass authentication checks
  3. Access protected features without proper authorization

Recommendation:
1. Implement proper permission checks
2. Use explicit intents for internal components
3. Add runtime permission validation
4. Implement proper authentication checks"""
    pdf.chapter_body(access_control)

    # Vulnerability 5: SQL Injection
    pdf.chapter_title('5. SQL Injection')
    sql_injection = """Severity: Critical
Risk: SQL injection vulnerabilities allow unauthorized database access and manipulation.

Technical Details:
- Location: SQL Injection Activity
- Issue: Raw SQL queries with unvalidated user input
- Impact: Attackers can:
  a) Extract unauthorized data
  b) Modify database contents
  c) Execute arbitrary SQL commands
- Proof of Concept:
  1. Input: ' OR '1'='1
  2. Input: '; DROP TABLE users;--
  3. Successfully bypass authentication

Recommendation:
1. Use parameterized queries
2. Implement input validation
3. Use ORM frameworks
4. Limit database user privileges"""
    pdf.chapter_body(sql_injection)

    # Recommendations Summary
    pdf.add_page()
    pdf.chapter_title('Overall Recommendations')
    recommendations = """1. Implement Secure Coding Practices:
- Follow OWASP Mobile Security Testing Guide
- Regular security training for developers
- Code review processes focusing on security

2. Enhance Data Protection:
- Implement encryption for all sensitive data
- Secure key management using Android Keystore
- Regular security assessments

3. Improve Access Controls:
- Proper authentication mechanisms
- Role-based access control
- Input validation and sanitization

4. Security Testing:
- Regular penetration testing
- Automated security scanning
- Vulnerability assessments

5. Monitoring and Logging:
- Implement secure logging practices
- Monitor for security incidents
- Regular security audits"""
    pdf.chapter_body(recommendations)

    # Save the report
    pdf.output('DIVA_Security_Report.pdf')

if __name__ == '__main__':
    generate_report()
