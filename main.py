import flask
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort
import os
import json
from dotenv import load_dotenv
import psycopg2
from flask_wtf import FlaskForm, CSRFProtect
import requests
from classes import classes
from speech import Speech
import os


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
ckeditor = CKEditor(app)
Bootstrap(app)
csrf = CSRFProtect(app)

##CONNECT TO DB
# if os.environ.get("LOCAL") == "True":
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SP3C_Kartik_Yatra.db'
# else:
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)

global variables
current_year = datetime.now().year
# #global variables for booking
# name_of_hotel = ""

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))
#
# def admin_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         #If id is not 1 then return abort with 403 error
#         if current_user.id != 1:
#             return abort(403)
#         #Otherwise continue with the route function
#         return f(*args, **kwargs)
#     return decorated_function
#
# def account_only(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         #If id is not 1 then return abort with 403 error
#         if current_user.id != 2:
#             return abort(403)
#         #Otherwise continue with the route function
#         return f(*args, **kwargs)
#     return decorated_function
#
# ##CONFIGURE TABLES
#
#
# class HotelList(db.Model):
#     __tablename__ = "hotel_lists"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(50), nullable=False)
#     category = db.Column(db.String(150), nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     booked = db.Column(db.Integer)
#     occupancy = db.Column(db.String(50), nullable=False)
#     occupancy1 = db.Column(db.String(50), nullable=False)
#     occupancy2 = db.Column(db.String(50), nullable=False)
#
# class User(UserMixin, db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), unique=True)
#     password = db.Column(db.String(100), nullable=False)
#     area = db.Column(db.String(100), nullable=False)
#     mobile = db.Column(db.String(100), nullable=False)
#
#
# class Booking(db.Model):
#     __tablename__ = "bookings"
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, nullable=False)
#     user_name = db.Column(db.String(100), nullable=False)
#     user_mobile = db.Column(db.String(15), nullable=False)
#     user_email = db.Column(db.String(100), nullable=False)
#     date_time = db.Column(db.String(100), nullable=False)
#     hotel = db.Column(db.String(50), nullable=False)
#     description = db.Column(db.String(50), nullable=False)
#     number_of_room_booked = db.Column(db.Integer, nullable=False)
#     amount_paid = db.Column(db.String(20), nullable=False)
#     utr_receipt_number = db.Column(db.String(100), nullable=False)
#     status = db.Column(db.String(20), nullable=False)
#     verification_date = db.Column(db.String(20))
#
#
# db.create_all()



# class HotelChoices():
#     def __init__(self):
#         pass
#     def hotel_name(self):
#         hotel_names = []
#         names = db.session.query(HotelList.name).distinct()
#         for name in names:
#             hotel_names.append(name.name)
#         return(hotel_names)
#     def hotel_description(hotel):
#         descriptions = []
#         desc = HotelList.query.filter_by(name=hotel).all()
#         for des in desc:
#             descriptions.append(des.description)
#         return (descriptions)
#
#     def room_availability(hotel, description):
#         total_rooms = HotelList.query.filter_by(name=hotel, description=description).first()
#         return total_rooms
#
# class DoBookingHotelForm(FlaskForm):
#     hotel_name = SelectField("Hotel Name", choices=HotelChoices.hotel_name(self=""), validators=[DataRequired()])
#     submit = SubmitField("Select Hotel")

@app.route('/')
def home():

    # return render_template("index.html", logged_in=current_user.is_authenticated, current_user=current_user, current_year=current_year)
    return render_template("index.html", current_year=current_year)

