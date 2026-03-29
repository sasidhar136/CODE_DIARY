"""
Export routes for generating PDF and other formats
"""
from flask import send_file
from io import BytesIO
from fpdf import FPDF
from flask_login import login_required, current_user
from app.routes import export_bp
from app.models import Entry

@export_bp.route('/pdf')
@login_required
def export_pdf():
    """Export all entries as PDF"""
    entries = Entry.query.filter_by(user_id=current_user.id).order_by(Entry.timestamp.asc()).all()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Code Diary - All Entries", ln=True, align="C")
    pdf.ln(10)

    if not entries:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="No entries to export.", ln=True, align="L")
    else:
        for entry in entries:
            # Date
            pdf.set_font("Arial", "B", size=10)
            pdf.cell(0, 10, txt=f"Date: {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

            # Content
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 5, txt=f"Learned: {entry.content}")
            pdf.ln(2)

            # Summary if available
            if entry.summary:
                pdf.set_font("Arial", "I", size=9)
                pdf.multi_cell(0, 5, txt=f"AI Summary: {entry.summary}")
                pdf.ln(2)

            pdf.ln(5)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(5)

    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return send_file(
        pdf_output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name='code_diary_entries.pdf'
    )
