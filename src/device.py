from .television import Television

class Device:
    power_on = False

    def __init__(self, mqtt_client):
        self.mqtt = mqtt_client
        self.television = Television()

    def connected(self):
        # Get latest settings from Blynk.Cloud
        self.mqtt.publish("get/ds", "TV Power,TV Volume,TV Channel")

    def process_message(self, topic, payload):
        # Handle TV power
        if topic == "downlink/ds/TV Power":
            self.handle_power_command(payload)
            if payload == "1":
                self.television.turn_on()
            elif payload == "0":
                self.television.turn_off()

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
        if payload == 1:
            self.television.turn_on()
            print("TV turned on.")
        elif payload == 0:
            self.television.turn_off()
            print("TV turned off.")
