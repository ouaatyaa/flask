from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_login import LoginManager
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
#from PIL import Image
from wtforms.validators import Email,DataRequired,InputRequired, Length, ValidationError, EqualTo,ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField,EmailField,TextAreaField

from website.models import User,Post

################################################################################# Forms 
#-1------------Register form
class RegisterForm(FlaskForm):
    username = StringField('UserName:', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email:',validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Password (Confirm):', validators=[DataRequired(),  EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self,username):    #Customized Validation for database errors
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('username alredy used , pleaze choose another user') #dont forget to import it
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()  #email field comming from the form in parameter of register()
        if user:
            raise ValidationError('Email alredy used , pleaze choose another one')
#--2-----------login form
class LoginForm(FlaskForm):
    username = StringField('UserName:', validators=[DataRequired(), Length(min=3, max=20)])
    #email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired(), Length(min=6, max=20)])
    remember = BooleanField('Remember Me')  #ici pas de validator c juste un bool
    submit = SubmitField('Login')

#--3-----------Update form
class UpdateAccountForm(FlaskForm):
    username = StringField('UserName:', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email:',validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture:', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')
    
    def validate_username(self,username):    #Customized Validation funct to check whether usr is in db
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('username alredy used , pleaze choose another user') #dont forget to import it
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()  #email field comming from the form in parameter of register()
            if user:
                raise ValidationError('Email alredy used , pleaze choose another one')
            
# ---------- add new post

class NewPost(FlaskForm):
    title =  StringField('Title:', validators=[DataRequired()])
    content = TextAreaField('Post Content',validators=[DataRequired()]) 
    submit = SubmitField('Post')               