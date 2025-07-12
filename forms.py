from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SelectField, IntegerField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province (Optional)', validators=[Length(max=100)])
    pincode = StringField('Pincode/ZIP Code', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Register')

class AddItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()], widget=TextArea())
    size = SelectField('Size', choices=[
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'XXL'),
        ('XXXL', 'XXXL')
    ], validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('tops', 'Tops'),
        ('bottoms', 'Bottoms'),
        ('dresses', 'Dresses'),
        ('outerwear', 'Outerwear'),
        ('shoes', 'Shoes'),
        ('accessories', 'Accessories'),
        ('bags', 'Bags'),
        ('jewelry', 'Jewelry')
    ], validators=[DataRequired()])
    condition = SelectField('Condition', choices=[
        ('new', 'New with tags'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair')
    ], validators=[DataRequired()])
    tags = StringField('Tags (comma-separated)', validators=[Length(max=500)])
    points_value = IntegerField('Points Value', validators=[DataRequired(), NumberRange(min=10, max=500)])
    images = FileField('Images', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Images only!')])
    submit = SubmitField('Add Item')

class SwapRequestForm(FlaskForm):
    message = TextAreaField('Message (optional)', widget=TextArea())
    submit = SubmitField('Request Swap')

class AdminActionForm(FlaskForm):
    action = SelectField('Action', choices=[
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('delete', 'Delete')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ShippingAddressForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    address_line1 = StringField('Address Line 1', validators=[DataRequired(), Length(max=200)])
    address_line2 = StringField('Address Line 2 (Optional)', validators=[Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    postal_code = StringField('Postal Code', validators=[DataRequired(), Length(max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    submit = SubmitField('Update Address')

class ShippingInfoForm(FlaskForm):
    shipping_method = SelectField('Shipping Method', choices=[
        ('mail', 'Mail/Postal Service'),
        ('pickup', 'Local Pickup'),
        ('meetup', 'Public Meetup')
    ], validators=[DataRequired()])
    tracking_number = StringField('Tracking Number (if applicable)', validators=[Length(max=100)])
    carrier = SelectField('Shipping Carrier (for mail)', choices=[
        ('', 'Select Carrier'),
        ('usps', 'USPS'),
        ('fedex', 'FedEx'),
        ('ups', 'UPS'),
        ('dhl', 'DHL'),
        ('other', 'Other')
    ])
    estimated_delivery = StringField('Estimated Delivery Date (YYYY-MM-DD)')
    meetup_location = StringField('Meetup Location (if applicable)', validators=[Length(max=200)])
    pickup_time = StringField('Pickup/Meetup Time', validators=[Length(max=100)])
    notes = TextAreaField('Additional Notes', widget=TextArea())
    submit = SubmitField('Update Shipping Info')

class DeliveryConfirmationForm(FlaskForm):
    condition_on_arrival = SelectField('Item Condition on Arrival', choices=[
        ('excellent', 'Excellent - As described'),
        ('good', 'Good - Minor differences'),
        ('poor', 'Poor - Significant issues')
    ], validators=[DataRequired()])
    rating = SelectField('Rate this exchange', choices=[
        ('5', '5 - Excellent'),
        ('4', '4 - Good'),
        ('3', '3 - Average'),
        ('2', '2 - Below Average'),
        ('1', '1 - Poor')
    ], validators=[DataRequired()])
    feedback = TextAreaField('Feedback for sender (optional)', widget=TextArea())
    submit = SubmitField('Confirm Delivery')


class DonationForm(FlaskForm):
    items_description = TextAreaField('Items Description', validators=[DataRequired()], widget=TextArea(),
                                     render_kw={"placeholder": "Describe the clothing items you want to donate (type, size, condition, quantity, etc.)"})
    estimated_value = IntegerField('Estimated Points Value', validators=[Optional(), NumberRange(min=10, max=1000)],
                                  render_kw={"placeholder": "Optional: Estimate point value"})
    message = TextAreaField('Message to NGO (optional)', widget=TextArea(),
                           render_kw={"placeholder": "Any special instructions or questions for the NGO"})
    pickup_address = TextAreaField('Pickup Address', validators=[DataRequired()],
                                  render_kw={"placeholder": "Where should they pick up the items?"})
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(max=20)],
                               render_kw={"placeholder": "Phone number for coordination"})
    preferred_contact_method = SelectField('Preferred Contact Method', choices=[
        ('email', 'Email'),
        ('phone', 'Phone Call'),
        ('text', 'Text Message')
    ], validators=[DataRequired()])
    submit = SubmitField('Submit Donation Request')


class NGOFilterForm(FlaskForm):
    city = StringField('City')
    focus_area = SelectField('Focus Area', choices=[
        ('', 'All Areas'),
        ('textiles', 'Textile Recycling'),
        ('environment', 'Environmental'),
        ('education', 'Education'),
        ('poverty', 'Poverty Relief'),
        ('children', 'Children & Youth'),
        ('women', 'Women Empowerment'),
        ('homeless', 'Homeless Support'),
        ('disaster', 'Disaster Relief')
    ])
    pickup_available = BooleanField('Pickup Available')
    verified_only = BooleanField('Verified NGOs Only')
    submit = SubmitField('Filter')
