import pdfplumber
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Create a sample financial PDF to test the app
file_path = "sample_financial_report.pdf"
c = canvas.Canvas(file_path, pagesize=letter)
c.setFont("Helvetica-Bold", 16)
c.drawString(50, 750, "Quarterly Financial Report Q3 2023")

c.setFont("Helvetica", 12)
c.drawString(50, 700, "Company: Bharat Innovations Pvt Ltd.")
c.drawString(50, 680, "Date: November 15, 2023")

c.setFont("Helvetica-Bold", 14)
c.drawString(50, 640, "Financial Highlights:")

c.setFont("Helvetica", 12)
c.drawString(50, 610, "We are pleased to report strong financial results. Below are the key figures.\n\n"
           "--- PAGE 1 ---\n"
           "Consolidated Income Statement (in Crores)\n"
           "Metric | Year Ended 2024 | Year Ended 2025\n"
           "Product Sales | ₹ 800.00 | ₹ 950.00\n"
           "Service Revenue | ₹ 200.00 | ₹ 250.00\n"
           "Total Revenue | ₹ 1,000.00 | ₹ 1,200.00\n"
           "Cost of Goods Sold | ₹ 400.00 | ₹ 450.00\n"
           "Gross Margin | ₹ 600.00 | ₹ 750.00\n"
           "Operating Expenses | ₹ 300.00 | ₹ 320.00\n"
           "Net Income | ₹ 300.00 | ₹ 430.00\n"
           "--- PAGE 2 ---\n"
           "Consolidated Balance Sheet (in Crores)\n"
           "Total Assets | ₹ 3,000.00 | ₹ 3,400.00\n"
           "Total Liabilities | ₹ 1,000.00 | ₹ 1,100.00\n"
           "Total Shareholders' Equity | ₹ 2,000.00 | ₹ 2,300.00\n"
           "\n"
           "The management attributes the 20% revenue growth to increased demand for our primary software products.")
c.drawString(50, 530, "Earnings Per Share (EPS): ₹115.50")

c.setFont("Helvetica-Oblique", 10)
c.drawString(50, 480, "Note: These figures are unaudited and subject to change.")

c.save()
print(f"Created sample PDF at {file_path}")
