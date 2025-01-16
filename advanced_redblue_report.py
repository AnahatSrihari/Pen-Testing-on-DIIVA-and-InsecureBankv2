from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt
import numpy as np

class AdvancedRedBlueReport:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.story = []
        self.risk_colors = {
            'Critical': colors.red,
            'High': colors.orange,
            'Medium': colors.yellow,
            'Low': colors.green
        }

    def create_custom_styles(self):
        """Create custom styles for the report"""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,
            textColor=colors.HexColor('#1B4F72')
        )
        
        self.heading1_style = ParagraphStyle(
            'Heading1',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceBefore=30,
            spaceAfter=10,
            textColor=colors.HexColor('#2874A6')
        )
        
        self.heading2_style = ParagraphStyle(
            'Heading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10,
            textColor=colors.HexColor('#2E86C1')
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceBefore=6,
            spaceAfter=6
        )

    def create_cover_page(self, data):
        """Create an attractive cover page"""
        self.story.append(Paragraph("RED TEAM & BLUE TEAM", self.title_style))
        self.story.append(Paragraph("SECURITY ASSESSMENT REPORT", self.title_style))
        self.story.append(Spacer(1, 60))
        
        # Report metadata
        metadata = [
            ['Report Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Target Application:', data['target_app']],
            ['Assessment Period:', data['assessment_period']],
            ['Overall Risk Level:', data['risk_level']],
            ['Total Vulnerabilities:', str(len(data['vulnerabilities']))]
        ]
        
        metadata_table = Table(metadata, colWidths=[2.5*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50'))
        ]))
        self.story.append(metadata_table)
        self.story.append(PageBreak())

    def create_executive_summary(self, data):
        """Create executive summary section"""
        self.story.append(Paragraph("Executive Summary", self.heading1_style))
        summary_text = f"""
        This report presents the findings of a comprehensive security assessment conducted on {data['target_app']}.
        The assessment included both Red Team offensive security testing and Blue Team defensive analysis.
        
        Key Findings:
        • {len(data['critical_findings'])} Critical Risk Findings
        • {len(data['high_findings'])} High Risk Findings
        • {len(data['medium_findings'])} Medium Risk Findings
        • {len(data['low_findings'])} Low Risk Findings
        
        Overall Risk Assessment: {data['risk_level']}
        
        {data['executive_summary']}
        """
        self.story.append(Paragraph(summary_text, self.normal_style))
        self.story.append(PageBreak())

    def create_red_team_findings(self, data):
        """Create detailed red team findings section"""
        self.story.append(Paragraph("Red Team Assessment", self.heading1_style))
        
        # Attack Categories
        for category in data['attack_categories']:
            self.story.append(Paragraph(category['name'], self.heading2_style))
            
            findings_data = [['Finding', 'Risk Level', 'Status', 'Details']]
            for finding in category['findings']:
                findings_data.append([
                    finding['name'],
                    finding['risk_level'],
                    finding['status'],
                    finding['details']
                ])
            
            findings_table = Table(findings_data, colWidths=[2*inch, 1.2*inch, 1.2*inch, 3.6*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.lightgrey])
            ]))
            self.story.append(findings_table)
            self.story.append(Spacer(1, 20))

    def create_blue_team_analysis(self, data):
        """Create blue team analysis and recommendations section"""
        self.story.append(Paragraph("Blue Team Analysis", self.heading1_style))
        
        # Defense Categories
        for category in data['defense_categories']:
            self.story.append(Paragraph(category['name'], self.heading2_style))
            
            # Current Defense Status
            self.story.append(Paragraph("Current Defense Status:", self.heading2_style))
            status_text = category['current_status']
            self.story.append(Paragraph(status_text, self.normal_style))
            
            # Recommendations
            self.story.append(Paragraph("Recommendations:", self.heading2_style))
            for rec in category['recommendations']:
                rec_text = f"• {rec['title']}: {rec['description']}"
                self.story.append(Paragraph(rec_text, self.normal_style))
            
            # Implementation Timeline
            if 'timeline' in category:
                self.story.append(Paragraph("Implementation Timeline:", self.heading2_style))
                timeline_data = [['Phase', 'Duration', 'Priority', 'Resources Required']]
                for phase in category['timeline']:
                    timeline_data.append([
                        phase['name'],
                        phase['duration'],
                        phase['priority'],
                        phase['resources']
                    ])
                
                timeline_table = Table(timeline_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 3*inch])
                timeline_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                self.story.append(timeline_table)
            
            self.story.append(Spacer(1, 20))

    def create_risk_matrix(self, data):
        """Create risk matrix visualization"""
        plt.figure(figsize=(8, 6))
        
        # Create risk matrix
        risk_matrix = np.zeros((5, 5))
        for vuln in data['vulnerabilities']:
            impact = vuln['impact_score'] - 1
            likelihood = vuln['likelihood_score'] - 1
            risk_matrix[impact, likelihood] += 1
        
        plt.imshow(risk_matrix, cmap='RdYlGn_r')
        plt.colorbar(label='Number of Vulnerabilities')
        
        plt.title('Risk Matrix')
        plt.xlabel('Likelihood')
        plt.ylabel('Impact')
        
        # Save the plot
        plt.savefig('risk_matrix.png')
        plt.close()
        
        # Add to report
        self.story.append(Paragraph("Risk Matrix", self.heading1_style))
        self.story.append(Image('risk_matrix.png', width=6*inch, height=4*inch))
        self.story.append(PageBreak())

    def create_appendices(self, data):
        """Create appendices with detailed technical information"""
        self.story.append(Paragraph("Appendices", self.heading1_style))
        
        # Appendix A: Technical Details
        self.story.append(Paragraph("Appendix A: Technical Details", self.heading2_style))
        for detail in data['technical_details']:
            self.story.append(Paragraph(detail['title'], self.heading2_style))
            self.story.append(Paragraph(detail['content'], self.normal_style))
        
        # Appendix B: Test Cases
        self.story.append(Paragraph("Appendix B: Test Cases", self.heading2_style))
        test_data = [['Test ID', 'Description', 'Result', 'Notes']]
        for test in data['test_cases']:
            test_data.append([
                test['id'],
                test['description'],
                test['result'],
                test['notes']
            ])
        
        test_table = Table(test_data, colWidths=[1*inch, 3*inch, 1*inch, 3*inch])
        test_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        self.story.append(test_table)

    def generate_report(self, data, output_file='Advanced_RedBlue_Report.pdf'):
        """Generate the complete report"""
        doc = SimpleDocTemplate(output_file, pagesize=letter)
        self.create_custom_styles()
        
        # Create report sections
        self.create_cover_page(data)
        self.create_executive_summary(data)
        self.create_red_team_findings(data)
        self.create_blue_team_analysis(data)
        self.create_risk_matrix(data)
        self.create_appendices(data)
        
        # Build the PDF
        doc.build(self.story)
        print(f"Advanced Red Team and Blue Team report generated successfully: {output_file}")

