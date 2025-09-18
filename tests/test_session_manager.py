"""
Unit tests for SessionManager.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

class TestSessionManager(unittest.TestCase):
    """Test cases for SessionManager class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock streamlit session state
        self.mock_session_state = {}
        
    @patch('streamlit.session_state', new_callable=lambda: MagicMock())
    def test_validate_user_input_valid(self, mock_st):
        """Test validation of valid user input."""
        from services.session_manager import SessionManager
        
        # Mock session state
        mock_st.__contains__ = lambda x: False
        mock_st.__setitem__ = lambda k, v: setattr(mock_st, k, v)
        
        session_manager = SessionManager()
        
        # Test valid input
        is_valid, error = session_manager.validate_user_input("This is a valid response with enough characters")
        self.assertTrue(is_valid)
        self.assertIsNone(error)
    
    @patch('streamlit.session_state', new_callable=lambda: MagicMock())
    def test_validate_user_input_invalid(self, mock_st):
        """Test validation of invalid user input."""
        from services.session_manager import SessionManager
        
        # Mock session state
        mock_st.__contains__ = lambda x: False
        mock_st.__setitem__ = lambda k, v: setattr(mock_st, k, v)
        
        session_manager = SessionManager()
        
        # Test invalid input (too short)
        is_valid, error = session_manager.validate_user_input("short")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)
        
        # Test empty input
        is_valid, error = session_manager.validate_user_input("")
        self.assertFalse(is_valid)
        self.assertIsNotNone(error)

if __name__ == '__main__':
    unittest.main()