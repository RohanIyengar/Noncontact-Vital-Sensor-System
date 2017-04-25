# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 14:19:56 2017

@author: Sai
"""

import logging
import time
import matlab.engine as mat
import csv
import Tkinter as tk   # python3
#import Tkinter as tk   # python
import threading
from threading import Timer
import numpy as np
import UART_Communication as com
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

time_vals = np.array([])
num_msg = time_vals = np.array([])
respTrans = np.array([])
heartTrans = np.array([])
timed_out = False
signal_data = np.array([])
thread_cond = False
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)

TITLE_FONT = ("Helvetica", 18, "bold")

global app

count = 0
heartRate = 10
respRate = 10
eng = mat.start_matlab()
print eng
eng.cd(r"C:/Users/Rohan/Documents/Noncontact-Vital-Sensor-System/Matlab Signal Processing")

def timeout():
    global timed_out
    timed_out = True

def int_error_check(i):
    try:
        return int(i)
    except ValueError:
        logger.error("An integer conversion errored with empty string: " + str(i == ""))
        return 0

def receive_realtime(in_time=10):
    global timed_out, time_vals, signal_data
    signal_data = []
    time_vals = np.array([])
    timed_out = False
    ser_obj = com.initializeSerial()
    last_time = 0
    logger.info("Initialized serial object to " + ser_obj.portstr)
    done = False
    line = ""
    t = Timer(in_time, timeout)
    start_time = time.time()
    t.start()
    while not timed_out:
        if ser_obj.inWaiting() > 0:
            new_data = ser_obj.read(ser_obj.inWaiting())
            end_time = time.time()
            new_msg = new_data.split(",")
            num_msg = [int_error_check(i) for i in new_msg]
            signal_data = np.append(signal_data, num_msg)
            time_vals = np.linspace(0, end_time - start_time, num=len(signal_data))
            line = line + new_data
    return line

def dataCall():
    global time_vals, signal_data
    sampRate = int(sampVar.get())
    timeDur = float(timeVar.get())
    message = receive_realtime(timeDur)
    new_msg = message.split(",")
    signal_data = [int_error_check(i) for i in new_msg]
    signal_data = np.array(signal_data[1:-1])
    time_vals = np.linspace(0, timeDur, num=len(signal_data))
    logger.info("Size of signal: " + str(signal_data.size) + " Size of Time: " + str(time_vals.size))
    data = zip(time_vals, signal_data)
    header = [("Label", ""),("Time(s)", "CH2")]
    with open("C:/Users/Rohan/Documents/Noncontact-Vital-Sensor-System/Matlab Signal Processing/sample_data.csv", "wb") as outfile:
        out1 = csv.writer(outfile, delimiter=',',quoting=csv.QUOTE_ALL)
        i_data = [data[i] for i in [0,1]];
        out1.writerows(header)
        out1.writerows(data)
    return "Hi"

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        
        global time_vals, signal_data, respTrans, heartTrans, heartRate, respRate, inFrame, inFrame2, thread_cond
        
        frame = self.frames[page_name]
        frame.tkraise()        
        
        if page_name == "PageOne":
            inFrame = frame

            t = threading.Thread(target=dataCall)
            t.start()
            thread_cond = True
            do_a_plot()
        
        if page_name == "PageTwo":
            inFrame2 = frame
            thread_cond = False
            update_page_two()

def update_page_two():
    
    global eng, heartRate, respRate
    time_excel, rawSignal, rawTransient, respirationTransient, heartRateTransient, respRate, heartRate = eng.processingFunctionNoHeartBeat("sample_data.csv", nargout=7)
    time_graph = np.asarray(time_excel)
    respTrans = np.asarray(respirationTransient)
    heartTrans = np.asarray(heartRateTransient)
    rawTrans = np.asarray(rawTransient)
    tempText1 = "Heart Rate: " + str(heartRate);
    tempText2 = "Respiratory Rate: " + str(respRate);
    tempText = tempText1 + " " + tempText2
    label1 = tk.Label(inFrame2, text=tempText)
    label1.grid(row=2, column = 1)

    fig = plt.figure()
    b = fig.add_subplot(313)
    c = fig.add_subplot(312)
    d = fig.add_subplot(311)

    b.set_title ("Heart Beat Transient", fontsize=16)
    c.set_title ("Respiration Transient", fontsize=16)
    d.set_title ("Filtered Raw Signal", fontsize=16)

    if (heartTrans.size != 0):
        b.set_xlabel("Time (s)")
        b.set_ylabel("Voltage (mV)")
        b.plot(time_graph, heartTrans)

    if (respTrans.size != 0):
        c.set_xlabel("Time (s)")
        c.set_ylabel("Voltage (mV)")
        c.plot(time_graph, respTrans)

    if (rawTrans.size != 0):
        d.set_xlabel("Time (s)")
        d.set_ylabel("Voltage (mV)")
        d.plot(time_graph, rawTrans)

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=inFrame2)
    canvas.get_tk_widget().grid(row=0,column=1)
    canvas.draw()

    toolbar = NavigationToolbar2TkAgg(canvas, inFrame2)
    toolbar.grid(row=1,column=1)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        
        global sampVar, timeVar
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        label = tk.Label(self, text="Non-contact Vital Sign Monitor", font=TITLE_FONT)
        label.grid(row=0, column=1, columnspan=2, rowspan=1)
        
        label1 = tk.Label(self, text="Sampling Rate")
        label1.grid(row=1, column=1)
        sampVar = tk.StringVar()
        name1 = tk.Entry(self, textvariable=sampVar)
        name1.grid(row=1, column=2)
        
        label2 = tk.Label(self, text="Duration")
        label2.grid(row=2, column=1)
        timeVar = tk.StringVar()
        name2 = tk.Entry(self, textvariable=timeVar)
        name2.grid(row=2, column=2)

        button1 = tk.Button(self, text="Start Sampling",
                            command=lambda: controller.show_frame("PageOne"))
        button1.grid(row=3, column=1, columnspan=2)

def do_a_plot():

    global count, time_vals, signal_data, fig, a, thread_cond

    if (count == 0):
        fig = plt.figure()
        a = fig.add_subplot(111)  
        fig.tight_layout()
        count+=1

    if (time_vals.size != 0 and time_vals.size == len(signal_data)):
        a.clear()
        a.set_title ("Raw Signal", fontsize=16)
        a.set_xlabel("Time (s)")
        a.set_ylabel("Voltage (mV)")
        a.plot(time_vals, signal_data)

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=inFrame)
    canvas.get_tk_widget().grid(row=0,column=1)
    canvas.draw()

    toolbar = NavigationToolbar2TkAgg(canvas, inFrame)
    toolbar.grid(row=1,column=1)

    if thread_cond:
        app.after(500, do_a_plot)

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global heartRate, respRate, fig, a, b, c, canvas
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the results page",
                           command=lambda: controller.show_frame("PageTwo"))
        button.grid(row=3,column=1)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        global heartRate, respRate, fig, a, b, c, canvas
        
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Signal Analysis Results", font=TITLE_FONT)
        label.grid(row=0,column=1)
        button = tk.Button(self, text="Go to Start Page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3,column=1)


if __name__ == "__main__":
    try:
        app = SampleApp()
        app.mainloop()
    except Exception as e:
        print e