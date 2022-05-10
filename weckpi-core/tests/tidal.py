"""Tests for the Tidal integration"""
import os
import unittest
from pathlib import Path

import tidalapi

from music import tidal


class TidalTests(unittest.TestCase):
    """Tests for the Tidal integration"""

    def test_tidal_login(self):
        """Test if the login works"""
        # Arrange
        try:
            # Remove the credential file
            os.remove('tidal_credential.yaml')
        except FileNotFoundError:
            pass

        # Act
        # Log in with the link
        session1 = tidal.TidalSession().login(Path('tidal_credential.yaml'))
        # Log in with the credential file
        session2 = tidal.TidalSession().login(Path('tidal_credential.yaml'))

        # Assert
        self.assertIsInstance(session1.session, tidalapi.Session)
        self.assertTrue(session1.is_logged_in())

        self.assertIsInstance(session2.session, tidalapi.Session)
        self.assertTrue(session2.is_logged_in())


if __name__ == '__main__':
    unittest.main()
