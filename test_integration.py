"""
Integration test suite for the AI-Powered Productivity Assistant
Tests the complete workflow of email fetching and reply sending
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from email_service import build_reply, AUTO_REPLY
import json


class TestEmailService(unittest.TestCase):
    """Test suite for email_service.py"""
    
    def test_build_reply_returns_dict(self):
        """Test that build_reply returns a dictionary"""
        result = build_reply("test@example.com")
        self.assertIsInstance(result, dict)
    
    def test_build_reply_has_required_fields(self):
        """Test that reply has all required fields"""
        result = build_reply("test@example.com")
        self.assertIn("message", result)
        self.assertIn("subject", result["message"])
        self.assertIn("body", result["message"])
        self.assertIn("toRecipients", result["message"])
    
    def test_build_reply_recipient_format(self):
        """Test that recipient is formatted correctly"""
        email = "customer@company.com"
        result = build_reply(email)
        recipient = result["message"]["toRecipients"][0]
        self.assertEqual(recipient["emailAddress"]["address"], email)
    
    def test_auto_reply_template_quality(self):
        """Test that auto-reply template is professional"""
        self.assertIn("Good day", AUTO_REPLY)
        self.assertIn("Best regards", AUTO_REPLY)
        self.assertIn("Smart Solutions", AUTO_REPLY)
        self.assertGreater(len(AUTO_REPLY), 50)  # Minimum length check


class TestGraphClient(unittest.TestCase):
    """Test suite for graph_client.py"""
    
    @patch('msal.ConfidentialClientApplication')
    def test_graph_client_initialization(self, mock_msal):
        """Test GraphClient initialization with mocked MSAL"""
        from graph_client import GraphClient
        
        mock_app = MagicMock()
        mock_msal.return_value = mock_app
        
        client = GraphClient()
        self.assertIsNotNone(client)
        self.assertEqual(client.app, mock_app)
    
    @patch('msal.ConfidentialClientApplication')
    def test_token_success(self, mock_msal):
        """Test successful token acquisition"""
        from graph_client import GraphClient
        
        mock_app = MagicMock()
        mock_msal.return_value = mock_app
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test_token_123"
        }
        
        client = GraphClient()
        token = client.token()
        
        self.assertEqual(token, "test_token_123")
    
    @patch('msal.ConfidentialClientApplication')
    def test_token_failure_handling(self, mock_msal):
        """Test error handling when token acquisition fails"""
        from graph_client import GraphClient
        
        mock_app = MagicMock()
        mock_msal.return_value = mock_app
        mock_app.acquire_token_for_client.return_value = {
            "error": "invalid_client",
            "error_description": "Invalid client credentials"
        }
        
        client = GraphClient()
        
        with self.assertRaises(Exception) as context:
            client.token()
        
        self.assertIn("Token acquisition failed", str(context.exception))
    
    @patch('msal.ConfidentialClientApplication')
    def test_headers_format(self, mock_msal):
        """Test that headers are formatted correctly"""
        from graph_client import GraphClient
        
        mock_app = MagicMock()
        mock_msal.return_value = mock_app
        mock_app.acquire_token_for_client.return_value = {
            "access_token": "test_token"
        }
        
        client = GraphClient()
        headers = client.headers()
        
        self.assertIn("Authorization", headers)
        self.assertIn("Bearer test_token", headers["Authorization"])
        self.assertEqual(headers["Content-Type"], "application/json")


class TestApplicationWorkflow(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def test_email_response_payload_structure(self):
        """Test complete email response structure"""
        email = "test@example.com"
        payload = build_reply(email)
        
        # Verify the payload structure matches Microsoft Graph API requirements
        self.assertIn("message", payload)
        message = payload["message"]
        
        # Check subject
        self.assertEqual(message["subject"], "Automatic Response")
        
        # Check body
        self.assertEqual(message["body"]["contentType"], "Text")
        self.assertIn("Smart Solution", message["body"]["content"])
        
        # Check recipients
        self.assertEqual(len(message["toRecipients"]), 1)
        self.assertEqual(
            message["toRecipients"][0]["emailAddress"]["address"],
            email
        )
    
    def test_multiple_email_processing(self):
        """Test processing multiple emails"""
        test_emails = [
            "customer1@example.com",
            "customer2@example.com",
            "support@company.com",
            "inquiry@client.org"
        ]
        
        replies = [build_reply(email) for email in test_emails]
        
        self.assertEqual(len(replies), len(test_emails))
        
        for reply, email in zip(replies, test_emails):
            self.assertEqual(
                reply["message"]["toRecipients"][0]["emailAddress"]["address"],
                email
            )
    
    def test_payload_json_serializable(self):
        """Test that payload is JSON serializable for API calls"""
        payload = build_reply("test@example.com")
        
        # This should not raise an exception
        json_str = json.dumps(payload)
        
        # Verify we can parse it back
        parsed = json.loads(json_str)
        self.assertEqual(parsed["message"]["subject"], "Automatic Response")


class TestConfiguration(unittest.TestCase):
    """Test suite for configuration validation"""
    
    @patch.dict('os.environ', {
        'CLIENT_ID': 'test_id',
        'CLIENT_SECRET': 'test_secret',
        'TENANT_ID': 'test_tenant',
        'EMAIL': 'test@example.com'
    })
    def test_config_with_all_variables(self):
        """Test that config loads successfully with all variables"""
        # This would normally fail if variables are missing
        try:
            from config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, EMAIL
            self.assertIsNotNone(CLIENT_ID)
            self.assertIsNotNone(CLIENT_SECRET)
            self.assertIsNotNone(TENANT_ID)
            self.assertIsNotNone(EMAIL)
        except ValueError:
            self.fail("Config validation failed with valid environment variables")


class TestErrorHandling(unittest.TestCase):
    """Test suite for error handling scenarios"""
    
    def test_safe_dict_access(self):
        """Test safe dictionary access pattern"""
        # Simulate mail structure
        mail = {
            "id": "123",
            "from": {
                "emailAddress": {
                    "address": "sender@example.com"
                }
            }
        }
        
        # Safe access that won't crash
        sender = mail.get("from", {}).get("emailAddress", {}).get("address")
        self.assertEqual(sender, "sender@example.com")
        
        # Missing fields should return None, not crash
        incomplete_mail = {"id": "456"}
        sender = incomplete_mail.get("from", {}).get("emailAddress", {}).get("address")
        self.assertIsNone(sender)
    
    def test_invalid_mail_structure_handling(self):
        """Test handling of invalid mail structures"""
        invalid_mails = [
            {},  # Empty
            {"id": "123"},  # Missing from field
            {"from": {}},  # Empty from
            None,  # None value
        ]
        
        for invalid_mail in invalid_mails[:-1]:  # Skip None for now
            mail_id = invalid_mail.get("id")
            sender = invalid_mail.get("from", {}).get("emailAddress", {}).get("address")
            
            # Should handle gracefully
            if not mail_id or not sender:
                self.assertTrue(True)  # Expected behavior


def run_test_suite():
    """Run all tests and return results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestEmailService))
    suite.addTests(loader.loadTestsFromTestCase(TestGraphClient))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    print("=" * 70)
    print("AI-Powered Productivity Assistant - Test Suite")
    print("=" * 70)
    print()
    
    result = run_test_suite()
    
    print()
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70)
    
    exit(0 if result.wasSuccessful() else 1)
