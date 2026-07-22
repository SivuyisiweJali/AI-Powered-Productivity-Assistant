from email_service import build_reply

def test_receiver():
    data = build_reply("customer@gmail.com")
    assert data["message"]["toRecipients"][0]["emailAddress"]["address"] == "customer@gmail.com"

def test_subject():
    data = build_reply("abc@test.com")
    assert data["message"]["subject"] == "Automatic Response"

def test_body():
    data = build_reply("abc@test.com")
    assert "Thank you for contacting" in data["message"]["body"]["content"]
