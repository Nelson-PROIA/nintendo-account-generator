import string
import unittest
from unittest.mock import patch

from nintendo_account_generator.utils import generate_username, generate_email, generate_password


class TestEmailGeneration(unittest.TestCase):

    @patch('random.randint')
    @patch('random.choices')
    def test_generate_username(self, mock_choices, mock_randint):
        # Mock the randint to return fixed values for testing
        mock_randint.side_effect = [5, 8, 4, 6]  # 5-8 letters, 4-6 digits

        # Mock the random.choices to return specific characters
        mock_choices.side_effect = [
            ['a', 'b', 'c', 'd', 'e'],  # 5 letters
            ['1', '2', '3', '4'],  # 4 digits
        ]

        username = generate_username(min_letters=5, max_letters=8, min_digits=4, max_digits=6)

        # Check that the username is generated correctly
        self.assertEqual(username, 'abcde1234')

    @patch('requests.get')
    def test_generate_email_success(self, mock_get):
        # Prepare mock response
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = ["domain1.com", "domain2.com"]

        # Test for a valid username
        email = generate_email("username")

        # Check that the email is generated correctly
        self.assertIn("@", email)
        self.assertIn("username", email)
        self.assertTrue(email.endswith("@domain1.com") or email.endswith("@domain2.com"))

    @patch('requests.get')
    def test_generate_email_failure_no_domains(self, mock_get):
        # Prepare mock response with no domains
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = []

        with self.assertRaises(RuntimeError):
            generate_email("username")

    @patch('requests.get')
    def test_generate_email_failure_request_error(self, mock_get):
        # Prepare mock response with a failed request
        mock_response = mock_get.return_value
        mock_response.status_code = 500

        with self.assertRaises(RuntimeError):
            generate_email("username")

    def test_generate_password(self):
        # Test password generation with default length (12)
        password = generate_password()

        # Check that the password is of correct length
        self.assertEqual(len(password), 12)
        self.assertTrue(all(c in string.ascii_letters + string.digits + string.punctuation for c in password))

        # Test password generation with a custom length
        password_custom = generate_password(16)
        self.assertEqual(len(password_custom), 16)


if __name__ == '__main__':
    unittest.main()
