"""Tests for the Tidal integration"""
import os
import unittest
from pathlib import Path

from music import tidal


class TidalTests(unittest.TestCase):
    """Tests for the Tidal integration"""
    def test_tidal_login(self):
        """Test, if the login works"""
        # Arrange
        # Remove the credentials file
        try:
            os.remove('tidal_credentials.json')
        except FileNotFoundError:
            pass

        # Act
        session = tidal.login(Path('tidal_credentials.json'))

        # Assert
        self.assertIsInstance(session, tidal.Session)
        self.assertTrue(session.check_login())


if __name__ == '__main__':
    unittest.main()
