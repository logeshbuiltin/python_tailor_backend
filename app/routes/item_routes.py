from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import ItemCategory, ItemType, ItemImage
from flask_jwt_extended import jwt_required, get_jwt_identity

item_bp = Blueprint('item', __name__)

# Get All Item Types
@item_bp.route('/item_type', methods=['GET'])
@jwt_required()
def get_item_types():
    category_id = request.args.get('category_id', type=int)
    if category_id:
        # Filter item types by category ID
        item_types = ItemType.query.filter_by(category_id=category_id).all()
    else:
        # Get all item types
        item_types = ItemType.query.all()

    return jsonify([{'id': item_type.id, 'item_name': item_type.item_name} for item_type in item_types]), 200

# Add Item Type
@item_bp.route('/item_type', methods=['POST'])
@jwt_required()
def add_item_type():
    data = request.get_json()
    if not data.get('item_name') or not data.get('category_id'):
        return jsonify({'message': 'Item name and category ID are required'}), 400

    # Check if the category exists
    category = ItemCategory.query.get(data.get('category_id'))
    if not category:
        return jsonify({'message': 'Category not found'}), 404

    new_item_type = ItemType(item_name=data['item_name'], category_id=data['category_id'])
    db.session.add(new_item_type)
    db.session.commit()

    return jsonify({'message': 'Item type added successfully'}), 201

# Update Item Type
@item_bp.route('/item_type/<int:item_type_id>', methods=['PUT'])
@jwt_required()
def update_item_type(item_type_id):
    data = request.get_json()
    if not data.get('item_name'):
        return jsonify({'message': 'Item name is required'}), 400

    item_type = ItemType.query.get(item_type_id)
    if not item_type:
        return jsonify({'message': 'Item type not found'}), 404

    item_type.item_name = data['item_name']
    db.session.commit()

    return jsonify({'message': 'Item type updated successfully'}), 200