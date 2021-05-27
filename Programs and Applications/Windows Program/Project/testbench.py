from tkinter import *
from PIL import ImageTk, Image
from playsound import playsound
from threading import Thread
from time import sleep

import win10toast


def testbench():
    def toast():
        toaster = win10toast.ToastNotifier()
        toaster.show_toast("Alerta Notificação", "Levanta-te!", duration=2, threaded=True)

    def custom():
        def countdown(time):
            if time == -1:
                custom_root.destroy()
            else:
                if time == 0:
                    label.configure(text="BOOM")
                else:
                    label.configure(text="time remaining: %d seconds" % time)

                custom_root.after(1000, countdown, time - 1)

        custom_root = Tk()
        custom_root.title("Alerta!")
        # get screen width and height
        ws = root.winfo_screenwidth()  # width of the screen
        hs = root.winfo_screenheight()  # height of the screen
        w = int(ws/5)
        h = int(hs/4)
        custom_root.geometry('%dx%d+%d+%d' % (w, h, ws - w - 10, hs - h - 100))

        image1 = Image.open("vect1.png")
        image1 = image1.resize((int(w/2 - 20), int(h - 60)), Image.ANTIALIAS)
        image1canvas = ImageTk.PhotoImage(image1, master=custom_root)

        image2 = Image.open("vect2.png")
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

        # countdown(10)

        # C:\Windows\Media\Windows Message Nudge.wav
        playsound("C:/Windows/Media/Windows Message Nudge.wav", block=False)

        custom_root.mainloop()

    root = Tk()
    root.title("TESTBENCH")
    root.geometry("100x100")

    top_frame = Frame(root, width=100, height=50, bg="pink", borderwidth=1)
    top_frame.pack(fill=BOTH, expand=True)
    top_frame_button = Button(top_frame, text="Windows POPUP", command=toast)
    top_frame_button.pack(fill=BOTH, expand=True)

    bottom_frame = Frame(root, width=100, height=50, bg="blue", borderwidth=1)
    bottom_frame.pack(fill=BOTH, expand=True)
    bottom_frame_button = Button(bottom_frame, text="Custom POPUP", command=custom)
    bottom_frame_button.pack(fill=BOTH, expand=True)

    """button = Button(root, text="Pop-up", command=toast, height=1.5, width=)
    button.place(relx=0.5, rely=0, anchor="n")

    button1 = Button(root, text="Custom Pop-up", command=custom)
    button1.place(relx=0.5, rely=1, anchor="s")"""

    root.mainloop()


# Exec main function
testbench()
