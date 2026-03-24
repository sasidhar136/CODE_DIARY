# Code Diary Project Structure

## Overview
This is a professional Flask application for tracking daily coding learning. The project follows a modular architecture for better maintainability and scalability.

## Project Structure

```
code_diary/
├── app/                          # Main application package
│   ├── __init__.py              # Flask app factory
│   ├── models.py                # Database models (Entry model)
│   ├── routes/                  # Application blueprints/routes
│   │   ├── __init__.py          # Blueprint initialization
│   │   ├── main.py              # Main routes (index, dashboard)
│   │   ├── entries.py           # Entry management routes
│   │   └── export.py            # Export functionality (PDF)
│   ├── utils/                   # Utility modules
│   │   ├── __init__.py
│   │   └── ai_summary.py        # AI summarization using Google Generative AI
│   ├── templates/               # Jinja2 HTML templates
│   │   ├── base.html            # Base template
│   │   ├── input.html           # New entry form
│   │   ├── dashboard.html       # Dashboard view
│   │   └── weekly_summary.html  # Weekly summary
│   └── static/                  # Static files
│       ├── css/
│       │   └── style.css        # Styling
│       └── js/                  # JavaScript (future)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   └── test_gemini.py          # API testing script
│
├── scripts/                     # Utility scripts
│   └── list_gemini_models.py   # List available Gemini models
│
├── venv/                        # Virtual environment
├── instance/                    # Instance folder (database, secrets)
├── config.py                    # Configuration settings
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── .env                         # Local environment (Git ignored)
├── .gitignore                   # Git ignore rules
├── README.md                    # Project documentation
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # License
└── list_gemini_models.py        # ⚠️ DEPRECATED - use scripts/list_gemini_models.py

```

## Key Features

✨ **Modular Flask Architecture** - Clean separation of concerns with blueprints
🤖 **AI-Powered Summaries** - Automatic summarization using Google Generative AI
📊 **Dashboard** - Track your learning progress
📅 **Weekly Summaries** - Consolidated weekly learning overview
📄 **PDF Export** - Export all entries as PDF
🎨 **Modern UI** - Responsive design with Bootstrap 5

## Setup Instructions

### Prerequisites
- Python 3.8+
- Virtual environment (`venv`)
- Google API Key (for AI features)

### Installation

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # On Windows
   # or
   source venv/bin/activate      # On macOS/Linux
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```

   The app will be available at: `http://localhost:10000`

## Development Guide

### Adding New Routes

1. Create a new file in `app/routes/` (e.g., `app/routes/analytics.py`)
2. Define your blueprint and routes
3. Register in `app/routes/__init__.py`:
   ```python
   from app.routes import analytics_bp
   app.register_blueprint(analytics_bp)
   ```

### Adding New Models

1. Edit `app/models.py` and add your model class
2. Models automatically inherit from `db.Model`
3. Run `db.create_all()` in app context (done automatically on startup)

### Adding Utilities

1. Create module in `app/utils/`
2. Import in relevant routes or models

### Environment Configuration

Edit `config.py` to manage different environments:
- **Development** - Debug mode enabled, development database
- **Production** - Debug mode disabled
- **Testing** - In-memory SQLite for tests

## Database Schema

### Entry Model
```
id (Integer, Primary Key)
content (Text) - Learning entry content
timestamp (DateTime) - When entry was created
summary (Text) - AI-generated summary
```

## Scripts

### List Available Gemini Models
```bash
python scripts/list_gemini_models.py
```

### Test Gemini API Connection
```bash
python tests/test_gemini.py
```

## API Reference

### Routes Structure
- **Prefix**: None for main routes, `/entries` for entry routes, `/export` for export routes
- All routes return HTML (Jinja2 templates)

### Main Routes (`app.routes.main`)
- `GET /` → Redirect to new entry
- `GET /dashboard` → Show dashboard

### Entry Routes (`app.routes.entries`)
- `GET /entries/new` → Show new entry form
- `POST /entries/add` → Save new entry
- `POST /entries/clear` → Delete all entries
- `GET /entries/weekly-summary` → Show weekly summary

### Export Routes (`app.routes.export`)
- `GET /export/pdf` → Download all entries as PDF

## Troubleshooting

### "localhost refused to connect"
- Make sure the server is running: `python run.py`
- Check port 10000 is not in use

### API Key not found
- Check `.env` file exists and has `GOOGLE_API_KEY` set
- Restart the application after changing `.env`

### Database errors
- Delete `instance/code_diary.db` to reset database
- Restart the application

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

See [LICENSE](LICENSE) for details.

## Future Enhancements

- 🔍 Search functionality
- 🏷️ Tags/Categories support
- 📈 Learning analytics
- ☁️ Cloud storage integration
- 📱 Mobile app
