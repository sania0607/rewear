# Running ReWear Locally

## Quick Start (5 minutes)

### 1. Download the Project
```bash
# If you have git installed
git clone [your-repo-url]
cd rewear

# Or download as ZIP and extract
```

### 2. Install Python
- Download Python 3.11+ from https://python.org/downloads/
- Make sure to check "Add to PATH" during installation

### 3. Install Dependencies
```bash
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms sqlalchemy werkzeug pillow email-validator gunicorn
```

### 4. Populate the Database with Sample Data
```bash
python populate_database.py
```

### 5. Run the Application
```bash
python run.py
```

That's it! Open your browser and go to: **http://localhost:5000**

## Default Login
- Username: `admin`
- Password: `admin123`

## Alternative Methods

### Method 1: Using pyproject.toml (Recommended)
```bash
pip install .
python run.py
```

### Method 2: Using Gunicorn (Production-like)
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

### Method 3: Using Virtual Environment (Best Practice)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms sqlalchemy werkzeug pillow email-validator gunicorn

# Run the app
python run.py
```

## Troubleshooting

### If you get "Module not found" errors:
```bash
pip install --upgrade pip
pip install flask flask-sqlalchemy flask-login flask-wtf wtforms sqlalchemy werkzeug pillow email-validator gunicorn
```

### If port 5000 is busy:
Edit `run.py` and change port to 8000:
```python
app.run(host='0.0.0.0', port=8000, debug=True)
```

### Database Issues:
The app creates a SQLite database automatically. If you have problems:
```bash
# Delete the database file and restart
rm rewear.db
python run.py
```

## What You'll See
- Browse page with 12 sample clothing items
- NGO donation section with 10 authentic Indian organizations
- User profiles with sustainability badges
- Admin panel for managing items

## Development Mode
The app runs in debug mode by default, so:
- Changes to code reload automatically
- Error messages show detailed information
- Database is SQLite (no setup needed)

## Next Steps
- Create your own user account
- Add new clothing items
- Explore the NGO donation features
- Check out the sustainability tracking