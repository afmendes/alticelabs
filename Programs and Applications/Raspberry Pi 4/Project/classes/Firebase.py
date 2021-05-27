import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class Firebase:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('certs/alticelabs_firebase.json')

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://alticelabs-92294-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.ref = db.reference("/raspberry/")
        self.esp_ref = db.reference("/esp8266/")
        self.pc_ref = db.reference("/windows_pc/")

    def push_data(self, data_json):
        ref = self.ref.child("data")
        ref.push(data_json)

    def push_ergonomics_position_data(self, pos, time):
        ref = self.ref.child("data").child("ergonomics").child("position")
        ref.push({
            "position": pos,
            "time": time
        })

        ref = self.pc_ref.child("data").child("position")
        ref.set(pos)

    def push_ergonomics_body_temperature(self, body_temp, time):
        ref = self.ref.child("data").child("ergonomics").child("body_data").child("body_temperature")
        ref.push({
            "value": body_temp,
            "time": time
        })

        ref = self.pc_ref.child("data").child("body_temperature")
        ref.set(body_temp)

    def push_ergonomics_body_respiration(self, respiration, time):
        ref = self.ref.child("data").child("ergonomics").child("body_data").child("respiration_rate")
        ref.push({
            "value": respiration,
            "time": time
        })

        ref = self.pc_ref.child("data").child("respiration_rate")
        ref.set(respiration)

    def push_ergonomics_body_bpm(self, bpm, time):
        ref = self.ref.child("data").child("ergonomics").child("body_data").child("bpm")
        ref.push({
            "value": bpm,
            "time": time
        })

        ref = self.pc_ref.child("data").child("bpm")
        ref.set(bpm)

    def push_dht_data(self, temperature, humidity, time):
        ref = self.ref.child("data").child("sensors").child("dht")
        ref.push({
            "temperature": temperature,
            "humidity": humidity,
            "time": time
        })

        ref = self.pc_ref.child("data").child("humidity")
        ref.set(humidity)
        ref = self.pc_ref.child("data").child("temperature")
        ref.set(temperature)

    def push_mcp_data(self, luminosity, co2, noise, time):
        ref = self.ref.child("data").child("sensors").child("dht")
        ref.push({
            "luminosity": luminosity,
            "co2": co2,
            "noise": noise,
            "time": time
        })

        ref = self.pc_ref.child("data").child("luminosity")
        ref.set(luminosity)
        ref = self.pc_ref.child("data").child("co2")
        ref.set(co2)
        ref = self.pc_ref.child("data").child("noise")
        ref.set(noise)
