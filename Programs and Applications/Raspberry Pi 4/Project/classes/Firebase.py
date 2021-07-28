import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from time import time


class Firebase:
    def __init__(self):
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('certs/alticelabs_firebase.json')

        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://alticelabs-92294-default-rtdb.europe-west1.firebasedatabase.app/'
        })
        self.ref = db.reference("/raspberry/")
        self.esp_ref = db.reference("/ESP/")
        self.pc_ref = db.reference("/windows_pc/")
        self.last_check = time()

    def push_data(self, data_json):
        ref = self.ref.child("data")
        ref.push(data_json)

    def push_ergonomics_position_data(self, pos, time):
        ref = self.ref.child("data").child("user").child("position")
        ref.push({
            "position": pos,
            "time": time
        })

        ref = self.pc_ref.child("data").child("user").child("position")
        ref.set(pos)

    def push_ergonomics_body_temperature(self, body_temp, time):
        ref = self.ref.child("data").child("user").child("body_temperature")
        ref.push({
            "value": body_temp,
            "time": time
        })

        ref = self.pc_ref.child("data").child("user").child("body_temperature")
        ref.set(body_temp)

    def push_ergonomics_body_respiration(self, respiration, time):
        if respiration < 11:
            respiration = 0
        ref = self.ref.child("data").child("user").child("respiration_rate")
        ref.push({
            "value": respiration,
            "time": time
        })
        print(respiration)

        ref = self.pc_ref.child("data").child("user").child("respiration_rate")
        ref.set(respiration)

    def push_ergonomics_body_bpm(self, bpm, time):
        ref = self.ref.child("data").child("user").child("bpm")
        ref.push({
            "value": bpm,
            "time": time
        })
        print(bpm)

        ref = self.pc_ref.child("data").child("user").child("bpm")
        ref.set(bpm)

    def push_dht_data(self, temperature, humidity, time):
        ref = self.ref.child("data").child("environment").child("dht")
        ref.push({
            "temperature": temperature,
            "humidity": humidity,
            "time": time
        })

        ref = self.pc_ref.child("data").child("environment").child("humidity")
        ref.set(humidity)
        ref = self.pc_ref.child("data").child("environment").child("temperature")
        ref.set(temperature)

        # TODO: AC Control Block / Logic
        ...

    def push_mcp_data(self, brightness, co2, noise, time_):
        ref = self.ref.child("data").child("environment").child("mcp")
        
        ref_auto = self.esp_ref.child("Light").child("Auto")
        ref_on = self.esp_ref.child("Light").child("OnOff")
        ref_bright = self.esp_ref.child("Light").child("Bright")
        
        
        if ref_auto.get() == "ON":
            if ref_bright.get() == 0:
                if not 25000 < brightness < 40000:
                    if brightness < 25000:
                        if ref_on.get() == "ON":
                            ref_bright.set(1)
                        elif ref_on.get() == "OFF":
                            self.last_check = time()
                            ref_on.set("ON")
                    else:
                        if time() - self.last_check >= 30:
                            ref_on.set("OFF")
                        else:
                            ref_bright.set(-1)
                else:
                    self.last_check = time()
                    
        if brightness < 25000:
            brightness_text = "Escuro"
        elif brightness > 40000:
            brightness_text = "Claro"
        else:
            brightness_text = "Normal"
            
        if noise < 10000:
            noise_text = "Nenhum"
        elif noise < 20000:
            noise_text = "Baixo"
        elif noise < 30000:
            noise_text = "Médio"
        else:
            noise_text = "Alto"
        
        ref.push({
            "brightness": brightness,
            "co2": co2,
            "noise": noise,
            "time": time_
        })
        
        ref = self.pc_ref.child("data").child("environment").child("brightness")
        ref.set(brightness_text)
        ref = self.pc_ref.child("data").child("environment").child("co2")
        ref.set(co2)
        ref = self.pc_ref.child("data").child("environment").child("noise")
        ref.set(noise_text)
