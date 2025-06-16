import vlc
import time
import os
from channels import channels

# URL of the M3U8 stream
chosen_channel = channels["Yle TV1"]

def main():
    """Plays the specified M3U8 stream using VLC."""
    try:
        # Set the DISPLAY environment variable explicitly if needed
        # This helps VLC find the display server
        if 'DISPLAY' not in os.environ:
            os.environ['DISPLAY'] = ':0'

        # Create a VLC instance with Raspberry Pi optimized parameters
        vlc_args = [
            '--fullscreen',                # Enable fullscreen mode
            '--no-video-title-show',      # Hide the video title
            '--intf', 'dummy',            # Use dummy interface (no GUI)
            '--extraintf', 'http',        # Enable HTTP interface for control
            '--no-osd',                   # Disable on-screen display
            '--video-on-top',             # Keep video on top
            '--no-video-deco',            # Remove window decorations
            '--no-embedded-video',        # Don't embed video in interface
            '--vout', 'gl'               # Use OpenGL output (good for Pi 5)
        ]
        
        instance = vlc.Instance(*vlc_args)

        # Create a MediaPlayer object
        player = instance.media_player_new()

        # Create a Media object from the URL
        media = instance.media_new(chosen_channel)

        # Set the media for the player
        player.set_media(media)

        # Start playing the media
        player.play()

        print(f"Playing stream: {chosen_channel}")
        print("Press Ctrl+C to stop.")

        # Wait for media to start playing before setting fullscreen
        time.sleep(2)
        
        # Force fullscreen after playback starts
        player.set_fullscreen(True)

        # Keep the script running while the video plays
        while True:
            state = player.get_state()
            # Stop if playback ends or encounters an error
            if state == vlc.State.Ended or state == vlc.State.Error:
                break
            time.sleep(1) # Sleep to avoid busy waiting

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'player' in locals() and player:
            player.stop()
        print("Playback stopped.")

if __name__ == "__main__":
    main()
