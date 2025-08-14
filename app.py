from flask import Flask,render_template,redirect,request,url_for,flash,send_file
from flask_sqlalchemy import SQLAlchemy
import os
import google.generativeai as genai
from fpdf import FPDF
from io import BytesIO
from datetime import datetime,timedelta

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__)) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'code_diary.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
print(f"DEBUG: Value of GOOGLE_API_KEY from os.environ.get(): '{os.environ.get('GOOGLE_API_KEY')}'")
app.config['SECRET_KEY']='a_very_secret_and_random_key_for_flash_messages'

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY")) 

db = SQLAlchemy(app)

class Entry(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.Text,nullable=False)
    timestamp=db.Column(db.DateTime,default=db.func.now())
    summary=db.Column(db.Text,nullable=True)
    def __repr__(self):
        return f'<Entry {self.id}>'
    
def get_ai_summary(text_content):

    try:
        model = genai.GenerativeModel('models/gemini-2.0-flash-lite')

        print(f"\n--- AI Summary Request ---") 
        print(f"Input content: {text_content[:100]}...")
        
        response = model.generate_content(
            f"Summarize the following technical learning entry concisely (2-3 sentences), focusing on key concepts learned and any technologies mentioned:\n\n{text_content}",
            generation_config={"max_output_tokens": 100}
        )
        
        print(f"Gemini Raw Response Type: {type(response)}") 
        print(f"Gemini Raw Response: {response}") 

        summary = None 

        if response and response.parts:
            print(f"Response has parts. Number of parts: {len(response.parts)}") 
            temp_summary_parts = []
            for i, part in enumerate(response.parts):
                print(f"  Part {i} Type: {type(part)}") 
                print(f"  Part {i} Has text attribute: {hasattr(part, 'text')}") 
                if hasattr(part, 'text'):
                    temp_summary_parts.append(part.text)
                    print(f"  Part {i} Text: {part.text[:50]}...")
                else:
                    print(f"  Part {i} is not a text part.") 

            if temp_summary_parts:
                summary = "".join(temp_summary_parts).strip()
            else:
                print("Gemini API returned an empty text response despite having parts.") 
        else:
            print("Gemini API returned an empty or unexpected response (no response object or no parts).") 

        print(f"Final Generated Summary: {summary}") 
        print(f"--- End AI Summary Request ---\n") 

        return summary

    except Exception as e:
        print(f"An error occurred during Gemini AI summary generation: {e}")
        flash(f"An unexpected error occurred during AI summary generation.", 'warning')
        return None

@app.route('/')
def index():
    return redirect(url_for('new_entry'))

@app.route('/new_entry')
def new_entry():
    return render_template('input.html',now=datetime.now)

@app.route('/add_entry',methods=['POST'])
def add_entry():
    if request.method == 'POST':
        content = request.form['content']
        if not content :
            flash('Your learning entry cannot be empty!','danger')
            return redirect(url_for('new_entry'))
    
    summary = get_ai_summary(content) 
    new_entry = Entry(content=content, summary=summary) 
    
    try:
        db.session.add(new_entry)
        db.session.commit()
        flash('Your entry is saved successfully!' + (' (with AI summary!)' if summary else ' (AI summary failed to generate.)'), 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while saving: {e}','danger') 
    return redirect(url_for('new_entry'))

@app.route('/dashboard')
def dashboard():
    entries=Entry.query.order_by(Entry.timestamp.desc()).all()
    return render_template('dashboard.html',entries=entries,now=datetime.now,timedelta=timedelta)
@app.route('/clear_all_entries', methods=['POST'])
def clear_all_entries():
    try:
        num_deleted = db.session.query(Entry).delete()
        db.session.commit()
        flash(f'Successfully deleted {num_deleted} entries!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred while clearing entries: {e}', 'danger')
    return redirect(url_for('dashboard'))
@app.route('/export_pdf')
def export_pdf():
    entries = Entry.query.order_by(Entry.timestamp.asc()).all()

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
            
            pdf.set_font("Arial", "B", size=10) 
            pdf.cell(0, 10, txt=f"Date: {entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
            
            
            pdf.set_font("Arial", size=10)
            
            pdf.multi_cell(0, 5, txt=f"Learned: {entry.content}")
            pdf.ln(2) 

            
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
@app.route('/weekly_summary')
def weekly_summary():
    seven_days_ago = datetime.now() - timedelta(days=7)
    recent_entries = Entry.query.filter(Entry.timestamp >= seven_days_ago).order_by(Entry.timestamp.asc()).all()

    combined_content = ""
    for entry in recent_entries:
        combined_content += f"On {entry.timestamp.strftime('%Y-%m-%d')}: {entry.content}\n\n"

    weekly_summary_text = None
    if combined_content.strip(): 
        weekly_summary_text = get_ai_summary(
            f"Generate a concise, high-level summary (3-5 sentences) of the following weekly technical learning entries. Focus on overarching themes, key technologies mentioned, and significant achievements:\n\n{combined_content}"
        )
    
    return render_template('weekly_summary.html', weekly_summary=weekly_summary_text,now=datetime.now)
if __name__ == '__main__' :
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0',port=10000,debug=True)