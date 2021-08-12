"""A video player class."""

import random
from .video_library import VideoLibrary
from .video_playlist import Playlist


class VideoPlayer:
    """A class used to represent a Video Player."""
    
    def __init__(self):
        """Video player constructor."""
        self._video_library = VideoLibrary()
        self.current_video = None
        self.video_paused = False
        self.playlists = []

    def get_playlist_by_name(self, name):
        """Gets playlist with the given name.

        Args:
            name: The name of the playlist to retrieve.
        """
        
        correct_playlist = None
        i = 0
        while correct_playlist == None and i < len(self.playlists):
            if self.playlists[i].name.upper() == name.upper():
                correct_playlist = self.playlists[i]
            i += 1
        return correct_playlist

    def get_tag_string(self, video):
        """Adds tags from a video to a string to be displayed.

        Args:
            video: The video to extract the tags from.
        """
        
        string = " "
        for tag in video.tags:
            string += tag
            string += " "
        return string

    def display_search_results(self, video_list, search_criteria):
        """Displays the results of searching by a search term or by a tag.

        Args:
            video_list: The list of videos to display.
            search_criteria: The criteria used to search for videos.
        """
        
        if len(video_list) == 0:
            print("No search results for " + search_criteria)
        else:
            print("Here are the results for " + search_criteria + ":")
            video_list.sort(key=lambda x:x.title)
            i = 0
            while i < len(video_list):
                if video_list[i].flag != None:
                    video_list[i] = None
                i += 1
            counter = 0
            
            for i in range(0, len(video_list)):
                if video_list[i] != None:
                    counter += 1
                    tag_string = self.get_tag_string(video_list[i])
                    print(str(counter) + ") " + video_list[i].title + " (" + video_list[i].video_id + ") [" + tag_string.strip() + "]")  

            print("Would you like to play any of the above? If yes, specify the number of the video.")
            print("If your answer is not a valid number, we will assume it's a no.")
            user_input = input()
            if user_input.isdigit():
                user_input = int(user_input)
                if user_input <= len(video_list):
                    self.play_video(video_list[user_input-1].video_id)
      
    def number_of_videos(self):
        """Displays number of videos."""
        
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        
        print("Here's a list of all available videos:")
        
        all_videos = self._video_library.get_all_videos()
        all_videos.sort(key=lambda x:x.title)
        for i in range(0, len(all_videos)):
            tag_string = self.get_tag_string(all_videos[i])           
            if all_videos[i].flag == None:
                print(all_videos[i].title + " (" + all_videos[i].video_id + ") [" + tag_string.strip() + "]")  
            else:
                print(all_videos[i].title + " (" + all_videos[i].video_id + ") [" + tag_string.strip() + "] - FLAGGED (reason: " + all_videos[i].flag + ")")

    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        
        video_to_play = self._video_library.get_video(video_id)
        if video_to_play == None:
            print("Cannot play video: Video does not exist")
        else:
            if video_to_play.flag == None:
                if self.current_video != None:
                    print("Stopping video: " + self.current_video.title)
                print("Playing video: " + video_to_play.title)
                self.current_video = video_to_play
                self.video_paused = False
            else:
                print("Cannot play video: Video is currently flagged (reason: " + video_to_play.flag + ")")

    def stop_video(self):
        """Stops the current video."""
        
        if self.current_video == None:
            print("Cannot stop video: No video is currently playing")
        else:
            print("Stopping video: " + self.current_video.title)
            self.current_video = None
            
    def play_random_video(self):
        """Plays a random video from the video library."""

        all_videos = self._video_library.get_all_videos()
        i = 0
        while i < len(all_videos):
            if all_videos[i].flag != None:
                all_videos[i] = None
            i += 1
  
        if len(all_videos) == 0 or all(x is None for x in all_videos):
            print("No videos available")
        else:
            random_video = random.choice(all_videos)
            if self.current_video != None:
                print("Stopping video: " + self.current_video.title)
            print("Playing video: " + random_video.title)
            self.current_video = random_video
            self.video_paused = False

    def pause_video(self):
        """Pauses the current video."""

        if self.current_video == None:
            print("Cannot pause video: No video is currently playing")
        else:
            if self.video_paused == False:
                print("Pausing video: " + self.current_video.title)
                self.video_paused = True
            else:
                print("Video already paused: " + self.current_video.title)      

    def continue_video(self):
        """Resumes playing the current video."""

        if self.current_video == None:
            print("Cannot continue video: No video is currently playing")
        else:
            if self.video_paused == True:
                print("Continuing video: " + self.current_video.title)
                self.video_paused = False
            else:
                print("Cannot continue video: Video is not paused")

    def show_playing(self):
        """Displays video currently playing."""

        if self.current_video == None:
            print("No video is currently playing")
        else:
            video_playing = self._video_library.get_video(self.current_video.video_id)
            tag_string = self.get_tag_string(video_playing)
            if self.video_paused == False:
                print("Currently playing: " + video_playing.title + " (" + video_playing.video_id + ") [" + tag_string.strip() + "]")
            else:
                print("Currently playing: " + video_playing.title + " (" + video_playing.video_id + ") [" + tag_string.strip() + "] - PAUSED")
                
    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        same_name = self.get_playlist_by_name(playlist_name)
        if same_name == None:
            new_playlist = Playlist(playlist_name)
            self.playlists.append(new_playlist)
            print("Successfully created new playlist: " + playlist_name)
        else:
            print("Cannot create playlist: A playlist with the same name already exists")
            
    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        current_playlist = self.get_playlist_by_name(playlist_name)
        video_to_add = self._video_library.get_video(video_id)

        if current_playlist == None:
            print("Cannot add video to " + playlist_name + ": Playlist does not exist")
        else:
            if video_to_add == None:
                print("Cannot add video to " + playlist_name + ": Video does not exist")
            else:
                if video_to_add.flag == None:
                    if current_playlist.video_in_playlist(video_id) == True:
                        print("Cannot add video to " + playlist_name + ": Video already added")
                    else:
                        current_playlist.add_video(video_id)
                        print("Added video to " + playlist_name + ": " + self._video_library.get_video(video_id).title)
                else:
                    print("Cannot add video to " + playlist_name + ": Video is currently flagged (reason: " + video_to_add.flag + ")")

    def show_all_playlists(self):
        """Display all playlists."""

        if len(self.playlists) == 0:
            print("No playlists exist yet")
        else:
            self.playlists.sort(key=lambda x:x.name)
            print("Showing all playlists:")
            for playlist in self.playlists:
                print(playlist.name)

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        current_playlist = self.get_playlist_by_name(playlist_name)

        if current_playlist == None:
            print("Cannot show playlist " + playlist_name + ": Playlist does not exist")
        else:
            print("Showing playlist: " + playlist_name)
            if len(current_playlist.video_list) == 0:
                print("No videos here yet")
            else:
                for video_id in current_playlist.video_list:
                    video = self._video_library.get_video(video_id)
                    tag_string = self.get_tag_string(video)
                    if video.flag == None:
                        print(video.title + " (" + video.video_id + ") [" + tag_string.strip() + "]")  
                    else:
                        print(video.title + " (" + video.video_id + ") [" + tag_string.strip() + "] - FLAGGED (reason: " + video.flag + ")")

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """
        current_playlist = self.get_playlist_by_name(playlist_name)
        if current_playlist == None:
            print("Cannot remove video from " + playlist_name + ": Playlist does not exist")
        else:
            video_to_remove = self._video_library.get_video(video_id)
            if video_to_remove == None:
                print("Cannot remove video from " + playlist_name + ": Video does not exist")
            else:
                if current_playlist.video_in_playlist(video_to_remove.video_id) == True:
                    current_playlist.remove_video(video_to_remove.video_id)
                    print("Removed video from " + playlist_name + ": " + video_to_remove.title)
                else:
                    print("Cannot remove video from " + playlist_name + ": Video is not in playlist")               

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        current_playlist = self.get_playlist_by_name(playlist_name)
        if current_playlist == None:
            print("Cannot clear playlist " + playlist_name + ": Playlist does not exist")
        else:
            current_playlist.clear()
            print("Successfully removed all videos from " + playlist_name)

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        
        current_playlist = self.get_playlist_by_name(playlist_name)
        if current_playlist == None:
            print("Cannot delete playlist " + playlist_name + ": Playlist does not exist")
        else:
            self.playlists.remove(current_playlist)
            print("Deleted playlist: " + playlist_name)

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """
        
        all_videos = self._video_library.get_all_videos()
        videos_to_show = []
        for video in all_videos:
            if search_term.upper() in video.title.upper():
                videos_to_show.append(video)
        self.display_search_results(videos_to_show, search_term)

    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """
        
        all_videos = self._video_library.get_all_videos()
        videos_to_show = []
        for video in all_videos:
            if video_tag.lower() in video.tags:
                videos_to_show.append(video)
        self.display_search_results(videos_to_show, video_tag)

    def flag_video(self, video_id, flag_reason=""):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        video_to_flag = self._video_library.get_video(video_id)
        if video_to_flag == None:
            print("Cannot flag video: Video does not exist")
        else:
            if video_to_flag.flag == None:
                if self.current_video != None:
                    if self.current_video.video_id == video_id:
                        self.stop_video()
                if flag_reason == "":
                    video_to_flag.set_flag("Not supplied")
                else:
                    video_to_flag.set_flag(flag_reason)
                print("Successfully flagged video: " + video_to_flag.title + " (reason: " + video_to_flag.flag + ")")
            else:
                print("Cannot flag video: Video is already flagged")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """
        video_to_allow = self._video_library.get_video(video_id)
        if video_to_allow == None:
            print("Cannot remove flag from video: Video does not exist")
        else:
            if video_to_allow.flag != None:
                video_to_allow.set_flag(None)
                print("Successfully removed flag from video: " + video_to_allow.title)
            else:
                print("Cannot remove flag from video: Video is not flagged")