@app.route('/subject/<string:id>', methods=["GET", "POST"])
def subject(id):
    if request.method == "POST":
        subject_name = request.form.get("subject_name")
        class_name = request.form.get("class_name")
        chapter_name = request.form.get("chapter_name")
        text_number = request.form.get("text_number")
        chapter_list = classes[subject_name][class_name]


        if chapter_name == "None" and text_number == "None":

            return render_template("subject.html", chapter_list=classes[subject_name][class_name], subject_name=subject_name, class_name=class_name, chapter_name="not known", text_number="not known", current_year=current_year)

        elif text_number == "None":

            return render_template("subject.html", slokas_list=classes[subject_name][class_name]['Chapters'][chapter_name], subject_name=subject_name,
                                   class_name=class_name, chapter_name=chapter_name, text_number="not known",
                                   current_year=current_year)

        else:
            Speech.speak(class_name, chapter_name, text_number)
            # print(f"final canto {class_name} chapter {chapter_name} text {text_number}")

            return redirect(url_for('home'))


    if request.method == "GET":
        
        if id != "Maths":
            return redirect(url_for('home'))
        else:
            return render_template("subject.html", classes_list=classes[id], subject_name=id, class_name="not known", chapter_name="not known", text_number="not known", current_year=current_year)


# @app.route('/sample', methods=["GET", "POST"])
# def sample():
#     if request.method == "POST":
#         subject_name = request.form.get("subject_name")
#         class_name = request.form.get("class_name")
#         chapter_name = request.form.get("chapter_name")
#         list_of_qstn = []
#
#         if subject_name == "Maths":
#             qstn = Maths_Qstn_Selection.Maths(class_name, chapter_name, "sample",'none', list_of_qstn)
#
#         return render_template("sample.html", logged_in=current_user.is_authenticated, current_user=current_user,
#                            qstn=qstn, subject_name=subject_name, class_name=class_name, chapter_name=chapter_name, current_year=current_year)
#
#     if request.method == "GET":
#         return redirect(url_for('home'))
#
#
# @app.route('/test', methods=["GET", "POST"])
# def test():
#     if request.method == "POST":
#         subject_name = request.form.get("subject_name")
#         class_name = request.form.get("class_name")
#         chapter_name = request.form.get("chapter_name")
#         qstn_number = int(request.form.get("qstn_number"))
#         option_selected = request.form.get("optionSelected")
#
#         if qstn_number == 0:
#             list_of_qstn = []
#             qstn_details = {0: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 1: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 2: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 3: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 4: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 5: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 6: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 7: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 8: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}, 9: {'text': "", 'answer': "", 'options': "", 'option_selected': ""}}
#         else:
#             qstn = eval(request.form.get("qstn"))
#             qstn_details = eval(request.form.get("qstn_details"))
#             list_of_qstn = qstn['list_of_qstn']
#             qstn_details[qstn_number - 1]['option_selected'] = option_selected
#
#         if qstn_number == 10:
#             score = 0
#             for x in range(10):
#                 if qstn_details[x]['option_selected'] is not None:
#                     if str(qstn_details[x]['option_selected']) == str(qstn_details[x]['answer']):
#                         score += 1
#
#             return render_template("test_result.html", logged_in=current_user.is_authenticated, current_user=current_user, score=score, chapter_name=chapter_name, current_year=current_year)
#
#         if subject_name == "Maths":
#             qstn = Maths_Qstn_Selection.Maths(class_name, chapter_name, "test", qstn_number, list_of_qstn)
#
#         qstn_details[qstn_number]['text'] = qstn['text']
#         qstn_details[qstn_number]['answer'] = qstn['answer']
#         qstn_details[qstn_number]['options'] = qstn['shuffled_options']
#
#         if qstn_number == 0:
#             list_of_qstn = qstn['list_of_qstn']
#
#         qstn_number += 1
#
#         return render_template("test.html", logged_in=current_user.is_authenticated, current_user=current_user, qstn_details=qstn_details,
#                             qstn=qstn, subject_name=subject_name, class_name=class_name, chapter_name=chapter_name, qstn_number=qstn_number, current_year=current_year)
#
#     if request.method == "GET":
#         return redirect(url_for('home'))


