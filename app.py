"""
AI Productivity Assistant - Flask Web Application
Main application entry point with routes and API endpoints
"""

from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from functools import wraps
import os
from datetime import timedelta
from ai_assistant import GoogleOAuthAIAssistant

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Initialize AI Assistant
ai_assistant = GoogleOAuthAIAssistant()


# Authentication decorator
def login_required(f):
    """Decorator to check if user is authenticated"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'session_token' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function


# ==================== AUTHENTICATION ROUTES ====================

@app.route('/api/auth/google/confirm', methods=['POST'])
def google_confirm():
    """
    Confirm Google OAuth session
    Expects: { user_id, email, name }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Confirm session with AI assistant
        result = ai_assistant.confirm_google_session(data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        # Store session token in Flask session
        session['session_token'] = result['session']['session_token']
        session['user_id'] = result['session']['user_id']
        session.permanent = True
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout user and end session"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.logout(session_token)
        
        # Clear session
        session.clear()
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Check authentication status"""
    if 'session_token' in session:
        return jsonify({
            'authenticated': True,
            'user_id': session.get('user_id')
        }), 200
    else:
        return jsonify({
            'authenticated': False
        }), 200


# ==================== CHAT ROUTES ====================

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    """
    Process user message and get AI response
    Expects: { message }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'No message provided'}), 400
        
        session_token = session.get('session_token')
        user_message = data['message']
        
        # Get AI response
        result = ai_assistant.chat(session_token, user_message)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversation-history', methods=['GET'])
@login_required
def get_history():
    """Get conversation history for current user"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.get_conversation_history(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/conversation-history', methods=['DELETE'])
@login_required
def clear_history():
    """Clear conversation history"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.clear_conversation_history(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PROFILE ROUTES ====================

@app.route('/api/profile', methods=['GET'])
@login_required
def get_profile():
    """Get user profile information"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.get_user_profile(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update user profile"""
    try:
        data = request.get_json()
        session_token = session.get('session_token')
        
        result = ai_assistant.update_user_profile(session_token, data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== TASK MANAGEMENT ROUTES ====================

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    """Get user's tasks"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.get_tasks(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['POST'])
@login_required
def create_task():
    """Create a new task"""
    try:
        data = request.get_json()
        session_token = session.get('session_token')
        
        result = ai_assistant.create_task(session_token, data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update a task"""
    try:
        data = request.get_json()
        session_token = session.get('session_token')
        
        result = ai_assistant.update_task(session_token, task_id, data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.delete_task(session_token, task_id)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== NOTES ROUTES ====================

@app.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    """Get user's notes"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.get_notes(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    """Create a new note"""
    try:
        data = request.get_json()
        session_token = session.get('session_token')
        
        result = ai_assistant.create_note(session_token, data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    """Update a note"""
    try:
        data = request.get_json()
        session_token = session.get('session_token')
        
        result = ai_assistant.update_note(session_token, note_id, data)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete a note"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.delete_note(session_token, note_id)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== ANALYTICS ROUTES ====================

@app.route('/api/analytics', methods=['GET'])
@login_required
def get_analytics():
    """Get productivity analytics"""
    try:
        session_token = session.get('session_token')
        result = ai_assistant.get_analytics(session_token)
        
        if result['status'] == 'error':
            return jsonify(result), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PAGE ROUTES ====================

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')


@app.route('/login')
def login_page():
    """Login page"""
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'session_token' not in session:
        return render_template('login.html')
    return render_template('dashboard.html')


@app.route('/chat')
def chat_page():
    """Chat interface page"""
    if 'session_token' not in session:
        return render_template('login.html')
    return render_template('chat.html')


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Development server
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.environ.get('FLASK_ENV') == 'development',
        use_reloader=True
    )
