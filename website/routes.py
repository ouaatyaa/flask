from flask import  url_for,redirect,flash,request,render_template 
from flask_login import login_user,current_user,logout_user,login_required
from website import app , db ,bcrypt
from website.forms import RegisterForm,LoginForm,UpdateAccountForm,NewPost
from website.models import User , Post
import secrets
import os
from PIL import Image   #pip install Pillow

@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html",title='home',posts=posts)
##                                                       ----Login---- 
@app.route("/login", methods=['GET', 'POST'])
def login():   
    form = LoginForm()
    if current_user.is_authenticated:   #chk if usr is alredy loggedIn
        return redirect(url_for('home'))

    if form.validate_on_submit(): # check if instance RegisterForm is valid with html form(login.html)
       user = User.query.filter_by(username=form.username.data).first()
       if user and bcrypt.check_password_hash(user.password,form.password.data):
          login_user(user,remember=form.remember.data)
          next_page=request.args.get('next')
          flash(f'User: { user.username } is Logged In !', 'success')
          return redirect(next_page) if next_page else redirect(url_for('home'))
       else:
           flash(f'login failed check username or password !', 'danger')               
    return render_template('login.html',title='login',form=form)
    
##                                                       ----Register---- 
@app.route("/register",methods=['GET', 'POST'])
def register():   # hadi asshel wa7da instancie la form et checkvalidateonsubmit et inject ds la base
    form = RegisterForm()
    if current_user.is_authenticated:  #chk if usr is alredy loggedIn
        return redirect(url_for('home'))

    if form.validate_on_submit(): # check if instance RegisterForm is valid with html form(register.html)
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_password)    
        db.session.add(user)  
        db.session.commit() 
        flash(f"User { form.username.data } Registered Successfuly ! you can now log in :",'success')        
        return redirect(url_for('login'))
    return render_template('register.html', title='register', form=form)

##   ####################                    ----logout---- 
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

##                                                       ----Account---- 
#################### Account route  and funCtion of saving Image and rezising img

def save_picture(form_pic):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path,'static/profile_pics',picture_fn)
    
    output_size = (125,125) 
    i = Image.open(form_pic)
    i.thumbnail(output_size)
    #form_pic.save(picture_path)   
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()  
          
    if form.validate_on_submit():
        if form.picture.data:
            pic_file = save_picture(form.picture.data)
            current_user.image_file = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account has been Updated ', 'success')                
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static',filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html',tite='Account',image_file=image_file,form=form)

# ------------------Add new post

@app.route('/post/new',methods=['GET', 'POST'])
@login_required
def new_post():
    form = NewPost()
    if form.validate_on_submit():
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('newpost.html',tite='New Post',form=form)