# @app.route('/register', methods=["GET", "POST"])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         if User.query.filter_by(email=form.email.data).first():
#             # User already exists
#             flash("You've already signed up with that email, log in instead!")
#             return redirect(url_for('login'))
#
#         hash_and_salted_password = generate_password_hash(
#             form.password.data,
#             method='pbkdf2:sha256',
#             salt_length=12
#         )
#         new_user = User(
#             name=form.name.data,
#             email=form.email.data,
#             password=hash_and_salted_password,
#             area=form.area.data,
#             mobile=form.mobile.data,
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         login_user(new_user)
#         return redirect(url_for("home"))
#
#     return render_template("register.html", form=form, logged_in=current_user.is_authenticated, current_user=current_user, current_year=current_year)


@app.route('/<path:invalid_path>')
def catch_all(invalid_path):
    # Redirect any invalid path to the home page
    return redirect(url_for('home'))

# @app.route('/login', methods=["GET", "POST"])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         user = User.query.filter_by(email=email).first()
#         if not user:
#             flash("That email does not exist, please try again.")
#             return redirect(url_for('login'))
#         elif not check_password_hash(user.password, password):
#             flash('Password incorrect, please try again.')
#             return redirect(url_for('login'))
#         else:
#             login_user(user)
#             return redirect(url_for('home'))
#
#     return render_template("login.html", form=form, logged_in=current_user.is_authenticated, current_user=current_user, current_year=current_year)
#
#
#
# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('home'))
#
# @app.route('/do_booking', methods=["GET", "POST"])
# def do_booking():
#     form = DoBookingHotelForm()
#
#     if form.validate_on_submit():
#         global name_of_hotel
#         if len(name_of_hotel) == 0:
#             name_of_hotel = form.hotel_name.data
#             choices = HotelChoices.hotel_description(name_of_hotel)
#             return render_template("do_booking.html", hotel=name_of_hotel, form=form, choices=choices, logged_in=current_user.is_authenticated, current_user=current_user)
#
#     if len(name_of_hotel) != 0:
#         roomDesc = request.form.get("description")
#         hotelName = request.form.get("hotel")
#         number_of_room = HotelChoices.room_availability(hotelName,roomDesc)
#         name_of_hotel = ""
#         if number_of_room.quantity > number_of_room.booked:
#             return render_template("do_booking.html", hotel=hotelName, form=form, description=roomDesc, quantity=number_of_room, logged_in=current_user.is_authenticated, current_user=current_user)
#         else:
#             return render_template("do_booking.html", hotel=hotelName, form=form, description=roomDesc, message="No rooms Available", logged_in=current_user.is_authenticated, current_user=current_user)
#
#     return render_template("do_booking.html", form=form, logged_in=current_user.is_authenticated, current_user=current_user)
#
# @app.route('/book_room', methods=["GET", "POST"])
# def book_room():
#     current_date_time = datetime.now()
#     hotel_list = HotelList.query.filter_by(name=request.form.get("hotel"), description=request.form.get("description")).first()
#     hotel_list.booked = int(int(request.form.get("already_booked")) + int(request.form.get("quantity_booked")))
#     db.session.commit()
#     new_booking = Booking(
#         user_id=request.form.get("user_id"),
#         user_name=request.form.get("user_name"),
#         user_mobile=request.form.get("user_mobile"),
#         user_email=request.form.get("user_email"),
#         date_time=current_date_time,
#         hotel=request.form.get("hotel"),
#         description=request.form.get("description"),
#         number_of_room_booked=request.form.get("quantity_booked"),
#         amount_paid=request.form.get("amount_paid"),
#         utr_receipt_number=request.form.get("utr"),
#         status="To be verified",
#     )
#     db.session.add(new_booking)
#     db.session.commit()
#     return render_template("index.html", logged_in=current_user.is_authenticated, current_user=current_user)
#
# @app.route('/review_booking', methods=["GET", "POST"])
# def review_booking():
#     my_bookings = Booking.query.filter_by(user_id=current_user.id).all()
#     return render_template("review_booking.html", bookings=my_bookings, logged_in=current_user.is_authenticated, current_user=current_user)
#
# @app.route('/verify_booking', methods=["GET", "POST"])
# @account_only
# def verify_booking():
#
#     if request.method == "POST":
#         verified_post = Booking.query.filter_by(id=request.form.get("booking_id")).first()
#         verified_post.status = "Verified"
#         db.session.commit()
#     to_be_verified = Booking.query.filter_by(status="To be verified").all()
#     return render_template("verify_booking.html", bookings_tbv=to_be_verified, logged_in=current_user.is_authenticated, current_user=current_user)
#
#
# @app.route("/post/<int:post_id>", methods=["GET", "POST"])
# def show_post(post_id):
#     form = CommentForm()
#     requested_post = BlogPost.query.get(post_id)
#     if form.validate_on_submit():
#         if current_user.is_authenticated:
#             new_comment = Comment(
#                 text=form.comment_text.data,
#                 comment_author=current_user,
#                 parent_post=requested_post
#             )
#             db.session.add(new_comment)
#             db.session.commit()
#         else:
#             flash("Please login/register, for posting comments")
#             return redirect(url_for('login'))
#     return render_template("post.html", post=requested_post, form=form, logged_in=current_user.is_authenticated, current_user=current_user)

