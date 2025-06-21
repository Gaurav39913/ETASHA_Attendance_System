from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
from app import db
from app.models import Admin, Center, Staff, Attendance
from app.forms import RegistrationForm, LoginForm, CenterForm, StaffForm, AttendanceForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return redirect(url_for('main.dashboard'))

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        admin = Admin(name=form.name.data, email=form.email.data)
        admin.set_password(form.password.data)
        db.session.add(admin)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('main.login'))
    return render_template('admin/register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(email=form.email.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('admin/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main.route('/dashboard')
@login_required
def dashboard():
    centers_count = Center.query.count()
    staff_count = Staff.query.count()
    recent_attendance = Attendance.query.order_by(Attendance.date.desc()).limit(5).all()
    return render_template('admin/dashboard.html', 
                         centers_count=centers_count,
                         staff_count=staff_count,
                         recent_attendance=recent_attendance)

@main.route('/centers', methods=['GET', 'POST'])
@login_required
def centers():
    form = CenterForm()
    if form.validate_on_submit():
        center = Center(name=form.name.data, 
                       coordinator=form.coordinator.data,
                       address=form.address.data)
        db.session.add(center)
        db.session.commit()
        flash('Center added successfully!', 'success')
        return redirect(url_for('main.centers'))
    centers = Center.query.all()
    return render_template('admin/centers.html', form=form, centers=centers)

@main.route('/center/delete/<int:id>', methods=['POST'])
@login_required
def delete_center(id):
    center = Center.query.get_or_404(id)
    db.session.delete(center)
    db.session.commit()
    flash('Center deleted successfully!', 'success')
    return redirect(url_for('main.centers'))

@main.route('/staff', methods=['GET', 'POST'])
@login_required
def staff():
    form = StaffForm()
    if form.validate_on_submit():
        staff = Staff(name=form.name.data,
                     position=form.position.data,
                     center_id=form.center.data)
        db.session.add(staff)
        db.session.commit()
        flash('Staff added successfully!', 'success')
        return redirect(url_for('main.staff'))
    staff_list = Staff.query.all()
    return render_template('admin/staff.html', form=form, staff_list=staff_list)

@main.route('/staff/delete/<int:id>', methods=['POST'])
@login_required
def delete_staff(id):
    staff = Staff.query.get_or_404(id)
    db.session.delete(staff)
    db.session.commit()
    flash('Staff deleted successfully!', 'success')
    return redirect(url_for('main.staff'))

@main.route('/attendance/mark', methods=['GET', 'POST'])
@login_required
def mark_attendance():
    form = AttendanceForm()
    staff_list = []
    if form.validate_on_submit():
        staff_list = Staff.query.filter_by(center_id=form.center.data).all()
    
    if request.method == 'POST' and 'submit_attendance' in request.form:
        date = datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
        for staff in Staff.query.filter_by(center_id=request.form.get('center_id')).all():
            status = request.form.get(f'status_{staff.id}')
            attendance = Attendance.query.filter_by(staff_id=staff.id, date=date).first()
            if attendance:
                attendance.status = status
            else:
                attendance = Attendance(staff_id=staff.id, date=date, status=status)
                db.session.add(attendance)
        db.session.commit()
        flash('Attendance marked successfully!', 'success')
        return redirect(url_for('main.mark_attendance'))
    
    return render_template('admin/mark_attendance.html', form=form, staff_list=staff_list)

@main.route('/attendance/view', methods=['GET', 'POST'])
@login_required
def view_attendance():
    form = AttendanceForm()
    attendance_records = []
    if form.validate_on_submit():
        attendance_records = db.session.query(Attendance, Staff)\
            .join(Staff)\
            .filter(Staff.center_id == form.center.data)\
            .filter(Attendance.date == form.date.data)\
            .all()
    return render_template('admin/view_attendance.html', form=form, attendance_records=attendance_records)
