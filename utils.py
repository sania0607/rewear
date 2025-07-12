import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file, item_id):
    """Save and resize uploaded image"""
    if not image_file or not allowed_file(image_file.filename):
        return None
    
    # Generate unique filename
    filename = secure_filename(image_file.filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{item_id}_{uuid.uuid4().hex}{ext}"
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save original image
    image_path = os.path.join(upload_dir, unique_filename)
    image_file.save(image_path)
    
    # Resize image
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize to max 800x800 while maintaining aspect ratio
            img.thumbnail((800, 800), Image.Resampling.LANCZOS)
            img.save(image_path, 'JPEG', quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")
        # If resize fails, keep original
        pass
    
    return unique_filename

def get_category_icon(category):
    """Get FontAwesome icon for category"""
    icons = {
        'tops': 'fas fa-tshirt',
        'bottoms': 'fas fa-shoe-prints',
        'dresses': 'fas fa-female',
        'outerwear': 'fas fa-coat',
        'shoes': 'fas fa-shoe-prints',
        'accessories': 'fas fa-gem',
        'bags': 'fas fa-shopping-bag',
        'jewelry': 'fas fa-ring'
    }
    return icons.get(category, 'fas fa-tag')

def get_condition_color(condition):
    """Get color class for condition"""
    colors = {
        'new': 'text-green-400',
        'excellent': 'text-blue-400',
        'good': 'text-yellow-400',
        'fair': 'text-orange-400'
    }
    return colors.get(condition, 'text-gray-400')
