# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 14:19:56 2017

@author: Sai
"""

import Tkinter as tk   # python3
#import Tkinter as tk   # python
import numpy as np
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

TITLE_FONT = ("Helvetica", 18, "bold")

eng = mat.start_matlab()

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
        
        global time_vals, num_msg, respTrans, heartTrans
        
        frame = self.frames[page_name]
        frame.tkraise()
        
        if page_name == "PageOne":
            sampRate = int(sampVar.get())
            timeDur = float(timeVar.get())
            message = com.receive_for(timeDur)
            new_msg = message.split(",")
            new_msg = new_msg[1:-1]
            #print new_msg
            num_msg = [int(i) for i in new_msg]
            time_vals = np.linspace(0, timeDur, num=len(num_msg))
            data = zip(time_vals,num_msg)
            #q_data = zip(data0,data3,data4)
            header = [("Label", ""),("Time(s)", "CH2")]
            out1 = csv.writer(open("sample_data.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
            #i_data = [data[i] for i in [0,1,2]];
            #print i_data
            out1.writerows(header)
            out1.writerows(data)
            time, rawSignal, respTrans, heartTrans, respRate, heartRate = eng.processingFunction("sample_data.csv")

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
        '''button2 = tk.Button(self, text="Go to Page Two",
                            command=lambda: controller.show_frame("PageTwo"))'''
        button1.grid(row=3, column=1, columnspan=2)
        '''button2.grid(row=4, column=2)'''


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global heartRate, respRate
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        tempText1 = "Heart Rate: " + str(heartRate);
        tempText2 = "Respiratory Rate: " + str(respRate);
        tempText = tempText1 + " " + tempText2
        
        label1 = tk.Label(self, text=tempText)
        label1.grid(row=2,column=1)
        
        x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
        p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
            19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])

        fig = plt.figure()
        a = fig.add_subplot(311)
        a.plot(time_vals, num_msg,color='blue')
        
        b = fig.add_subplot(312)
        b.plot(time_vals, heartTrans)
    
        c = fig.add_subplot(313)
        c.plot(time_vals, respTrans)

        a.set_title ("Raw Signal", fontsize=16)
        b.set_title ("Heart Beat Transient", fontsize=16)
        c.set_title ("Respiration Transient", fontsize=16)

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().grid(row=0,column=1)
        canvas.draw()
        
        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.grid(row=1,column=1)

        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3,column=1)

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2", font=TITLE_FONT)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()