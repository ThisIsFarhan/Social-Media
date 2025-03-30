from flask import request, jsonify
from config import app, db, bcrypt
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

@app.route('/register', methods=["POST"])
def register():
    usr_name = request.json.get("username")
    password = request.json.get("password")

    if User.query.filter_by(username=usr_name).first():
        return jsonify({"error": "Username already exists"}), 400
    
    new_user = User(username=usr_name)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully!"}), 201


@app.route('/login',methods=["POST"])
def login():
    usr_name = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=usr_name).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    
    access_token = create_access_token(identity=usr_name)
    return jsonify(access_token=access_token), 200

@app.route('/delete_usr', methods=["DELETE"])
@jwt_required()
def delete_usr():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

@app.route('/posts', methods=["GET"])
@jwt_required()
def posts():
    current_user = get_jwt_identity()
    return jsonify({"message": f"Hello, {current_user}!"}), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)