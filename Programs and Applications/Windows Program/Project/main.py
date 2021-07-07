from tkinter import *
from PIL import ImageTk, Image
from playsound import playsound
from threading import Thread
from time import sleep

from classes.Firebase import Firebase

firebase = Firebase()


class Line:
    def __init__(self, master, text, var, bg, first=False, last=False):
        if first:
            Label(master, text=text, font=("Times", 20), bg=bg, width=20, anchor=W).pack(
                side=LEFT, fill=BOTH, expand=TRUE, padx=(2, 1), pady=(2, 1))
            Label(master, textvariable=var, font=("Times", 20), bg=bg, width=5, anchor=W).pack(
                side=RIGHT, fill=BOTH, expand=TRUE, padx=(1, 2), pady=(2, 1))
        elif last:
            Label(master, text=text, font=("Times", 20), bg=bg, width=20, anchor=W).pack(
                side=LEFT, fill=BOTH, expand=TRUE, padx=(2, 1), pady=(1, 2))
            Label(master, textvariable=var, font=("Times", 20), bg=bg, width=5, anchor=W).pack(
                side=RIGHT, fill=BOTH, expand=TRUE, padx=(1, 2), pady=(1, 2))
        else:
            Label(master, text=text, font=("Times", 20), bg=bg, width=20, anchor=W).pack(
                side=LEFT, fill=BOTH, expand=TRUE, padx=(2, 1), pady=1)
            Label(master, textvariable=var, font=("Times", 20), bg=bg, width=5, anchor=W).pack(
                side=RIGHT, fill=BOTH, expand=TRUE, padx=(1, 2), pady=1)


class Table:
    def __init__(self, master, data: dict, bg, bg2):
        size = len(data.values())
        count = 0
        for x, i in data.items():
            count += 1
            frame = Frame(master, bg=bg, width=1000)
            frame.pack(fill=BOTH, expand=TRUE)
            if count == 1:
                Line(frame, x, i, bg2, first=True)
            elif count == size:
                Line(frame, x, i, bg2, last=True)
            else:
                Line(frame, x, i, bg2)


class LightControl(Toplevel):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.auto_state = None
        self.on_off_state = None

        self.top_frame = Frame(self)
        self.top_frame.pack()

        self.auto_button = Button(self.top_frame, text="Automatic", font=("Times", 20), command=self.auto_button_func)
        self.auto_button.pack()

        self.mid_frame = Frame(self)
        self.mid_frame.pack(fill=BOTH, expand=TRUE)

        self.on_off_button = Button(self.mid_frame, text="ON/OFF", font=("Times", 20), command=self.on_off_button_func)
        self.on_off_button.pack()

        self.bottom_frame = Frame(self)
        self.bottom_frame.pack(fill=BOTH, expand=TRUE)

        self.brighter_button = Button(self.bottom_frame, text="Brighter", font=("Times", 20), command=self.brighter_button_func)
        self.brighter_button.pack(side=LEFT)

        self.darker_button = Button(self.bottom_frame, text="Darker", font=("Times", 20), command=self.darker_button_func)
        self.darker_button.pack(side=RIGHT)

        self.update_state()

    def auto_button_func(self):
        firebase.lights_auto_toggle()
        self.update_state()

    def on_off_button_func(self):
        firebase.lights_toggle()
        self.update_state()

    def brighter_button_func(self):
        firebase.lights_brighter()
        self.update_state()

    def darker_button_func(self):
        firebase.lights_darker()
        self.update_state()

    def update_state(self):
        self.auto_state = firebase.lights_auto_state()
        if self.auto_state == "ON":
            self.auto_button.configure(bg="green")
            self.on_off_button.configure(bg="gray")
            self.on_off_button.configure(state=DISABLED)
            self.brighter_button.configure(state=DISABLED)
            self.darker_button.configure(state=DISABLED)
            pass
        elif self.auto_state == "OFF":

            self.auto_button.configure(bg="red")
            self.on_off_button.configure(state=NORMAL)
            self.brighter_button.configure(state=NORMAL)
            self.darker_button.configure(state=NORMAL)
            self.on_off_state = firebase.lights_state()
            if self.on_off_state == "ON":
                self.on_off_button.configure(bg="green")
            elif self.on_off_state == "OFF":
                self.on_off_button.configure(bg="red")


def arrange_data(data: dict):
    for x, i in data.items():
        if type(i) == str:
            data[x] = StringVar()
            data[x].set(i)


