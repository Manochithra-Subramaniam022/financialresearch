import pyclbr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import sys
import os

def generate_multi_year_financials():
    filename = "5_year_income_statement.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph("Globex Corporation", title_style))
    elements.append(Paragraph("Consolidated Statement of Net Income", styles['Heading3']))
    elements.append(Paragraph("For the years ended Dec 31 (In Millions USD)", styles['Normal']))
    elements.append(Spacer(1, 0.25*inch))
    
    data = [
        ["Metric", "2020", "2021", "2022", "2023", "2024"],
        ["Product Revenue", "$1,450", "$1,600", "$1,850", "$2,100", "$2,400"],
        ["Service Revenue", "$350", "$400", "$500", "$650", "$850"],
        ["Total Revenue", "$1,800", "$2,000", "$2,350", "$2,750", "$3,250"],
        ["Cost of Revenue", "$800", "$900", "$1,050", "$1,200", "$1,400"],
        ["Gross Profit", "$1,000", "$1,100", "$1,300", "$1,550", "$1,850"],
        ["Operating Expenses", "$400", "$450", "$550", "$600", "$700"],
        ["Operating Income", "$600", "$650", "$750", "$950", "$1,150"],
        ["Net Income", "$450", "$490", "$580", "$720", "$880"]
    ]
    
    t = Table(data, colWidths=[2.5*inch] + [1*inch]*5)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("--- PAGE 1 ---", styles['Normal']))
    
    doc.build(elements)
    print(f"Created {filename}")

def generate_stock_data():
    filename = "apple_stock_jan_2025.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("AAPL - Apple Inc. Historical Stock Prices", styles['Heading1']))
    elements.append(Paragraph("January 2025 Daily Trading Data", styles['Normal']))
    elements.append(Spacer(1, 0.25*inch))
    
    data = [
        ["Date", "Open", "High", "Low", "Close", "Adj Close", "Volume"],
        ["2025-01-02", "190.50", "192.15", "189.20", "191.05", "191.05", "45,210,500"],
        ["2025-01-03", "191.20", "193.50", "190.10", "193.25", "193.25", "52,104,200"],
        ["2025-01-04", "192.90", "194.80", "191.50", "194.40", "194.40", "48,901,100"],
        ["2025-01-05", "194.10", "195.20", "192.80", "193.60", "193.60", "41,500,800"],
        ["2025-01-08", "193.50", "194.10", "190.50", "191.20", "191.20", "46,705,300"],
        ["2025-01-09", "191.80", "193.30", "191.10", "192.50", "192.50", "39,800,200"],
        ["2025-01-10", "192.10", "195.40", "191.90", "194.80", "194.80", "43,209,500"]
    ]
    
    t = Table(data, colWidths=[1.2*inch]*7)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
        ('ALIGN', (0,0), (0,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTSIZE', (0,0), (-1,-1), 8)
    ]))
    
    elements.append(t)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph("--- PAGE 1 ---", styles['Normal']))
    
    doc.build(elements)
    print(f"Created {filename}")

if __name__ == "__main__":
    generate_multi_year_financials()
    generate_stock_data()
