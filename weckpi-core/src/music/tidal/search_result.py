import logging
from dataclasses import dataclass
from typing import Union

import tidalapi

logger = logging.getLogger('weckpi.music.tidal')


@dataclass(repr=False, eq=False, order=False, frozen=True, kw_only=True)
class SearchResult:
    """Represents the search result from Tidal"""
    top_hit: Union[tidalapi.Artist, tidalapi.Album, tidalapi.Track, tidalapi.Video, tidalapi.Playlist]
    artists: list[tidalapi.Artist]
    albums: list[tidalapi.Album]
    tracks: list[tidalapi.Track]
    videos: list[tidalapi.Video]
    playlists: list[tidalapi.Playlist]

    @staticmethod
    def from_api_result(api_result: dict) -> 'SearchResult':
        """Create a SearchResult from the API result"""
        return SearchResult(
            top_hit=api_result.get('top_hit', None),
            artists=api_result.get('artists', None),
            albums=api_result.get('albums', None),
            tracks=api_result.get('tracks', None),
            videos=api_result.get('videos', None),
            playlists=api_result.get('playlists', None)
        )
