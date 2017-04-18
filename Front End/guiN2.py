import matlab.engine as mat
import csv
import Tkinter as tk   # python3
#import Tkinter as tk   # python
import numpy as np
import UART_Communication as com
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

TITLE_FONT = ("Helvetica", 18, "bold")

heartRate = 1;
respRate = 2;
eng = mat.start_matlab()
eng.cd(r"C:/Users/Rohan/Documents/Noncontact-Vital-Sensor-System/Matlab Signal Processing")

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
        print "Init App"

    def show_frame(self, page_name):
        print "Started showFrame"
        '''Show a frame for the given page name'''
        print page_name
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
            print "Heart rate: " + heartRate
            print "Respiration Rate " + respRate 

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
        print "Start page init"


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        
        global heartRate, respRate
        
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        # button1 = tk.Button(self, text="Plot", command=plotthem)
        # button1.grid(row=0, column=0)
        
        fig1 = plt.Figure()
        
        canvas1 = FigureCanvasTkAgg(fig1, master=self)
        canvas1.get_tk_widget().grid(row=0,column=1)
        
        tempText1 = "Heart Rate: " + str(heartRate);
        tempText2 = "Respiratory Rate: " + str(respRate);
        tempText = tempText1 + " " + tempText2
        
        label1 = tk.Label(self, text=tempText)
        label1.grid(row=2,column=1)
        
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row=3,column=1)
        
    def plotthem():
        plt.figure(1)
        plt.clf()
        x = np.arange(0.0,3.0,0.01)
        y = np.sin(2*np.pi*x+random.random())
        plt.plot(x,y)
        plt.gcf().canvas.draw()
    
        plt.figure(2)
        plt.clf()
        x = np.arange(0.0,3.0,0.01)
        y = np.tan(2*np.pi*x+random.random())
        plt.plot(x,y)
        plt.gcf().canvas.draw()

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