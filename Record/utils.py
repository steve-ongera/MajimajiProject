import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from django.utils import timezone  # Ensure you import timezone from django.utils

# utils.py
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

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












def generate_tenant_pdf(tenant, payments):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Define styles
    

    styles = getSampleStyleSheet()
    body_style = styles['BodyText']
    body_style.fontName = 'Helvetica'
    body_style.fontSize = 12
    
    title_style = styles['Title']
    title_style.fontName = 'Helvetica-Bold'
    title_style.fontSize = 16

    # Add Company Logo
    logo_path = 'media/logotap.png'  # Adjust path as necessary
    logo = Image(logo_path, width=80, height=80)
    elements.append(logo)
    elements.append(Spacer(1, 20))

    # Title
    title = Paragraph("Payment Receipt", title_style)
    elements.append(title)
    elements.append(Spacer(1, 20))

    # Add tenant information
    elements.append(Paragraph(f"Tenant Information", styles['Heading1']))
    elements.append(Paragraph(f"Username: {tenant.user_name} ", styles['Normal']))
    elements.append(Paragraph(f"Name: {tenant.first_name} {tenant.last_name}", styles['Normal']))
    elements.append(Paragraph(f"Identification Number: {tenant.identification_number}", styles['Normal']))
    elements.append(Paragraph(f"Email: {tenant.email} ", styles['Normal']))
    elements.append(Paragraph(f"Phone: {tenant.phone} ", styles['Normal']))
    elements.append(Paragraph(f"Address: {tenant.address} ", styles['Normal']))
    elements.append(Paragraph(f"House: {tenant.house} ", styles['Normal']))
    elements.append(Paragraph(f"Tap No: {tenant.tap_no} ", styles['Normal']))
    elements.append(Paragraph("Payment History", styles['Heading2']))

    # Create table data
    data = [['month','Date', 'Amount', 'mpesa code']]
    for payment in payments:
        data.append([ payment.month , str(payment.date_paid) , f"{ str(payment.amount) } ksh", payment.mpesa_code])

    # Create table
    table = Table(data)

    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    table.setStyle(style)
    elements.append(table)

    elements.append(Spacer(1, 70))

    # Footer
   
    footer_text = f" majiyashanzu@gmail.com - {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    footer = Paragraph(footer_text, body_style)
    elements.append(Spacer(1, 20))
    elements.append(footer)


    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def create_pdf_response(pdf_content, filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    response.write(pdf_content)
    return response