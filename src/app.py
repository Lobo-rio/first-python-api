from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///first_database'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

@app.route('/users', methods=['GET'])
def get_users():
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    name = request.json['name']
    email = request.json['email']

    user_existed = Users.query.filter_by(email = email).first()
    if user_existed:
        return jsonify({'error': 'User already exists!'}), 400
    
    user = Users(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_existed = Users.query.filter_by(id = user_id).first()
    if not user_existed:
        return jsonify({'error': 'User does not exist!'}), 404
    
    db.session.delete(user_existed)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, port=3003)