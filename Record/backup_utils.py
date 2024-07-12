import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from django.utils import timezone  # Ensure you import timezone from django.utils

def generate_receipt(payment):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=80, bottomMargin=80)
    styles = getSampleStyleSheet()

    # Define styles
    title_style = styles['Title']
    heading_style = styles['Heading1']
    body_style = styles['BodyText']

    # Elements to build the PDF
    elements = []

    

    # Add Company Logo
    logo_path = 'media/logotap.png'  # Adjust path as necessary
    logo = Image(logo_path, width=200, height=50)
    logo.drawHeight = 50  # Set logo height
    logo.drawWidth = 200  # Set logo width
    logo.hAlign = TA_CENTER  # Center align logo
    elements.append(logo)
    elements.append(Spacer(1, 20))

    # Title
    title = Paragraph("Payment Receipt", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Tenant Information
    tenant_info = [
        [Paragraph('<b>Tenant Name:</b>', body_style), Paragraph(f"{payment.tenant.first_name} {payment.tenant.last_name}", body_style)],
        [Paragraph('<b>Tenant ID:</b>', body_style), payment.tenant.identification_number],
        [Paragraph('<b>Email:</b>', body_style), payment.tenant.email],
        [Paragraph('<b>Phone:</b>', body_style), payment.tenant.phone]
    ]
    tenant_table = Table(tenant_info, colWidths=[120, '*'])
    tenant_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BACKGROUND', (1, 0), (-1, 0), colors.white),
    ]))
    elements.append(tenant_table)
    elements.append(Spacer(1, 20))

    # Payment Information
    payment_info = [
        [Paragraph('<b>Month:</b>', body_style), payment.month.name],
        [Paragraph('<b>Amount:</b>', body_style), f"ksh {payment.amount}"],
        [Paragraph('<b>Date Paid:</b>', body_style), payment.date_paid.strftime('%Y-%m-%d')],
        [Paragraph('<b>Mpesa Code:</b>', body_style), payment.mpesa_code]
    ]
    payment_table = Table(payment_info, colWidths=[120, '*'])
    payment_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('BACKGROUND', (1, 0), (-1, 0), colors.white),
    ]))
    elements.append(payment_table)

    # Footer (Optional)
    footer_text = "majiyashanzu@gmail.com"
    footer = Paragraph(footer_text, body_style)
    elements.append(Spacer(1, 20))
    elements.append(footer)

    # Build the PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer
