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
        self.rasp_ref = db.reference("/raspberry/")
        # self.esp_ref = db.reference("/esp8266/")
        self.esp_ref = db.reference("/ESP/")
        self.ref = db.reference("/windows_pc/")

    def lights_off(self):
        "commands/luminosity/on_off"
        ref = self.esp_ref.child("Light").child("OnOff")
        ref.set("OFF")

    def lights_on(self):
        "commands/luminosity/on_off"
        ref = self.esp_ref.child("Light").child("OnOff")
        ref.set("ON")

    def lights_toggle(self):
        "commands/luminosity/on_off"
        ref = self.esp_ref.child("Light").child("OnOff")
        if ref.get() == "ON":
            ref.set("OFF")
        else:
            ref.set("ON")

    def lights_state(self):
        "commands/luminosity/on_off"
        ref = self.esp_ref.child("Light").child("OnOff")
        return ref.get()

    def lights_brighter(self):
        "commands/luminosity/bright"
        ref = self.esp_ref.child("Light").child("Bright")
        ref.set(1)

    def lights_darker(self):
        "commands/luminosity/bright"
        ref = self.esp_ref.child("Light").child("Bright")
        ref.set(-1)

    def lights_auto_toggle(self):
        "commands/luminosity/automatic"
        ref = self.esp_ref.child("Light").child("Auto")
        if ref.get() == "ON":
            ref.set("OFF")
        else:
            ref.set("ON")

    def lights_auto_state(self):
        ref = self.esp_ref.child("Light").child("Auto")
        return ref.get()


