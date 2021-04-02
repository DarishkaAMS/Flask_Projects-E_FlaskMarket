from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from Market import app, db
from Market.forms import LoginForm, PurchaseItemForm, RegisterForm, SellItemForm
from Market.models import Item, User


@app.route('/')
@app.route('/home')
def home_page_view():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page_view():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You've purchased {p_item_object.name} "
                      f"for {p_item_object.price} $", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}", category='danger')

        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You've sold {s_item_object.name} "
                      f"for {s_item_object.price} $", category='success')
            else:
                flash(f"Something went wrong, you can't sell {s_item_object.name}", category='danger')

        return redirect(url_for('market_page_view'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items,
                               owned_items=owned_items,
                               purchase_form=purchase_form,
                               selling_form=selling_form)


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
            flash(f'Welcome Back, {attempted_user.username} !', category='success')
            return redirect(url_for('market_page_view'))
        else:
            flash('Sorry... But username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page_view():
    logout_user()
    flash('Bye now! Come back again!', category='info')
    return redirect(url_for('home_page_view'))
