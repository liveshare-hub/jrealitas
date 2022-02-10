from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template, render_to_string

from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict={}):
    # html_string = render_to_string("kunjungan/detil_kunjungan.html",context_dict,request=request)
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type="application/pdf")
    return None