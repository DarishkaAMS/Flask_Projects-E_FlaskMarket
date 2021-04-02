from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from Market import app, db
from Market.forms import LoginForm, PurchaseItemForm, RegisterForm, SellItemForm
from Market.models import Item, User


@app.route('/')
@app.route('/home')
def home_page_view():
    return render_template('home.html')


@app.route('/market')
@login_required
def market_page_view():
    purchase_form = PurchaseItemForm()
    items = Item.query.all()
    return render_template('market.html', items=items, purchase_form=purchase_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page_view():
    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are logged in as {user_to_create.username}", category='success')
        return redirect(url_for('market_page_view'))

    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page_view():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash('Welcome Back!', category='success')
            return redirect(url_for('market_page_view'))
        else:
            flash('Sorry... But username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page_view():
    logout_user()
    flash('Bye now! Come back again!', category='info')
    return redirect(url_for('home_page_view'))
