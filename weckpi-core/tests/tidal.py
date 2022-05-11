"""Tests for the Tidal integration"""
import os
import unittest
from pathlib import Path

import tidalapi

from music.tidal import TidalSession


class TidalTests(unittest.TestCase):
    """Tests for the Tidal integration"""
    # TODO: Expand testing
    _shared_session: TidalSession = None

    @property
    def shared_session(self) -> TidalSession:
        """
                Create a shared session, so we will not repeatedly send login requests

                :return: The shared session
                """
        if self._shared_session is None:
            self._shared_session = TidalSession().login(Path('tidal_credential.yaml'))
        return self._shared_session

    @unittest.skip('Testing')
    def test_login(self):
        """Test if the login works"""
        # Arrange
        try:
            # Remove the credential file
            os.remove('tidal_credential.yaml')
        except FileNotFoundError:
            pass

        # Act
        # Log in with the link
        session1 = TidalSession().login(Path('tidal_credential.yaml'))
        # Log in with the credential file
        session2 = TidalSession().login(Path('tidal_credential.yaml'))

        # Assert
        self.assertIsInstance(session1.session, tidalapi.Session)
        self.assertTrue(session1.is_logged_in())

        self.assertIsInstance(session2.session, tidalapi.Session)
        self.assertTrue(session2.is_logged_in())

    def test_search(self):
        """Test if the search works as expected"""
        # Arrange
        search_term = 'vnv nation'

        # Act
        results = self.shared_session.search(search_term)

        # Assert
        self.assertEqual('VNV Nation', results.artists[0].name)


if __name__ == '__main__':
    unittest.main()
