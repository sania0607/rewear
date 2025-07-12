import os
import uuid
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from PIL import Image
from app import app, db
from models import User, Item, ItemImage, Swap, PointsTransaction, NGO, Donation
from forms import LoginForm, RegisterForm, AddItemForm, SwapRequestForm, AdminActionForm, ShippingAddressForm, ShippingInfoForm, DeliveryConfirmationForm, DonationForm, NGOFilterForm
from utils import save_image, allowed_file

@app.route('/')
def index():
    # Get featured items (latest approved items)
    featured_items = Item.query.filter_by(status='approved').order_by(Item.created_at.desc()).limit(6).all()
    return render_template('index.html', featured_items=featured_items)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('Username or email already exists', 'error')
        else:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password_hash=generate_password_hash(form.password.data),
                city=form.city.data,
                state=form.state.data,
                pincode=form.pincode.data
            )
            db.session.add(user)
            db.session.commit()
            
            # Add welcome points
            transaction = PointsTransaction(
                user_id=user.id,
                amount=100,
                type='bonus',
                description='Welcome bonus'
            )
            db.session.add(transaction)
            db.session.commit()
            
            flash('Registration successful! Welcome to ReWear!', 'success')
            login_user(user)
            return redirect(url_for('dashboard'))
    
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    from carbon_utils import get_sustainability_message
    from models import UserBadge
    
    # Get user's items
    user_items = Item.query.filter_by(user_id=current_user.id).order_by(Item.created_at.desc()).all()
    
    # Get pending swaps
    pending_swaps = Swap.query.filter_by(receiver_id=current_user.id, status='pending').all()
    
    # Get sent swaps
    sent_swaps = Swap.query.filter_by(sender_id=current_user.id).order_by(Swap.created_at.desc()).limit(5).all()
    
    # Get recent transactions
    recent_transactions = PointsTransaction.query.filter_by(user_id=current_user.id).order_by(PointsTransaction.created_at.desc()).limit(5).all()
    
    # Get user's badges
    user_badges = UserBadge.query.filter_by(user_id=current_user.id).order_by(UserBadge.earned_at.desc()).all()
    
    # Calculate total impact
    total_items = current_user.total_items_swapped + current_user.total_items_donated
    sustainability_message = get_sustainability_message(current_user.total_co2_saved, total_items)
    
    return render_template('dashboard.html', 
                         user_items=user_items,
                         pending_swaps=pending_swaps,
                         sent_swaps=sent_swaps,
                         recent_transactions=recent_transactions,
                         user_badges=user_badges,
                         sustainability_message=sustainability_message)

