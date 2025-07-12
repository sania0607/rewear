#!/usr/bin/env python3
"""
Populate the database with sample data
Run this script to add sample items and NGOs to your local database
"""

import os
from datetime import datetime
from werkzeug.security import generate_password_hash


# Only set defaults if not already set (so Render stays untouched)
os.environ.setdefault('DATABASE_URL', 'sqlite:///rewear.db')
os.environ.setdefault('SESSION_SECRET', 'dev-secret-key-change-in-production')


from app import app, db
from models import User, Item, ItemImage, NGO, Donation, Badge, UserBadge, CarbonFootprint

def populate_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        
        print("Creating sample users...")
        
        # Create sample users
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@rewear.com',
                'password': 'admin123',
                'points': 500,
                'is_admin': True,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400001'
            },
            {
                'username': 'priya_mumbai',
                'email': 'priya@gmail.com',
                'password': 'password123',
                'points': 320,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400020'
            },
            {
                'username': 'arjun_delhi',
                'email': 'arjun@gmail.com',
                'password': 'password123',
                'points': 280,
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001'
            },
            {
                'username': 'sneha_bangalore',
                'email': 'sneha@gmail.com',
                'password': 'password123',
                'points': 250,
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001'
            },
            {
                'username': 'rahul_chennai',
                'email': 'rahul@gmail.com',
                'password': 'password123',
                'points': 180,
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600001'
            },
            {
                'username': 'kavya_pune',
                'email': 'kavya@gmail.com',
                'password': 'password123',
                'points': 220,
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411001'
            }
        ]
        
        for user_data in users_data:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    points=user_data['points'],
                    is_admin=user_data.get('is_admin', False),
                    city=user_data['city'],
                    state=user_data['state'],
                    pincode=user_data['pincode']
                )
                db.session.add(user)
        
        db.session.commit()
        print("Sample users created!")
        
        print("Creating sample items...")
        
        # Create sample items
        items_data = [
            {
                'title': 'Elegant Silk Saree',
                'description': 'Beautiful handwoven silk saree in deep maroon with gold border. Perfect for festivals and special occasions.',
                'size': 'M',
                'category': 'dresses',
                'condition': 'excellent',
                'tags': 'silk, traditional, indian, festival, wedding',
                'points_value': 180,
                'status': 'approved',
                'user_id': 2,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400020'
            },
            {
                'title': 'Cotton Kurti with Palazzo Set',
                'description': 'Comfortable cotton kurti with matching palazzo pants. Great for daily wear and office.',
                'size': 'L',
                'category': 'tops',
                'condition': 'good',
                'tags': 'cotton, kurti, palazzo, comfortable, office',
                'points_value': 120,
                'status': 'approved',
                'user_id': 3,
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001'
            },
            {
                'title': 'Denim Jacket - Vintage Style',
                'description': 'Classic denim jacket with vintage wash. Perfect for layering in cooler weather.',
                'size': 'M',
                'category': 'outerwear',
                'condition': 'good',
                'tags': 'denim, jacket, vintage, casual, layering',
                'points_value': 95,
                'status': 'approved',
                'user_id': 2,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400020'
            },
            {
                'title': 'Formal White Shirt',
                'description': 'Crisp white formal shirt, barely used. Perfect for office meetings and professional events.',
                'size': 'L',
                'category': 'tops',
                'condition': 'excellent',
                'tags': 'formal, white, shirt, office, professional',
                'points_value': 85,
                'status': 'approved',
                'user_id': 4,
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001'
            },
            {
                'title': 'Floral Summer Dress',
                'description': 'Light and breezy floral print dress, perfect for summer outings and brunches.',
                'size': 'S',
                'category': 'dresses',
                'condition': 'good',
                'tags': 'floral, summer, dress, light, brunch',
                'points_value': 110,
                'status': 'approved',
                'user_id': 5,
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600001'
            },
            {
                'title': 'Palazzo Pants - Navy Blue',
                'description': 'Comfortable navy blue palazzo pants with elastic waistband. Great for comfort and style.',
                'size': 'M',
                'category': 'bottoms',
                'condition': 'excellent',
                'tags': 'palazzo, navy, comfortable, elastic, style',
                'points_value': 75,
                'status': 'approved',
                'user_id': 6,
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411001'
            },
            {
                'title': 'Leather Handbag - Brown',
                'description': 'Genuine leather handbag in rich brown color. Multiple compartments for organization.',
                'size': 'M',
                'category': 'bags',
                'condition': 'good',
                'tags': 'leather, handbag, brown, genuine, compartments',
                'points_value': 160,
                'status': 'approved',
                'user_id': 3,
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001'
            },
            {
                'title': 'White Sneakers',
                'description': 'Clean white sneakers, lightly used. Comfortable for walking and casual wear.',
                'size': 'L',
                'category': 'shoes',
                'condition': 'good',
                'tags': 'sneakers, white, comfortable, walking, casual',
                'points_value': 90,
                'status': 'approved',
                'user_id': 2,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'pincode': '400020'
            },
            {
                'title': 'Silver Jhumka Earrings',
                'description': 'Traditional silver jhumka earrings with intricate design. Perfect for ethnic wear.',
                'size': 'S',
                'category': 'jewelry',
                'condition': 'excellent',
                'tags': 'silver, jhumka, earrings, traditional, ethnic',
                'points_value': 65,
                'status': 'approved',
                'user_id': 4,
                'city': 'Bangalore',
                'state': 'Karnataka',
                'pincode': '560001'
            },
            {
                'title': 'Black Formal Blazer',
                'description': 'Sharp black blazer for formal occasions. Well-tailored and professional look.',
                'size': 'L',
                'category': 'outerwear',
                'condition': 'excellent',
                'tags': 'blazer, black, formal, professional, tailored',
                'points_value': 140,
                'status': 'approved',
                'user_id': 5,
                'city': 'Chennai',
                'state': 'Tamil Nadu',
                'pincode': '600001'
            },
            {
                'title': 'Silk Scarf - Floral Print',
                'description': 'Elegant silk scarf with beautiful floral print. Can be worn multiple ways.',
                'size': 'S',
                'category': 'accessories',
                'condition': 'new',
                'tags': 'silk, scarf, floral, elegant, versatile',
                'points_value': 55,
                'status': 'approved',
                'user_id': 6,
                'city': 'Pune',
                'state': 'Maharashtra',
                'pincode': '411001'
            },
            {
                'title': 'Blue Jeans - Skinny Fit',
                'description': 'Classic blue jeans in skinny fit. Comfortable stretch fabric, perfect for daily wear.',
                'size': 'M',
                'category': 'bottoms',
                'condition': 'good',
                'tags': 'jeans, blue, skinny, stretch, daily',
                'points_value': 100,
                'status': 'approved',
                'user_id': 3,
                'city': 'Delhi',
                'state': 'Delhi',
                'pincode': '110001'
            }
        ]
        
        for item_data in items_data:
            if not Item.query.filter_by(title=item_data['title']).first():
                item = Item(**item_data)
                db.session.add(item)
        
        db.session.commit()
        print("Sample items created!")
        
        print("Creating sample NGOs...")
        
        # Create sample NGOs
        ngos_data = [
            {
                'name': 'Goonj',
                'description': 'Goonj is a non-governmental organization that undertakes disaster relief, humanitarian aid and community development in rural India.',
                'website': 'https://goonj.org',
                'email': 'info@goonj.org',
                'phone': '+91-11-26972351',
                'address': 'R-195A, Raj Nagar-II, Palam Colony, New Delhi-110077',
                'focus_areas': 'disaster relief, rural development, textile reuse, education',
                'accepts_donations': True,
                'pickup_available': True,
                'drop_off_location': 'Multiple locations across Delhi NCR',
                'operating_hours': 'Mon-Sat: 10:00 AM - 6:00 PM',
                'instagram': 'goonj_official',
                'facebook': 'GonjOfficial',
                'twitter': 'goonj_official',
                'verified': True,
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India'
            },
            {
                'name': 'Pratham',
                'description': 'Pratham is one of the largest non-governmental organizations in India, working to provide quality education to underprivileged children.',
                'website': 'https://pratham.org',
                'email': 'info@pratham.org',
                'phone': '+91-22-26732439',
                'address': 'A-8, Sector-26, Noida-201301, Uttar Pradesh',
                'focus_areas': 'education, children, literacy, vocational training',
                'accepts_donations': True,
                'pickup_available': True,
                'drop_off_location': 'Pratham centers across Mumbai and Delhi',
                'operating_hours': 'Mon-Fri: 9:00 AM - 6:00 PM',
                'instagram': 'pratham_education',
                'facebook': 'PrathamEducation',
                'twitter': 'Pratham_Edu',
                'verified': True,
                'city': 'Mumbai',
                'state': 'Maharashtra',
                'country': 'India'
            },
            {
                'name': 'Oxfam India',
                'description': 'Oxfam India is committed to creating a more equal world by fighting inequality and injustice.',
                'website': 'https://oxfamindia.org',
                'email': 'info@oxfamindia.org',
                'phone': '+91-11-4653-8000',
                'address': '4th and 5th Floor, Shriram Bhartiya Kala Kendra, 1, Copernicus Marg, New Delhi-110001',
                'focus_areas': 'poverty alleviation, gender equality, disaster response, livelihoods',
                'accepts_donations': True,
                'pickup_available': False,
                'drop_off_location': 'Oxfam office in New Delhi',
                'operating_hours': 'Mon-Fri: 9:30 AM - 6:00 PM',
                'instagram': 'oxfam_india',
                'facebook': 'OxfamIndia',
                'twitter': 'OxfamIndia',
                'verified': True,
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India'
            },
            {
                'name': 'Smile Foundation',
                'description': 'Smile Foundation is a national level development organization directly benefiting over 1.5 million children and families every year.',
                'website': 'https://smilefoundationindia.org',
                'email': 'info@smilefoundationindia.org',
                'phone': '+91-11-43123700',
                'address': 'Smile Foundation, 2nd Floor, Lado Sarai, New Delhi-110030',
                'focus_areas': 'child welfare, education, healthcare, women empowerment',
                'accepts_donations': True,
                'pickup_available': True,
                'drop_off_location': 'Smile Foundation centers',
                'operating_hours': 'Mon-Sat: 10:00 AM - 7:00 PM',
                'instagram': 'smilefoundation_india',
                'facebook': 'SmileFoundationIndia',
                'twitter': 'SmileFoundationIndia',
                'verified': True,
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India'
            },
            {
                'name': 'HelpAge India',
                'description': 'HelpAge India is a leading charity in India working with and for disadvantaged elderly for nearly 4 decades.',
                'website': 'https://helpage.org',
                'email': 'info@helpage.org',
                'phone': '+91-11-41688955',
                'address': 'C-14, Qutab Institutional Area, New Delhi-110016',
                'focus_areas': 'elderly care, healthcare, disaster response, livelihood',
                'accepts_donations': True,
                'pickup_available': True,
                'drop_off_location': 'HelpAge centers across India',
                'operating_hours': 'Mon-Fri: 9:00 AM - 6:00 PM',
                'instagram': 'helpageindia',
                'facebook': 'HelpAgeIndia',
                'twitter': 'HelpAgeIndia',
                'verified': True,
                'city': 'Delhi',
                'state': 'Delhi',
                'country': 'India'
            },
            {
                'name': 'Akshaya Patra Foundation',
                'description': 'The Akshaya Patra Foundation is a non-profit organization that feeds over 1.8 million children every day in India.',
                'website': 'https://akshayapatra.org',
                'email': 'info@akshayapatra.org',
                'phone': '+91-80-30143400',
                'address': 'The Akshaya Patra Foundation, Vasanthapura, Bangalore-560082',
                'focus_areas': 'child nutrition, education, mid-day meals, rural development',
                'accepts_donations': True,
                'pickup_available': False,
                'drop_off_location': 'Akshaya Patra kitchen locations',
                'operating_hours': 'Mon-Sat: 8:00 AM - 6:00 PM',
                'instagram': 'theakshayapatra',
                'facebook': 'AkshayaPatra',
                'twitter': 'AkshayaPatra',
                'verified': True,
                'city': 'Bangalore',
                'state': 'Karnataka',
                'country': 'India'
            }
        ]
        
        for ngo_data in ngos_data:
            if not NGO.query.filter_by(name=ngo_data['name']).first():
                ngo = NGO(**ngo_data)
                db.session.add(ngo)
        
        db.session.commit()
        print("Sample NGOs created!")
        
        print("Creating sustainability badges...")
        
        # Create badges
        badges_data = [
            {
                'name': 'Eco Warrior',
                'description': 'Saved 10 kg of CO₂ through sustainable actions',
                'icon': '🌱',
                'requirement_type': 'co2_saved',
                'requirement_value': 10.0,
                'color': '#4CAF50'
            },
            {
                'name': 'Green Champion',
                'description': 'Saved 25 kg of CO₂ through eco-friendly choices',
                'icon': '🌿',
                'requirement_type': 'co2_saved',
                'requirement_value': 25.0,
                'color': '#2E7D32'
            },
            {
                'name': 'First Step',
                'description': 'Completed your first eco-friendly action',
                'icon': '👟',
                'requirement_type': 'co2_saved',
                'requirement_value': 1.0,
                'color': '#607D8B'
            },
            {
                'name': 'Donation Star',
                'description': 'Donated 5 items to help communities',
                'icon': '⭐',
                'requirement_type': 'donated_items',
                'requirement_value': 5,
                'color': '#FF9800'
            },
            {
                'name': 'Swap Master',
                'description': 'Completed 10 successful clothing swaps',
                'icon': '🔄',
                'requirement_type': 'swapped_items',
                'requirement_value': 10,
                'color': '#2196F3'
            }
        ]
        
        for badge_data in badges_data:
            if not Badge.query.filter_by(name=badge_data['name']).first():
                badge = Badge(**badge_data)
                db.session.add(badge)
        
        db.session.commit()
        print("Sustainability badges created!")
        
        print("Database populated successfully!")
        print("\nYou can now:")
        print("- Login with admin/admin123 for admin access")
        print("- Browse 12 sample clothing items")
        print("- Explore 6 authentic Indian NGOs")
        print("- See sustainability badges and tracking")
        print("- Register new accounts and test the platform")

if __name__ == '__main__':
    populate_database()