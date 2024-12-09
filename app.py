from flask import Flask, render_template, redirect, url_for, request, flash
#import os
# from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_migrate import Migrate
from models import db, User, Product, CartItem
from forms import RegistrationForm, LoginForm, ProductForm, UpdateProductForm

# Initialize Flask app and extensions
app = Flask(__name__)
#app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pharmacy.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
migrate = Migrate(app, db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Login unsuccessful. Check email and password", "danger")
    return render_template("login.html", form=form)
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.route("/medicines", methods=["GET", "POST"])
@login_required
def catalog():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data, price=form.price.data, stock=form.stock.data
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Medicine added successfully!", "success")
        return redirect(url_for("catalog"))
    products = Product.query.all()
    return render_template("catalog.html", products=products, form=form)
@app.route("/update_medicine/<int:product_id>", methods=["GET", "POST"])
@login_required
def update_medicine(product_id):
    product = Product.query.get_or_404(product_id)
    form = UpdateProductForm()
    if form.validate_on_submit():
        product.price = form.price.data
        product.stock = form.stock.data
        db.session.commit()
        flash("Medicine updated successfully!", "success")
        return redirect(url_for("catalog"))
    elif request.method == "GET":
        form.price.data = product.price
        form.stock.data = product.stock
    return render_template("update_medicine.html", product=product, form=form)


@app.route("/delete_medicine/<int:product_id>", methods=["POST"])
@login_required
def delete_medicine(product_id):
    product = Product.query.get(product_id)
    if product:
        CartItem.query.filter_by(product_id=product_id).delete()
        db.session.delete(product)
        db.session.commit()
        flash("Medicine and associated cart items deleted successfully!", "success")
    else:
        flash("The product does not exist.", "danger")
    return redirect(url_for("catalog"))


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
@login_required
def add_to_cart(product_id):
    product = Product.query.get(product_id)
    if product is None:
        flash("The selected product does not exist.", "danger")
        return redirect(url_for("catalog"))

    if product.stock <= 0:
        flash("This product is out of stock.", "warning")
        return redirect(url_for("catalog"))

 cart_item = CartItem.query.filter_by(
        user_id=current_user.id, product_id=product_id
    ).first()
    if cart_item:
        if product.stock >= (cart_item.quantity + 1):
            cart_item.quantity += 1
            product.stock -= 1
        else:
            flash("Not enough stock available.", "warning")
            return redirect(url_for("catalog"))
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
        product.stock -= 1

    db.session.commit()
    flash("Added to cart!", "success")
    return redirect(url_for("catalog"))


@app.route("/cart")
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = 0
    valid_cart_items = []

    for item in cart_items:
        if item.product is not None:
            total += item.product.price * item.quantity
            valid_cart_items.append(item)
        else:
            db.session.delete(item)
            db.session.commit()
            flash("Removed an invalid item from your cart.", "warning")

    return render_template("cart.html", cart_items=valid_cart_items, total=total)

@app.route("/remove_from_cart/<int:item_id>", methods=["POST"])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get(item_id)
    if cart_item and cart_item.user_id == current_user.id:
        product = cart_item.product
        product.stock += cart_item.quantity  # Restock when item is removed
        db.session.delete(cart_item)
        db.session.commit()
        flash("Item removed from cart and stock updated.", "success")
    else:
        flash("The item does not exist in your cart.", "danger")
    return redirect(url_for("cart"))


@app.route("/payment_success")
def payment_success():
    return render_template("payment_success.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
