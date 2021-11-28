# /***************************
#  *  gui.py
#  * Version Number	: 1.1
#  * Configuration Identifier: 
#  * Modified by:  Shrilesh Kale    
#  * Modified Date:  16/09/2021       
#  * Description: Source code for UI interface of Inkjet printer
#  **************************/

# -*- coding: utf-8 -*-
try:
    import serial as s
    import time as t
    import os
    import sys
    import tkinter as tk
    from tkinter import ttk
    from tkinter import * 
    import time
    from tkinter.ttk import *
    from tkinter.filedialog import askopenfile
    import matplotlib.image as mpimg
    from PIL import ImageTk, Image
    from tkinter import filedialog
    import tkinter.messagebox
    import serial.tools.list_ports
    import threading
    import matplotlib
    import matplotlib.pyplot as plt
    matplotlib.use("TkAgg")
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    import matplotlib.pyplot as pltlib
    from random import randrange
    import re
    import logging
    import numpy as np
    logging.basicConfig(level=logging.INFO)

except ImportError as e:
    print('Check import library:-  {}'.format(e))

root = tk.Tk()
main_menu = tk.Menu(root)
root.wm_attributes('-fullscreen', 'true')
root.wm_title('Inkjet Printer GUI')

var = tk.IntVar()
varForFan = tk.IntVar()
dpi_x = tk.IntVar()
dpi_y = tk.IntVar()
dpi_x.set(5)
dpi_y.set(5)

