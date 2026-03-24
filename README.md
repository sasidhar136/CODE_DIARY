# Code Diary

A Flask-based web application for documenting and tracking your daily technical learning. Each entry is automatically summarized using Google's Gemini AI, and you can generate weekly summaries of your progress.

## Features

✨ **AI-Powered Summaries** - Automatically summarize your learning entries using Google Gemini AI  
📅 **Daily Learning Tracker** - Log your daily technical learnings and discoveries  
📊 **Weekly Summaries** - Generate high-level summaries of your weekly progress  
📥 **PDF Export** - Export your entries as a downloadable PDF document  
🗄️ **SQLite Database** - Persistent storage of all entries and summaries  
🎨 **Clean UI** - Simple and intuitive web interface built with Flask and Bootstrap  

## Prerequisites

- Python 3.8 or higher
- Google Generative AI API key (free tier available)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/sasidhar136/CODE_DIARY.git
cd CODE_DIARY
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the project root (use `.env.example` as a template):
```bash
cp .env.example .env
```

Then edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

Get your free API key from [Google AI Studio](https://aistudio.google.com/app/apikeys)

### 5. Run the Application
```bash
python app.py
```

The application will be available at: `http://localhost:10000`

## Project Structure

```
code_diary/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── code_diary.db          # SQLite database (auto-created)
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   ├── input.html         # Entry input page
│   ├── dashboard.html     # Dashboard/list of entries
│   └── weekly_summary.html # Weekly summary page
├── static/                # Static files
│   └── style.css          # Custom CSS styles
└── README.md              # This file
```

## Usage

1. **New Entry**: Click "New Entry" and write about what you learned today
2. **View Dashboard**: See all your entries with AI-generated summaries
3. **Weekly Summary**: Get an overview of the week's learning
4. **Export**: Download your entries as a PDF

## Technologies Used

- **Backend**: Flask, Flask-SQLAlchemy
- **Database**: SQLite
- **AI**: Google Generative AI (Gemini)
- **Frontend**: HTML, CSS, Bootstrap
- **PDF Generation**: FPDF2

## API Configuration

The application uses Google's Generative AI API with the **Gemini 2.0 Flash Lite** model for fast, efficient summarization. The free tier provides:
- 15 requests per minute
- 1,500 requests per day

For higher limits, upgrade to a paid plan in [Google Cloud Console](https://console.cloud.google.com/)

## Troubleshooting

### "GOOGLE_API_KEY not found" Error
- Ensure your `.env` file exists in the project root
- Verify the API key is correctly set in the `.env` file
- Restart the Flask application

### Database Issues
- Delete `code_diary.db` to reset the database
- The database will be recreated on next application start

### Port Already in Use
If port 10000 is busy, modify the port in `app.py`:
```python
app.run(host='0.0.0.0', port=YOUR_PORT, debug=True)
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created by [sasidhar136](https://github.com/sasidhar136)

## Support

For issues, questions, or suggestions, please visit the [GitHub Issues](https://github.com/sasidhar136/CODE_DIARY/issues) page.
