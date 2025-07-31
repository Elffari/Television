import os
import vlc

def initialize_vlc_player(channel_url):
    """Initializes a VLC player instance for the given channel URL."""
    if 'DISPLAY' not in os.environ:
        os.environ['DISPLAY'] = ':0'

    vlc_args = [
        '--fullscreen',
        '--no-video-title-show',
        '--intf', 'dummy',
        '--extraintf', 'http',
        '--no-osd',
        '--video-on-top',
        '--no-video-deco',
        '--no-embedded-video',
        '--vout', 'gl'
    ]
    try:
        instance = vlc.Instance(*vlc_args)
        player = instance.media_player_new()
        media = instance.media_new(channel_url)
        player.set_media(media)
        return player
    except Exception as e:
        print(f"Error initializing VLC player: {e}")
        return None


def change_channel(player, new_channel_url):
    """
    Changes the channel on an existing VLC player instance.

    Args:
        player: The VLC player instance
        new_channel_url: URL of the new channel to play

    Returns:
        True if successful, False otherwise
    """
    if player is None:
        return False

    if new_channel_url is None:
        print("New channel URL is None.")
        return False

    try:
        # Get the VLC instance from the player
        instance = player.get_instance()

        # Create a new media object with the new URL
        media = instance.media_new(new_channel_url)

        # Set the new media to the player
        player.set_media(media)

        # Start playing the new channel
        player.play()
        return True
    except Exception as e:
        print(f"Error changing channel: {e}")
        return False
