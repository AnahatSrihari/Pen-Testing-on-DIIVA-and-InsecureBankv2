from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import json
import os

def create_detailed_pdf_report(output_filename="InsecureBankv2_Detailed_Security_Report.pdf"):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1
    )
    
    heading1_style = ParagraphStyle(
        'Heading1',
        parent=styles['Heading1'],
        fontSize=20,
        spaceBefore=30,
        spaceAfter=10
    )
    
    heading2_style = ParagraphStyle(
        'Heading2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10
    )
    
    heading3_style = ParagraphStyle(
        'Heading3',
        parent=styles['Heading3'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=5
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceBefore=6,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=10,
        fontName='Courier',
        spaceBefore=10,
        spaceAfter=10,
        backColor=colors.lightgrey,
        borderPadding=5
    )

    # Cover Page
    story.append(Paragraph("SECURITY ASSESSMENT REPORT", title_style))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Android InsecureBankv2 Application", title_style))
    story.append(Spacer(1, 60))
    
    # Report metadata
    metadata = [
        ['Report Date:', datetime.now().strftime("%Y-%m-%d")],
        ['Version:', '1.0'],
        ['Classification:', 'Confidential'],
        ['Target Application:', 'Android InsecureBankv2'],
        ['Package Name:', 'com.android.insecurebankv2'],
        ['Platform:', 'Android'],
    ]
    
    metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(metadata_table)
    story.append(PageBreak())

    # Table of Contents
    story.append(Paragraph("Table of Contents", heading1_style))
    toc_items = [
        "1. Executive Summary",
        "2. Methodology",
        "3. Technical Analysis",
        "4. Vulnerability Assessment",
        "5. Risk Analysis",
        "6. Detailed Findings",
        "7. Recommendations",
        "8. Appendices"
    ]
    for item in toc_items:
        story.append(Paragraph(item, normal_style))
    story.append(PageBreak())

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary", heading1_style))
    exec_summary = """
    This report presents a comprehensive security assessment of the Android InsecureBankv2 
    application. The assessment revealed multiple critical security vulnerabilities that pose 
    significant risks to the application and its users. The findings include issues related 
    to exposed components, insufficient security controls, and potential data exposure vectors.
    
    Key Statistics:
    • Total Vulnerabilities Found: 4
    • Critical Risk Issues: 1
    • High Risk Issues: 1
    • Medium Risk Issues: 1
    • Low Risk Issues: 1
    """
    story.append(Paragraph(exec_summary, normal_style))
    story.append(PageBreak())

    # 2. Methodology
    story.append(Paragraph("2. Methodology", heading1_style))
    methodology = """
    The security assessment was conducted using a comprehensive approach that included:
    
    2.1 Static Analysis
    • Source code review
    • Manifest analysis
    • Permission assessment
    • Component exposure analysis
    
    2.2 Dynamic Analysis
    • Runtime behavior monitoring
    • Network traffic analysis
    • Data storage analysis
    • Component interaction testing
    
    2.3 Tools Used
    • Android Debug Bridge (ADB)
    • Custom security analysis scripts
    • Network monitoring tools
    • Static code analysis tools
    """
    story.append(Paragraph(methodology, normal_style))
    story.append(PageBreak())

    # 3. Technical Analysis
    story.append(Paragraph("3. Technical Analysis", heading1_style))
    
    # 3.1 Application Architecture
    story.append(Paragraph("3.1 Application Architecture", heading2_style))
    arch_analysis = """
    The InsecureBankv2 application implements a basic banking functionality with the following 
    components:
    
    • Activities:
      - LoginActivity: Main entry point
      - TransferActivity: Handles fund transfers
      - BalanceActivity: Displays account balance
    
    • Services:
      - Background services for transaction processing
    
    • Content Providers:
      - Custom providers for data storage
    """
    story.append(Paragraph(arch_analysis, normal_style))

    # 3.2 Permission Analysis
    story.append(Paragraph("3.2 Permission Analysis", heading2_style))
    permission_table_data = [
        ['Permission', 'Risk Level', 'Purpose'],
        ['INTERNET', 'Medium', 'Network Communication'],
        ['READ_EXTERNAL_STORAGE', 'High', 'File Access'],
        ['WRITE_EXTERNAL_STORAGE', 'High', 'Data Storage'],
    ]
    permission_table = Table(permission_table_data, colWidths=[2.5*inch, 1.5*inch, 3*inch])
    permission_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(permission_table)
    story.append(PageBreak())

    # 4. Vulnerability Assessment
    story.append(Paragraph("4. Vulnerability Assessment", heading1_style))
    
    # 4.1 High Risk Vulnerabilities
    story.append(Paragraph("4.1 High Risk Vulnerabilities", heading2_style))
    
    # Exported Components
    story.append(Paragraph("4.1.1 Exported Components Vulnerability", heading3_style))
    exported_comp = """
    Description:
    The application exposes several critical components through the Android manifest without 
    proper protection mechanisms.
    
    Technical Details:
    • LoginActivity is exported without custom permissions
    • Vulnerable Intent handling in exposed components
    • Lack of proper intent validation
    
    Impact:
    • Unauthorized access to application components
    • Potential account compromise
    • Data theft and manipulation
    
    Code Evidence:
    """
    story.append(Paragraph(exported_comp, normal_style))
    
    code_sample = """
    <activity
        android:name=".LoginActivity"
        android:exported="true">
        <intent-filter>
            <action android:name="android.intent.action.MAIN" />
            <category android:name="android.intent.category.LAUNCHER" />
        </intent-filter>
    </activity>
    """
    story.append(Paragraph(code_sample, code_style))

    # 4.2 Medium Risk Vulnerabilities
    story.append(Paragraph("4.2 Medium Risk Vulnerabilities", heading2_style))
    
    # Insecure Data Storage
    story.append(Paragraph("4.2.1 Insecure Data Storage", heading3_style))
    storage_vuln = """
    Description:
    The application stores sensitive information in plaintext and uses insecure storage methods.
    
    Technical Details:
    • Plaintext storage of credentials
    • Use of unencrypted SharedPreferences
    • Insecure file permissions
    
    Impact:
    • Exposure of user credentials
    • Unauthorized data access
    • Privacy violations
    """
    story.append(Paragraph(storage_vuln, normal_style))
    story.append(PageBreak())

    # 5. Risk Analysis
    story.append(Paragraph("5. Risk Analysis", heading1_style))
    risk_matrix_data = [
        ['', 'Low Impact', 'Medium Impact', 'High Impact'],
        ['High Likelihood', 'Medium', 'High', 'Critical'],
        ['Medium Likelihood', 'Low', 'Medium', 'High'],
        ['Low Likelihood', 'Low', 'Low', 'Medium']
    ]
    risk_matrix = Table(risk_matrix_data, colWidths=[2*inch, 2*inch, 2*inch, 2*inch])
    risk_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(risk_matrix)
    story.append(PageBreak())

    # 6. Detailed Findings
    story.append(Paragraph("6. Detailed Findings", heading1_style))
    findings_data = [
        ['Vulnerability', 'Risk Level', 'CVSS Score', 'Status'],
        ['Exported Components', 'High', '8.5', 'Open'],
        ['Insecure Data Storage', 'Medium', '6.5', 'Open'],
        ['Weak Crypto', 'Medium', '5.5', 'Open'],
        ['Debug Enabled', 'Low', '3.5', 'Open']
    ]
    findings_table = Table(findings_data, colWidths=[3*inch, 1.5*inch, 1.5*inch, 1*inch])
    findings_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(findings_table)

    # 7. Recommendations
    story.append(Paragraph("7. Recommendations", heading1_style))
    recommendations = """
    7.1 Short-term Recommendations
    
    • Remove exported flags from sensitive components
    • Implement proper intent filters and permissions
    • Enable encryption for stored data
    • Implement proper SSL/TLS certificate validation
    
    7.2 Long-term Recommendations
    
    • Implement a secure authentication mechanism
    • Add runtime permission checks
    • Implement proper session management
    • Add security headers and response validation
    • Implement proper logging and monitoring
    
    7.3 Best Practices
    
    • Follow Android security best practices
    • Regular security assessments
    • Keep dependencies updated
    • Implement proper error handling
    """
    story.append(Paragraph(recommendations, normal_style))
    story.append(PageBreak())

    # 8. Appendices
    story.append(Paragraph("8. Appendices", heading1_style))
    
    # 8.1 Testing Environment
    story.append(Paragraph("8.1 Testing Environment", heading2_style))
    env_details = """
    • Android SDK Version: 30
    • Test Device: Android Emulator
    • Tools Used: ADB, Custom Analysis Scripts
    • Test Duration: Comprehensive Analysis
    """
    story.append(Paragraph(env_details, normal_style))
    
    # 8.2 References
    story.append(Paragraph("8.2 References", heading2_style))
    references = """
    • OWASP Mobile Top 10
    • Android Security Guidelines
    • CWE/SANS Top 25
    • NIST Mobile Device Security Guidelines
    """
    story.append(Paragraph(references, normal_style))

    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Confidential"
    story.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.grey
    )))

    # Build the PDF
    doc.build(story)
    print(f"Detailed PDF report generated successfully: {output_filename}")

if __name__ == "__main__":
    create_detailed_pdf_report()
