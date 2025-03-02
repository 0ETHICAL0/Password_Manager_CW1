import unittest
from unittest.mock import patch, MagicMock
import json
from password_manager import generate_password, encrypt_data, save_password, cipher  

class TestPasswordManager(unittest.TestCase):

    def test_generate_password(self):
        """Test password generation to ensure correct length and character mix."""
        password = generate_password()
        self.assertTrue(any(c.islower() for c in password), "Should contain lowercase letters")
        self.assertTrue(any(c.isupper() for c in password), "Should contain uppercase letters")
        self.assertTrue(any(c.isdigit() for c in password), "Should contain numbers")
        self.assertTrue(any(c in "!#$%&()*+" for c in password), "Should contain symbols")
        self.assertGreaterEqual(len(password), 12, "Password should be at least 12 characters long")

    def test_encrypt_data(self):
        """Test if encryption works correctly and returns a different value than input."""
        test_string = "securepassword"
        encrypted = encrypt_data(test_string)
        self.assertNotEqual(test_string, encrypted, "Encrypted text should not match input")

    @patch("builtins.open", new_callable=unittest.mock.mock_open, read_data='{}')
    @patch("json.load", return_value={})
    @patch("json.dump")
    def test_save_password(self, mock_json_dump, mock_json_load, mock_open):
        """Test save_password to ensure it writes encrypted data to a JSON file."""
        with patch("tkinter.Entry.get", side_effect=["test.com", "user@test.com", "securepass"]):
            save_password()

        mock_open.assert_called_once_with("data.json", "r")  # Ensure file is opened for reading
        mock_json_dump.assert_called_once()  # Ensure data is written
        args, _ = mock_json_dump.call_args
        saved_data = args[0]
        
        # Check if password is encrypted
        self.assertIn("test.com", saved_data)
        self.assertIn("password", saved_data["test.com"])
        self.assertNotEqual(saved_data["test.com"]["password"], "securepass", "Password should be encrypted")

if __name__ == "__main__":
    unittest.main()
