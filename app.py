from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend compatibility
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///announcements.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Announcement Model
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create Database
with app.app_context():
    db.create_all()

# Student View (Frontend Display)
@app.route('/')
def index():
    return render_template('index.html')

# Admin View (Manage Announcements)
@app.route('/admin')
def admin():
    return render_template('admin.html')

# Get Announcements
@app.route('/get_announcements')
def get_announcements():
    announcements = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify([
        {"id": a.id, "title": a.title, "content": a.content, "created_at": a.created_at.strftime('%Y-%m-%d %H:%M')}
        for a in announcements
    ])

# Add New Announcement
@app.route('/add_announcement', methods=['POST'])
def add_announcement():
    data = request.json
    if not data or "title" not in data or "content" not in data:
        return jsonify({"error": "Invalid data"}), 400

    new_announcement = Announcement(title=data['title'], content=data['content'])
    db.session.add(new_announcement)
    db.session.commit()
    return jsonify({"message": "Announcement added successfully!"})

# Edit Announcement
@app.route('/edit/<int:id>', methods=['POST'])
def edit_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    data = request.json
    announcement.title = data['title']
    announcement.content = data['content']
    db.session.commit()
    return jsonify({"message": "Announcement updated successfully!"})

# Delete Announcement
@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_announcement(id):
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    return jsonify({"message": "Announcement deleted successfully!"})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)