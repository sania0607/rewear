# Carbon Footprint and Sustainability Tracking Utils

# Real CO2 emission factors for textile production (kg CO2 per item)
CARBON_FOOTPRINTS = {
    'tops': {
        'tshirt': 2.1,
        'shirt': 2.8,
        'blouse': 2.5,
        'sweater': 5.2,
        'hoodie': 4.8,
        'jacket': 6.5,
        'default': 3.0
    },
    'bottoms': {
        'jeans': 8.2,  # Denim is carbon-intensive
        'pants': 4.1,
        'shorts': 2.8,
        'skirt': 2.9,
        'leggings': 3.2,
        'default': 4.0
    },
    'dresses': {
        'casual': 4.5,
        'formal': 7.2,
        'wedding': 12.0,
        'default': 5.5
    },
    'outerwear': {
        'coat': 8.5,
        'jacket': 6.5,
        'blazer': 5.8,
        'cardigan': 4.2,
        'default': 6.0
    },
    'shoes': {
        'sneakers': 11.9,
        'boots': 14.2,
        'heels': 9.8,
        'sandals': 6.5,
        'default': 10.0
    },
    'accessories': {
        'bag': 3.8,
        'belt': 1.2,
        'scarf': 2.1,
        'hat': 1.8,
        'jewelry': 0.8,
        'default': 2.0
    },
    'bags': {
        'backpack': 5.2,
        'handbag': 4.1,
        'tote': 3.8,
        'clutch': 2.5,
        'default': 4.0
    },
    'jewelry': {
        'necklace': 0.9,
        'bracelet': 0.6,
        'earrings': 0.4,
        'ring': 0.3,
        'default': 0.6
    }
}

# Average weights for different item types (kg)
ITEM_WEIGHTS = {
    'tops': {
        'tshirt': 0.15,
        'shirt': 0.2,
        'blouse': 0.18,
        'sweater': 0.4,
        'hoodie': 0.5,
        'jacket': 0.8,
        'default': 0.3
    },
    'bottoms': {
        'jeans': 0.6,
        'pants': 0.4,
        'shorts': 0.25,
        'skirt': 0.3,
        'leggings': 0.2,
        'default': 0.35
    },
    'dresses': {
        'casual': 0.35,
        'formal': 0.6,
        'wedding': 1.2,
        'default': 0.45
    },
    'outerwear': {
        'coat': 1.2,
        'jacket': 0.8,
        'blazer': 0.7,
        'cardigan': 0.5,
        'default': 0.8
    },
    'shoes': {
        'sneakers': 0.8,
        'boots': 1.2,
        'heels': 0.6,
        'sandals': 0.4,
        'default': 0.7
    },
    'accessories': {
        'bag': 0.3,
        'belt': 0.15,
        'scarf': 0.1,
        'hat': 0.12,
        'jewelry': 0.05,
        'default': 0.15
    },
    'bags': {
        'backpack': 0.6,
        'handbag': 0.4,
        'tote': 0.3,
        'clutch': 0.2,
        'default': 0.4
    },
    'jewelry': {
        'necklace': 0.08,
        'bracelet': 0.05,
        'earrings': 0.03,
        'ring': 0.02,
        'default': 0.05
    }
}

def calculate_carbon_footprint(category, item_type=None, title=None):
    """Calculate CO2 footprint for an item based on category and type"""
    category = category.lower()
    
    if category not in CARBON_FOOTPRINTS:
        return 3.0  # Default fallback
    
    category_data = CARBON_FOOTPRINTS[category]
    
    # Try to determine item type from title if not provided
    if not item_type and title:
        title_lower = title.lower()
        for key in category_data.keys():
            if key != 'default' and key in title_lower:
                item_type = key
                break
    
    # Get CO2 footprint
    if item_type and item_type.lower() in category_data:
        return category_data[item_type.lower()]
    else:
        return category_data['default']

def calculate_item_weight(category, item_type=None, title=None):
    """Calculate estimated weight for an item based on category and type"""
    category = category.lower()
    
    if category not in ITEM_WEIGHTS:
        return 0.3  # Default fallback
    
    category_data = ITEM_WEIGHTS[category]
    
    # Try to determine item type from title if not provided
    if not item_type and title:
        title_lower = title.lower()
        for key in category_data.keys():
            if key != 'default' and key in title_lower:
                item_type = key
                break
    
    # Get weight
    if item_type and item_type.lower() in category_data:
        return category_data[item_type.lower()]
    else:
        return category_data['default']

def get_sustainability_message(co2_saved, items_count):
    """Generate motivational message about environmental impact"""
    if co2_saved < 5:
        return f"🌱 Great start! You've saved {co2_saved:.1f} kg of CO₂ with {items_count} item{'s' if items_count != 1 else ''}!"
    elif co2_saved < 20:
        return f"🌿 Amazing progress! You've prevented {co2_saved:.1f} kg of CO₂ emissions by reusing {items_count} item{'s' if items_count != 1 else ''}!"
    elif co2_saved < 50:
        return f"🌳 Fantastic impact! You've saved {co2_saved:.1f} kg of CO₂ - equivalent to driving {co2_saved * 4.6:.0f} km less!"
    else:
        return f"🌍 Incredible eco-warrior! You've prevented {co2_saved:.1f} kg of CO₂ emissions - that's like planting {co2_saved / 22:.0f} trees!"

def check_badge_eligibility(user):
    """Check if user is eligible for any new badges"""
    from models import Badge, UserBadge
    
    # Get all badges user doesn't have yet
    earned_badge_ids = [ub.badge_id for ub in user.badges]
    available_badges = Badge.query.filter(~Badge.id.in_(earned_badge_ids)).all()
    
    newly_earned = []
    
    for badge in available_badges:
        if badge.requirement_type == 'donated_items' and user.total_items_donated >= badge.requirement_value:
            newly_earned.append(badge)
        elif badge.requirement_type == 'swapped_items' and user.total_items_swapped >= badge.requirement_value:
            newly_earned.append(badge)
        elif badge.requirement_type == 'co2_saved' and user.total_co2_saved >= badge.requirement_value:
            newly_earned.append(badge)
        elif badge.requirement_type == 'weight_reused' and user.total_weight_reused >= badge.requirement_value:
            newly_earned.append(badge)
    
    return newly_earned

def award_badges(user, newly_earned_badges):
    """Award new badges to user"""
    from app import db
    from models import UserBadge
    
    for badge in newly_earned_badges:
        user_badge = UserBadge(user_id=user.id, badge_id=badge.id)
        db.session.add(user_badge)
    
    if newly_earned_badges:
        db.session.commit()
    
    return newly_earned_badges

def update_user_stats(user, action_type, item_weight, co2_saved):
    """Update user's environmental impact statistics"""
    from app import db
    
    user.total_co2_saved += co2_saved
    user.total_weight_reused += item_weight
    
    if action_type == 'donation':
        user.total_items_donated += 1
    elif action_type == 'swap':
        user.total_items_swapped += 1
    
    db.session.commit()
    
    # Check and award badges
    newly_earned = check_badge_eligibility(user)
    if newly_earned:
        award_badges(user, newly_earned)
    
    return newly_earned

def create_carbon_record(user_id, action_type, co2_saved, item_weight, item_category, item_id=None):
    """Create a carbon footprint tracking record"""
    from app import db
    from models import CarbonFootprint
    
    record = CarbonFootprint(
        user_id=user_id,
        action_type=action_type,
        co2_saved=co2_saved,
        item_weight=item_weight,
        item_category=item_category,
        item_id=item_id
    )
    
    db.session.add(record)
    db.session.commit()
    
    return record