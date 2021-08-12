"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, given_name):
        """Video playlist constructor."""
        self.name = given_name
        self.video_list = []

    def add_video(self, new_video):
        """Adds video to playlist.

        Args:
            new_video: The id of the video to be added.
        """
        self.video_list.append(new_video)

    def video_in_playlist(self, video_to_check):
        """Checks if video is in playlist.

        Args:
            video_to_check: The id of the video to check.
        """
        if video_to_check in self.video_list:
            return True
        else:
            return False

    def remove_video(self, video_to_remove):
        """Removes video from playlist.

        Args:
            video_to_remove: The id of the video to be removed.
        """
        self.video_list.remove(video_to_remove)

    def clear(self):
        """ Removes all videos from playlist"""
        self.video_list = []
        
