from app import db
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import func

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    points = db.Column(db.Integer, default=100)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Location information for filtering
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    
    # Shipping information
    full_name = db.Column(db.String(200))
    address_line1 = db.Column(db.String(200))
    address_line2 = db.Column(db.String(200))
    shipping_city = db.Column(db.String(100))
    shipping_state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    
    # Environmental impact tracking
    total_co2_saved = db.Column(db.Float, default=0.0)  # in kg
    total_items_donated = db.Column(db.Integer, default=0)
    total_items_swapped = db.Column(db.Integer, default=0)
    total_weight_reused = db.Column(db.Float, default=0.0)  # in kg
    
    # Relationships
    items = db.relationship('Item', backref='owner', lazy=True, cascade='all, delete-orphan')
    sent_swaps = db.relationship('Swap', foreign_keys='Swap.sender_id', backref='sender', lazy=True)
    received_swaps = db.relationship('Swap', foreign_keys='Swap.receiver_id', backref='receiver', lazy=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    size = db.Column(db.String(10), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    condition = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.String(500))  # Comma-separated tags
    points_value = db.Column(db.Integer, default=50)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, swapped
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Environmental impact data
    estimated_weight = db.Column(db.Float, default=0.0)  # in kg
    co2_footprint = db.Column(db.Float, default=0.0)  # CO2 saved in kg
    
    # Location information (copied from owner at time of listing)
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    images = db.relationship('ItemImage', backref='item', lazy=True, cascade='all, delete-orphan')
    swaps = db.relationship('Swap', backref='item', lazy=True)
    
    def __repr__(self):
        return f'<Item {self.title}>'
    
    def get_tags_list(self):
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    
    # Foreign keys
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    def __repr__(self):
        return f'<ItemImage {self.filename}>'

class Swap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected, completed, shipped, delivered
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Shipping information
    shipping_method = db.Column(db.String(50))  # mail, pickup, meetup
    tracking_number = db.Column(db.String(100))
    carrier = db.Column(db.String(50))  # usps, fedex, ups, dhl, other
    shipped_at = db.Column(db.DateTime)
    estimated_delivery = db.Column(db.DateTime)
    meetup_location = db.Column(db.String(200))
    pickup_time = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    # Delivery confirmation
    condition_on_arrival = db.Column(db.String(20))  # excellent, good, poor
    exchange_rating = db.Column(db.Integer)  # 1-5 rating
    receiver_feedback = db.Column(db.Text)
    
    # Foreign keys
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    def __repr__(self):
        return f'<Swap {self.id}>'

class PointsTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # earned, spent, bonus
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f'<PointsTransaction {self.amount} {self.type}>'


class NGO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    website = db.Column(db.String(200))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    focus_areas = db.Column(db.String(500))  # Comma-separated: textiles, environment, education, etc.
    
    # Contact preferences
    accepts_donations = db.Column(db.Boolean, default=True)
    pickup_available = db.Column(db.Boolean, default=False)
    drop_off_location = db.Column(db.Text)
    operating_hours = db.Column(db.String(200))
    
    # Social media
    instagram = db.Column(db.String(100))
    facebook = db.Column(db.String(100))
    twitter = db.Column(db.String(100))
    
    # Status and metadata
    verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Location for filtering
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Relationships
    donations = db.relationship('Donation', backref='ngo', lazy=True)
    
    def __repr__(self):
        return f'<NGO {self.name}>'
    
    def get_focus_areas_list(self):
        if self.focus_areas:
            return [area.strip() for area in self.focus_areas.split(',')]
        return []


class Donation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed
    message = db.Column(db.Text)
    items_description = db.Column(db.Text, nullable=False)
    estimated_value = db.Column(db.Integer)  # in points equivalent
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_pickup = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Logistics
    pickup_address = db.Column(db.Text)
    contact_phone = db.Column(db.String(20))
    preferred_contact_method = db.Column(db.String(20))  # email, phone, text
    
    # Relationships
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ngo_id = db.Column(db.Integer, db.ForeignKey('ngo.id'), nullable=False)
    
    def __repr__(self):
        return f'<Donation {self.id}: {self.user_id} -> {self.ngo_id}>'


class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), nullable=False)  # emoji or icon class
    requirement_type = db.Column(db.String(50), nullable=False)  # donated_items, swapped_items, co2_saved, weight_reused
    requirement_value = db.Column(db.Float, nullable=False)
    color = db.Column(db.String(20), default='#4caf50')
    
    # Relationships
    user_badges = db.relationship('UserBadge', backref='badge', lazy=True)
    
    def __repr__(self):
        return f'<Badge {self.name}>'


class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_id = db.Column(db.Integer, db.ForeignKey('badge.id'), nullable=False)
    
    # Prevent duplicate badges for same user
    __table_args__ = (db.UniqueConstraint('user_id', 'badge_id', name='unique_user_badge'),)
    
    def __repr__(self):
        return f'<UserBadge {self.user_id}: {self.badge_id}>'


class CarbonFootprint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(50), nullable=False)  # swap, donation, reuse
    co2_saved = db.Column(db.Float, nullable=False)  # in kg
    item_weight = db.Column(db.Float, nullable=False)  # in kg
    item_category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=True)  # null for donations
    
    def __repr__(self):
        return f'<CarbonFootprint {self.user_id}: {self.co2_saved}kg CO2>'