# @app.route("/about")
# def about():
#     return render_template("about.html", logged_in=current_user.is_authenticated, current_user=current_user)
#
# @app.route("/add_hotels", methods=["GET", "POST"])
# @admin_only
# def add_hotels():
#     form = AddHotelForm()
#     if form.validate_on_submit():
#         new_hotel = HotelList(
#             name=form.name.data,
#             description=form.description.data,
#             category=form.category.data,
#             quantity=form.quantity.data,
#             booked=form.booked.data,
#             occupancy=form.occupancy.data,
#             occupancy1=form.occupancy1.data,
#             occupancy2=form.occupancy2.data,
#         )
#         db.session.add(new_hotel)
#         db.session.commit()
#         return redirect(url_for("home"))
#     return render_template("add_hotel.html", form=form, logged_in=current_user.is_authenticated, current_user=current_user)
#
#
# @app.route("/hotel")
# def hotel_details():
#     hotels = HotelList.query.all()
#     return render_template("hotels.html", hotels=hotels, logged_in=current_user.is_authenticated, current_user=current_user)
#
#
# @app.route("/new-post", methods=["GET", "POST"])
# @admin_only
# def add_new_post():
#     form = CreatePostForm()
#     if form.validate_on_submit():
#         new_post = BlogPost(
#             title=form.title.data,
#             subtitle=form.subtitle.data,
#             body=form.body.data,
#             img_url=form.img_url.data,
#             author=current_user,
#             date=date.today().strftime("%B %d, %Y")
#         )
#         db.session.add(new_post)
#         db.session.commit()
#         return redirect(url_for("home"))
#     return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated, current_user=current_user)
#
#
# @app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
# @admin_only
# @admin_only
# def edit_post(post_id):
#     post = BlogPost.query.get(post_id)
#     edit_form = CreatePostForm(
#         title=post.title,
#         subtitle=post.subtitle,
#         img_url=post.img_url,
#         author=post.author,
#         body=post.body
#     )
#     if edit_form.validate_on_submit():
#         post.title = edit_form.title.data
#         post.subtitle = edit_form.subtitle.data
#         post.img_url = edit_form.img_url.data
#         post.author = edit_form.author.data
#         post.body = edit_form.body.data
#         db.session.commit()
#         return redirect(url_for("show_post", post_id=post.id))
#
#     return render_template("make-post.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated, current_user=current_user)
#
#
# @app.route("/delete/<int:post_id>")
# @admin_only
# def delete_post(post_id):
#     post_to_delete = BlogPost.query.get(post_id)
#     db.session.delete(post_to_delete)
#     db.session.commit()
#     return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
    # app.run(host='0.0.0.0', port=5000)
