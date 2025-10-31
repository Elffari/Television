from .channels import *
from . import vlc_helper
import os
import vlc
import time

class Television:
    def __init__(self):
        self.volume = 100
        self.current_channel = "24" # Default channel index
        self.is_on = False # Track power state
        self.player = None

    def turn_on(self):
        if self.is_on and self.player and self.player.is_playing():
            print(f"TV is already on and playing.")
            return

        if self.player: # Stop existing player if any
            self.player.stop()
            self.player.release() # Release the player instance
            self.player = None

        channel_name, channel_url = channels.get(self.current_channel)
        if not channel_url:
            print(f"Channel URL for {channel_name} not found.")
            self.is_on = False
            return

        self.player = vlc_helper.initialize_vlc_player(channel_url)

        if self.player:
            self.player.play()
            print(f"Playing stream: {channel_name}")
            self.is_on = True
            # Set volume (VLC player might reset volume on new media)
            self.player.audio_set_volume(self.volume)

            # Handle fullscreen. This might need to be threaded if non-blocking.
            # For simplicity, direct call here.
            time.sleep(2) # Allow player to initialize
            try:
                if self.player.is_playing():
                    self.player.set_fullscreen(True)
            except Exception as e:
                print(f"Error setting fullscreen: {e}")
        else:
            print(f"Failed to turn on TV for channel {channel_name}.")
            self.is_on = False

    def turn_off(self):
        if self.player:
            self.player.stop()
            self.player.release() # Important to release VLC resources
            self.player = None
        self.is_on = False
        print("TV turned off.")

    def change_channel(self, payload: str):
        # Check if the TV is on before changing channels
        if not self.is_on:
            print("TV is off. Please turn it on first.")
            return

        # Check if player instance exists
        if not self.player:
            print("No player instance available. Cannot change channel.")
            return

        try:
            # Use .get() for a safe lookup
            channel_data = channels.get(payload)

            if channel_data:
                channel_name, url = channel_data
                print(f"Changing to channel: {channel_name}")

                success = vlc_helper.change_channel(self.player, url)

                if success:
                    print(f"Now playing: {channel_name}")
                else:
                    print("Failed to change channel.")
            else:
                print(f"Channel {payload} not found in the channel list.")
        except (KeyError, IndexError):
            print(f"Invalid channel index: {payload}")

    def set_volume(self, volume_level):
        if 0 <= volume_level <= 100:
            self.volume = volume_level
            if self.player and self.is_on:
                self.player.audio_set_volume(self.volume)
            print(f"Volume set to {self.volume}")
        else:
            print("Volume must be between 0 and 100.")

    # You might add an update method to check player state periodically
    # if you need to handle unexpected stops or other events.
    def check_player_status(self):
        if self.is_on and self.player:
            state = self.player.get_state()
            if state == vlc.State.Error:
                print(f"Playback encountered an error. Shutting down TV.")
                self.turn_off()
            elif state == vlc.State.Ended:
                print(f"Playback ended normally.")
                # Don't turn off - TV stays on
        # This method would need to be called from your main application loop.

    def play_sequence(self, media_files):
        """
        Plays a sequence of media files one after another.
        
        Args:
            media_files: List of file paths to play in sequence
        """
        if not self.player:
            print("No player instance available.")
            return
        
        for media_file in media_files:
            if not os.path.exists(media_file):
                print(f"Media file not found: {media_file}")
                continue
                
            try:
                instance = self.player.get_instance()
                media = instance.media_new(media_file)
                self.player.set_media(media)
                self.player.play()
                
                # Wait for the media to finish playing
                while self.player.get_state() not in [vlc.State.Ended, vlc.State.Error, vlc.State.Stopped]:
                    time.sleep(0.1)
                    
                print(f"Finished playing: {media_file}")
            except Exception as e:
                print(f"Error playing {media_file}: {e}")