def window():
    def custom_toast(pos: int = 1):
        image_paths = [
            ["images/sentado_direito.png", "images/inclinado_direito.png"],  # position 1
            ["images/sentado_direito.png", "images/inclinado_frente.png"],  # position 2
            ["images/sentado_direito.png", "images/inclinado_frente.png"],  # position 3
            ["images/sentado_direito.png", "images/inclinado_tras.png"],  # position 4
            ["images/inclinado_direita.png", "images/inclinado_direito.png"],  # position 5
            ["images/inclinado_esquerda.png", "images/inclinado_direito.png"],  # position 6
            ["images/perna_direita_cruzada.png", "images/inclinado_direito.png"],  # position 7
            ["images/perna_esquerda_cruzada.png", "images/inclinado_direito.png"],  # position 8
        ]

        # front view -> side view
        position_image1, position_image2 = image_paths[pos - 1]

        def countdown(time):
            if time == -1:
                custom_root.destroy()
            else:
                custom_root.after(1000, countdown, time - 1)

        custom_root = Tk()
        custom_root.title("Alerta!")
        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w = int(ws/5)
        h = int(hs/4)
        custom_root.geometry('%dx%d+%d+%d' % (w, h, ws - w - 10, hs - h - 100))

        image1 = Image.open(position_image1)
        image1 = image1.resize((int(w/2 - 20), int(h - 60)), Image.ANTIALIAS)
        image1canvas = ImageTk.PhotoImage(image1, master=custom_root)

        image2 = Image.open(position_image2)
        image2 = image2.resize((int(w/2 - 20), int(h - 60)), Image.ANTIALIAS)
        image2canvas = ImageTk.PhotoImage(image2, master=custom_root)

        canvas = Canvas(custom_root, width=int(w), height=int(h-50))
        canvas.pack(fill=BOTH, expand=True)

        canvas.create_image(10, 10, anchor="nw", image=image1canvas)
        canvas.create_image(int(w-10), 10, anchor="ne", image=image2canvas)

        label = Label(custom_root, width=30)
        label.configure(bg="pink")
        label.pack(fill=BOTH, expand=True)
        label.configure(text="POSIÇAO INCORRETA")

        countdown(5)

        # C:\Windows\Media\Windows Message Nudge.wav
        playsound("C:/Windows/Media/Windows Message Nudge.wav", block=False)

        custom_root.mainloop()

    def on_closing():
        print("killing processes")
        root.destroy()

    def update():
        user_ref = firebase.user_ref
        user_ref.listen(user_ref_update)
        env_ref = firebase.env_ref
        env_ref.listen(env_ref_update)

    def user_ref_update(Event):
        path = Event.path
        data = Event.data
        if path == "/body_temperature":
            user_data["Temperatura"].set(data)
        elif path == "/bpm":
            user_data["Frequência cardíaca"].set(data)
        elif path == "/respiration_rate":
            user_data["Frequência respiratória"].set(data)
        elif path == "/position":
            if data != 1:
                custom_toast(data)
        elif path == "/":
            temp_data = data["body_temperature"]
            bpm_data = data["bpm"]
            rr_data = data["respiration_rate"]
            pos_data = data["position"]
            user_data["Temperatura"].set(temp_data)
            user_data["Frequência cardíaca"].set(bpm_data)
            user_data["Frequência respiratória"].set(rr_data)
            if pos_data != 1:
                custom_toast(data)

    def env_ref_update(Event):
        path = Event.path
        data = Event.data
        if path == "/brightness":
            ambient_data["Luminosidade"].set(data)
        elif path == "/co2":
            ambient_data["CO2"].set(data)
        elif path == "/humidity":
            ambient_data["Humidade relativa"].set(data)
        elif path == "/noise":
            ambient_data["Ruído"].set(data)
        elif path == "/temperature":
            ambient_data["Temperatura"].set(data)
        elif path == "/":
            env_brightness = data["brightness"]
            env_co2 = data["co2"]
            env_humidity = data["humidity"]
            env_noise = data["noise"]
            temperature = data["temperature"]
            ambient_data["Luminosidade"].set(env_brightness)
            ambient_data["CO2"].set(env_co2)
            ambient_data["Humidade relativa"].set(env_humidity)
            ambient_data["Ruído"].set(env_noise)
            ambient_data["Temperatura"].set(temperature)

    def lum_button_func():
        # ac_control(root)
        LightControl(root)

    root = Tk()
    root.geometry("450x600")
    root.resizable(False, False)
    root.configure(bg="white")

    # - Left Side
    left_side = Frame(root, bg="#d9d9d9")
    left_side.pack(side=LEFT, expand=TRUE, fill=BOTH)

    # -- Ambient
    text = "Informação sobre o ambiente"
    ambient_text_frame = Frame(left_side)
    ambient_text_frame.pack(expand=TRUE, fill=BOTH)
    ambient_text_label = Label(ambient_text_frame, text=text, font=("Times", 20), fg="#0070c0", bg="#d9d9d9")
    ambient_text_label.pack(expand=TRUE, fill=BOTH)

    ambient_data = {
        "Temperatura": "xx",
        "Humidade relativa": "xx",
        "Ruído": "xx",
        "Luminosidade": "xx",
        "CO2": "xx"
    }
    arrange_data(ambient_data)

    ambient_table_frame = Frame(left_side)
    ambient_table_frame.pack(pady=5)

    ambient_table = Table(ambient_table_frame, ambient_data, "#0070c0", "#dae3f3")

    # -- User
    text = "Informação sobre o utilizador"
    user_text_frame = Frame(left_side)
    user_text_frame.pack(expand=TRUE, fill=BOTH)
    user_text_label = Label(user_text_frame, text=text, font=("Times", 20), fg="#c00000", bg="#d9d9d9")
    user_text_label.pack(expand=TRUE, fill=BOTH)

    user_data = {
        "Temperatura": "xx",
        "Frequência cardíaca": "xx",
        "Frequência respiratória": "xx"
    }
    arrange_data(user_data)

    user_table_frame = Frame(left_side)
    user_table_frame.pack(pady=5)

    user_table = Table(user_table_frame, user_data, "#c00000", "#fbe5d6")

    # -- Buttons
    buttons_frame = Frame(left_side, bg="#d9d9d9")
    buttons_frame.pack(pady=5)

    ac_button = Button(buttons_frame, text="Controle\nTemperatura(AC)", bg="#92d050",
                       fg="white", font=("Times", 20))
    ac_button.pack(side=LEFT, padx=(10, 5))

    lum_button = Button(buttons_frame, text="Controle\nLuminosidade", bg="#92d050",
                        fg="white", font=("Times", 20), command=lum_button_func)
    lum_button.pack(side=RIGHT, padx=(5, 10))

    update()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


window()
