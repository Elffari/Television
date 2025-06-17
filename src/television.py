from channels import *
import vlc_helper
import vlc
import time

class Television:
    def __init__(self):
        self.volume = 50
        self.current_channel_name = "Yle TV1" # Store channel name
        self.is_on = False # Track power state
        self.player = None
        # self.channels = channels # Assuming 'channels' is defined globally or passed in

    def turn_on(self):
        if self.is_on and self.player and self.player.is_playing():
            print(f"TV is already on and playing {self.current_channel_name}.")
            return

        if self.player: # Stop existing player if any
            self.player.stop()
            self.player.release() # Release the player instance
            self.player = None

        channel_url = channels.get(self.current_channel_name)
        if not channel_url:
            print(f"Channel URL for {self.current_channel_name} not found.")
            self.is_on = False
            return

        self.player = vlc_helper.initialize_vlc_player(channel_url)

        if self.player:
            self.player.play()
            print(f"Playing stream: {self.current_channel_name}")
            self.is_on = True
            # Set volume (VLC player might reset volume on new media)
            self.player.audio_set_volume(self.volume)

            # Handle fullscreen. This might need to be threaded if non-blocking.
            # For simplicity, direct call here.
            time.sleep(2) # Allow player to initialize
            if self.player.is_playing():
                 self.player.set_fullscreen(True)
        else:
            print(f"Failed to turn on TV for channel {self.current_channel_name}.")
            self.is_on = False

    def turn_off(self):
        if self.player:
            self.player.stop()
            self.player.release() # Important to release VLC resources
            self.player = None
        self.is_on = False
        print("TV turned off.")

    def change_channel(self, new_channel_name):
        if new_channel_name not in channels:
            print(f"Channel {new_channel_name} not found.")
            return

        self.current_channel_name = new_channel_name
        print(f"Changing channel to {self.current_channel_name}.")
        if self.is_on:
            # Turn "off" (stop current stream) and then "on" (start new stream)
            self.turn_on() # This will stop current and start new
        else:
            # If TV is off, just set the channel, it will be used when turned on
            print(f"TV is off. Channel set to {self.current_channel_name}. Turn TV on to watch.")


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
            if state == vlc.State.Ended or state == vlc.State.Error:
                print(f"Playback for {self.current_channel_name} ended or encountered an error.")
                self.turn_off() # Or attempt to restart, etc.
        # This method would need to be called from your main application loop.