import contextlib
import serial
from tkinter import *
from dotenv import load_dotenv
import os

load_dotenv()

DEVICE_PORT = os.getenv('DEVICE_PORT')
DEFAULT_ALARM = os.getenv('DEFAULT_ALARM')

# while True:
#     if distance := serial_com.readline().decode():
#         print(f"{distance}")

class Application:
    def __init__(self) -> None:
        self.window: Tk = Tk()
        self.window.title("Get distance")
        self.window.geometry('500x500')
        self.window.resizable(0, 0)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        self.intVar_actual_alarm_value: IntVar = IntVar(value=DEFAULT_ALARM)
        self.intVar_new_alarm_value: IntVar = IntVar()
        self.intVar_distance_value: IntVar = IntVar()
        self.stringVar_error_serial_port: StringVar = StringVar(value='')
        # open a serial connection
        try:
            self.serial_port: serial.Serial = serial.Serial(DEVICE_PORT, 9600, timeout=0)
        except serial.SerialException:
            self.stringVar_error_serial_port.set("There is an error with the serial port")
    
    def launch(self):  # sourcery skip: extract-duplicate-method
        frame_window: Frame = Frame(self.window)
        frame_window.grid(column=0, row=0, sticky="nsew")
        frame_window.grid_columnconfigure(0, weight=1)
        frame_window.grid_rowconfigure(0, weight=1)
        frame_window.grid_rowconfigure(1, weight=1)
        frame_window.grid_rowconfigure(2, weight=2)

        frame_actual_distance: Frame = Frame(frame_window)
        frame_actual_distance.grid(column=0, row=0, sticky='nsew')
        frame_actual_distance.grid_columnconfigure(0, weight=2)
        frame_actual_distance.grid_columnconfigure(1, weight=1)
        frame_actual_distance.grid_columnconfigure(2, weight=1)
        frame_actual_distance.grid_rowconfigure(0, weight=1)

        label_text_actual_distance: Label = Label(frame_actual_distance, text="Distance :", anchor=E)
        label_text_actual_distance.grid(column=0, row=0, sticky="nsew")

        label_get_actual_distance: Label= Label(frame_actual_distance, textvariable=self.intVar_distance_value, anchor=E)
        label_get_actual_distance.grid(column=1, row=0, sticky="nsew")

        label_text_actual_distance_cm = Label(frame_actual_distance, text="cm.", anchor=W)
        label_text_actual_distance_cm.grid(column=2, row=0, sticky="nsew")

        frame_actual_alarm = Frame(frame_window, bg="black")
        frame_actual_alarm.grid(column=0, row=1, sticky="nsew")
        frame_actual_alarm.grid_columnconfigure(0, weight=2)
        frame_actual_alarm.grid_columnconfigure(1, weight=1)
        frame_actual_alarm.grid_columnconfigure(2, weight=1)
        frame_actual_alarm.grid_rowconfigure(0, weight=1)

        label_text_actual_alarm = Label(frame_actual_alarm, text="Actual alarm :", anchor=E)
        label_text_actual_alarm.grid(column=0, row=0, sticky="nsew")

        label_get_actual_alarm= Label(frame_actual_alarm, textvariable=self.intVar_actual_alarm_value, anchor=E)
        label_get_actual_alarm.grid(column=1, row=0, sticky="nsew")

        label_text_actual_alarm_cm = Label(frame_actual_alarm, text="cm.", anchor=W)
        label_text_actual_alarm_cm.grid(column=2, row=0, sticky="nsew")
        
        if not self.stringVar_error_serial_port.get():
            frame_alarm = Frame(frame_window)
            frame_alarm.grid(column=0, row=2, rowspan=3, sticky="nsew")
            for i in range(4):
                frame_alarm.grid_columnconfigure(i, weight=1)
            for i in range(4):
                frame_alarm.grid_rowconfigure(i, weight=1)

            label_new_alarm = Label(frame_alarm, text="Set a new alarm :")
            label_new_alarm.grid(column=1, columnspan=2, row=1, sticky="nsew")

            vcmd = (self.window.register(self.check_only_int))
            entry_new_alarm = Entry(frame_alarm, textvariable=self.intVar_new_alarm_value, validate = 'key', validatecommand = (vcmd, '%P'))
            entry_new_alarm.grid(column=1, columnspan=2, row=2, rowspan=2, sticky="nsew")

            button_send_new_alarm = Button(frame_alarm, text="Send", command=self.send_new_alarm)
            button_send_new_alarm.grid(column=3, row=3, sticky="nsew")
        
        else:
            label_error: Label = Label(frame_window, textvariable=self.stringVar_error_serial_port, relief='groove')
            label_error.grid(column=0, row=2, rowspan=3, sticky="nsew")
        self.receive_new_distance()
        self.window.mainloop()
    
    def receive_new_distance(self):
        with contextlib.suppress(serial.SerialException):
            with contextlib.suppress(AttributeError):
                if distance_received := self.serial_port.readline().decode().strip():
                    self.intVar_distance_value.set(distance_received)
                    print(distance_received)
                self.window.after(500, self.receive_new_distance)
    
    def send_new_alarm(self):
        with contextlib.suppress(serial.SerialException):
            self.serial_port.write(f"alarm={self.intVar_new_alarm_value.get()}\n".encode())
            self.intVar_actual_alarm_value.set(self.intVar_new_alarm_value.get())
    
    def check_only_int(self, key: str):
        return bool(str.isdigit(key) or not key)


if __name__=="__main__":
    app = Application()
    app.launch()