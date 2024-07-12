import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone  # Ensure you import timezone from django.utils

def generate_receipt(payment):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=80, bottomMargin=80)
    styles = getSampleStyleSheet()

    # Define styles
    

    styles = getSampleStyleSheet()
    body_style = styles['BodyText']
    body_style.fontName = 'Helvetica'
    body_style.fontSize = 12
    
    title_style = styles['Title']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 16

    # Elements to build the PDF
    elements = []

    # Add Company Logo
    logo_path = 'media/logotap.png'  # Adjust path as necessary
    logo = Image(logo_path, width=80, height=80)
    elements.append(logo)
    elements.append(Spacer(1, 20))

    # Title
    title = Paragraph("Payment Receipt", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Tenant Information
    # Tenant Information (Paragraphs)
    tenant_info = [
        f"<b>Tenant Name:</b> {payment.tenant.first_name} {payment.tenant.last_name}",
        f"<b>Tenant ID:</b> {payment.tenant.identification_number}",
        f"<b>Tap Number:</b> {payment.tenant.tap_no or 'N/A'}",
        f"<b>Address:</b> {payment.tenant.address}",
        f"<b>House:</b> {payment.tenant.house.name}",
        f"<b>Email:</b> {payment.tenant.email}",
        f"<b>Phone:</b> {payment.tenant.phone}"
    ]
    for info in tenant_info:
        elements.append(Paragraph(info, body_style))
        elements.append(Spacer(1, 10))

    # Spacer between tenant info and payment info
    elements.append(Spacer(1, 20))

    # Payment Information
    payment_info = [
        [Paragraph('<b>Month:</b>', body_style), payment.month.name],
        [Paragraph('<b>Amount:</b>', body_style), f"ksh {payment.amount}"],
        [Paragraph('<b>Date Paid:</b>', body_style), payment.date_paid.strftime('%b %d, %Y')],  # Adjusted date format
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
    elements.append(Spacer(1, 130))

    # Footer
    footer_text = f"Generated for {payment.tenant.first_name} {payment.tenant.last_name} - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer = Paragraph(footer_text, body_style)
    elements.append(Spacer(1, 20))
    elements.append(footer)

    # Build the PDF
    doc.build(elements)

    buffer.seek(0)
    return buffer
