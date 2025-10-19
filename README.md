# Television

## Sources for iptv (.m3u8)

https://iptv-org.github.io/


## Config file that needs to be added

```py
# Fill in information from Blynk Device Info here.
BLYNK_TEMPLATE_ID   = ""
BLYNK_TEMPLATE_NAME = ""
BLYNK_AUTH_TOKEN    = ""

# Change the default Blynk server. Applicable for users with a white label plan.
BLYNK_MQTT_BROKER   = "blynk.cloud"
#fra1.blynk.cloud – Frankfurt
#lon1.blynk.cloud – London
#ny3.blynk.cloud – New York
#sgp1.blynk.cloud – Singapore
#blr1.blynk.cloud – Bangalore
```

## Move Systemd Service file to /etc/systemd/system