from io import BytesIO, StringIO
from xhtml2pdf import pisa

from flask import render_template

def html_to_pdf(template_name: str, **kwargs):
    html = render_template(template_name, **kwargs)
    
    pdf = BytesIO()

    status = pisa.CreatePDF(StringIO(html), pdf)
    if status.err:
        return None
    
    pdf.seek(0)

    return pdf