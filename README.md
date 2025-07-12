# ReWear - Community Clothing Exchange Platform

ReWear is a sustainable fashion platform that enables users to exchange clothing items using a points-based system and donate to NGOs. The application promotes circular economy principles and environmental consciousness.

## Features

- **Clothing Exchange**: Points-based system for swapping clothing items
- **NGO Donations**: Partner with verified NGOs for clothing donations
- **Environmental Impact**: Track CO₂ savings and earn sustainability badges
- **Location-based**: Find nearby items and NGOs in your city
- **Admin Panel**: Moderation system for quality control

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd rewear
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export DATABASE_URL="your_database_url"
export SESSION_SECRET="your_secret_key"
```

4. Run the application:
```bash
python main.py
```

Or using Gunicorn:
```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Database Setup

The application supports both SQLite (for development) and PostgreSQL (for production).

For PostgreSQL:
```bash
export DATABASE_URL="postgresql://user:password@localhost/rewear"
```

For SQLite (default):
```bash
export DATABASE_URL="sqlite:///rewear.db"
```


## Technology Stack

- **Backend**: Flask, SQLAlchemy, Flask-Login
- **Database**: PostgreSQL/SQLite
- **Frontend**: Jinja2 templates, CSS3, JavaScript
- **Image Processing**: Pillow
- **Forms**: Flask-WTF, WTForms

## Environmental Impact

ReWear tracks real environmental data:
- T-shirt: 2.1 kg CO₂ saved per item
- Jeans: 8.2 kg CO₂ saved per item
- Dress: 3.0 kg CO₂ saved per item

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License
