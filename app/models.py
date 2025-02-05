from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    item_categories = db.relationship('ItemCategory', backref='user', lazy=True)

class ItemCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def serialize(self):
        return {
            'id': self.id,
            'category_name': self.category_name,
        } 

class ItemType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('item_category.id'), nullable=False)
    item_name = db.Column(db.String(80), nullable=False)

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('item_type.id'), nullable=False)
    image_url = db.Column(db.String(120), nullable=False)
