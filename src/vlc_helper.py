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
