#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 07:40:09 2018

@author: davidhagan
"""

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Menu
import boto3
import decimal
from datetime import datetime

#################
#Dynamodb connection:
session = boto3.setup_default_session(profile_name='dynamo')
dynamodb = boto3.resource('dynamodb',region_name='us-east-1')

table = dynamodb.Table('wellness')

#################
# FUNCTIONS
#################


# Exit GUI cleanly
def _quit():
	win.quit()
	win.destroy()
	exit()
    
    
#################
# Procedural Code
#################

# instantiate
win = tk.Tk()

# title
win.title('wellness input')

#tab control / notebook intro here

tabControl = ttk.Notebook(win)  	#create tab control

tab1=ttk.Frame(tabControl)			#create a tab
tabControl.add(tab1, text='Supplements')	#add the tab

tab2 = ttk.Frame(tabControl)		#create 2nd tab control
tabControl.add(tab2, text='Measurements')	#add the tab

tabControl.pack(expand=1, fill='both')	#make visible

#----------------------------------------------------
#we are creating a container to hold all the widgets
supp_frame = ttk.LabelFrame(tab1, text='Supplement Input')
meas_frame = ttk.LabelFrame(tab2, text='Measurements Input')

# using the tkinter grid layout method
supp_frame.grid(column=1, row=0, padx=8, pady=4)
meas_frame.grid(column=1, row=0, padx=8, pady=4)

#################
# measurements
#################

# functions
measurement_capture = {}

def submit_meas_data_current():
    measurement_capture['fat'] = decimal.Decimal(fat_input.get())
    measurement_capture['weight'] = decimal.Decimal(weight_input.get())
    measurement_capture['hydration'] = decimal.Decimal(hydration_input.get())
    measurement_capture['waist'] = decimal.Decimal(waist_input.get())
    measurement_capture['left-calf'] = decimal.Decimal(ltcalf_input.get())
    measurement_capture['right-calf'] = decimal.Decimal(rtcalf_input.get())
    measurement_capture['left-leg'] = decimal.Decimal(ltleg_input.get())
    measurement_capture['right-leg'] = decimal.Decimal(rtleg_input.get())
    measurement_capture['right-grip'] = decimal.Decimal(rtgrip_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    for key in list(measurement_capture.keys()):  ## creates a list of all keys
        if measurement_capture[key] == 0.0:
            del measurement_capture[key]
            
    realm = 'measurements'
    timestamp = str(datetime.today())
    required_hash_data = {
        'realm': realm,
        'timestamp': timestamp
    }
#    #combine dicts
    final_input_data = measurement_capture.copy()
    final_input_data.update(required_hash_data)
    print(final_input_data)
#    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)

    print("PutItem succeeded:")

def submit_meas_data_historical():
    measurement_capture['fat'] = decimal.Decimal(fat_input.get())
    measurement_capture['weight'] = decimal.Decimal(weight_input.get())
    measurement_capture['hydration'] = decimal.Decimal(hydration_input.get())
    measurement_capture['waist'] = decimal.Decimal(waist_input.get())
    measurement_capture['left-calf'] = decimal.Decimal(ltcalf_input.get())
    measurement_capture['right-calf'] = decimal.Decimal(rtcalf_input.get())
    measurement_capture['left-leg'] = decimal.Decimal(ltleg_input.get())
    measurement_capture['right-leg'] = decimal.Decimal(rtleg_input.get())
    measurement_capture['right-grip'] = decimal.Decimal(rtgrip_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    for key in list(measurement_capture.keys()):  ## creates a list of all keys
        if measurement_capture[key] == 0.0:
            del measurement_capture[key]
            
    realm = 'measurements'
    timestamp = hist_meas_input.get()
    required_hash_data = {
        'realm': realm,
        'timestamp': timestamp
    }
#    #combine dicts 	
    final_input_data = measurement_capture.copy()
    final_input_data.update(required_hash_data)

#    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)

    print("PutItem succeeded:")

#add the submit and cancel buttons
tk.Button(meas_frame, text='Submit Current', command=submit_meas_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(meas_frame, text='Submit Historical', command=submit_meas_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_meas_input = tk.StringVar(value='2017-05-07 08:00:00')
tk.Entry(meas_frame, text='what', textvariable=hist_meas_input).grid(row=1, column=2, columnspan=2)
tk.Button(meas_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)

#inputs
ttk.Label(meas_frame, text='Right Grip').grid(row=2, column=0, sticky = 'E')
rtgrip_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtgrip_input).grid(row=2, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Left Grip').grid(row=3, column=0, sticky = 'E')
ltgrip_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=ltgrip_input).grid(row=3, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Weight in lbs').grid(row=4, column=0, sticky = 'E')
weight_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=weight_input).grid(row=4, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Fat %').grid(row=5, column=0, sticky = 'E')
fat_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=fat_input).grid(row=5, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Hydration %').grid(row=6, column=0, sticky = 'E')
hydration_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=hydration_input).grid(row=6, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Waist in Inches').grid(row=7, column=0, sticky = 'E')
waist_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=waist_input).grid(row=7, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Left Calf in Inches').grid(row=8, column=0, sticky = 'E')
ltcalf_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=ltcalf_input).grid(row=8, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Right Calf in Inches').grid(row=9, column=0, sticky = 'E')
rtcalf_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtcalf_input).grid(row=9, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Left Leg in Inches').grid(row=10, column=0, sticky = 'E')
ltleg_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=ltleg_input).grid(row=10, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Right Leg in Inches').grid(row=11, column=0, sticky = 'E')
rtleg_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtleg_input).grid(row=11, column=1,sticky = tk.E+tk.W)



#################
# supplements
#################
    
data = {}
def submit_data_current():
    data['taurine'] = decimal.Decimal(taurine.get())
    data['vitaminD'] = decimal.Decimal(vitaminD.get())
    data['beta-alanine'] = decimal.Decimal(betaAlanine.get())
    data['liver'] = decimal.Decimal(liver.get())
    data['curcumin'] = decimal.Decimal(curcumin.get())
    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
    data['garlic'] = decimal.Decimal(garlic.get()*500)
    data['parsley'] = decimal.Decimal(garlic.get()*150)
    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
    data['tyrosine'] = decimal.Decimal(tyrosine.get())
    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
    data['creatine'] = decimal.Decimal(creatine.get()*700)
    for key in list(data.keys()):  ## creates a list of all keys
        if data[key] == 0:
            del data[key]
            
    realm = 'supplements'
    timestamp = str(datetime.today())
    required_hash_data = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data = data.copy()
    final_input_data.update(required_hash_data)
    print(final_input_data)

    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)

    print("PutItem succeeded:")
    
def submit_data_historical():
    data['taurine'] = decimal.Decimal(taurine.get())
    data['vitaminD'] = decimal.Decimal(vitaminD.get())
    data['beta-alanine'] = decimal.Decimal(betaAlanine.get())
    data['liver'] = decimal.Decimal(liver.get())
    data['curcumin'] = decimal.Decimal(curcumin.get())
    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
    data['garlic'] = decimal.Decimal(garlic.get()*500)
    data['parsley'] = decimal.Decimal(garlic.get()*150)
    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
    data['tyrosine'] = decimal.Decimal(tyrosine.get())
    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
    data['creatine'] = decimal.Decimal(creatine.get()*700)
    data['niacin'] = decimal.Decimal(niacin.get()*100)
    data['msm'] = decimal.Decimal(msm.get()*100)
    for key in list(data.keys()):  ## creates a list of all keys
        if data[key] == 0:
            del data[key]
            
    realm = 'supplements'
    timestamp = hist_input.get()
    required_hash_data = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data = data.copy()
    final_input_data.update(required_hash_data)
    print(final_input_data)

    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)

    print("PutItem succeeded:")

# entry width wag
ENTRY_WIDTH = 20

# adding Label and Text Entry widgets
#----------------------------------------
#add the submit and cancel buttons
tk.Button(supp_frame, text='Submit Current', command=submit_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(supp_frame, text='Submit Historical', command=submit_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_input = tk.StringVar(value='2017-05-07 08:00:00')
tk.Entry(supp_frame, text='what', textvariable=hist_input).grid(row=1, column=2, columnspan=2)
tk.Button(supp_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)

#BR Nutrition L-Tyrosine
ttk.Label(supp_frame, text='L-Tyrosine').grid(row=2, column=0, sticky = 'E')
tyrosine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=tyrosine, value=0).grid(row=2, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=tyrosine, value=500).grid(row=2, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=tyrosine, value=1000).grid(row=2, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=2, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=2, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=2, column=6,sticky = tk.E+tk.W)

#vitaminD
ttk.Label(supp_frame, text='VitaminD (liquid)').grid(row=3, column=0, sticky = 'E')
vitaminD = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=vitaminD, bg='tan', pady=5, value=0).grid(row=3, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 drop', variable=vitaminD, padx=5,  bg='tan', pady=5, value=400).grid(row=3, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=800).grid(row=3, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=1200).grid(row=3, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=1600).grid(row=3, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=2000).grid(row=3, column=6, sticky = tk.E+tk.W)
#----------------------------------------------------
#beta alanine
ttk.Label(supp_frame, text='beta-alanine').grid(row=4, column=0, sticky = 'E')
betaAlanine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=betaAlanine, bg='tan', pady=5, value=0).grid(row=4, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=1500).grid(row=4, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=2250).grid(row=4, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=3000).grid(row=4, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=4, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=4, column=6,sticky = tk.E+tk.W)
#liver pills
ttk.Label(supp_frame, text='Liver pills').grid(row=5, column=0, sticky = 'E')
liver = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=liver, bg='tan', pady=5, value=0).grid(row=5, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=liver, bg='tan', pady=5, value=750).grid(row=5, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=liver, bg='tan', pady=5, value=1500).grid(row=5, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=liver, bg='tan', pady=5, value=2250).grid(row=5, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=liver, bg='tan', pady=5, value=3000).grid(row=5, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=liver, bg='tan', pady=5, value=3750).grid(row=5, column=6, sticky = tk.E+tk.W)
#curcumin
ttk.Label(supp_frame, text='Curcumin').grid(row=6, column=0, sticky = 'E')
curcumin = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=curcumin, value=0).grid(row=6, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=curcumin, value=500).grid(row=6, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=curcumin, value=1000).grid(row=6, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=6,sticky = tk.E+tk.W)
#Jarrow QH/PQQ
ttk.Label(supp_frame, text='QH-absorb/PQQ').grid(row=7, column=0, sticky = 'E')
qh_pqq = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=qh_pqq, value=0).grid(row=7, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=qh_pqq, value=1).grid(row=7, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=qh_pqq, value=2).grid(row=7, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=6,sticky = tk.E+tk.W)
#garlic BR Nutrition
ttk.Label(supp_frame, text='Garlic').grid(row=8, column=0, sticky = 'E')
garlic = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=garlic, bg='tan', pady=5, value=0).grid(row=8, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=garlic, bg='tan', pady=5, value=1).grid(row=8, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=garlic, bg='tan', pady=5, value=2).grid(row=8, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=garlic, bg='tan', pady=5, value=3).grid(row=8, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=garlic, bg='tan', pady=5, value=4).grid(row=8, column=5, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=8, column=6, sticky = tk.E+tk.W)
#Jarrow Pantothenic Acid B5
ttk.Label(supp_frame, text='Pantothenic Acid B5').grid(row=9, column=0, sticky = 'E')
pant_acid = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=pant_acid, value=0).grid(row=9, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=pant_acid, value=500).grid(row=9, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=pant_acid, value=1000).grid(row=9, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=6,sticky = tk.E+tk.W)
#BR Nutrition Acetyl-L-Carnitine
ttk.Label(supp_frame, text='Acetyl-l-Carnitine').grid(row=10, column=0, sticky = 'E')
acetylCarnitine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=0).grid(row=10, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=1).grid(row=10, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=2).grid(row=10, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=6,sticky = tk.E+tk.W)
#Biotest Flameout Fish oil
ttk.Label(supp_frame, text='Fish Oil').grid(row=11, column=0, sticky = 'E')
fishoil = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=fishoil, bg='tan', pady=5, value=0).grid(row=11, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=fishoil, bg='tan', pady=5, value=1).grid(row=11, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=2).grid(row=11, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=3).grid(row=11, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=4).grid(row=11, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=5).grid(row=11, column=6, sticky = tk.E+tk.W)
#Bayer Aspirin
ttk.Label(supp_frame, text='Aspirin').grid(row=12, column=0, sticky = 'E')
aspirin = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=aspirin, value=0).grid(row=12, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=aspirin, value=1).grid(row=12, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=aspirin, value=2).grid(row=12, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=6,sticky = tk.E+tk.W)
#Scott's Finest Purecee
ttk.Label(supp_frame, text='Creatine ethyl').grid(row=13, column=0, sticky = 'E')
creatine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=creatine, bg='tan', pady=5, value=0).grid(row=13, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=creatine, bg='tan', pady=5, value=1).grid(row=13, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=creatine, bg='tan', pady=5, value=2).grid(row=13, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=creatine, bg='tan', pady=5, value=3).grid(row=13, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=creatine, bg='tan', pady=5, value=4).grid(row=13, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=creatine, bg='tan', pady=5, value=5).grid(row=13, column=6, sticky = tk.E+tk.W)
#Source Naturals Niacin
ttk.Label(supp_frame, text='Niacin').grid(row=14, column=0, sticky = 'E')
niacin = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=niacin, bg='tan', pady=5, value=0).grid(row=14, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=niacin, bg='tan', pady=5, value=1).grid(row=14, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=niacin, bg='tan', pady=5, value=2).grid(row=14, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=niacin, bg='tan', pady=5, value=3).grid(row=14, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=niacin, bg='tan', pady=5, value=4).grid(row=14, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=niacin, bg='tan', pady=5, value=5).grid(row=14, column=6, sticky = tk.E+tk.W)
#Jarrow MSM
ttk.Label(supp_frame, text='MSM').grid(row=15, column=0, sticky = 'E')
msm = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=msm, bg='tan', pady=5, value=0).grid(row=15, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=1).grid(row=15, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/2 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=2).grid(row=15, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=3).grid(row=15, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=4).grid(row=15, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/5 TBS', padx=5, variable=msm, bg='tan', pady=5, value=6).grid(row=15, column=6, sticky = tk.E+tk.W)

ttk.Label(supp_frame, text='Taurine').grid(row=16, column=0, sticky = 'E')
taurine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=taurine, value=0).grid(row=16, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=taurine, value=500).grid(row=16, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=taurine, value=1000).grid(row=16, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=16, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=16, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=16, column=6,sticky = tk.E+tk.W)


win.mainloop()