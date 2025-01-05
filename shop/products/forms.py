from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf import FlaskForm
from wtforms import Form, IntegerField,StringField,BooleanField,TextAreaField,validators, SelectField, DecimalField

class AddproductsForm(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price', [validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    desc = TextAreaField('Desc', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])

    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])