@app.route('/add_item', methods=['GET', 'POST'])
@login_required
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        # Create item with owner's location
        item = Item(
            title=form.title.data,
            description=form.description.data,
            size=form.size.data,
            category=form.category.data,
            condition=form.condition.data,
            tags=form.tags.data,
            points_value=form.points_value.data,
            user_id=current_user.id,
            city=current_user.city,
            state=current_user.state,
            pincode=current_user.pincode
        )
        
        # Calculate environmental impact
        from carbon_utils import calculate_carbon_footprint, calculate_item_weight
        item.co2_footprint = calculate_carbon_footprint(item.category, title=item.title)
        item.estimated_weight = calculate_item_weight(item.category, title=item.title)
        
        db.session.add(item)
        db.session.flush()  # Get the item ID
        
        # Handle image upload
        if form.images.data:
            filename = save_image(form.images.data, item.id)
            if filename:
                item_image = ItemImage(
                    filename=filename,
                    item_id=item.id,
                    is_primary=True
                )
                db.session.add(item_image)
        
        db.session.commit()
        flash('Item added successfully! It\'s pending admin approval.', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_item.html', form=form)

@app.route('/browse')
def browse():
    # Get filter parameters
    category = request.args.get('category')
    size = request.args.get('size')
    condition = request.args.get('condition')
    search = request.args.get('search')
    location_filter = request.args.get('location_filter')  # all, city, pincode
    new_only = request.args.get('new_only')  # checkbox
    local_only = request.args.get('local_only')  # checkbox
    
    # Build query
    query = Item.query.filter_by(status='approved')
    
    if category:
        query = query.filter_by(category=category)
    if size:
        query = query.filter_by(size=size)
    if condition:
        query = query.filter_by(condition=condition)
    if search:
        query = query.filter(Item.title.contains(search) | Item.description.contains(search))
    
    # New items only filter
    if new_only:
        query = query.filter_by(condition='new')
    
    # Local pickup filter (items from user's city)
    if local_only and current_user.is_authenticated and current_user.city:
        query = query.filter_by(city=current_user.city)
    
    # Location-based filtering
    if current_user.is_authenticated and location_filter:
        if location_filter == 'city' and current_user.city:
            query = query.filter_by(city=current_user.city)
        elif location_filter == 'pincode' and current_user.pincode:
            query = query.filter_by(pincode=current_user.pincode)
    
    items = query.order_by(Item.created_at.desc()).all()
    
    return render_template('browse.html', items=items, 
                         current_category=category,
                         current_size=size,
                         current_condition=condition,
                         current_search=search,
                         current_location_filter=location_filter)

@app.route('/item/<int:item_id>')
def item_detail(item_id):
    item = Item.query.get_or_404(item_id)
    if item.status != 'approved' and (not current_user.is_authenticated or item.user_id != current_user.id):
        flash('Item not found', 'error')
        return redirect(url_for('browse'))
    
    # Get related items
    related_items = Item.query.filter(
        Item.category == item.category,
        Item.id != item.id,
        Item.status == 'approved'
    ).limit(4).all()
    
    form = SwapRequestForm()
    return render_template('item_detail.html', item=item, related_items=related_items, form=form)

@app.route('/swap_request/<int:item_id>', methods=['POST'])
@login_required
def swap_request(item_id):
    item = Item.query.get_or_404(item_id)
    
    if item.user_id == current_user.id:
        flash('You cannot swap with yourself', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    if item.status != 'approved':
        flash('Item is not available for swap', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    # Check if swap already exists
    existing_swap = Swap.query.filter_by(
        sender_id=current_user.id,
        item_id=item_id,
        status='pending'
    ).first()
    
    if existing_swap:
        flash('You already have a pending swap request for this item', 'warning')
        return redirect(url_for('item_detail', item_id=item_id))
    
    form = SwapRequestForm()
    if form.validate_on_submit():
        swap = Swap(
            sender_id=current_user.id,
            receiver_id=item.user_id,
            item_id=item_id,
            message=form.message.data
        )
        db.session.add(swap)
        db.session.commit()
        
        flash('Swap request sent successfully!', 'success')
        return redirect(url_for('item_detail', item_id=item_id))
    
    return redirect(url_for('item_detail', item_id=item_id))

@app.route('/redeem_item/<int:item_id>')
@login_required
def redeem_item(item_id):
    item = Item.query.get_or_404(item_id)
    
    if item.user_id == current_user.id:
        flash('You cannot redeem your own item', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    if item.status != 'approved':
        flash('Item is not available for redemption', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    if current_user.points < item.points_value:
        flash('You don\'t have enough points to redeem this item', 'error')
        return redirect(url_for('item_detail', item_id=item_id))
    
    # Process redemption
    current_user.points -= item.points_value
    item.status = 'swapped'
    
    # Add points to item owner
    item.owner.points += item.points_value
    
    # Create transactions
    buyer_transaction = PointsTransaction(
        user_id=current_user.id,
        amount=-item.points_value,
        type='spent',
        description=f'Redeemed: {item.title}'
    )
    seller_transaction = PointsTransaction(
        user_id=item.user_id,
        amount=item.points_value,
        type='earned',
        description=f'Sold: {item.title}'
    )
    
    db.session.add(buyer_transaction)
    db.session.add(seller_transaction)
    db.session.commit()
    
    flash('Item redeemed successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/swap_action/<int:swap_id>/<action>')
@login_required
def swap_action(swap_id, action):
    swap = Swap.query.get_or_404(swap_id)
    
    if swap.receiver_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))
    
    if action == 'accept':
        swap.status = 'accepted'
        swap.item.status = 'swapped'
        
        # Award points to both users
        swap.sender.points += 25
        swap.receiver.points += 25
        
        # Track environmental impact for both users
        from carbon_utils import update_user_stats, create_carbon_record
        
        # Update environmental stats for both users
        newly_earned_sender = update_user_stats(
            swap.sender, 'swap', swap.item.estimated_weight, swap.item.co2_footprint
        )
        newly_earned_receiver = update_user_stats(
            swap.receiver, 'swap', swap.item.estimated_weight, swap.item.co2_footprint
        )
        
        # Create carbon tracking records
        create_carbon_record(
            swap.sender_id, 'swap', swap.item.co2_footprint, 
            swap.item.estimated_weight, swap.item.category, swap.item.id
        )
        create_carbon_record(
            swap.receiver_id, 'swap', swap.item.co2_footprint, 
            swap.item.estimated_weight, swap.item.category, swap.item.id
        )
        
        # Create transactions
        sender_transaction = PointsTransaction(
            user_id=swap.sender_id,
            amount=25,
            type='earned',
            description=f'Swap completed: {swap.item.title}'
        )
        receiver_transaction = PointsTransaction(
            user_id=swap.receiver_id,
            amount=25,
            type='earned',
            description=f'Swap completed: {swap.item.title}'
        )
        
        db.session.add(sender_transaction)
        db.session.add(receiver_transaction)
        
        # Check for new badges
        badge_message = ""
        if newly_earned_sender:
            badge_message += f" You earned {len(newly_earned_sender)} new badge(s)!"
        
        flash(f'Swap accepted successfully! You saved {swap.item.co2_footprint:.1f} kg of CO₂!{badge_message}', 'success')
        
    elif action == 'reject':
        swap.status = 'rejected'
        flash('Swap rejected', 'info')
    
    db.session.commit()
    return redirect(url_for('dashboard'))

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    # Get pending items
    pending_items = Item.query.filter_by(status='pending').order_by(Item.created_at.desc()).all()
    
    # Get all users
    users = User.query.order_by(User.created_at.desc()).all()
    
    # Get recent swaps
    recent_swaps = Swap.query.order_by(Swap.created_at.desc()).limit(10).all()
    
    return render_template('admin.html', 
                         pending_items=pending_items,
                         users=users,
                         recent_swaps=recent_swaps)

@app.route('/admin_action/<int:item_id>/<action>')
@login_required
def admin_action(item_id, action):
    if not current_user.is_admin:
        flash('Access denied', 'error')
        return redirect(url_for('dashboard'))
    
    item = Item.query.get_or_404(item_id)
    
    if action == 'approve':
        item.status = 'approved'
        flash('Item approved', 'success')
    elif action == 'reject':
        item.status = 'rejected'
        flash('Item rejected', 'info')
    elif action == 'delete':
        db.session.delete(item)
        flash('Item deleted', 'warning')
    
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/profile')
@login_required
def profile():
    # Get user's transaction history
    transactions = PointsTransaction.query.filter_by(user_id=current_user.id).order_by(PointsTransaction.created_at.desc()).all()
    
    # Get user's items stats
    total_items = Item.query.filter_by(user_id=current_user.id).count()
    approved_items = Item.query.filter_by(user_id=current_user.id, status='approved').count()
    swapped_items = Item.query.filter_by(user_id=current_user.id, status='swapped').count()
    
    return render_template('profile.html', 
                         transactions=transactions,
                         total_items=total_items,
                         approved_items=approved_items,
                         swapped_items=swapped_items)

@app.route('/shipping_address', methods=['GET', 'POST'])
@login_required
def shipping_address():
    form = ShippingAddressForm()
    
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.address_line1 = form.address_line1.data
        current_user.address_line2 = form.address_line2.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.postal_code = form.postal_code.data
        current_user.country = form.country.data
        current_user.phone = form.phone.data
        
        db.session.commit()
        flash('Shipping address updated successfully!', 'success')
        return redirect(url_for('profile'))
    
    # Pre-populate form with existing data
    if request.method == 'GET':
        form.full_name.data = current_user.full_name
        form.address_line1.data = current_user.address_line1
        form.address_line2.data = current_user.address_line2
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.postal_code.data = current_user.postal_code
        form.country.data = current_user.country
        form.phone.data = current_user.phone
    
    return render_template('shipping_address.html', form=form)

@app.route('/swap_details/<int:swap_id>')
@login_required
def swap_details(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    
    # Only sender and receiver can view swap details
    if swap.sender_id != current_user.id and swap.receiver_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('swap_details.html', swap=swap)

@app.route('/update_shipping/<int:swap_id>', methods=['GET', 'POST'])
@login_required
def update_shipping(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    
    # Only the item owner (receiver) can update shipping info
    if swap.receiver_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))
    
    if swap.status != 'accepted':
        flash('Can only update shipping for accepted swaps', 'error')
        return redirect(url_for('swap_details', swap_id=swap_id))
    
    form = ShippingInfoForm()
    if form.validate_on_submit():
        swap.shipping_method = form.shipping_method.data
        swap.tracking_number = form.tracking_number.data
        swap.carrier = form.carrier.data
        swap.meetup_location = form.meetup_location.data
        swap.pickup_time = form.pickup_time.data
        swap.notes = form.notes.data
        swap.status = 'shipped'
        swap.shipped_at = datetime.utcnow()
        
        # Parse estimated delivery date
        if form.estimated_delivery.data:
            try:
                from datetime import datetime
                swap.estimated_delivery = datetime.strptime(form.estimated_delivery.data, '%Y-%m-%d')
            except ValueError:
                pass
        
        db.session.commit()
        flash('Shipping information updated!', 'success')
        return redirect(url_for('swap_details', swap_id=swap_id))
    
    return render_template('update_shipping.html', form=form, swap=swap)

@app.route('/confirm_delivery/<int:swap_id>', methods=['GET', 'POST'])
@login_required
def confirm_delivery(swap_id):
    swap = Swap.query.get_or_404(swap_id)
    
    # Only the requester (sender) can confirm delivery
    if swap.sender_id != current_user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('dashboard'))
    
    if swap.status != 'shipped':
        flash('Item must be shipped before confirming delivery', 'error')
        return redirect(url_for('swap_details', swap_id=swap_id))
    
    form = DeliveryConfirmationForm()
    if form.validate_on_submit():
        swap.condition_on_arrival = form.condition_on_arrival.data
        swap.exchange_rating = int(form.rating.data)
        swap.receiver_feedback = form.feedback.data
        swap.status = 'delivered'
        swap.completed_at = datetime.utcnow()
        
        # If item condition was poor, refund some points
        if form.condition_on_arrival.data == 'poor':
            refund_amount = int(swap.item.points_value * 0.5)  # 50% refund
            current_user.points += refund_amount
            swap.receiver.points -= refund_amount
            
            # Record transaction
            refund_transaction = PointsTransaction(
                user_id=current_user.id,
                amount=refund_amount,
                type='refund',
                description=f'Partial refund for item condition issues - {swap.item.title}'
            )
            db.session.add(refund_transaction)
            
            deduct_transaction = PointsTransaction(
                user_id=swap.receiver_id,
                amount=-refund_amount,
                type='deduction',
                description=f'Points deducted for item condition issues - {swap.item.title}'
            )
            db.session.add(deduct_transaction)
        
        db.session.commit()
        flash('Delivery confirmed! Thank you for your feedback.', 'success')
        return redirect(url_for('swap_details', swap_id=swap_id))
    
    return render_template('confirm_delivery.html', form=form, swap=swap)

@app.route('/delivery_tracking')
@login_required
def delivery_tracking():
    # Get all swaps for the current user that are in shipping process
    sent_swaps = Swap.query.filter_by(sender_id=current_user.id).filter(
        Swap.status.in_(['shipped', 'delivered'])
    ).order_by(Swap.shipped_at.desc()).all()
    
    received_swaps = Swap.query.filter_by(receiver_id=current_user.id).filter(
        Swap.status.in_(['shipped', 'delivered'])
    ).order_by(Swap.shipped_at.desc()).all()
    
    return render_template('delivery_tracking.html', 
                         sent_swaps=sent_swaps, 
                         received_swaps=received_swaps)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.route('/ngos')
def ngos():
    form = NGOFilterForm()
    
    # Build query with filters
    query = NGO.query
    
    # Apply filters if form data is present
    city_filter = request.args.get('city', '').strip()
    focus_area_filter = request.args.get('focus_area', '')
    pickup_filter = request.args.get('pickup_available')
    verified_filter = request.args.get('verified_only')
    
    if city_filter:
        query = query.filter(NGO.city.ilike(f'%{city_filter}%'))
    
    if focus_area_filter:
        query = query.filter(NGO.focus_areas.contains(focus_area_filter))
    
    if pickup_filter:
        query = query.filter(NGO.pickup_available == True)
    
    if verified_filter:
        query = query.filter(NGO.verified == True)
    
    ngos_list = query.order_by(NGO.verified.desc(), NGO.name).all()
    
    return render_template('ngos.html', ngos=ngos_list, form=form)

@app.route('/ngo/<int:ngo_id>')
def ngo_detail(ngo_id):
    ngo = NGO.query.get_or_404(ngo_id)
    return render_template('ngo_detail.html', ngo=ngo)

@app.route('/donate/<int:ngo_id>', methods=['GET', 'POST'])
@login_required
def donate_to_ngo(ngo_id):
    ngo = NGO.query.get_or_404(ngo_id)
    
    if not ngo.accepts_donations:
        flash('This NGO is not currently accepting donations.', 'error')
        return redirect(url_for('ngo_detail', ngo_id=ngo_id))
    
    form = DonationForm()
    
    if form.validate_on_submit():
        donation = Donation(
            items_description=form.items_description.data,
            estimated_value=form.estimated_value.data,
            message=form.message.data,
            pickup_address=form.pickup_address.data,
            contact_phone=form.contact_phone.data,
            preferred_contact_method=form.preferred_contact_method.data,
            user_id=current_user.id,
            ngo_id=ngo.id
        )
        
        db.session.add(donation)
        
        # Calculate environmental impact (estimate based on description)
        from carbon_utils import calculate_carbon_footprint, calculate_item_weight, update_user_stats, create_carbon_record
        
        # Basic estimation - 1 item donation with average values
        estimated_items = 1
        estimated_category = 'tops'  # Default category
        estimated_co2 = calculate_carbon_footprint(estimated_category) * estimated_items
        estimated_weight = calculate_item_weight(estimated_category) * estimated_items
        
        # Track environmental impact
        newly_earned = update_user_stats(current_user, 'donation', estimated_weight, estimated_co2)
        create_carbon_record(current_user.id, 'donation', estimated_co2, estimated_weight, estimated_category)
        
        # Award points for donation (incentivize giving)
        if form.estimated_value.data:
            bonus_points = min(form.estimated_value.data // 2, 50)  # Half the estimated value, max 50
        else:
            bonus_points = 20  # Default bonus
        
        current_user.points += bonus_points
        
        # Record transaction
        transaction = PointsTransaction(
            user_id=current_user.id,
            amount=bonus_points,
            type='bonus',
            description=f'Donation bonus - {ngo.name}'
        )
        db.session.add(transaction)
        
        db.session.commit()
        
        # Check for new badges
        badge_message = ""
        if newly_earned:
            badge_message = f" You earned {len(newly_earned)} new badge(s)!"
        
        flash(f'Donation request submitted to {ngo.name}! You saved {estimated_co2:.1f} kg of CO₂ and earned {bonus_points} points!{badge_message}', 'success')
        return redirect(url_for('ngo_detail', ngo_id=ngo.id))
    
    # Pre-fill pickup address with user's address if available
    if request.method == 'GET' and current_user.address_line1:
        address_parts = []
        if current_user.address_line1:
            address_parts.append(current_user.address_line1)
        if current_user.address_line2:
            address_parts.append(current_user.address_line2)
        if current_user.city:
            address_parts.append(f"{current_user.city}, {current_user.state} {current_user.postal_code}")
        form.pickup_address.data = '\n'.join(address_parts)
        form.contact_phone.data = current_user.phone
    
    return render_template('donate.html', form=form, ngo=ngo)

@app.route('/my_donations')
@login_required
def my_donations():
    donations = Donation.query.filter_by(user_id=current_user.id).order_by(Donation.created_at.desc()).all()
    return render_template('my_donations.html', donations=donations)



@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
