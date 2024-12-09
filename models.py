from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Initialize SQLAlchemy
db = SQLAlchemy()

"""
This module defines the database models for the pharmacy website,
including User, Product, and CartItem.
It defines the relationships between users, products, and their cart items.
"""

class User(db.Model, UserMixin):
    """
    Represents a user in the system, with related cart items.
    The User model allows users to add products to their cart.
    """
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    cart_items = db.relationship('CartItem', backref='user', lazy=True)

    def add_cart_item(self, product, quantity):
        """Add a product to the user's cart."""
        cart_item = CartItem(user_id=self.id, product_id=product.id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()

    def get_cart_items(self):
        """Fetch all items in the user's cart."""
        return CartItem.query.filter_by(user_id=self.id).all()


class Product(db.Model):
    """
    Represents a product in the catalog, including name, price, and stock.
    The Product model defines the behavior for managing product stock.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade="all, delete-orphan")

    def reduce_stock(self, quantity):
        """Reduce the stock of the product when added to cart."""
        if self.stock >= quantity:
            self.stock -= quantity
            db.session.commit()
        else:
            raise ValueError("Not enough stock")

    def increase_stock(self, quantity):
        """Increase the stock of the product."""
        self.stock += quantity
        db.session.commit()


class CartItem(db.Model):
    """
    Represents an item in the user's cart, with quantity and associated product.
    The CartItem model helps track the products users add to their cart.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    def update_quantity(self, new_quantity):
        """Update the quantity of the cart item."""
        self.quantity = new_quantity
        db.session.commit()

    def remove_item(self):
        """Remove the item from the cart."""
        db.session.delete(self)
        db.session.commit()
