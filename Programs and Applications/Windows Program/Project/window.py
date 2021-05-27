from tkinter import *
from PIL import ImageTk, Image
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

class ACControl(Toplevel):
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
    def on_closing():
        nonlocal flag_thread
        print("killing processes")
        flag_thread = False
        while update_thread.is_alive():
            print(".")
            sleep(1)
        root.destroy()


    def update():
        ref = firebase.ref
        env = ref.child("data").child("environment")
        user = ref.child("data").child("user")
        while True:
            if not flag_thread:
                print("stop")
                return

            print("Getting Data")
            amb_temperature = env.child("temperature").get()
            amb_humidity = env.child("humidity").get()
            amb_noise = env.child("noise").get()
            amb_brightness = env.child("brightness").get()

            user_temperature = user.child("temperature").get()
            user_bpm = user.child("bpm").get()
            user_rr = user.child("rr").get()

            if flag_thread:
                print("Updating data")
                ambient_data["Temperatura"].set(amb_temperature)
                ambient_data["Humidade relativa"].set(amb_humidity)
                ambient_data["Ruído"].set(amb_noise)
                ambient_data["Luminosidade"].set(amb_brightness)

                user_data["Temperatura"].set(user_temperature)
                user_data["Frequência cardíaca"].set(user_bpm)
                user_data["Frequência respiratória"].set(user_rr)
            else:
                print("stop")
                return

            sleep(1)



    def lum_button_func():
        # ac_control(root)
        ACControl(root)

    root = Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    root.configure(bg="white")

    # - Left Side
    left_side = Frame(root, bg="#d9d9d9")
    left_side.pack(side=LEFT, expand=FALSE, fill=BOTH)

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
        "Luminosidade": "xx"
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

    # - Right Side
    right_side = Frame(root, bg="white")
    right_side.pack(side=RIGHT, expand=TRUE, fill=BOTH)

    image_frame = Frame(right_side, bg="white")
    image_frame.pack(expand=TRUE, fill=BOTH)

    image1 = Image.open("vect1.png")
    image1 = image1.resize((150, 500), Image.ANTIALIAS)
    image1canvas = ImageTk.PhotoImage(image1, master=image_frame)

    image2 = Image.open("vect2.png")
    image2 = image2.resize((150, 500), Image.ANTIALIAS)
    image2canvas = ImageTk.PhotoImage(image2, master=image_frame)

    left_image = Label(image_frame, image=image1canvas, relief="solid")
    left_image.pack(side=LEFT, padx=(10, 5))

    right_image = Label(image_frame, image=image2canvas, relief="solid")
    right_image.pack(side=RIGHT, padx=(5, 10))

    text_frame = Frame(right_side, bg="white")
    text_frame.pack(expand=FALSE, fill=BOTH)

    """bottom_text = Label(text_frame, text="O JOÃO É GAY!", bg="#fbe5d6", font=("Times", 20))
    bottom_text.pack(side=BOTTOM, pady=5)"""
    flag_thread = True
    update_thread = Thread(target=update)
    update_thread.start()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


window()
