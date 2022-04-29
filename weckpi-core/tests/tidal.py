import unittest
from music import tidal
from pathlib import Path
import os


class TidalTests(unittest.TestCase):
    def test_tidal_login(self):
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
