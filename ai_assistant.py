"""
Enhanced AI Assistant Module
Core logic for chat, task management, notes, and analytics
"""

import json
import logging
from datetime import datetime
from typing import Dict, Optional, Any, List
import hashlib
import secrets
import uuid

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoogleOAuthAIAssistant:
    """
    Enhanced AI-powered Google OAuth confirmation assistant
    Manages user sessions, credentials, and AI interactions with full productivity features
    """
    
    def __init__(self):
        """Initialize the AI assistant with all data stores"""
        self.sessions = {}
        self.user_profiles = {}
        self.conversation_history = {}
        self.user_tasks = {}
        self.user_notes = {}
        self.logger = logger
        
    # ==================== AUTHENTICATION ====================
    
    def confirm_google_session(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Confirms and processes Google OAuth session with AI analysis
        
        Args:
            session_data (dict): Session data from Google OAuth callback
            
        Returns:
            dict: Confirmation response with session details and AI greeting
        """
        try:
            # Validate session data
            if not session_data or 'user_id' not in session_data:
                return self._error_response('Invalid session data')
            
            user_id = session_data['user_id']
            
            # Create secure session token
            session_token = self._generate_session_token()
            
            # Process confirmation
            confirmed_session = {
                'status': 'confirmed',
                'user_id': user_id,
                'provider': 'google',
                'session_token': session_token,
                'timestamp': datetime.now().isoformat(),
                'email': session_data.get('email', 'unknown'),
                'name': session_data.get('name', 'User')
            }
            
            # Store session
            self.sessions[session_token] = confirmed_session
            self.user_profiles[user_id] = {
                'email': session_data.get('email'),
                'name': session_data.get('name'),
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat()
            }
            
            # Initialize data stores
            self.conversation_history[user_id] = []
            self.user_tasks[user_id] = {}
            self.user_notes[user_id] = {}
            
            # Generate AI greeting
            ai_greeting = self._generate_greeting(session_data.get('name', 'User'))
            
            self.logger.info(f"Session confirmed for user: {user_id}")
            
            return {
                'status': 'success',
                'message': 'Session confirmed successfully',
                'session': confirmed_session,
                'ai_assistant': {
                    'greeting': ai_greeting,
                    'capabilities': self._get_capabilities()
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error confirming session: {str(e)}")
            return self._error_response(str(e))
    
    def logout(self, session_token: str) -> Dict[str, Any]:
        """
        End user session
        
        Args:
            session_token (str): User's session token
            
        Returns:
            dict: Logout confirmation
        """
        try:
            if session_token in self.sessions:
                user_id = self.sessions[session_token]['user_id']
                del self.sessions[session_token]
                self.logger.info(f"User {user_id} logged out")
                
            return {
                'status': 'success',
                'message': 'Logged out successfully'
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== CHAT & CONVERSATIONS ====================
    
    def chat(self, session_token: str, user_message: str) -> Dict[str, Any]:
        """
        Process user message and generate AI response
        
        Args:
            session_token (str): User's session token
            user_message (str): User's message
            
        Returns:
            dict: AI response with conversation context
        """
        try:
            # Validate session
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            session = self.sessions[session_token]
            user_id = session['user_id']
            
            # Add user message to history
            self.conversation_history[user_id].append({
                'role': 'user',
                'content': user_message,
                'timestamp': datetime.now().isoformat()
            })
            
            # Generate AI response
            ai_response = self._generate_ai_response(user_message, user_id)
            
            # Add AI response to history
            self.conversation_history[user_id].append({
                'role': 'assistant',
                'content': ai_response,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'status': 'success',
                'user_message': user_message,
                'ai_response': ai_response,
                'conversation_length': len(self.conversation_history[user_id]),
                'user': session.get('name', 'User')
            }
            
        except Exception as e:
            self.logger.error(f"Error in chat: {str(e)}")
            return self._error_response(str(e))
    
    def get_conversation_history(self, session_token: str) -> Dict[str, Any]:
        """
        Retrieve conversation history for user
        
        Args:
            session_token (str): User's session token
            
        Returns:
            dict: Conversation history
        """
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            history = self.conversation_history.get(user_id, [])
            
            return {
                'status': 'success',
                'history': history,
                'total_messages': len(history)
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def clear_conversation_history(self, session_token: str) -> Dict[str, Any]:
        """Clear conversation history"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            self.conversation_history[user_id] = []
            
            return {
                'status': 'success',
                'message': 'Conversation history cleared'
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== USER PROFILE ====================
    
    def get_user_profile(self, session_token: str) -> Dict[str, Any]:
        """
        Retrieve user profile information
        
        Args:
            session_token (str): User's session token
            
        Returns:
            dict: User profile data
        """
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            profile = self.user_profiles.get(user_id, {})
            
            return {
                'status': 'success',
                'profile': profile
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def update_user_profile(self, session_token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update user profile"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            profile = self.user_profiles.get(user_id, {})
            
            # Update allowed fields
            allowed_fields = ['name', 'email', 'preferences']
            for field in allowed_fields:
                if field in data:
                    profile[field] = data[field]
            
            profile['updated_at'] = datetime.now().isoformat()
            self.user_profiles[user_id] = profile
            
            return {
                'status': 'success',
                'message': 'Profile updated',
                'profile': profile
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== TASK MANAGEMENT ====================
    
    def get_tasks(self, session_token: str) -> Dict[str, Any]:
        """Get user's tasks"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            tasks = list(self.user_tasks.get(user_id, {}).values())
            
            return {
                'status': 'success',
                'tasks': tasks,
                'total': len(tasks)
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def create_task(self, session_token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            task_id = str(uuid.uuid4())
            task = {
                'id': task_id,
                'title': data.get('title', 'Untitled Task'),
                'description': data.get('description', ''),
                'status': 'pending',
                'priority': data.get('priority', 'medium'),
                'created_at': datetime.now().isoformat(),
                'due_date': data.get('due_date'),
                'tags': data.get('tags', [])
            }
            
            self.user_tasks[user_id][task_id] = task
            
            return {
                'status': 'success',
                'message': 'Task created',
                'task': task
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def update_task(self, session_token: str, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a task"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            if task_id not in self.user_tasks.get(user_id, {}):
                return self._error_response('Task not found')
            
            task = self.user_tasks[user_id][task_id]
            
            # Update fields
            for field in ['title', 'description', 'status', 'priority', 'due_date', 'tags']:
                if field in data:
                    task[field] = data[field]
            
            task['updated_at'] = datetime.now().isoformat()
            
            return {
                'status': 'success',
                'message': 'Task updated',
                'task': task
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def delete_task(self, session_token: str, task_id: str) -> Dict[str, Any]:
        """Delete a task"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            if task_id not in self.user_tasks.get(user_id, {}):
                return self._error_response('Task not found')
            
            del self.user_tasks[user_id][task_id]
            
            return {
                'status': 'success',
                'message': 'Task deleted'
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== NOTES ====================
    
    def get_notes(self, session_token: str) -> Dict[str, Any]:
        """Get user's notes"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            notes = list(self.user_notes.get(user_id, {}).values())
            
            return {
                'status': 'success',
                'notes': notes,
                'total': len(notes)
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def create_note(self, session_token: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new note"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            note_id = str(uuid.uuid4())
            note = {
                'id': note_id,
                'title': data.get('title', 'Untitled Note'),
                'content': data.get('content', ''),
                'created_at': datetime.now().isoformat(),
                'tags': data.get('tags', []),
                'color': data.get('color', 'white')
            }
            
            self.user_notes[user_id][note_id] = note
            
            return {
                'status': 'success',
                'message': 'Note created',
                'note': note
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def update_note(self, session_token: str, note_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update a note"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            if note_id not in self.user_notes.get(user_id, {}):
                return self._error_response('Note not found')
            
            note = self.user_notes[user_id][note_id]
            
            # Update fields
            for field in ['title', 'content', 'tags', 'color']:
                if field in data:
                    note[field] = data[field]
            
            note['updated_at'] = datetime.now().isoformat()
            
            return {
                'status': 'success',
                'message': 'Note updated',
                'note': note
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    def delete_note(self, session_token: str, note_id: str) -> Dict[str, Any]:
        """Delete a note"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            if note_id not in self.user_notes.get(user_id, {}):
                return self._error_response('Note not found')
            
            del self.user_notes[user_id][note_id]
            
            return {
                'status': 'success',
                'message': 'Note deleted'
            }
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== ANALYTICS ====================
    
    def get_analytics(self, session_token: str) -> Dict[str, Any]:
        """Get productivity analytics"""
        try:
            if session_token not in self.sessions:
                return self._error_response('Invalid session token')
            
            user_id = self.sessions[session_token]['user_id']
            
            # Calculate analytics
            tasks = self.user_tasks.get(user_id, {})
            notes = self.user_notes.get(user_id, {})
            conversation = self.conversation_history.get(user_id, [])
            
            completed_tasks = sum(1 for t in tasks.values() if t.get('status') == 'completed')
            pending_tasks = sum(1 for t in tasks.values() if t.get('status') == 'pending')
            high_priority = sum(1 for t in tasks.values() if t.get('priority') == 'high')
            
            analytics = {
                'status': 'success',
                'summary': {
                    'total_tasks': len(tasks),
                    'completed_tasks': completed_tasks,
                    'pending_tasks': pending_tasks,
                    'high_priority_tasks': high_priority,
                    'total_notes': len(notes),
                    'total_conversations': len(conversation) // 2,  # pairs of user-ai messages
                    'completion_rate': (completed_tasks / len(tasks) * 100) if tasks else 0
                },
                'task_breakdown': {
                    'by_priority': {
                        'high': sum(1 for t in tasks.values() if t.get('priority') == 'high'),
                        'medium': sum(1 for t in tasks.values() if t.get('priority') == 'medium'),
                        'low': sum(1 for t in tasks.values() if t.get('priority') == 'low')
                    },
                    'by_status': {
                        'pending': pending_tasks,
                        'in_progress': sum(1 for t in tasks.values() if t.get('status') == 'in_progress'),
                        'completed': completed_tasks
                    }
                }
            }
            
            return analytics
            
        except Exception as e:
            return self._error_response(str(e))
    
    # ==================== HELPER METHODS ====================
    
    def _generate_session_token(self) -> str:
        """Generate a secure session token"""
        return hashlib.sha256(secrets.token_bytes(32)).hexdigest()
    
    def _generate_greeting(self, name: str) -> str:
        """Generate personalized AI greeting"""
        return f"Hello {name}! 👋 I'm your AI Productivity Assistant. How can I help you today?"
    
    def _generate_ai_response(self, user_message: str, user_id: str) -> str:
        """
        Generate contextual AI response
        
        Args:
            user_message (str): User's input
            user_id (str): User identifier
            
        Returns:
            str: AI-generated response
        """
        message_lower = user_message.lower()
        
        # Intent recognition
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            return "Hi there! 👋 I'm here to help you with productivity tasks, scheduling, notes, and more. What would you like to work on?"
        
        elif any(word in message_lower for word in ['help', 'what can you do', 'capabilities', 'features']):
            capabilities = self._get_capabilities()
            return f"I can help you with:\n" + "\n".join([f"• {cap}" for cap in capabilities])
        
        elif any(word in message_lower for word in ['time', 'schedule', 'calendar', 'meeting', 'plan']):
            return "I can help you manage your schedule. Would you like to:\n• View your calendar\n• Schedule a meeting\n• Set reminders\n• Find available time slots"
        
        elif any(word in message_lower for word in ['note', 'memo', 'remember', 'write', 'document']):
            return "I can help you take notes and organize your thoughts. Would you like to:\n• Create a new note\n• View existing notes\n• Search notes\n• Set up reminders"
        
        elif any(word in message_lower for word in ['task', 'todo', 'work', 'project', 'goal']):
            return "I can help you manage tasks and projects. Would you like to:\n• Create a new task\n• View your task list\n• Set priorities\n• Track progress"
        
        elif any(word in message_lower for word in ['analyze', 'summary', 'report', 'stats', 'productivity']):
            return "I can provide productivity analysis and insights based on your activities. Would you like me to generate:\n• Daily summary\n• Weekly report\n• Task completion stats\n• Time management analysis"
        
        elif any(word in message_lower for word in ['bye', 'goodbye', 'exit', 'quit', 'close']):
            return "Goodbye! Remember to stay productive. See you next time! 👋"
        
        else:
            return f"That's interesting! I understood: '{user_message}'\n\nHow can I assist you with this? I can help with:\n• Task management\n• Scheduling\n• Note-taking\n• Productivity analysis\n• And more!"
    
    def _get_capabilities(self) -> list:
        """Get list of AI assistant capabilities"""
        return [
            "Task Management & To-Do Lists",
            "Calendar & Schedule Management",
            "Note-Taking & Documentation",
            "Productivity Analytics",
            "Meeting Scheduling",
            "Reminder Management",
            "Goal Tracking",
            "Time Management Insights",
            "Natural Language Processing",
            "Personalized Recommendations"
        ]
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """Generate standardized error response"""
        return {
            'status': 'error',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }


# Initialize global assistant instance
ai_assistant = GoogleOAuthAIAssistant()
