from flask import Blueprint, request, jsonify, url_for
from app.extensions import db
from app.models import ItemImage, ItemType
from flask_jwt_extended import jwt_required, get_jwt_identity

image_bp = Blueprint('image', __name__)

@image_bp.route('/item_image', methods=['GET'])
@jwt_required()
def get_item_images():
    print(f"Request Args: {request.args}")  # Debugging query parameters
    type_id = request.args.get('type_id')
    if not type_id:
        return jsonify({'message': 'Type ID is required'}), 400

    try:
        type_id = int(type_id)
    except ValueError:
        return jsonify({'message': 'Invalid Type ID'}), 400

    images = ItemImage.query.filter_by(type_id=type_id).all()
    if not images:
        return jsonify({'message': 'No images found for the given Type ID'}), 404

    return jsonify([{'id': img.id, 'image_url': img.image_url} for img in images]), 200

@image_bp.route('/item_image', methods=['POST'])
@jwt_required()
def add_item_image():
    data = request.get_json()
    if not data.get('image_url') or not data.get('type_id'):
        return jsonify({'message': 'Image URL and type ID are required'}), 400
    item_type = ItemType.query.get(data['type_id'])
    if not item_type:
        return jsonify({'message': 'Invalid type ID'}), 400

    # Handle dynamic image URLs
    if data.get('image_url').startswith('/'):
        image_url = url_for('static', filename=data.get('image_url')[1:]) 
    else:
        image_url = data.get('image_url') 

    new_image = ItemImage(image_url=image_url, type_id=data['type_id'])
    db.session.add(new_image)
    db.session.commit()

    return jsonify({'message': 'Item image added successfully'}), 201

@image_bp.route('/item_image/<int:image_id>', methods=['PUT'])
@jwt_required()
def update_item_image(image_id):
    data = request.get_json()
    if not data.get('image_url'):
        return jsonify({'message': 'Image URL is required'}), 400

    item_image = ItemImage.query.get(image_id)
    if not item_image:
        return jsonify({'message': 'Item image not found'}), 404

    # Handle dynamic image URLs
    if data.get('image_url').startswith('/'):
        image_url = url_for('static', filename=data.get('image_url')[1:]) 
    else:
        image_url = data.get('image_url') 

    item_image.image_url = image_url
    db.session.commit()

    return jsonify({'message': 'Item image updated successfully'}), 200