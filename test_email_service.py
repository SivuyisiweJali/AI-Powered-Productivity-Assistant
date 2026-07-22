"""
Test suite for email_service.py
Demonstrates the auto-reply generation functionality
"""

import pytest
from email_service import build_reply, AUTO_REPLY


def test_build_reply_structure():
    """Test that build_reply returns correct structure"""
    receiver = "test@example.com"
    result = build_reply(receiver)
    
    assert "message" in result
    assert "subject" in result["message"]
    assert "body" in result["message"]
    assert "toRecipients" in result["message"]


def test_build_reply_receiver_address():
    """Test that receiver email is correctly set"""
    receiver = "customer@company.com"
    result = build_reply(receiver)
    
    recipients = result["message"]["toRecipients"]
    assert len(recipients) == 1
    assert recipients[0]["emailAddress"]["address"] == receiver


def test_build_reply_subject():
    """Test that subject line is correct"""
    result = build_reply("test@example.com")
    assert result["message"]["subject"] == "Automatic Response"


def test_build_reply_body_content():
    """Test that body contains expected content"""
    result = build_reply("test@example.com")
    body_content = result["message"]["body"]["content"]
    
    assert "Smart Solution" in body_content
    assert "Thank you" in body_content
    assert "24 hours" in body_content


def test_build_reply_body_type():
    """Test that body content type is Text"""
    result = build_reply("test@example.com")
    assert result["message"]["body"]["contentType"] == "Text"


def test_auto_reply_contains_instructions():
    """Test that AUTO_REPLY template contains important instructions"""
    assert "full name" in AUTO_REPLY.lower()
    assert "ID number" in AUTO_REPLY
    assert "cellphone number" in AUTO_REPLY


def test_multiple_recipients():
    """Test handling multiple email scenarios"""
    emails = [
        "customer1@example.com",
        "customer2@example.com",
        "support@company.com"
    ]
    
    for email in emails:
        result = build_reply(email)
        assert result["message"]["toRecipients"][0]["emailAddress"]["address"] == email


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
