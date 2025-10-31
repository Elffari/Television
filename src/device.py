import threading
import random
import os
from .television import Television

class Device:
    power_on = False

    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.television = Television()

    def connected(self):
        # Get latest settings from Blynk.Cloud
        self.mqtt.publish("get/ds", "TV Power,TV Volume,TV Channel")

    def _play_phone_sequence(self):
        """Plays ring sound followed by random kid sound in a separate thread"""
        try:
            ring_sound = "src/Assets/Ring/puhelin2.mp3"
            kid_sounds_dir = "src/Assets/Kids"
            
            kid_sounds = [
                os.path.join(kid_sounds_dir, f) 
                for f in os.listdir(kid_sounds_dir)
                if f.endswith(('.mp3', '.wav', '.m4a'))
            ]
            
            sounds_to_play = [ring_sound]
            if kid_sounds:
                random_kid_sound = random.choice(kid_sounds)
                sounds_to_play.append(random_kid_sound)
                print(f"Playing kid sound: {random_kid_sound}")

            print(f"Sound sequence to play: {sounds_to_play}")
            self.television.play_sequence(sounds_to_play)
            
        except Exception as e:
            print(f"Phone sequence error: {e}")

    def process_message(self, topic, payload):
        # Handle TV power
        if topic == "downlink/ds/TV Power":
            self.handle_power_command(payload)

        # Handle TV volume
        elif topic == "downlink/ds/TV Volume":
            try:
                volume = int(payload)
                self.television.set_volume(volume)
            except ValueError as e:
                print(f"Error setting TV volume: {e}")

        # Handle TV channel
        elif topic == "downlink/ds/TV Channel":
            try:
                self.television.change_channel(payload)
            except ValueError as e:
                print(f"Error changing TV channel: {e}")

        # Handle Phone call
        elif topic == "downlink/ds/Ring":
            # Play sounds in background thread
            threading.Thread(target=self._play_phone_sequence, daemon=True).start()

        # Handle unknown topics
        else:
            print(f"Unknown topic: {topic}. Payload: {payload}")

    def update(self):
        # This method can be used to update the device state or perform periodic tasks
        # Like this:
        # self._update_temperature()
        # self._update_widget_state()
        self.television.check_player_status()
        pass

    def handle_power_command(self, payload):
        if payload == "1":
            self.television.turn_on()
            print("TV turned on.")
        elif payload == "0":
            self.television.turn_off()
            print("TV turned off.")
