# from flask import Blueprint, request, jsonify
# from app.models import ItemCategory, User
# from app.extensions import db
# from flask_jwt_extended import jwt_required, get_jwt_identity

# category_bp = Blueprint('category', __name__)

# @category_bp.route('/item_category', methods=['POST'])
# @jwt_required()
# def add_item_category():
#     data = request.get_json()
#     if not data.get('category_name'):
#         return jsonify({'message': 'Category name is required'}), 400

#     current_user = get_jwt_identity()
#     user = User.query.filter_by(username=current_user['username']).first()

#     if not user:
#         return jsonify({'message': 'User not found'}), 404

#     new_category = ItemCategory(category_name=data['category_name'], user_id=user.id)
#     db.session.add(new_category)
#     db.session.commit()
#     return jsonify({'message': 'Item category added successfully'}), 201
from flask import Blueprint, request, jsonify
from app.models import ItemCategory, User
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
# from flask_jwt_extended import create_access_token



category_bp = Blueprint('category', __name__)

@category_bp.route('/item_category', methods=['POST'])
@jwt_required()
def add_item_category():
    
    # Parse JSON data from the request
    data = request.get_json()
    print(data)
    if not data or not data.get('category_name'):
        return jsonify({'message': 'Category name is required'}), 400

    # Retrieve the current user's identity from the JWT
    # current_user_username = get_jwt_identity()
    # if not current_user_username:
    #     return jsonify({'message': 'Invalid token or user not authenticated'}), 401
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id) 
    if not user:
        return jsonify({'message': 'User not found'}), 404
    # Fetch the user from the database
    # user = User.query.filter_by(username=current_user_username).first()
    # if not user:
    #     return jsonify({'message': 'User not found'}), 404

    # Check if the category already exists for the user
    existing_category = ItemCategory.query.filter_by(
        category_name=data['category_name'], user_id=user.id
    ).first()
    # Ensure user.id is converted to a string
    
    if existing_category:
        return jsonify({'message': 'Category already exists'}), 409

    # Create and save the new item category
    new_category = ItemCategory(category_name=data['category_name'], user_id=user.id)
    db.session.add(new_category)
    db.session.commit()

    return jsonify({'message': 'Item category added successfully'}), 201
# Add a GET route for retrieving item categories
@category_bp.route('/item_category', methods=['GET'])
@jwt_required()
def get_item_categories():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    item_categories = user.item_categories 
    return jsonify([category.serialize() for category in item_categories])
@category_bp.route('/item_category/<int:category_id>', methods=['PUT'])
@jwt_required()
def update_item_category(category_id):
    data = request.get_json()
    if not data or not data.get('category_name'):
        return jsonify({'message': 'Category name is required'}), 400

    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    category_to_update = ItemCategory.query.get(category_id)
    if not category_to_update:
        return jsonify({'message': 'Category not found'}), 404

    # Check if the user owns the category
    if category_to_update.user_id != user.id:
        return jsonify({'message': 'Unauthorized to update this category'}), 403

    category_to_update.category_name = data['category_name']
    db.session.commit()

    return jsonify({'message': 'Item category updated successfully'}), 200 