class Gui(tk.Frame):
    ListOfFiles = []
    def __init__(self, master):
        self.exec_path = sys.executable
        tk.Frame.__init__(self, master)
        self.ytemp = []
        self.xtemp = []
        self.count = 0
        self.filename = None
        self.incrementValue = 0
        self.iteration_cnt = 1
        self.xCor = int()
        self.yCor = int()
        self.zCor = int()
        Gui.reset = False
        self.master = master
        frame = Frame(master)
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # UI design components

        # tabs creation
        self.tabs = ttk.Notebook(master)
        self.tabs.pack(expand=1, fill="both", side=tk.BOTTOM,
                       padx=screen_width * .01, pady=screen_height * .01)  # , pady=80)

        #self.tabFrame = ttk.Frame(self.tabs, borderwidth=4, relief="solid")
        self.tabFrame2 = ttk.Frame(self.tabs, borderwidth=4, relief="solid")
        self.tabFrame3 = ttk.Frame(self.tabs, borderwidth=4, relief="solid")
        self.tabDemo = ttk.Frame(self.tabs, borderwidth=4, relief="solid")

        self.tabss = ["Main", "Sensors", "Img/path"]

        self.tabFrames = [self.tabDemo, self.tabFrame2, self.tabFrame3]
        for (j, i) in zip(self.tabss, self.tabFrames):
            print(i)
            self.tabs.add(i, text=j)

        self.tabs.bind("<<NotebookTabChanged>>", self.graph)
        vcmd = (self.tabs.register(self.callback))

        # Demo Frmae
        # top vertical frame
        self.vertical_frame_v0 = ttk.Frame(
            self.tabDemo, borderwidth=1, relief="solid", width=.94 * screen_width, height=.14 * screen_height)
        self.vertical_frame_v0.grid(
            row=0, column=0, padx=15, pady=10, columnspan=3)
        self.connected_label_v0 = tk.Label(
            self.tabDemo, text="Connected", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=3, sticky='NW')
        self.printing_label_v0 = tk.Label(
            self.tabDemo, text="Printing", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=3, sticky='NW')
        self.cc_label_v0 = tk.Label(self.tabDemo, text="Cover Closed",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=3, sticky='NW')
        self.connected_buttn_v0 = tk.Label(
            self.tabDemo, text="", bg="light green", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_buttn_v0.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=3, sticky='SW')
        self.printing_buttn_v0 = tk.Label(
            self.tabDemo, text="", bg="dark green", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_buttn_v0.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=3, sticky='SW')
        self.cc_buttn_v0 = tk.Label(self.tabDemo, text="", bg="dark green",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_buttn_v0.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=3, sticky='SW')

        self.tac_label_v0 = tk.Label(
            self.tabDemo, text="Temp. Auto Control", borderwidth=1, relief="solid", width=18)
        self.tac_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='NW')
        # , command=lambda: self.StepperDirection('FanControl'))
        self.AutoCRadioButton_v0 = Radiobutton(
            self.tabDemo, width=12, text='Target in °C')
        self.AutoCRadioButton_v0.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                                      screen_width, column=0, rowspan=1, columnspan=3, sticky='SW')
        self.TargetTemp = Entry(self.tabDemo, width=5,
                                validate='all', validatecommand=(vcmd, '%P'))
        self.TargetTemp.grid(row=0, pady=0.045 * screen_height, padx=0.34 *
                             screen_width, column=0, rowspan=1, columnspan=3, sticky='SW')

        self.tc_label_v0 = tk.Label(
            self.tabDemo, text="Thermal Control", borderwidth=1, relief="solid", width=13)
        self.tc_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                              screen_height, column=0, rowspan=1, columnspan=3, sticky='N')
        self.ven_label_v0 = tk.Label(
            self.tabDemo, text="Ventilation", borderwidth=1, relief="solid", width=13)
        self.ven_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                               screen_height, column=0, rowspan=1, columnspan=3, sticky='S')
        self.tc_buttn_v0 = tk.Label(
            self.tabDemo, text="", bg="light green", borderwidth=1, relief="solid", width=2)
        self.tc_buttn_v0.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                              screen_width, column=0, rowspan=1, columnspan=3, sticky='NW')
        self.ven_buttn_v0 = tk.Label(
            self.tabDemo, text="", bg="dark green", borderwidth=1, relief="solid", width=2)
        self.ven_buttn_v0.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='SW')

        self.tPh_label_v0 = tk.Label(
            self.tabDemo, text="T Peltier hot / °C", width=14, borderwidth=1, relief="solid")
        self.tPh_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')
        self.tPh_value_v0 = tk.Label(
            self.tabDemo, text=" T1 ", width=6, borderwidth=1, relief="solid")
        self.tPh_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')

        self.tPc_label_v0 = tk.Label(
            self.tabDemo, text="T Peltier cold / °C", width=14, borderwidth=1, relief="solid")
        self.tPc_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')
        self.tPc_value_v0 = tk.Label(
            self.tabDemo, text=" T2 ", width=6, borderwidth=1, relief="solid")
        self.tPc_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')
        self.tR_label_v0 = tk.Label(
            self.tabDemo, text="T Room / °C", width=10, borderwidth=1, relief="solid")
        self.tR_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')
        self.tR_value_v0 = tk.Label(
            self.tabDemo, text=" T3 ", width=6, borderwidth=1, relief="solid")
        self.tR_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')
        self.tT_label_v0 = tk.Label(
            self.tabDemo, text="T Tank / °C", width=10, borderwidth=1, relief="solid")
        self.tT_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')
        self.tT_value_v0 = tk.Label(
            self.tabDemo, text=" T4 ", width=6, borderwidth=1, relief="solid")
        self.tT_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')

        self.tPH_label_v0 = tk.Label(
            self.tabDemo, text="T Print head / °C", width=14, borderwidth=1, relief="solid")
        self.tPH_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')
        self.tPH_value_v0 = tk.Label(
            self.tabDemo, text=" T5 ", width=6, borderwidth=1, relief="solid")
        self.tPH_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='NE')
        self.tPb_label_v0 = tk.Label(
            self.tabDemo, text="T Print bed / °C", width=14, borderwidth=1, relief="solid")
        self.tPb_label_v0.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')
        self.tPb_value_v0 = tk.Label(
            self.tabDemo, text=" T6 ", width=6, borderwidth=1, relief="solid")
        self.tPb_value_v0.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=3, sticky='SE')

        # column 1
        i = ttk.Frame(self.tabDemo, borderwidth=1, relief="solid", width=screen_width * .275,
                      height=screen_height * .70).grid(row=1, column=0, padx=0.01 * screen_width, pady=0.011 * screen_height)
        self.image_frame = ttk.Frame(self.tabDemo, borderwidth=1, relief="solid", width=screen_width * .265,
                                     height=screen_height * .30).grid(row=1, column=0, padx=0.005 * screen_width, pady=0.035 * screen_height, sticky='N')

        tk.Label(self.tabDemo, text="Axis Control", borderwidth=1, relief="solid", width=15, font=(
            None, 12)).grid(row=1, pady=0.017 * screen_height, column=0, rowspan=1, columnspan=1, sticky='N')
        tk.Label(self.tabDemo, text="GoTo", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.32 * screen_height, padx=0.02 * screen_width, column=0, sticky='W')
        tk.Label(self.tabDemo, text="Velocity", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.315 * screen_height, padx=0.02 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="Acceleration", width=10, borderwidth=1, relief="solid").grid(
            row=1, pady=0.28 * screen_height, padx=0.02 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="X", width=1, borderwidth=1, relief="solid").grid(
            row=1, pady=0.32 * screen_height, padx=0.078 * screen_width, column=0, sticky='W')
        tk.Label(self.tabDemo, text="X", width=1, borderwidth=1, relief="solid").grid(
            row=1, pady=0.315 * screen_height, padx=0.078 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="X", width=1, borderwidth=1, relief="solid").grid(
            row=1, pady=0.28 * screen_height, padx=0.078 * screen_width, column=0, sticky='SW')
        self.x = Entry(self.tabDemo, width=5, validate='all',validatecommand=(vcmd, '%P'))
        self.x.grid(row=1, pady=0.32 * screen_height,padx=0.091 * screen_width, column=0, sticky='W')
        self.speed_x = Entry(self.tabDemo, width=5, validate='all',validatecommand=(vcmd, '%P'))
        self.speed_x.grid(row=1, pady=0.315 * screen_height,padx=0.091 * screen_width, column=0, sticky='SW')
        self.acceleration_x = Entry(self.tabDemo, width=5, validate='all',validatecommand=(vcmd, '%P'))
        self.acceleration_x.grid(row=1, pady=0.28 * screen_height,padx=0.091 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="Y", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.32 * screen_height, padx=0.123 * screen_width, column=0, sticky='W')
        tk.Label(self.tabDemo, text="Y", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.315 * screen_height, padx=0.123 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="Y", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.28 * screen_height, padx=0.123 * screen_width, column=0, sticky='SW')
        self.y = Entry(self.tabDemo, width=5, validate='all',validatecommand=(vcmd, '%P'))
        self.y.grid(row=1, pady=0.32 * screen_height,padx=0.136 * screen_width, column=0, sticky='W')
        self.speed_y = Entry(self.tabDemo, width=5, validate='all', validatecommand=(vcmd, '%P'))
        self.speed_y.grid(row=1, pady=0.315 * screen_height, padx=0.136 * screen_width, column=0, sticky='SW')
        self.acceleration_y = Entry(self.tabDemo, width=5, validate='all', validatecommand=(vcmd, '%P'))
        self.acceleration_y.grid(row=1, pady=0.28 * screen_height, padx=0.136 * screen_width, column=0, sticky='SW')
        tk.Label(self.tabDemo, text="Z", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.32 * screen_height, padx=0.12 * screen_width, column=0, sticky='E')
        tk.Label(self.tabDemo, text="Z", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.315 * screen_height, padx=0.12 * screen_width, column=0, sticky='SE')
        tk.Label(self.tabDemo, text="Z", width=1, borderwidth=1, relief="solid").grid(row=1, pady=0.28 * screen_height, padx=0.12 * screen_width, column=0, sticky='SE')
        self.z = Entry(self.tabDemo, width=5, validate='all',validatecommand=(vcmd, '%P'))
        self.z.grid(row=1, pady=0.32 * screen_height,padx=0.091 * screen_width, column=0, sticky='E')
        self.speed_z = Entry(self.tabDemo, width=5, validate='all', validatecommand=(vcmd, '%P'))
        self.speed_z.grid(row=1, pady=0.315 * screen_height, padx=0.091 * screen_width, column=0, sticky='SE')
        self.acceleration_z = Entry(self.tabDemo, width=5, validate='all', validatecommand=(vcmd, '%P'))
        self.acceleration_z.grid(row=1, pady=0.28 * screen_height, padx=0.091 * screen_width, column=0, sticky='SE')
        self.move10 = tk.Button(self.tabDemo, width=5, text="Move", bg="green", activebackground="red", command=lambda: self.report_change('manualControl')).grid(row=1, pady=0.034 * screen_height, padx=0.045 * screen_width, column=0, sticky='E')
        self.set10 = tk.Button(self.tabDemo, width=5, text="Set", bg="green", activebackground="red", command=lambda: self.report_change('speed','v'))
        self.set10.grid(row=1, pady=0.31 * screen_height, padx=0.045 * screen_width, column=0, sticky='SE')
        self.set11 = tk.Button(self.tabDemo, width=5, text="Set", bg="green", activebackground="red",command=lambda: self.report_change('acceleration','a'))
        self.set11.grid(row=1, pady=0.27 * screen_height, padx=0.045 * screen_width, column=0, sticky='SE')
        self.cal11 = tk.Button(self.tabDemo, width=5, height=9, text="Cal", bg="green", activebackground="red", command=lambda: self.report_change(
            'Calibrate')).grid(row=1, pady=0.07 * screen_height, padx=0.052 * screen_width, column=0, sticky='WS')
        X_011 = tk.Button(self.tabDemo, width=5, height=2, text="X-", bg="green", activebackground="red", command=lambda:self.incrementalChangeButton('xButton-'))
        X_011.grid(row=1, pady=0.127 * screen_height, padx=0.097 * screen_width, column=0, sticky='WS')
        Y_020 = tk.Button(self.tabDemo, width=5, height=2, text="Y+", bg="green",activebackground="red" , command=lambda:self.incrementalChangeButton('yButton+'))
        Y_020.grid(row=1, pady=0.185 * screen_height, padx=0, column=0, sticky='S')
        O_021 = tk.Button(self.tabDemo, width=5, height=2, text="0", bg="green", activebackground="red", command=lambda:self.incrementalChangeButton('zeroPosition'))
        O_021.grid(row=1, pady=0.127 * screen_height, padx=0, column=0, sticky='S')
        Y_122 = tk.Button(self.tabDemo, width=5, height=2, text="Y-", bg="green",activebackground="red" , command=lambda:self.incrementalChangeButton('yButton-'))
        Y_122.grid(row=1, pady=0.07 * screen_height, padx=0, column=0, sticky='S')
        X_031 = tk.Button(self.tabDemo, width=5, height=2, text="X+", bg="green", activebackground="red" , command=lambda:self.incrementalChangeButton('xButton+'))
        X_031.grid(row=1, pady=0.127 * screen_height, padx=0.097 * screen_width, column=0, sticky='SE')
        Z_041 = tk.Button(self.tabDemo, width=5, height=2, text="Z+", bg="green", activebackground="red" , command=lambda:self.incrementalChangeButton('zButton+'))
        Z_041.grid(row=1, pady=0.156 * screen_height, padx=0.052 * screen_width, column=0, sticky='SE')
        Z_141 = tk.Button(self.tabDemo, width=5, height=2, text="Z-", bg="green", activebackground="red" , command=lambda: self.incrementalChangeButton('zButton-'))
        Z_141.grid(row=1, pady=0.098 * screen_height, padx=0.052 * screen_width, column=0, sticky='SE')

        # column 2
        i = ttk.Frame(self.tabDemo, borderwidth=1, relief="solid", width=screen_width * .310,
                      height=screen_height * .70).grid(row=1, rowspan=2, column=1, padx=0.01 * screen_width, pady=.011 * screen_height)
        tk.Label(self.tabDemo, text="Thermal Control System", borderwidth=1, relief="solid", width=25, font=(
            None, 12)).grid(row=1, pady=0.017 * screen_height, column=1, rowspan=1, columnspan=1, sticky='N')  # , padx=40)
        Fan1RadioButton = tk.Button(self.tabDemo, width=5, text="Submit", bg="green", activebackground="red").grid(
            row=1, pady=0.055 * screen_height, padx=0.072 * screen_width, column=1, sticky='WN')  # , command=lambda: self.StepperDirection('DirectionControl'))
        Fan2RadioButton = tk.Button(self.tabDemo, width=5, text="Submit", bg="green", activebackground="red").grid(
            row=1, pady=0.095 * screen_height, padx=0.072 * screen_width, column=1, sticky='WN')
        tk.Label(self.tabDemo, text="Fan 1", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.057 * screen_height, padx=0.118 * screen_width, column=1, sticky='WN')
        tk.Label(self.tabDemo, text="Fan 2", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.097 * screen_height, padx=0.118 * screen_width, column=1, sticky='WN')
        self.rpm1_01 = Entry(self.tabDemo, width=10, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.057 * screen_height, padx=0.118 * screen_width, column=1, sticky='NE')
        self.rpm1_02 = Entry(self.tabDemo, width=10, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.097 * screen_height, padx=0.118 * screen_width, column=1, sticky='NE')
        tk.Label(self.tabDemo, text="RPM", width=5, borderwidth=1, relief="solid").grid(
            row=1, pady=0.057 * screen_height, padx=0.077 * screen_width, column=1, sticky='NE')
        tk.Label(self.tabDemo, text="RPM", width=5, borderwidth=1, relief="solid").grid(
            row=1, pady=0.097 * screen_height, padx=0.077 * screen_width, column=1, sticky='NE')

        # Print Head Temperature
        tk.Label(self.tabDemo, text="Print Head Temperature", width=25, borderwidth=1, relief="solid").grid(
            row=1, pady=0.167 * screen_height, padx=0.086 * screen_width, column=1, sticky='N')
        #  tk.Label(self.tabDemo, text="", width=48, height=8, borderwidth=1, relief="solid").grid(row=1, pady=0.23*screen_height, padx=0.05*screen_width, column=1, sticky='NW')
        tk.Label(self.tabDemo, text="Actual Temp / °C", width=14, borderwidth=1, relief="solid").grid(
            row=1, pady=0.207 * screen_height, padx=0.103 * screen_width, column=1, sticky='NW')
        self.actualTemp1 = Entry(self.tabDemo, width=7, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.207 * screen_height, padx=0.103 * screen_width, column=1, sticky='EN')
        tk.Label(self.tabDemo, text="Target Temp / °C", width=14, borderwidth=1, relief="solid").grid(
            row=1, pady=0.247 * screen_height, padx=0.103 * screen_width, column=1, sticky='NW')
        self.targetTemp1 = Entry(self.tabDemo, width=7, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.247 * screen_height, padx=0.103 * screen_width, column=1, sticky='EN')
        Controller01 = tk.Button(self.tabDemo, width=6, text="Submit", bg="green", activebackground="red").grid(
            row=1, pady=0.287 * screen_height, padx=0.120 * screen_width, column=1, sticky='NW')
        tk.Label(self.tabDemo, text="Controller", width=9, borderwidth=1, relief="solid").grid(
            row=1, pady=0.292 * screen_height, padx=0.098 * screen_width, column=1, sticky='NE')

        # Print Bed Temperature
        tk.Label(self.tabDemo, text="Print Bed Temperature", width=25, borderwidth=1, relief="solid").grid(
            row=1, column=1, pady=0.33 * screen_height, padx=0.086 * screen_width, sticky='S')
        #  tk.Label(self.tabDemo, text="", width=48, height=8, borderwidth=1, relief="solid").grid(row=1, pady=0.16*screen_height, padx=0.05*screen_width, column=1, sticky='SW')
        tk.Label(self.tabDemo, text="Actual Temp / °C", width=14, borderwidth=1, relief="solid").grid(
            row=1, pady=0.29 * screen_height, padx=0.103 * screen_width, column=1, sticky='WS')
        self.actualTemp2 = Entry(self.tabDemo, width=7, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.29 * screen_height, padx=0.103 * screen_width, column=1, sticky='SE')
        tk.Label(self.tabDemo, text="Target Temp / °C", width=14, borderwidth=1, relief="solid").grid(
            row=1, pady=0.25 * screen_height, padx=0.103 * screen_width, column=1, sticky='WS')
        self.targetTemp2 = Entry(self.tabDemo, width=7, validate='all', validatecommand=(vcmd, '%P')).grid(
            row=1, pady=0.25 * screen_height, padx=0.103 * screen_width, column=1, sticky='SE')
        Controller02 = tk.Button(self.tabDemo, width=6, text="Submit", bg="green", activebackground="red").grid(
            row=1, pady=0.21 * screen_height, padx=0.120 * screen_width, column=1, sticky='WS')
        tk.Label(self.tabDemo, text="Controller", width=9, borderwidth=1, relief="solid").grid(
            row=1, pady=0.215 * screen_height, padx=0.098 * screen_width, column=1, sticky='SE')

        # DPI Control
        tk.Label(self.tabDemo, text="DPI Control", width=25, borderwidth=1, relief="solid").grid(
            row=1, pady=0.147 * screen_height, padx=0.086 * screen_width, column=1, sticky='S')
        tk.Label(self.tabDemo, text="DPI X", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.107 * screen_height, padx=0.090 * screen_width, column=1, sticky='WS')
        tk.Label(self.tabDemo, text="DPI Y", width=7, borderwidth=1, relief="solid").grid(
            row=1, pady=0.067 * screen_height, padx=0.090 * screen_width, column=1, sticky='WS')
        self.dpi_x = Entry(self.tabDemo, width=10, validate='all', validatecommand=(
            vcmd, '%P'), textvariable=dpi_x).grid(row=1, pady=0.107 * screen_height, column=1, sticky='S')
        self.dpi_y = Entry(self.tabDemo, width=10, validate='all', validatecommand=(
            vcmd, '%P'), textvariable=dpi_y).grid(row=1, pady=0.067 * screen_height, column=1, sticky='S')
        self.dpi_button = tk.Button(self.tabDemo, width=7, text="Submit", activebackground="green", command=self.dpi_control).grid(
            row=1, pady=0.087 * screen_height, padx=0.090 * screen_width, column=1, sticky='SE')

        # Column 3
        i = ttk.Frame(self.tabDemo, borderwidth=1, relief="solid", width=screen_width * .32, height=screen_height * .70).grid(
            row=1, column=2, rowspan=2, padx=.010 * screen_width, pady=0.012 * screen_height)
        # canvasforTab1
        self.image_path_frame = ttk.Frame(self.tabDemo, borderwidth=1, relief="solid", width=screen_width * .29,
                                          height=screen_height * .55).grid(row=1, column=2, padx=0.005 * screen_width, pady=0.035 * screen_height, sticky='N')

        Gui.my_progress = ttk.Progressbar(
            self.tabDemo, orient=HORIZONTAL, length=.29 * screen_width, mode='determinate')
        Gui.my_progress.grid(
            row=1, pady=0.1 * screen_height, column=2, sticky='S')
        tk.Label(self.tabDemo, text="Image", borderwidth=1, relief="solid", width=15, font=(None, 12)).grid(
            row=1, column=2, pady=0.017 * screen_height, rowspan=1, columnspan=1, sticky='N')
        self.print_button = tk.Button(self.tabDemo, width=10, text="Print", bg='green', command=lambda: self.python_process_deploy("print_execution")).grid(
            row=1, pady=0.045 * screen_height, padx=.03 * screen_width, column=2, sticky='SE')  # command=lambda: self.printExecution()
        self.pause_button = tk.Button(self.tabDemo, width=10, text="Browse", bg='yellow', command=lambda: self.open_file(
        )).grid(row=1, pady=0.045 * screen_height, padx=0.081 * screen_width, column=2, sticky='SE')
        Gui.abort_button = tk.Button(self.tabDemo, width=10, text="Abort", bg='red', command=self.stop, state = DISABLED)
        Gui.abort_button.grid(row=1, pady=0.045 * screen_height, padx=0.13 * screen_width, column=2, sticky='SE')
       # self.abort_button["state"] = DISABLED
        #  BrowseButton = tk.Button(self.tabDemo, width=10, text="Browse", bg='red').grid(row=1, pady=0.045*screen_height, padx=0.149*screen_width, column=2, sticky='SE')

        # Frame 2
        # top vertical frame
        self.vertical_frame_v1 = ttk.Frame(
            self.tabFrame2, borderwidth=1, relief="solid", width=.94 * screen_width, height=.14 * screen_height)
        self.vertical_frame_v1.grid(
            row=0, column=0, padx=15, pady=10, columnspan=1)
        self.connected_label_v1 = tk.Label(
            self.tabFrame2, text="Connected", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=1, sticky='NW')
        self.printing_label_v1 = tk.Label(
            self.tabFrame2, text="Printing", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=1, sticky='NW')
        self.cc_label_v1 = tk.Label(self.tabFrame2, text="Cover Closed",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=1, sticky='NW')
        self.connected_buttn_v1 = tk.Label(
            self.tabFrame2, text="", bg="light green", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_buttn_v1.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=1, sticky='SW')
        self.printing_buttn_v1 = tk.Label(
            self.tabFrame2, text="", bg="dark green", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_buttn_v1.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=1, sticky='SW')
        self.cc_buttn_v1 = tk.Label(self.tabFrame2, text="", bg="dark green",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_buttn_v1.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=1, sticky='SW')

        self.tac_label_v1 = tk.Label(
            self.tabFrame2, text="Temp. Auto Control", borderwidth=1, relief="solid", width=18)
        self.tac_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='NW')
        # , command=lambda: self.StepperDirection('FanControl'))
        self.AutoCRadioButton_v1 = Radiobutton(
            self.tabFrame2, width=12, text='Target in °C')
        self.AutoCRadioButton_v1.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                                      screen_width, column=0, rowspan=1, columnspan=1, sticky='SW')
        self.TargetTemp = Entry(self.tabFrame2, width=5,
                                validate='all', validatecommand=(vcmd, '%P'))
        self.TargetTemp.grid(row=0, pady=0.045 * screen_height, padx=0.34 *
                             screen_width, column=0, rowspan=1, columnspan=1, sticky='SW')

        self.tc_label_v1 = tk.Label(
            self.tabFrame2, text="Thermal Control", borderwidth=1, relief="solid", width=13)
        self.tc_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                              screen_height, column=0, rowspan=1, columnspan=1, sticky='N')
        self.ven_label_v1 = tk.Label(
            self.tabFrame2, text="Ventilation", borderwidth=1, relief="solid", width=13)
        self.ven_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                               screen_height, column=0, rowspan=1, columnspan=1, sticky='S')
        self.tc_buttn_v1 = tk.Label(
            self.tabFrame2, text="", bg="light green", borderwidth=1, relief="solid", width=2)
        self.tc_buttn_v1.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                              screen_width, column=0, rowspan=1, columnspan=1, sticky='NW')
        self.ven_buttn_v1 = tk.Label(
            self.tabFrame2, text="", bg="dark green", borderwidth=1, relief="solid", width=2)
        self.ven_buttn_v1.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='SW')

        self.tPh_label_v1 = tk.Label(
            self.tabFrame2, text="T Peltier hot / °C", width=14, borderwidth=1, relief="solid")
        self.tPh_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')
        self.tPh_value_v1 = tk.Label(
            self.tabFrame2, text=" T1 ", width=6, borderwidth=1, relief="solid")
        self.tPh_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')

        self.tPc_label_v1 = tk.Label(
            self.tabFrame2, text="T Peltier cold / °C", width=14, borderwidth=1, relief="solid")
        self.tPc_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')
        self.tPc_value_v1 = tk.Label(
            self.tabFrame2, text=" T2 ", width=6, borderwidth=1, relief="solid")
        self.tPc_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')
        self.tR_label_v1 = tk.Label(
            self.tabFrame2, text="T Room / °C", width=10, borderwidth=1, relief="solid")
        self.tR_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')
        self.tR_value_v1 = tk.Label(
            self.tabFrame2, text=" T3 ", width=6, borderwidth=1, relief="solid")
        self.tR_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')
        self.tT_label_v1 = tk.Label(
            self.tabFrame2, text="T Tank / °C", width=10, borderwidth=1, relief="solid")
        self.tT_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')
        self.tT_value_v1 = tk.Label(
            self.tabFrame2, text=" T4 ", width=6, borderwidth=1, relief="solid")
        self.tT_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')

        self.tPH_label_v1 = tk.Label(
            self.tabFrame2, text="T Print head / °C", width=14, borderwidth=1, relief="solid")
        self.tPH_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')
        self.tPH_value_v1 = tk.Label(
            self.tabFrame2, text=" T5 ", width=6, borderwidth=1, relief="solid")
        self.tPH_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='NE')
        self.tPb_label_v1 = tk.Label(
            self.tabFrame2, text="T Print bed / °C", width=14, borderwidth=1, relief="solid")
        self.tPb_label_v1.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')
        self.tPb_value_v1 = tk.Label(
            self.tabFrame2, text=" T6 ", width=6, borderwidth=1, relief="solid")
        self.tPb_value_v1.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=1, sticky='SE')

        #   self.temp_frame2 = ttk.Frame(self.tabFrame2, borderwidth=1, relief="solid", width=.94*screen_width, height=.55*screen_height).grid(row=1, column=0, padx=15, pady=10, columnspan=2)
        # Real time graph stop button
        start = tk.Button(self.tabFrame2, text="Start Data", font=(
            'calbiri', 12), command=lambda: self.plot_start())  # self.python_process_deploy("realtime_temp_graph")
        start.place(x=500, y=600)
        stop = tk.Button(self.tabFrame2, text="Stop Data", font=(
            'calbiri', 12), command=lambda: self.plot_stop())
        stop.place(x=600, y=600)
        #  stop.grid(row=1, column=1)

        self.Demo2ndFrame = []
        # Image Frame
        # top vertical frame
        self.vertical_frame_v2 = ttk.Frame(
            self.tabFrame3, borderwidth=1, relief="solid", width=.94 * screen_width, height=.14 * screen_height)
        self.vertical_frame_v2.grid(
            row=0, column=0, padx=15, pady=10, columnspan=2)
        self.connected_label_v2 = tk.Label(
            self.tabFrame3, text="Connected", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=2, sticky='NW')
        self.printing_label_v2 = tk.Label(
            self.tabFrame3, text="Printing", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=2, sticky='NW')
        self.cc_label_v2 = tk.Label(self.tabFrame3, text="Cover Closed",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=2, sticky='NW')
        self.connected_buttn_v2 = tk.Label(
            self.tabFrame3, text="", bg="light green", borderwidth=1, relief="solid", width=10, font=(None, 12))
        self.connected_buttn_v2.grid(row=0, pady=0.045 * screen_height, padx=0.04 *
                                     screen_height, column=0, rowspan=1, columnspan=2, sticky='SW')
        self.printing_buttn_v2 = tk.Label(
            self.tabFrame3, text="", bg="dark green", borderwidth=1, relief="solid", width=9, font=(None, 12))
        self.printing_buttn_v2.grid(row=0, pady=0.045 * screen_height, padx=0.18 *
                                    screen_height, column=0, rowspan=1, columnspan=2, sticky='SW')
        self.cc_buttn_v2 = tk.Label(self.tabFrame3, text="", bg="dark green",
                                    borderwidth=1, relief="solid", width=12, font=(None, 12))
        self.cc_buttn_v2.grid(row=0, pady=0.045 * screen_height, padx=0.31 *
                              screen_height, column=0, rowspan=1, columnspan=2, sticky='SW')

        self.tac_label_v2 = tk.Label(
            self.tabFrame3, text="Temp. Auto Control", borderwidth=1, relief="solid", width=18)
        self.tac_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='NW')
        # , command=lambda: self.StepperDirection('FanControl'))
        self.AutoCRadioButton_v2 = Radiobutton(
            self.tabFrame3, width=12, text='Target in °C')
        self.AutoCRadioButton_v2.grid(row=0, pady=0.045 * screen_height, padx=0.27 *
                                      screen_width, column=0, rowspan=1, columnspan=2, sticky='SW')
        self.TargetTemp = Entry(self.tabFrame3, width=5,
                                validate='all', validatecommand=(vcmd, '%P'))
        self.TargetTemp.grid(row=0, pady=0.045 * screen_height, padx=0.34 *
                             screen_width, column=0, rowspan=1, columnspan=2, sticky='SW')

        self.tc_label_v2 = tk.Label(
            self.tabFrame3, text="Thermal Control", borderwidth=1, relief="solid", width=13)
        self.tc_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                              screen_height, column=0, rowspan=1, columnspan=2, sticky='N')
        self.ven_label_v2 = tk.Label(
            self.tabFrame3, text="Ventilation", borderwidth=1, relief="solid", width=13)
        self.ven_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.70 *
                               screen_height, column=0, rowspan=1, columnspan=2, sticky='S')
        self.tc_buttn_v2 = tk.Label(
            self.tabFrame3, text="", bg="light green", borderwidth=1, relief="solid", width=2)
        self.tc_buttn_v2.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                              screen_width, column=0, rowspan=1, columnspan=2, sticky='NW')
        self.ven_buttn_v2 = tk.Label(
            self.tabFrame3, text="", bg="dark green", borderwidth=1, relief="solid", width=2)
        self.ven_buttn_v2.grid(row=0, pady=0.045 * screen_height, padx=0.42 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='SW')

        self.tPh_label_v2 = tk.Label(
            self.tabFrame3, text="T Peltier hot / °C", width=14, borderwidth=1, relief="solid")
        self.tPh_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')
        self.tPh_value_v2 = tk.Label(
            self.tabFrame3, text=" T1 ", width=6, borderwidth=1, relief="solid")
        self.tPh_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')

        self.tPc_label_v2 = tk.Label(
            self.tabFrame3, text="T Peltier cold / °C", width=14, borderwidth=1, relief="solid")
        self.tPc_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.065 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')
        self.tPc_value_v2 = tk.Label(
            self.tabFrame3, text=" T2 ", width=6, borderwidth=1, relief="solid")
        self.tPc_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.025 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')
        self.tR_label_v2 = tk.Label(
            self.tabFrame3, text="T Room / °C", width=10, borderwidth=1, relief="solid")
        self.tR_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')
        self.tR_value_v2 = tk.Label(
            self.tabFrame3, text=" T3 ", width=6, borderwidth=1, relief="solid")
        self.tR_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')
        self.tT_label_v2 = tk.Label(
            self.tabFrame3, text="T Tank / °C", width=10, borderwidth=1, relief="solid")
        self.tT_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.195 *
                              screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')
        self.tT_value_v2 = tk.Label(
            self.tabFrame3, text=" T4 ", width=6, borderwidth=1, relief="solid")
        self.tT_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.155 *
                              screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')

        self.tPH_label_v2 = tk.Label(
            self.tabFrame3, text="T Print head / °C", width=14, borderwidth=1, relief="solid")
        self.tPH_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')
        self.tPH_value_v2 = tk.Label(
            self.tabFrame3, text=" T5 ", width=6, borderwidth=1, relief="solid")
        self.tPH_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='NE')
        self.tPb_label_v2 = tk.Label(
            self.tabFrame3, text="T Print bed / °C", width=14, borderwidth=1, relief="solid")
        self.tPb_label_v2.grid(row=0, pady=0.045 * screen_height, padx=0.305 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')
        self.tPb_value_v2 = tk.Label(
            self.tabFrame3, text=" T6 ", width=6, borderwidth=1, relief="solid")
        self.tPb_value_v2.grid(row=0, pady=0.045 * screen_height, padx=0.265 *
                               screen_width, column=0, rowspan=1, columnspan=2, sticky='SE')

        # sub frame
        self.subFrame = ['subFrame1', 'subFrame2']
        i = ttk.Frame(self.tabFrame3, borderwidth=1, relief="solid", width=.46 * screen_width,
                      height=0.50 * screen_height).grid(row=1, column=0, padx=15, pady=10)
        i = ttk.Frame(self.tabFrame3, borderwidth=1, relief="solid", width=.46 * screen_width,
                      height=0.50 * screen_height).grid(row=1, column=1, padx=15, pady=10)
        i = ttk.Frame(self.tabFrame3, borderwidth=1, relief="solid", width=.94 * screen_width,
                      height=0.10 * screen_height).grid(row=2, column=0, padx=15, pady=10, columnspan=2)
        # change image button
        pButton = tk.Button(self.tabFrame3, text="Change Image",
                            command=lambda: self.open_file())
        pButton.grid(row=2, columnspan=2)
        
        # Menu bar
        sensors_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Sensors", menu=sensors_menu)
        motors_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Motors", menu=motors_menu)
        comm_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Print", menu=comm_menu)
        help_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Help", menu=help_menu)
        exit_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Exit", menu=exit_menu)
        exit_menu.add_command(label="Exit", command=self.exit)

    # function for temperature update in horizontal bar
    def update_temp(self):
        try:
            serial_data = ser_sensor.readline().decode("utf-8")
            decode_serial_temp_data = re.findall(r"[-+]?\d*\.\d+|\d+", serial_data)
            random_num5 = str(randrange(20, 35))
            random_num6 = str(randrange(20, 35))
            self.tPh_value_v0.config(text=float(decode_serial_temp_data[0]))
            self.tPc_value_v0.config(text=float(decode_serial_temp_data[1]))
            self.tR_value_v0.config(text=float(decode_serial_temp_data[2]))
            self.tT_value_v0.config(text=float(decode_serial_temp_data[3]))
            self.tPH_value_v0.config(text=50)
            self.tPb_value_v0.config(text=51)
            self.tPh_value_v1.config(text=float(decode_serial_temp_data[0]))
            self.tPc_value_v1.config(text=float(decode_serial_temp_data[1]))
            self.tR_value_v1.config(text=float(decode_serial_temp_data[2]))
            self.tT_value_v1.config(text=float(decode_serial_temp_data[3]))
            self.tPH_value_v1.config(text=50)
            self.tPb_value_v1.config(text=51)

            self.tPh_value_v2.config(text=float(decode_serial_temp_data[0]))
            self.tPc_value_v2.config(text=float(decode_serial_temp_data[1]))
            self.tR_value_v2.config(text=float(decode_serial_temp_data[2]))
            self.tT_value_v2.config(text=float(decode_serial_temp_data[3]))
            self.tPH_value_v2.config(text=50)
            self.tPb_value_v2.config(text=51)

            self.tPh_value_v0.after(1000, self.update_temp)
        except NameError as e:
            logging.info(e)
      
    

    def graph(self, event):
        graphs.tempGraph(self)

    def on(self, event):
        pass

    def off(self, event):
        pass

        print('inside off')

    def exit(self):
        ser.close()  # close serial port
        quit()

    # to stop temperature graph plot
    def plot_stop(self):
        graphs.cond = False
        self.after_cancel(self.reference)

    # to start temperature graph plot 
    def plot_start(self):
        try:
            if ser_sensor != '':
                graphs.cond = True
                graphs.tempGraph(self)
                self.reference = self.after(1000, self.plot_start)
            else:
                logging.info('Sensor controller is not detected')
        except NameError as error:
            logging.info('Sensor controller is not connected to PC')

    # to update progress bar
    @staticmethod
    def start(value):
        Gui.my_progress['value'] = value
        root.update_idletasks()

    # to stop progress bar
    def stop(self):
        Gui.reset = True
        Gui.my_progress.stop()
        tkinter.messagebox.showinfo(
                        "Notification", "Printing aborted!!")
        return

    # to decide whether entered value is integer or not
    def callback(self, P):
        if str.isdigit(P) or P == "":
            return True
        else:
            return False

    # function to control dpi (dot per inch)
    def dpi_control(self):
        try:
            if (dpi_x.get() or dpi_y.get()) != "":
                self.dpi_x1 = dpi_x.get()
                self.dpi_y1 = dpi_y.get()

                if self.dpi_x1 > 40:
                    self.dpi_x1 = 40

                if self.dpi_y1 > 40:
                    self.dpi_y1 = 40

                if self.dpi_x1 == "":
                    self.dpi_x1 = 1

                if self.dpi_y1 == "":
                    self.dpi_y1 = 1

                return self.dpi_x1, self.dpi_y1

        except Exception as e:
            dpi_x.set(5)
            dpi_y.set(5)
            self.dpi_x1 = dpi_x.set(5)
            self.dpi_y1 = dpi_y.set(5)
            return self.dpi_x1, self.dpi_y1

    # for manual control inputs - set speed,acceleration and manual coordinates
    def report_change(self, operation, mode = 'm'):

        if operation == 'speed':
            x = tk.StringVar()
            y = tk.StringVar()
            z = tk.StringVar()

            if (self.speed_x.get() and self.speed_y.get()) != '':
                xyzlist = [(int(self.speed_x.get()), int(self.speed_y.get()), 0)]

            if self.speed_x.get() != '':
                if self.y.get() == '':
                    xyzlist = [(int(self.speed_x.get()), 0, 0)]

            if self.speed_y.get() != '':
                if self.speed_x.get() == '':
                    xyzlist = [(0, int(self.speed_y.get()), 0)]

            if self.speed_x.get() == '':
                if self.speed_y.get() == '':
                    xyzlist = [(0, 0, 0)]

            x.set(mode + 'x' + self.speed_x.get())
            y.set(mode + 'y' + self.speed_y.get())
            z.set(mode + 'z' + self.speed_z.get())

            # X Y and Z coordinate
            if (self.speed_x.get() and self.speed_y.get() and self.speed_z.get()) != '':  # x.y and z movement
                logging.info('speed is:- ', str(self.speed_z.get()))
                x.set(mode + 'x' + self.speed_x.get())
                y.set('y' + self.speed_y.get())
                z.set('z' + self.speed_z.get())
                # you can add it and write it to serial buffer
                s = x.get() + y.get() + z.get()
                ser.write(s.encode())
            else:
                if self.speed_x.get() != '':  
                    if self.speed_y.get() == '' and self.speed_z.get() == '':
                        x.set(mode + 'x' + self.speed_x.get())
                        ser.write(x.get().encode())
                        s = x.get()
                        logging.info("set speed is {}".format(x.get()))

                if self.speed_y.get() != '':  # y movement
                    if self.speed_x.get() == '' and self.speed_z.get() == '':
                        y.set(mode + 'y' + self.speed_y.get())
                        ser.write(y.get().encode())
                        s = y.get()
                        logging.info("set speed is {}".format(y.get()))

                if self.speed_z.get() != '': 
                    if self.speed_x.get() == '' and self.speed_y.get() == '':
                        z.set(mode + 'z' + self.speed_z.get())
                        ser.write(z.get().encode())
                        s = z.get()
                        logging.info("set speed is {}".format(z.get()))
            if self.speed_z.get() == '':  
                if self.speed_x.get() != '':
                    if self.speed_y.get() != '':
                        x.set(mode + 'x' + self.speed_x.get())
                        y.set('y' + self.speed_y.get())
                        s = x.get() + y.get()
                        logging.info("Print coordinates are {}".format(s))
                        ser.write(s.encode())

            if self.speed_x.get() == '':  
                if self.speed_y.get() != '':
                    if self.speed_z.get() != '':
                        y.set(mode + 'y' + self.speed_y.get())
                        z.set('z' + self.speed_z.get())
                        s = y.get() + z.get()
                        logging.info("Print coordinates are {}".format(s))
                        ser.write(s.encode())
            

            if self.speed_x.get() == '':
                if self.speed_y.get() == '':
                    if self.speed_z.get() == '':
                        tkinter.messagebox.showinfo(
                            "Notification", "Please give velocity values")
                      
            else:
                tkinter.messagebox.showinfo(
                    "Notification", "Velocity values set successfully")
    

        elif operation == 'acceleration':
            x = tk.StringVar()
            y = tk.StringVar()
            z = tk.StringVar()

            if (self.acceleration_x.get() and self.acceleration_y.get()) != '':
                xyzlist = [(int(self.acceleration_x.get()), int(self.acceleration_y.get()), 0)]

            if self.acceleration_x.get() != '':
                if self.acceleration_y.get() == '':
                    xyzlist = [(int(self.acceleration_x.get()), 0, 0)]

            if self.acceleration_y.get() != '':
                if self.acceleration_x.get() == '':
                    xyzlist = [(0, int(self.acceleration_y.get()), 0)]

            if self.acceleration_x.get() == '':
                if self.acceleration_y.get() == '':
                    xyzlist = [(0, 0, 0)]

            x.set(mode + 'x' + self.acceleration_x.get())
            y.set(mode + 'y' + self.acceleration_y.get())
            z.set(mode + 'z' + self.acceleration_z.get())

            if (self.acceleration_x.get() and self.acceleration_y.get() and self.acceleration_z.get()) != '':  # x.y and z movement
                logging.info('acceleration is:- ', str(self.acceleration_z.get()))
                x.set(mode + 'x' + self.acceleration_x.get())
                y.set('y' + self.acceleration_y.get())
                z.set('z' + self.acceleration_z.get())
                # you can add it and write it to serial buffer
                s = x.get() + y.get() + z.get()
                logging.info("set acceleration is {}".format(s))
                ser.write(s.encode())
            else:
                if self.acceleration_x.get() != '':  
                    if self.acceleration_y.get() == '' and self.acceleration_z.get() == '':
                        x.set(mode + 'x' + self.acceleration_x.get())
                        ser.write(x.get().encode())
                        s = x.get()
                        logging.info("set acceleration is {}".format(x.get()))

                if self.acceleration_y.get() != '': 
                    if self.acceleration_x.get() == '' and self.acceleration_z.get() == '':
                        y.set(mode + 'y' + self.acceleration_y.get())
                        ser.write(y.get().encode())
                        s = y.get()

                if self.acceleration_z.get() != '':  
                    if self.acceleration_x.get() == '' and self.acceleration_y.get() == '':
                        z.set(mode + 'z' + self.acceleration_z.get())
                        ser.write(z.get().encode())
                        s = z.get()

            if self.acceleration_z.get() == '':  
                if self.acceleration_x.get() != '':
                    if self.acceleration_y.get() != '':
                        x.set(mode + 'x' + self.acceleration_x.get())
                        y.set('y' + self.acceleration_y.get())
                        s = x.get() + y.get()
                        ser.write(s.encode())

            if self.acceleration_x.get() == '': 
                if self.acceleration_y.get() != '':
                    if self.acceleration_z.get() != '':
                        y.set(mode + 'y' + self.acceleration_y.get())
                        z.set('z' + self.acceleration_z.get())
                        s = y.get() + z.get()
                        ser.write(s.encode())

            if self.acceleration_x.get() == '':
                if self.acceleration_y.get() == '':
                    if self.acceleration_z.get() == '':
                        tkinter.messagebox.showinfo(
                            "Notification", "Please give acceleration values")
                      
            else:
                tkinter.messagebox.showinfo(
                    "Notification", "Acceleration values set successfully")

        elif operation == 'manualControl':
            x = tk.StringVar()
            y = tk.StringVar()
            z = tk.StringVar()
            self.iteration_cnt = 1
            self.listXyz = [self.x.get(), self.y.get(), self.z.get()]

            if (self.x.get() and self.y.get()) != '':
                xyzlist = [(int(self.x.get()), int(self.y.get()), 0)]

            if self.x.get() != '':
                if self.y.get() == '':
                    xyzlist = [(int(self.x.get()), 0, 0)]

            if self.y.get() != '':
                if self.x.get() == '':
                    xyzlist = [(0, int(self.y.get()), 0)]

            if self.x.get() == '':
                if self.y.get() == '':
                    xyzlist = [(0, 0, 0)]

            x.set(mode + 'x' + self.x.get())
            y.set(mode + 'y' + self.y.get())
            z.set(mode + 'z' + self.z.get())
            logging.info(xyzlist)
            graphs.pathGraph(self, xyzlist)
            self.tabFrame3.update()
            self.tabDemo.update()

            # X Y and Z coordinate
            if (self.x.get() and self.y.get() and self.z.get()) != '':  # x.y and z movement
                logging.info('z is:- ', str(self.z.get()))
                x.set(mode + 'x' + self.x.get())
                y.set('y' + self.y.get())
                z.set('z' + self.z.get())
                # you can add it and write it to serial buffer
                s = x.get() + y.get() + z.get()
                logging.info("logging.info coordinates are {}".format(s))
                ser.write(s.encode())
            else:
                if self.x.get() != '':  # x movement
                    if self.y.get() == '' and self.z.get() == '':
                        x.set(mode + 'x' + self.x.get())
                        ser.write(x.get().encode())
                        s = x.get()
                        logging.info("logging.info coordinates are {}".format(x.get()))

                if self.y.get() != '':  # y movement
                    if self.x.get() == '' and self.z.get() == '':
                        y.set(mode + 'y' + self.y.get())
                        ser.write(y.get().encode())
                        s = y.get()
                        logging.info("logging.info coordinates are {}".format(y.get()))

                if self.z.get() != '':  # z movement
                    if self.x.get() == '' and self.y.get() == '':
                        z.set(mode + 'z' + self.z.get())
                        ser.write(z.get().encode())
                        s = z.get()
                        logging.info("logging.info coordinates are {}".format(z.get()))
            # x and y
            if self.z.get() == '':  # x and y movement
                if self.x.get() != '':
                    if self.y.get() != '':
                        x.set(mode + 'x' + self.x.get())
                        y.set('y' + self.y.get())
                        s = x.get() + y.get()
                        logging.info("logging.info coordinates are {}".format(s))
                        ser.write(s.encode())

            if self.x.get() == '':
                if self.y.get() == '':
                    if self.z.get() == '':
                        tkinter.messagebox.showinfo(
                            "Notification", "Please give manual coordinates")
                        with open("CoordinateFile.txt", "w") as file:
                            for item in self.listXyz:
                                file.write(str(item) + "\n")
            
                   #   return
            else:
                logging.info('inside else')
                with open("CoordinateFile.txt", "w") as file:
                    for item in self.listXyz:
                        file.write(str(item) + "\n")
             #   return
            logging.info('after else')

        elif operation == 'Calibrate':
            ser.write(b'h')
           

    # function for x+,y+,z+,x-,y- and z- buttons 
    def incrementalChangeButton(self,buttonClicked=None):
        xValue = tk.StringVar()
        yValue = tk.StringVar()
        zValue = tk.StringVar()

        if self.iteration_cnt == 1:
            with open("CoordinateFile.txt", "r") as file:
                readLines = file.readlines()
            if len(readLines) == 3 and readLines[2] != '\n':
                self.xCor = int(readLines[0])
                self.yCor = int(readLines[1])
                self.zCor = int(readLines[2])
            else:
                logging.info('check no of lines in CoordinateFile.txt')
                self.xCor = int(readLines[0])
                if readLines[1] == '\n':
                    self.yCor = 1
                if readLines[2] == '\n':
                    self.zCor = 1
            self.iteration_cnt = 2
        try:
            if int(self.xCor) > 0  and int(self.yCor) > 0  and int(self.zCor) > 0:

                if buttonClicked == 'xButton+':
                    self.incrementValue = self.xCor + 1
                    self.xCor+=1
                    xValue.set('m' + 'x' + str(self.incrementValue))
                    ser.write(xValue.get().encode())
                    logging.info(xValue.get())

                if buttonClicked == 'xButton-':
                    self.incrementValue = self.xCor - 1
                    self.xCor-=1
                    xValue.set('m' + 'x' + str(self.incrementValue))
                    ser.write(xValue.get().encode())
                    logging.info(xValue.get())

                if buttonClicked == 'yButton+':
                    self.incrementValue = self.yCor + 1
                    self.yCor+=1
                    yValue.set('m' + 'y' + str(self.incrementValue))
                    ser.write(yValue.get().encode())
                    logging.info(yValue.get())

                if buttonClicked == 'yButton-':
                    self.incrementValue = self.yCor - 1
                    self.yCor-=1
                    yValue.set('m' + 'y' + str(self.incrementValue))
                    ser.write(yValue.get().encode())
                    logging.info(yValue.get())

                if buttonClicked == 'zButton+':
                    self.incrementValue = self.zCor + 1
                    self.zCor+=1
                    zValue.set('m' + 'z' + str(self.incrementValue))
                    ser.write(zValue.get().encode())
                    logging.info(zValue.get())

                if buttonClicked == 'zButton-':
                    self.incrementValue = self.zCor - 1
                    self.zCor-=1
                    zValue.set('m' + 'z' + str(self.incrementValue))
                    ser.write(zValue.get().encode())
                    logging.info(zValue.get())

                if buttonClicked == 'zeroPosition':
                    data = 'mx0y0z0'
                    ser.write(data.encode())
             
                if buttonClicked != 'zeroPosition':
                    pass
            else:
                logging.info('Number is less than 0')
                if self.xCor == 0:
                    logging.info('x')
                    self.xCor = 1
                elif self.yCor == 0:
                    logging.info('y')
                    self.yCor = 1
                elif self.zCor == 0:
                    logging.info('z')
                    self.zCor = 1
                tkinter.messagebox.showinfo("Notification", "Either X/Y/Z has reached 0, logging.infoer will move to X/Y/Z = 1")

        except Exception as e:
            logging.info(e)

    # to control ventillation fan and other peripherals
    def utility_control(self, button):
        try:
            if button == 'fanControl':

                if (varForFan.get()) == 2:
                    ser.write(b'y')
                    tkinter.messagebox.showinfo(
                        "Notification", "Fan turned on successfully")

                elif (varForFan.get()) == 3:
                    ser.write(b'x')
                    tkinter.messagebox.showinfo(
                        "Notification", "Fan turned off successfully")

        except Exception as e:
            logging.info('Please press the button again {}'.format(e))

    # function for will be used to browse .bmp files
    def open_file(self):
        intialdir = "/Users/Default/Desktop/work/3d_gui_printer/"
        self.filename = filedialog.askopenfilenames(initialdir=intialdir, title="Select a File", filetypes=(
            ("Text files", "*.bmp*"), ("all files", "*.*")))

        img = Image.open(self.filename[0])
        img = img.resize((590, 360), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.tabFrame3, image=img)
        panel.image = img
        panel.grid(row=1, column=0)
        return True

    # function to start printing process by calling imageprocessing() function
    def printExecution(self):
        try:
            Gui.abort_button['state'] = NORMAL
            self.ListOfFiles = list()
            start = "C:/Users/Default/Desktop/work/3d_gui_printer/"
            if self.filename != None:
                tkinter.messagebox.showinfo(
                    "Print Button Clicked", "Printing started Successfully")
                for i in self.filename:
                    logging.info(i)
                    relative_path = os.path.relpath(i, start)
                    self.ListOfFiles.append(relative_path)
                logging.info(self.ListOfFiles)
                x, y = self.dpi_control()
               
                if x >= 10 and y >= 10:
                    size = (x, y)
                    im = Image.open(self.ListOfFiles[0])
                    im_resized = im.resize(size, Image.ANTIALIAS)
                    im_resized.save("my_image_resized.bmp", "BMP")
                    self.ListOfFiles[0] = "my_image_resized.bmp"
                    self.ListOfFiles[0] = "my_image_resized.bmp"
                else:
                    logging.info('Please select proper DPI value')

                # call to imageprocessing method
                ImageProcess.imageprocessing(self, self.ListOfFiles)
            else:
                tkinter.messagebox.showinfo(
                    "Print Button Clicked", "Image not selected")
                logging.info('Files not selected')

        except NameError as e:
            logging.info('{}'.format(e))

    # function to deploy functions in threads
    def python_process_deploy(self, thread_to_deploy):
        try:
            if thread_to_deploy == "print_execution":
                threading.Thread(target=self.printExecution).start()

            if thread_to_deploy == "temp_update":
                threading.Thread(target=self.update_temp).start()

            if thread_to_deploy == "realtime_temp_graph":
                threading.Thread(target=self.plot_start).start()

        except Exception as e:
            logging.info(e)

# Class for image processing activities
class ImageProcess(Gui):

    def __init__(self):
        np.set_printoptions(threshold=sys.maxsize)

    # function to extract print coordinates from an image and pass it to inkjet printer 
    @staticmethod
    def imageprocessing(self, imageFile):
        logging.info('inside image processing')
        listofimages = imageFile
        finalXYZList = []
        command = 'Enter Command:'
        z = -2
        count = 0
        if listofimages != []:
            for images in listofimages:
                imgfile = Image.open(images)
                imgarray = np.array(imgfile)
                x, y = np.where((imgarray[:, :, 0:3] == [0, 0, 0]).all(2))
                count += 1
                logging.info(x, y)
                logging.info('Image Count:- ', count)
                z = z + 2
                completeTuple = [(m, n, z) for m, n in zip(x, y)]
                for x, y, z in completeTuple:
                    finalX = str('m') + str('x') + str(x)
                    finalY = str('y') + str(y)
                    finalZ = str('z') + str(z)
                    finalXYZList.append(finalX + finalY + finalZ)

                graphs.pathGraph(self, completeTuple)
                self.tabFrame3.update()
                self.tabDemo.update()
                logging.info(finalXYZList)
                self.length_of_coordinates_list = len(finalXYZList)
                ImageProcess.cnt = 0
                while True:
                    for i in finalXYZList:
                        if Gui.reset == False:
                            logging.info('Reset status is', Gui.reset)
                            ImageProcess.print_coordinate(i)
                            progress_value = (
                                ImageProcess.cnt / self.length_of_coordinates_list) * 100
                            Gui.start(progress_value)

                        else:
                            logging.info('Reset status is {}'.format(Gui.reset))
                            Gui.start(0)
                            Gui.reset = False
                            break
                    break
                Gui.abort_button['state'] = DISABLED
                logging.info('Printing Done...')
                tkinter.messagebox.showinfo(
                    "Notification", "Printing Done..!!")
                finalXYZList = []

        else:
            logging.info('Print Images not selected')

    # recursive function to to send print coordinates to inkjet printer
    def print_coordinate(i):
        command = 'Enter Command:'
        # serial flush could be required here becuase buffer should not have any data intially
        if command in (ser.readline().decode("utf-8")):
            ImageProcess.cnt += 1
            ser.write(i.encode())
        else:
            ImageProcess.print_coordinate(i)

# Class for printing graphs on UI
class graphs():
    data = np.array([])
    sensor_2 = list()
    sensor_3 = list()
    sensor_4 = list()
    cond = False
    selected = True
    ymaxx = 100
    xmaxx = 20

    # function for graph layout on UI
    # Note- labels for each sensor could be added
    @staticmethod
    def graph_plot(self):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        if graphs.selected == True:
            logging.info('inside selected')
            fig = Figure()
            self.ax = fig.add_subplot(111)
            self.ax.set_title('Temperature Data')
            self.ax.set_xlabel('Time')
            self.ax.set_ylabel('Temperature')
            self.ax.set_xlim(0, graphs.xmaxx)
            self.ax.set_ylim(0, graphs.ymaxx)
            self.line_1 = self.ax.plot([], [])[0]
            self.line_2 = self.ax.plot([], [])[0]
            self.line_3 = self.ax.plot([], [])[0]
            self.line_4 = self.ax.plot([], [])[0]
            self.canvas = FigureCanvasTkAgg(fig, master=self.tabFrame2)
            self.canvas.get_tk_widget().place(x=30, y=150, width=.92 *
                                              screen_width, height=0.5 * screen_height)
            self.canvas.draw()

    # to get real time temperature graph on UI
    @staticmethod
    def tempGraph(self):
        if str(self.tabs.index(self.tabs.select())) == '1':
            try:
                serial_data = ser_sensor.readline().decode("utf-8")
            except NameError as e:
                logging.info(e)

            graphs.graph_plot(self)
            graphs.selected = False
            if graphs.cond == True:
                serial_data = ser_sensor.readline().decode("utf-8")
                a = re.findall(r"[-+]?\d*\.\d+|\d+", serial_data)
                a[1] = float(a[1])
                a[2] = float(a[2])
                a[3] = float(a[3])

                if (len(graphs.data) < 2000):
                    graphs.data = np.append(graphs.data, float(a[0][0:4]))

                else:
                    graphs.data[0:99] = graphs.data[1:100]
                    graphs.data[99] = float(a[0][0:4])

                graphs.sensor_2.append(a[1])
                graphs.sensor_3.append(a[2])
                graphs.sensor_4.append(a[3])
                data = np.arange(0, len(graphs.data))
                xmax = np.max(data)

                if xmax >= graphs.xmaxx:
                    graphs.xmaxx += 20
                    self.ax.set_xlim(0, graphs.xmaxx)

                self.line_1.set_xdata(np.arange(0, len(graphs.data)))
                self.line_1.set_ydata(graphs.data)
                self.line_2.set_xdata(np.arange(0, len(graphs.sensor_2)))
                self.line_2.set_ydata(graphs.sensor_2)
                self.line_3.set_xdata(np.arange(0, len(graphs.sensor_3)))
                self.line_3.set_ydata(graphs.sensor_3)
                self.line_4.set_xdata(np.arange(0, len(graphs.sensor_4)))
                self.line_4.set_ydata(graphs.sensor_4)
                self.canvas.draw()
        else:
            if hasattr(self, 'reference'):
                pass

    # to get image coordinate graph (red dots) on UI
    @staticmethod
    def pathGraph(self, xAndYlist):
        x1 = []
        y1 = []
        graphs.cond = False
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        for x, y, z in xAndYlist:
            x1.append(x)
            y1.append(y)

        logging.info('in path graph')

        if str(self.tabs.index(self.tabs.select())) == "0":
            logging.info('inside if loop of path graph')
            self.tabFrame3.update()
            self.tabDemo.update()
            figure = Figure(figsize=(13.2, 8), dpi=45)
            plot = figure.add_subplot(1, 1, 1)
            plot.set_title('Path View')
            plot.minorticks_on()
            plot.plot(x1, y1, 'ro')
            plot.grid(b=True, which='major', color='#666666', linestyle='-')
            plot.grid(b=True, which='minor', color='#999999',
                      linestyle='-', alpha=0.2)

            figure_2 = Figure(figsize=(4.9, 5.1), dpi=75)
            plot_2 = figure_2.add_subplot(1, 1, 1)
            plot_2.set_title('Path View')
            plot_2.minorticks_on()
            plot_2.plot(x1, y1, 'ro')
            plot_2.grid(b=True, which='major', color='#666666', linestyle='-')
            plot_2.grid(b=True, which='minor', color='#999999',
                        linestyle='-', alpha=0.2)

            figure_3 = Figure(figsize=(4.4, 2.6), dpi=75)
            plot_3 = figure_3.add_subplot(1, 1, 1)
            plot_3.set_title('Current position of axis')
            plot_3.minorticks_on()
            plot_3.plot([x1[-1:]], [y1[-1:]], 'ro')
            plot_3.grid(b=True, which='major', color='#666666', linestyle='-')
            plot_3.grid(b=True, which='minor', color='#999999',
                        linestyle='-', alpha=0.2)

            canvas = FigureCanvasTkAgg(figure, self.tabFrame3)
            canvas.get_tk_widget().grid(row=1, column=1, pady=0.05 * screen_height, sticky='N')

            canvasforTab1 = FigureCanvasTkAgg(figure_2, self.tabDemo)
            canvasforTab1.get_tk_widget().grid(
                row=1, column=2, pady=0.05 * screen_height, sticky='N')

            canvasforTab2 = FigureCanvasTkAgg(figure_3, self.tabDemo)
            canvasforTab2.get_tk_widget().grid(
                row=1, column=0, pady=0.05 * screen_height, sticky='N')

        else:
            logging.info("Not in img/path tab")

# main function to call UI 
def main():
    guiObj = Gui(root)
    guiObj.python_process_deploy("temp_update")
    guiObj.python_process_deploy("realtime_temp_graph")
    root.config(menu=main_menu)
    root.mainloop()


# Detects serial device, If found, UI starts working
if __name__ == "__main__":
    pid = '16C0'
    hid = '0483'
    printer_controller_serial_number = '8158090'
    sensor_controller_serial_number = '9584710'
    ports = serial.tools.list_ports.comports()
    if ports != []:
        for p in ports:
            if pid and hid in p.hwid:
                serial_port_no = p.device
                logging.info('Device is {}'.format(str(p.hwid)))
                if p.serial_number == printer_controller_serial_number:
                    try:
                        # check your com port
                        ser = s.Serial(serial_port_no, 9600)
                        logging.info(
                            'Printer controller connected port is {}'.format(serial_port_no))
                      #  main()
                    except Exception as e:
                        logging.info(
                            'Please check the serial port Number {}'.format(e))

                if p.serial_number == sensor_controller_serial_number:
                    serial_port_no = p.device
                    try:
                        # check your com port
                        ser_sensor = s.Serial(serial_port_no, 9600)
                        logging.info(
                            'Sensor controller connected port is {}'.format(serial_port_no))
                        main()

                    except Exception as e:
                        logging.info(
                            'Please check the serial port Number {}'.format(e))

            else:
                logging.info(
                    'Please connect the device to the computer and check the serial port')
    else:
        logging.info(
            'Please connect the device to the computer and check the serial port')
