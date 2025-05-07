from flask import render_template, redirect, url_for, request, flash,session
from flask_login import login_user, login_required, logout_user, current_user
from models import db, User, LeaveRequest
from app import app,login_manager
from werkzeug.security import check_password_hash

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin123"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
        
@app.route('/')
def start():
    return render_template("start.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        mobile = request.form.get("mobile")
        role = request.form.get("role")

      
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

  
        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for("register"))


        new_user = User(name=name, email=email, mobile=mobile, role=role)
        new_user.set_password(password)  

        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for("login"))  

    return render_template("register.html")





@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

      
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['admin'] = True
            flash("Admin login successful!", "success")
            return redirect(url_for("admin"))

 
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")

            if user.role == 'admin':
                return redirect(url_for("admin"))
            else:
                return redirect(url_for("index"))
        else:
            flash("Invalid credentials!", "danger")

    return render_template("login.html")



@app.route('/index')
@login_required
def index():
    user=current_user
    if current_user.role == 'admin':
        leave_requests = LeaveRequest.query.all()
        return render_template('admin.html', leave_requests=leave_requests)
    else:
        leave_requests = LeaveRequest.query.filter_by(id=current_user.id).all()
        return render_template('index.html', leave_requests=leave_requests,user=user)



@app.route('/admin')
def admin():
    user = current_user
    return render_template("admin.html",user=user) 


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))



@app.route('/leave')
def leave():
    leave_requests = LeaveRequest.query.all()
    return render_template('leave.html', leave_requests=leave_requests)

@app.route('/leave1')
def leave1():
    leave_requests = LeaveRequest.query.all()
    return render_template('leave1.html', leave_requests=leave_requests)


@app.route('/apply', methods=['GET', 'POST'])
def apply_leave():
    if request.method == 'POST':
        employee_name = request.form['employee_name']
        leave_type = request.form['leave_type']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        new_leave = LeaveRequest(employee_name=employee_name, leave_type=leave_type,
                                 start_date=start_date, end_date=end_date)
        db.session.add(new_leave)
        db.session.commit()
        return redirect(url_for('leave1'))  

    return render_template('apply_leave.html')


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    leave_request = LeaveRequest.query.get_or_404(id)
    action = request.form['action']
    if action == 'approve':
        leave_request.status = 'Approved'
    elif action == 'reject':
        leave_request.status = 'Rejected'
    elif action == 'delete':
        db.session.delete(leave_request)
    db.session.commit()
    return redirect(url_for('leave')) 




@app.route('/clear', methods=['POST'])
def clear():
   
    db.session.query(LeaveRequest).delete()
    db.session.commit()
    return redirect(url_for('leave'))


@app.route('/clear1', methods=['POST'])
def clear1():
    
    db.session.query(LeaveRequest).delete()
    db.session.commit()
    return redirect(url_for('leave1'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
       
        email = request.form.get('email')
        if email:
            print(f"Password reset request for email: {email}")
            return redirect(url_for('password_reset_success'))
    return render_template('forgot.html')


@app.route('/reset-success')
def password_reset_success():
    return render_template('reset.html')

@app.route('/base')
def base():
    return render_template("base.html")

@app.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template("profile.html", user=user)

@app.route('/workers')
def workers():
    return render_template("workers.html")

@app.route('/AboutUs')
def AboutUs():
    return render_template("aboutUs.html")

@app.route('/policy')
def policy():
    return render_template("policy.html")