if __name__ == "__main__":
    # Sample data structure
    sample_data = {
        "target_app": "Android InsecureBankv2",
        "assessment_period": "2024-01-15 to 2024-01-30",
        "risk_level": "High",
        "executive_summary": "Critical security vulnerabilities were identified...",
        "critical_findings": ["SQL Injection", "Authentication Bypass"],
        "high_findings": ["Weak Encryption", "Insecure Data Storage"],
        "medium_findings": ["Insufficient Logging", "Weak Password Policy"],
        "low_findings": ["Information Disclosure", "Debug Flags Enabled"],
        "vulnerabilities": [
            {"impact_score": 5, "likelihood_score": 4},
            {"impact_score": 4, "likelihood_score": 5},
            {"impact_score": 3, "likelihood_score": 3}
        ],
        "attack_categories": [
            {
                "name": "Authentication Attacks",
                "findings": [
                    {
                        "name": "Password Brute Force",
                        "risk_level": "High",
                        "status": "Exploited",
                        "details": "Successfully bypassed authentication..."
                    }
                ]
            }
        ],
        "defense_categories": [
            {
                "name": "Access Control",
                "current_status": "Current implementation lacks proper authentication...",
                "recommendations": [
                    {
                        "title": "Implement MFA",
                        "description": "Deploy multi-factor authentication..."
                    }
                ],
                "timeline": [
                    {
                        "name": "Planning",
                        "duration": "2 weeks",
                        "priority": "High",
                        "resources": "Security Team, Development Team"
                    }
                ]
            }
        ],
        "technical_details": [
            {
                "title": "Authentication Mechanism Analysis",
                "content": "Detailed technical analysis of current authentication..."
            }
        ],
        "test_cases": [
            {
                "id": "AUTH-001",
                "description": "Test authentication bypass...",
                "result": "Failed",
                "notes": "Successfully bypassed using SQL injection"
            }
        ]
    }
    
    # Generate report
    report_generator = AdvancedRedBlueReport()
    report_generator.generate_report(sample_data)
