"""
Entry point for running the Code Diary application
"""
import os
from app import create_app

if __name__ == '__main__':
    # Determine environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Create and run app
    app = create_app(env)
    app.run(host='0.0.0.0', port=10000, debug=(env == 'development'))
