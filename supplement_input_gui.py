#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  5 07:40:09 2018

@author: davidhagan
"""
#import encodings.idna
import tkinter as tk
import tkinter.ttk as ttk
import boto3
import decimal
import time



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
tabControl.add(tab1, text='Supplements1')	#add the tab

tab2 = ttk.Frame(tabControl)		#create 2nd tab control
tabControl.add(tab2, text='Supplements2')	#add the tab

tab3 = ttk.Frame(tabControl)		#create 2nd tab control
tabControl.add(tab3, text='Supplements3')	#add the tab

tab4 = ttk.Frame(tabControl)		#create 2nd tab control
tabControl.add(tab4, text='Measurements')	#add the tab

tabControl.pack(expand=1, fill='both')	#make visible

#----------------------------------------------------
#we are creating a container to hold all the widgets
supp_frame = ttk.LabelFrame(tab1, text='Supplement1 Input')
supp2_frame = ttk.LabelFrame(tab2, text='Supplement2 Input')
supp3_frame = ttk.LabelFrame(tab3, text='Supplement3 Input')
meas_frame = ttk.LabelFrame(tab4, text='Measurements Input')

# using the tkinter grid layout method
supp_frame.grid(column=1, row=0, padx=8, pady=4)
supp2_frame.grid(column=1, row=0, padx=8, pady=4)
supp3_frame.grid(column=1, row=0, padx=8, pady=4)
meas_frame.grid(column=1, row=0, padx=8, pady=4)

# functions
###############

#################
# measurements
#################

# measurement submit function

measurement_capture = {}

def submit_meas_data_current():
    measurement_capture['readiness'] = decimal.Decimal(readiness_input.get())
    measurement_capture['overall'] = decimal.Decimal(overall_input.get())
    measurement_capture['waist'] = decimal.Decimal(waist_input.get())
    measurement_capture['fasting-duration'] = decimal.Decimal(fast_duration_input.get())
    measurement_capture['systolic'] = decimal.Decimal(rtcalf_input.get())
    measurement_capture['diastolic'] = decimal.Decimal(ltleg_input.get())
    measurement_capture['right-leg'] = decimal.Decimal(rtleg_input.get())
    measurement_capture['right-grip'] = decimal.Decimal(rtgrip_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    measurement_capture['blood-glucose'] = decimal.Decimal(blood_glucose_input.get())
    measurement_capture['depression'] = decimal.Decimal(dep_input.get())
    measurement_capture['anxiety'] = decimal.Decimal(anx_input.get())
    measurement_capture['obsessing'] = decimal.Decimal(obs_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    measurement_capture['libido'] = decimal.Decimal(lib_input.get())
    for key in list(measurement_capture.keys()):  ## creates a list of all keys
        if measurement_capture[key] == 0.0:
            del measurement_capture[key]

    realm = 'measurements'
    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
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
    #print result
    result = "PutItem succeeded"
    tm1.insert(tk.END, result)
    tm1.after(10000, lambda: tm1.delete(1.0, tk.END))

def submit_meas_data_historical():
    measurement_capture['readiness'] = decimal.Decimal(readiness_input.get())
    measurement_capture['overall'] = decimal.Decimal(overall_input.get())
    measurement_capture['waist'] = decimal.Decimal(waist_input.get())
    measurement_capture['fasting-duration'] = decimal.Decimal(fast_duration_input.get())
    measurement_capture['systolic'] = decimal.Decimal(rtcalf_input.get())
    measurement_capture['diastolic'] = decimal.Decimal(ltleg_input.get())
    measurement_capture['right-leg'] = decimal.Decimal(rtleg_input.get())
    measurement_capture['right-grip'] = decimal.Decimal(rtgrip_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    measurement_capture['blood-glucose'] = decimal.Decimal(blood_glucose_input.get())
    measurement_capture['depression'] = decimal.Decimal(dep_input.get())
    measurement_capture['anxiety'] = decimal.Decimal(anx_input.get())
    measurement_capture['obsessing'] = decimal.Decimal(obs_input.get())
    measurement_capture['left-grip'] = decimal.Decimal(ltgrip_input.get())
    measurement_capture['libido'] = decimal.Decimal(lib_input.get())
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
    #print result
    result = "PutItem succeeded"
    tm1.insert(tk.END, result)
    tm1.after(10000, lambda: tm1.delete(1.0, tk.END))
    
# end of measurment submit to dynamodb function
################################################
    
# tkinter interface and data capture to provide data for measurment function
#############################################################################

#add the submit and cancel buttons
tk.Button(meas_frame, text='Submit Current', command=submit_meas_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(meas_frame, text='Submit Historical', command=submit_meas_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_meas_input = tk.StringVar(value='2018-05-07 08:00:00')
tk.Entry(meas_frame, text='what', textvariable=hist_meas_input).grid(row=1, column=2, columnspan=2)
tm1=tk.Text(meas_frame, height=1, width=20)
tm1.grid(row=1, column=4,columnspan=2, padx=(1,2),pady=(1,2))
tk.Button(meas_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)


#inputs
#vars for row number, to more easily rearrange
readiness_row_var = 11 #overall readiness to train
overall_row_var =  12 #overall motiviation for life, learning, general health
anx_row_var = 13 #anxiety
lib_row_var = 14 #libido
obs_row_var = 15 #obsessing
dep_row_var = 16 #depression
rtgrip_row_var = 17
ltgrip_row_var = 18
blood_glucose_row_var = 19
waist_row_var = 21
fast_dur_row_var = 20
rt_calf_row_var = 22
lft_leg_row_var =  23
rt_leg_row_var = 24



ttk.Label(meas_frame, text='Right Grip').grid(row=rtgrip_row_var, column=0, sticky = 'E')
rtgrip_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtgrip_input).grid(row=rtgrip_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Left Grip').grid(row=ltgrip_row_var, column=0, sticky = 'E')
ltgrip_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=ltgrip_input).grid(row=ltgrip_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Blood Glucose').grid(row=blood_glucose_row_var, column=0, sticky = 'E')
blood_glucose_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=blood_glucose_input).grid(row=blood_glucose_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Obsessing').grid(row=obs_row_var, column=0, sticky = 'E')
obs_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=obs_input).grid(row=obs_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='1-none : 3-little : 5-excessive').grid(row=obs_row_var, column=2, columnspan=3, sticky = 'W')

ttk.Label(meas_frame, text='Depression').grid(row=dep_row_var, column=0, sticky = 'E')
dep_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=dep_input).grid(row=dep_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='1 good to 5 bad').grid(row=dep_row_var, column=2, columnspan=3, sticky = 'W')

ttk.Label(meas_frame, text='Anxiety').grid(row=anx_row_var, column=0, sticky = 'E')
anx_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=anx_input).grid(row=anx_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='1 good to 5 bad').grid(row=anx_row_var, column=2, columnspan=3, sticky = 'W')

ttk.Label(meas_frame, text='Libido').grid(row=lib_row_var, column=0, sticky = 'E')
lib_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=lib_input).grid(row=lib_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='1 good to 5 bad').grid(row=lib_row_var, column=2, columnspan=3, sticky = 'W')

ttk.Label(meas_frame, text='Subjective Readiness').grid(row=readiness_row_var, column=0, sticky = 'E')
readiness_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=readiness_input).grid(row=readiness_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='1-kickass! 3-ok 5-exhausted, readiness to train/overall fatigue or lack of').grid(row=readiness_row_var, column=2, columnspan=3, sticky = 'W')

ttk.Label(meas_frame, text='Subjective Overall Wellness').grid(row=overall_row_var, column=0, sticky = 'E')
overall_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=overall_input).grid(row=overall_row_var, column=1,sticky = tk.E+tk.W)
ttk.Label(meas_frame, text='Overall feeling, motivation, general malaise or excellence').grid(row=overall_row_var, column=2, columnspan=3, sticky = 'W')

# currently taken with nokia scale
#ttk.Label(meas_frame, text='Hydration %').grid(row=36, column=0, sticky = 'E')
#hydration_input = tk.StringVar(value='0.0')
#tk.Entry(meas_frame, textvariable=hydration_input).grid(row=36, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Waist in Inches').grid(row=waist_row_var, column=0, sticky = 'E')
waist_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=waist_input).grid(row=waist_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='time in mins since last food').grid(row=fast_dur_row_var, column=0, sticky = 'E')
fast_duration_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=fast_duration_input).grid(row=fast_dur_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Systolic').grid(row=rt_calf_row_var, column=0, sticky = 'E')
rtcalf_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtcalf_input).grid(row=rt_calf_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Diastolic').grid(row=lft_leg_row_var, column=0, sticky = 'E')
ltleg_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=ltleg_input).grid(row=lft_leg_row_var, column=1,sticky = tk.E+tk.W)

ttk.Label(meas_frame, text='Right Leg in Inches').grid(row=rt_leg_row_var, column=0, sticky = 'E')
rtleg_input = tk.StringVar(value='0.0')
tk.Entry(meas_frame, textvariable=rtleg_input).grid(row=rt_leg_row_var, column=1,sticky = tk.E+tk.W)



#################
# supplements1 - creating 3 frames in lieu of scrolling
#########################################################

# supplement1 submit function, it generally will contain things taken in the morning only
#
data = {}
def submit_data_current():
    data['vitaminD'] = decimal.Decimal(vitaminD.get()*400)
    data['vitaminC'] = decimal.Decimal(vitaminC.get()*500)
    data['boron'] = decimal.Decimal(boron.get()*2)
    data['garlic'] = decimal.Decimal(garlic.get()*500)
    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get()*500)
    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
    data['tyrosine'] = decimal.Decimal(tyrosine.get()*500)
    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
    data['alpha-lipoic-acid'] = decimal.Decimal(ala.get()*300)
    data['k2'] = decimal.Decimal(k2.get()*5)
    data['msm'] = decimal.Decimal(msm.get()*100)
    data['methyl-b12'] = decimal.Decimal(b12Folate.get()*1000) #jarrows methylb12,methylFolate
    data['methyl-folate'] = decimal.Decimal(b12Folate.get()*400) #jarrows methylb12,methylFolate
    data['vitaminB6'] = decimal.Decimal(b12Folate.get()*1.5) #jarrows methylb12,methylFolate
    data['ceylon-cinnamon'] = decimal.Decimal(cinnamon.get()*500)
    data['mag_malate'] = decimal.Decimal(mag_malate.get()*400)
    data['teacrine'] = decimal.Decimal(teacrine.get()*50)
    data['betaine-tmg'] = decimal.Decimal(betaine_tmg.get()*606)
    for key in list(data.keys()):  ## creates a list of all keys
        if data[key] == 0:
            del data[key]

    realm = 'supplements'
    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    required_hash_data = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data = data.copy()
    final_input_data.update(required_hash_data)
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)
    #print result
    result = "PutItem succeeded"
    t1.insert(tk.END, result)
    t1.after(10000, lambda: t1.delete(1.0, tk.END))


def submit_data_historical():
    data['vitaminD'] = decimal.Decimal(vitaminD.get()*400)
    data['vitaminC'] = decimal.Decimal(vitaminC.get()*500)
    data['boron'] = decimal.Decimal(boron.get()*2)
    data['garlic'] = decimal.Decimal(garlic.get()*500)
    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get()*500)
    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
    data['tyrosine'] = decimal.Decimal(tyrosine.get()*500)
    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
    data['alpha-lipoic-acid'] = decimal.Decimal(ala.get()*300)
    data['k2'] = decimal.Decimal(k2.get()*5)
    data['msm'] = decimal.Decimal(msm.get()*100)
    data['methyl-b12'] = decimal.Decimal(b12Folate.get()*1000) #jarrows methylb12,methylFolate
    data['methyl-folate'] = decimal.Decimal(b12Folate.get()*400) #jarrows methylb12,methylFolate
    data['vitaminB6'] = decimal.Decimal(b12Folate.get()*1.5) #jarrows methylb12,methylFolate
    data['ceylon-cinnamon'] = decimal.Decimal(cinnamon.get()*500)
    data['mag_malate'] = decimal.Decimal(mag_malate.get()*400)
    data['teacrine'] = decimal.Decimal(teacrine.get()*50)
    data['betaine-tmg'] = decimal.Decimal(betaine_tmg.get()*606)
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
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data)
    #print result
    result = "PutItem succeeded"
    t1.insert(tk.END, result)
    t1.after(10000, lambda: t1.delete(1.0, tk.END))
# entry width wag
ENTRY_WIDTH = 20

# adding Label and Text Entry widgets
# row vars
vitd_row = 3
vitk2_row = 5
boron_row = 7
garlic_row = 33
vitb5_row = 9
fish_row = 11
tyrosine_row = 13
msm_row = 15
carn_row = 17
ala_row = 35
vitc_row = 21
mag_mal_row = 23
vitb6_row = 25
folate_row = 27
betain_tmg_row = 28
b12Folate_row = 29
cin_row = 31
teacrine_row = 33


#----------------------------------------
#add the submit and cancel buttons
tk.Button(supp_frame, text='Submit Current', command=submit_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(supp_frame, text='Submit Historical', command=submit_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_input = tk.StringVar(value='2019-01-07 08:00:00')
tk.Entry(supp_frame, text='what', textvariable=hist_input).grid(row=1, column=2, columnspan=2)
t1=tk.Text(supp_frame, height=1, width=20)
t1.grid(row=1, column=4,columnspan=2, padx=(1,2),pady=(1,2))
tk.Button(supp_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)

#vitaminD
ttk.Label(supp_frame, text='VitaminD 1000mg').grid(row=vitd_row, column=0, sticky = 'E')
vitaminD = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=vitaminD, bg='tan', pady=5, value=0).grid(row=vitd_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1k', variable=vitaminD, padx=5,  bg='tan', pady=5, value=1).grid(row=vitd_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2k', padx=5, variable=vitaminD, bg='tan', pady=5, value=2).grid(row=vitd_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3k', padx=5, variable=vitaminD, bg='tan', pady=5, value=3).grid(row=vitd_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4k', padx=5, variable=vitaminD, bg='tan', pady=5, value=4).grid(row=vitd_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5k', padx=5, variable=vitaminD, bg='tan', pady=5, value=5).grid(row=vitd_row, column=6, sticky = tk.E+tk.W)

# vitamin k2
ttk.Label(supp_frame, text='VitaminK2 5mg').grid(row=vitk2_row, column=0, sticky = 'E')
k2 = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=k2, bg='tan', pady=5, value=0).grid(row=vitk2_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5mg', padx=5, variable=k2, bg='tan', pady=5, value=1).grid(row=vitk2_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='10mg', padx=5, variable=k2, bg='tan', pady=5, value=2).grid(row=vitk2_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='15mg', padx=5, variable=k2, bg='tan', pady=5, value=3).grid(row=vitk2_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='20mg', padx=5, variable=k2, bg='tan', pady=5, value=4).grid(row=vitk2_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='25mg', padx=5, variable=k2, bg='tan', pady=5, value=5).grid(row=vitk2_row, column=6, sticky = tk.E+tk.W)
# 2mg boron
ttk.Label(supp_frame, text='2mg Boron').grid(row=boron_row, column=0, sticky = 'E')
boron = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=boron, value=0).grid(row=boron_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=boron, value=1).grid(row=boron_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=boron, value=2).grid(row=boron_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=boron_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=boron_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=boron_row, column=6,sticky = tk.E+tk.W)

#garlic BR Nutrition
ttk.Label(supp_frame, text='Garlic').grid(row=garlic_row, column=0, sticky = 'E')
garlic = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=garlic, bg='tan', pady=5, value=0).grid(row=garlic_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=garlic, bg='tan', pady=5, value=1).grid(row=garlic_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=garlic, bg='tan', pady=5, value=2).grid(row=garlic_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=garlic, bg='tan', pady=5, value=3).grid(row=garlic_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=garlic, bg='tan', pady=5, value=4).grid(row=garlic_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=garlic_row, column=garlic_row, sticky = tk.E+tk.W)
#Jarrow Pantothenic Acid B5
ttk.Label(supp_frame, text='Pantothenic Acid B5').grid(row=vitb5_row, column=0, sticky = 'E')
pant_acid = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=pant_acid, value=0).grid(row=vitb5_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=pant_acid, value=1).grid(row=vitb5_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=pant_acid, value=2).grid(row=vitb5_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=vitb5_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=vitb5_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=vitb5_row, column=6,sticky = tk.E+tk.W)

#Biotest Flameout Fish oil
ttk.Label(supp_frame, text='Fish Oil').grid(row=fish_row, column=0, sticky = 'E')
fishoil = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=fishoil, bg='tan', pady=5, value=0).grid(row=fish_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=fishoil, bg='tan', pady=5, value=1).grid(row=fish_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=2).grid(row=fish_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=3).grid(row=fish_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=4).grid(row=fish_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=5).grid(row=fish_row, column=6, sticky = tk.E+tk.W)

#BR Nutrition L-Tyrosine
ttk.Label(supp_frame, text='L-Tyrosine').grid(row=tyrosine_row, column=0, sticky = 'E')
tyrosine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=tyrosine, value=0).grid(row=tyrosine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.5 pill', padx=5, pady=5, bg='tan', variable=tyrosine, value=250).grid(row=tyrosine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pills', padx=5, pady=5, bg='tan', variable=tyrosine, value=500).grid(row=tyrosine_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=tyrosine_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=tyrosine_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=tyrosine_row, column=6,sticky = tk.E+tk.W)
#Jarrow MSM
ttk.Label(supp_frame, text='MSM').grid(row=msm_row, column=0, sticky = 'E')
msm = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=msm, bg='tan', pady=5, value=0).grid(row=msm_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=1).grid(row=msm_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/2 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=2).grid(row=msm_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=3).grid(row=msm_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=4).grid(row=msm_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1/5 TBS', padx=5, variable=msm, bg='tan', pady=5, value=6).grid(row=msm_row, column=6, sticky = tk.E+tk.W)

##Jarrow L-Carnitine Tartrate
ttk.Label(supp_frame, text='Carnitine Tartrate').grid(row=carn_row, column=0, sticky = 'E')
carnitine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=carnitine, bg='tan', pady=5, value=0).grid(row=carn_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=carnitine, bg='tan', pady=5, value=1).grid(row=carn_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=2).grid(row=carn_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=3).grid(row=carn_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=4).grid(row=carn_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=5).grid(row=carn_row, column=6, sticky = tk.E+tk.W)

##Ester-C
ttk.Label(supp_frame, text='vitaminC').grid(row=vitc_row, column=0, sticky = 'E')
vitaminC = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=vitaminC, bg='tan', pady=5, value=0).grid(row=vitc_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=vitaminC, bg='tan', pady=5, value=1).grid(row=vitc_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=vitaminC, bg='tan', pady=5, value=2).grid(row=vitc_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=vitaminC, bg='tan', pady=5, value=3).grid(row=vitc_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=vitaminC, bg='tan', pady=5, value=4).grid(row=vitc_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=vitaminC, bg='tan', pady=5, value=5).grid(row=vitc_row, column=6, sticky = tk.E+tk.W)
## kal magnesium malate
ttk.Label(supp_frame, text='Mag Malate').grid(row=mag_mal_row, column=0, sticky = 'E')
mag_malate = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=mag_malate, bg='tan', pady=5, value=0).grid(row=mag_mal_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=mag_malate, bg='tan', pady=5, value=1).grid(row=mag_mal_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=mag_malate, bg='tan', pady=5, value=2).grid(row=mag_mal_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=mag_malate, bg='tan', pady=5, value=3).grid(row=mag_mal_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=mag_malate, bg='tan', pady=5, value=4).grid(row=mag_mal_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=mag_malate, bg='tan', pady=5, value=5).grid(row=mag_mal_row, column=6, sticky = tk.E+tk.W)
##Jarrow methyl b12/Methyl Folate
ttk.Label(supp_frame, text='Jarrow B12/Folate B12').grid(row=b12Folate_row, column=0, sticky = 'E')
b12Folate = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=b12Folate, bg='tan', pady=5, value=0).grid(row=b12Folate_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.25 pill', padx=5, variable=b12Folate, bg='tan', pady=5, value=.25).grid(row=b12Folate_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.5 pills', padx=5, variable=b12Folate, bg='tan', pady=5, value=.5).grid(row=b12Folate_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.75 pills', padx=5, variable=b12Folate, bg='tan', pady=5, value=.75).grid(row=b12Folate_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pills', padx=5, variable=b12Folate, bg='tan', pady=5, value=1).grid(row=b12Folate_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1.5 pills', padx=5, variable=b12Folate, bg='tan', pady=5, value=1.5).grid(row=b12Folate_row, column=6, sticky = tk.E+tk.W)
### Jarrow methyl folate
ttk.Label(supp_frame, text='Jarrow B12/Folate Folate').grid(row=folate_row, column=0, sticky = 'E')
folate = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=folate, bg='tan', pady=5, value=0).grid(row=folate_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.25 pill', padx=5, variable=folate, bg='tan', pady=5, value=.25).grid(row=folate_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.5 pills', padx=5, variable=folate, bg='tan', pady=5, value=.5).grid(row=folate_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.75 pills', padx=5, variable=folate, bg='tan', pady=5, value=.75).grid(row=folate_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pills', padx=5, variable=folate, bg='tan', pady=5, value=1).grid(row=folate_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1.5 pills', padx=5, variable=folate, bg='tan', pady=5, value=1.5).grid(row=folate_row, column=6, sticky = tk.E+tk.W)
## 
ttk.Label(supp_frame, text='Jarrow B12/Folate B6').grid(row=vitb6_row, column=0, sticky = 'E')
b6 = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=b6, bg='tan', pady=5, value=0).grid(row=vitb6_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.25 pill', padx=5, variable=b6, bg='tan', pady=5, value=.25).grid(row=vitb6_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.5 pills', padx=5, variable=b6, bg='tan', pady=5, value=.5).grid(row=vitb6_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.75 pills', padx=5, variable=b6, bg='tan', pady=5, value=.75).grid(row=vitb6_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pills', padx=5, variable=b6, bg='tan', pady=5, value=1).grid(row=vitb6_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1.5 pills', padx=5, variable=b6, bg='tan', pady=5, value=1.5).grid(row=vitb6_row, column=6, sticky = tk.E+tk.W)
#Jarrow Alpha Lipoic Sustain
ttk.Label(supp_frame, text='Alpha Lipoic').grid(row=ala_row, column=0, sticky = 'E')
ala = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=ala, bg='tan', pady=5, value=0).grid(row=ala_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=ala, bg='tan', pady=5, value=1).grid(row=ala_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=ala, bg='tan', pady=5, value=2).grid(row=ala_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=ala, bg='tan', pady=5, value=3).grid(row=ala_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=ala, bg='tan', pady=5, value=4).grid(row=ala_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=ala, bg='tan', pady=5, value=5).grid(row=ala_row, column=6, sticky = tk.E+tk.W)
#ceylon cinnamon
ttk.Label(supp_frame, text='Ceylon Cinnamon').grid(row=cin_row, column=0, sticky = 'E')
cinnamon = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=cinnamon, bg='tan', pady=5, value=0).grid(row=cin_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=cinnamon, bg='tan', pady=5, value=1).grid(row=cin_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=cinnamon, bg='tan', pady=5, value=2).grid(row=cin_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=cinnamon, bg='tan', pady=5, value=3).grid(row=cin_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=cinnamon, bg='tan', pady=5, value=4).grid(row=cin_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=cinnamon, bg='tan', pady=5, value=5).grid(row=cin_row, column=6, sticky = tk.E+tk.W)

#primaforce teacrine
ttk.Label(supp_frame, text='Teacrine').grid(row=teacrine_row, column=0, sticky = 'E')
teacrine = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=teacrine, bg='tan', pady=5, value=0).grid(row=teacrine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=teacrine, bg='tan', pady=5, value=1).grid(row=teacrine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=teacrine, bg='tan', pady=5, value=2).grid(row=teacrine_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=teacrine, bg='tan', pady=5, value=3).grid(row=teacrine_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=teacrine, bg='tan', pady=5, value=4).grid(row=teacrine_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=teacrine, bg='tan', pady=5, value=5).grid(row=teacrine_row, column=6, sticky = tk.E+tk.W)

#betaine tmg
ttk.Label(supp_frame, text='Betain TMG').grid(row=betain_tmg_row, column=0, sticky = 'E')
betaine_tmg = tk.IntVar()
tk.Radiobutton(supp_frame, text='None', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=0).grid(row=betain_tmg_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.25 tsp', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=1).grid(row=betain_tmg_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.5  tsp', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=2).grid(row=betain_tmg_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='.75 tsp', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=3).grid(row=betain_tmg_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1 tsp', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=4).grid(row=betain_tmg_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp_frame, text='1.25 tsp', padx=5, variable=betaine_tmg, bg='tan', pady=5, value=5).grid(row=betain_tmg_row, column=6, sticky = tk.E+tk.W)

#################
# supplements2 - creating 2 frames in lieu of scrolling
#########################################################



# supplement2 submit function, it generally will contain things taken in the evening
# or several times a day
data2 = {}
def submit_data2_current():
    data2['pqq'] = decimal.Decimal(qh_pqq.get()*10)
    data2['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
    data2['beta-alanine'] = decimal.Decimal(betaAlanine.get()*1800)
    data2['parsley'] = decimal.Decimal(parsley.get()*150)
    data2['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
    data2['creatine'] = decimal.Decimal(creatine.get()*5000)
    data2['rez-v'] = decimal.Decimal(rezV.get()*200)
    data2['tongkat-ali'] = decimal.Decimal(tongkatali.get()*40)
    data2['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
    data2['tribulus'] = decimal.Decimal(trib.get()*250)
    data2['forskolin'] = decimal.Decimal(forskolin.get()*20)
    data2['rhodiola-rosea'] = decimal.Decimal(rhodiola.get()*500)
    data2['nicotinamide-riboside'] = decimal.Decimal(basis.get()*125)
    data2['pterostilbene'] = decimal.Decimal(basis.get()*25)
    data2['d-asparticAcid'] = decimal.Decimal(daa.get()*3000)
    data2['grapeseed-ext'] = decimal.Decimal(gse.get()*3000)
    data2['ginkgo'] = decimal.Decimal(ginkgo.get()*135)
    data2['huperzineA'] = decimal.Decimal(huper.get()*200)
    data2['citrulline-malate'] = decimal.Decimal(citrulline.get()*2000)
    data2['mag-10'] = decimal.Decimal(mag10.get())
    data2['methyl-b12'] = decimal.Decimal(b12.get()*1000) #jarrows methylb12,methylFolate
    data2['agmatine'] = decimal.Decimal(agmatine.get()*500)
    for key in list(data2.keys()):  ## creates a list of all keys
        if data2[key] == 0:
            del data2[key]

    realm = 'supplements'
    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    required_hash_data2 = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data2 = data2.copy()
    final_input_data2.update(required_hash_data2)
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data2)
    #print result
    result = "PutItem succeeded"
    t2.insert(tk.END, result)
    t2.after(10000, lambda: t1.delete(1.0, tk.END))


def submit_data2_historical():
    data2['pqq'] = decimal.Decimal(qh_pqq.get()*10)
    data2['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
    data2['beta-alanine'] = decimal.Decimal(betaAlanine.get()*1800)
    data2['parsley'] = decimal.Decimal(parsley.get()*150)
    data2['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
    data2['creatine'] = decimal.Decimal(creatine.get()*5000)
    data2['rez-v'] = decimal.Decimal(rezV.get()*200)
    data2['tongkat-ali'] = decimal.Decimal(tongkatali.get()*40)
    data2['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
    data2['tribulus'] = decimal.Decimal(trib.get()*250)
    data2['forskolin'] = decimal.Decimal(forskolin.get()*20)
    data2['rhodiola-rosea'] = decimal.Decimal(rhodiola.get()*500)
    data2['nicotinamide-riboside'] = decimal.Decimal(basis.get()*125)
    data2['pterostilbene'] = decimal.Decimal(basis.get()*25)
    data2['d-asparticAcid'] = decimal.Decimal(daa.get()*3000)
    data2['grapeseed-ext'] = decimal.Decimal(gse.get()*3000)
    data2['ginkgo'] = decimal.Decimal(ginkgo.get()*135)
    data2['huperzineA'] = decimal.Decimal(huper.get()*200)
    data2['citrulline-malate'] = decimal.Decimal(citrulline.get()*2000)
    data2['mag-10'] = decimal.Decimal(mag10.get())
    data2['methyl-b12'] = decimal.Decimal(b12.get()*5000) #jarrows methylb12,methylFolate
    data2['agmatine'] = decimal.Decimal(agmatine.get()*500)
    for key in list(data2.keys()):  ## creates a list of all keys
        if data2[key] == 0:
            del data2[key]

    realm = 'supplements'
    timestamp = hist_input.get()
    required_hash_data2 = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data2 = data2.copy()
    final_input_data2.update(required_hash_data2)
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data2)
    #print result
    result = "PutItem succeeded"
    t2.insert(tk.END, result)
    t2.after(10000, lambda: t1.delete(1.0, tk.END))
# entry width wag
ENTRY_WIDTH = 20

# adding Label and Text Entry widgets
#----------------------------------------
qh_pqq_row = 3
creatine_row = 5
beta_alanine_row = 19
basis_row = 7
trib_row = 9
citrulline_row = 11
tongkatali_row = 13
parsley_row = 15
rhodiola_row = 21
acetylCarnitine_row = 25
daa_row = 31
gse_row = 17
ginkgo_row = 27
mag_row = 28
huper_row =  29
r_ginseng_row = 23
forskolin_row = 33
rezV_row = 35
vitb12_row = 24
agmatine_row = 37


#add the submit and cancel buttons
tk.Button(supp2_frame, text='Submit Current', command=submit_data2_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(supp2_frame, text='Submit Historical', command=submit_data2_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_input = tk.StringVar(value='2018-05-07 08:00:00')
tk.Entry(supp2_frame, text='what', textvariable=hist_input).grid(row=1, column=2, columnspan=2)
t2=tk.Text(supp2_frame, height=1, width=20)
t2.grid(row=1, column=4,columnspan=2, padx=(1,2),pady=(1,2))
tk.Button(supp2_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)


#----------------------------------------------------
#beta alanine MUST FIX for ON brand powder
ttk.Label(supp2_frame, text='beta-alanine').grid(row=beta_alanine_row, column=0, sticky = 'E')
betaAlanine = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=betaAlanine, bg='tan', pady=5, value=0).grid(row=beta_alanine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1scoop', padx=5, variable=betaAlanine, bg='tan', pady=5, value=1).grid(row=beta_alanine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2scoops', padx=5, variable=betaAlanine, bg='tan', pady=5, value=2).grid(row=beta_alanine_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3scoops', padx=5, variable=betaAlanine, bg='tan', pady=5, value=3).grid(row=beta_alanine_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=beta_alanine_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=beta_alanine_row, column=6,sticky = tk.E+tk.W)

#rhodiola-rosea
ttk.Label(supp2_frame, text='Rhodiola-rosea').grid(row=rhodiola_row, column=0, sticky = 'E')
rhodiola = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=rhodiola, bg='tan', pady=5, value=0).grid(row=rhodiola_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, variable=rhodiola, bg='tan', pady=5, value=1).grid(row=rhodiola_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=2).grid(row=rhodiola_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=3).grid(row=rhodiola_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=4).grid(row=rhodiola_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='5 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=5).grid(row=rhodiola_row, column=6, sticky = tk.E+tk.W)

#Jarrow QH/PQQ
ttk.Label(supp2_frame, text='QH-absorb/PQQ').grid(row=qh_pqq_row, column=0, sticky = 'E')
qh_pqq = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=qh_pqq, value=0).grid(row=qh_pqq_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=qh_pqq, value=1).grid(row=qh_pqq_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=qh_pqq, value=2).grid(row=qh_pqq_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=qh_pqq_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=qh_pqq_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=qh_pqq_row, column=6,sticky = tk.E+tk.W)

#BR Nutrition Acetyl-L-Carnitine
ttk.Label(supp2_frame, text='Acetyl-l-Carnitine').grid(row=acetylCarnitine_row, column=0, sticky = 'E')
acetylCarnitine = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=0).grid(row=acetylCarnitine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=1).grid(row=acetylCarnitine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=2).grid(row=acetylCarnitine_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=acetylCarnitine_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=acetylCarnitine_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=acetylCarnitine_row, column=6,sticky = tk.E+tk.W)

#Biotest Micronized Creatine
ttk.Label(supp2_frame, text='Creatine').grid(row=creatine_row, column=0, sticky = 'E')
creatine = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=creatine, bg='tan', pady=5, value=0).grid(row=creatine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 scoops', padx=5, variable=creatine, bg='tan', pady=5, value=1).grid(row=creatine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 scoops', padx=5, variable=creatine, bg='tan', pady=5, value=2).grid(row=creatine_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=13, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=13, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=13, column=6,sticky = tk.E+tk.W)

#Biotest RezV
ttk.Label(supp2_frame, text='Resveratrol').grid(row=rezV_row, column=0, sticky = 'E')
rezV = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=rezV, bg='tan', pady=5, value=0).grid(row=rezV_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, variable=rezV, bg='tan', pady=5, value=1).grid(row=rezV_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, variable=rezV, bg='tan', pady=5, value=2).grid(row=rezV_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, variable=rezV, bg='tan', pady=5, value=3).grid(row=rezV_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=rezV_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=rezV_row, column=6,sticky = tk.E+tk.W)


ttk.Label(supp2_frame, text='tongkatali').grid(row=tongkatali_row, column=0, sticky = 'E')
tongkatali = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=tongkatali, value=0).grid(row=tongkatali_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='.5 pill', padx=5, pady=5, bg='tan', variable=tongkatali, value=.5).grid(row=tongkatali_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pills', padx=5, pady=5, bg='tan', variable=tongkatali, value=1).grid(row=tongkatali_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=tongkatali_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=tongkatali_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=tongkatali_row, column=6,sticky = tk.E+tk.W)

##prima force daa powder
ttk.Label(supp2_frame, text='DAA Powder').grid(row=daa_row, column=0, sticky = 'E')
daa = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=daa, bg='tan', pady=5, value=0).grid(row=daa_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1scoop', padx=5, variable=daa, bg='tan', pady=5, value=1).grid(row=daa_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2scoop', padx=5, variable=daa, bg='tan', pady=5, value=2).grid(row=daa_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3scoop', padx=5, variable=daa, bg='tan', pady=5, value=3).grid(row=daa_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4scoop', padx=5, variable=daa, bg='tan', pady=5, value=4).grid(row=daa_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='5scoop', padx=5, variable=daa, bg='tan', pady=5, value=5).grid(row=daa_row, column=6, sticky = tk.E+tk.W)

#Biotest Carbolin 19
ttk.Label(supp2_frame, text='Carbolin 19').grid(row=forskolin_row, column=0, sticky = 'E')
forskolin = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=forskolin, bg='tan', pady=5, value=0).grid(row=forskolin_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, variable=forskolin, bg='tan', pady=5, value=1).grid(row=forskolin_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=2).grid(row=forskolin_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=3).grid(row=forskolin_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=4).grid(row=forskolin_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='5 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=5).grid(row=forskolin_row, column=6, sticky = tk.E+tk.W)

# Elysium Basis
ttk.Label(supp2_frame, text='Basis').grid(row=basis_row, column=0, sticky = 'E')
basis = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=basis, bg='tan', pady=5, value=0).grid(row=basis_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, variable=basis, bg='tan', pady=5, value=1).grid(row=basis_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, variable=basis, bg='tan', pady=5, value=2).grid(row=basis_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, variable=basis, bg='tan', pady=5, value=3).grid(row=basis_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4 pills', padx=5, variable=basis, bg='tan', pady=5, value=4).grid(row=basis_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='5 pills', padx=5, variable=basis, bg='tan', pady=5, value=5).grid(row=basis_row, column=6, sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Red Ginseng').grid(row=r_ginseng_row, column=0, sticky = 'E')
r_ginseng = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=r_ginseng, value=0).grid(row=r_ginseng_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=r_ginseng, value=1).grid(row=r_ginseng_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=r_ginseng, value=2).grid(row=r_ginseng_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=r_ginseng_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=r_ginseng_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=r_ginseng_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Tribulus').grid(row=trib_row, column=0, sticky = 'E')
trib = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=trib, value=0).grid(row=trib_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=trib, value=1).grid(row=trib_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=trib, value=2).grid(row=trib_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, pady=5, bg='tan', variable=trib, value=3).grid(row=trib_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4 pills', padx=5, pady=5, bg='tan', variable=trib, value=4).grid(row=trib_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=trib_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Grape Seed Ext').grid(row=gse_row, column=0, sticky = 'E')
gse = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=gse, value=0).grid(row=gse_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=gse, value=1).grid(row=gse_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=gse, value=2).grid(row=gse_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=gse_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=gse_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=gse_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Ginkgo').grid(row=ginkgo_row, column=0, sticky = 'E')
ginkgo = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=ginkgo, value=0).grid(row=ginkgo_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=ginkgo, value=1).grid(row=ginkgo_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=ginkgo, value=2).grid(row=ginkgo_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3 pills', padx=5, pady=5, bg='tan', variable=ginkgo, value=3).grid(row=ginkgo_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4 pills', padx=5, pady=5, bg='tan', variable=ginkgo, value=4).grid(row=ginkgo_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=ginkgo_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Huperzine A').grid(row=huper_row, column=0, sticky = 'E')
huper = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=huper, value=0).grid(row=huper_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='.5 pill', padx=5, pady=5, bg='tan', variable=huper, value=.5).grid(row=huper_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pills', padx=5, pady=5, bg='tan', variable=huper, value=1).grid(row=huper_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1.5 pills', padx=5, pady=5, bg='tan', variable=huper, value=1.5).grid(row=huper_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=huper, value=2).grid(row=huper_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=huper_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Citrulline Malate').grid(row=citrulline_row, column=0, sticky = 'E')
citrulline = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=citrulline, value=0).grid(row=citrulline_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1scoop', padx=5, pady=5, bg='tan', variable=citrulline, value=1).grid(row=citrulline_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2scoops', padx=5, pady=5, bg='tan', variable=citrulline, value=2).grid(row=citrulline_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3scoops', padx=5, pady=5, bg='tan', variable=citrulline, value=3).grid(row=citrulline_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4scoops', padx=5, pady=5, bg='tan', variable=citrulline, value=4).grid(row=citrulline_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=citrulline_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Jarrow B12').grid(row=vitb12_row, column=0, sticky = 'E')
b12 = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=b12, bg='tan', pady=5, value=0).grid(row=vitb12_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='.5 pill', padx=5, variable=b12, bg='tan', pady=5, value=.5).grid(row=vitb12_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 pills', padx=5, variable=b12, bg='tan', pady=5, value=1).grid(row=vitb12_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1.5 pills', padx=5, variable=b12, bg='tan', pady=5, value=1.5).grid(row=vitb12_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2 pills', padx=5, variable=b12, bg='tan', pady=5, value=2).grid(row=vitb12_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2.5 pills', padx=5, variable=b12, bg='tan', pady=5, value=2.5).grid(row=vitb12_row, column=6, sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Parsley').grid(row=parsley_row, column=0, sticky = 'E')
parsley = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=parsley, value=0).grid(row=parsley_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1scoop', padx=5, pady=5, bg='tan', variable=parsley, value=1).grid(row=parsley_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2scoops', padx=5, pady=5, bg='tan', variable=parsley, value=2).grid(row=parsley_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3scoops', padx=5, pady=5, bg='tan', variable=parsley, value=3).grid(row=parsley_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4scoops', padx=5, pady=5, bg='tan', variable=parsley, value=4).grid(row=parsley_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=parsley_row, column=6,sticky = tk.E+tk.W)

ttk.Label(supp2_frame, text='Mag-10').grid(row=mag_row, column=0, sticky = 'E')
mag10 = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, pady=5, bg='tan', variable=mag10, value=0).grid(row=mag_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1scoop', padx=5, pady=5, bg='tan', variable=mag10, value=1).grid(row=mag_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='2scoops', padx=5, pady=5, bg='tan', variable=mag10, value=2).grid(row=mag_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3scoops', padx=5, pady=5, bg='tan', variable=mag10, value=3).grid(row=mag_row, column=4, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='4scoops', padx=5, pady=5, bg='tan', variable=mag10, value=4).grid(row=mag_row, column=5, sticky = tk.E+tk.W)
tk.Label(supp2_frame, background='tan', padx=5, pady=5).grid(row=mag_row, column=6,sticky = tk.E+tk.W)


#agmatine
ttk.Label(supp2_frame, text='Agmatine').grid(row=agmatine_row, column=0, sticky = 'E')
agmatine = tk.IntVar()
tk.Radiobutton(supp2_frame, text='None', padx=5, variable=agmatine, bg='tan', pady=5, value=0).grid(row=agmatine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1/8 tsp', padx=5, variable=agmatine, bg='tan', pady=5, value=1).grid(row=agmatine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1/4 tsp', padx=5, variable=agmatine, bg='tan', pady=5, value=2).grid(row=agmatine_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='3/8 tsp', padx=5, variable=agmatine, bg='tan', pady=5, value=3).grid(row=agmatine_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1/2 tsp', padx=5, variable=agmatine, bg='tan', pady=5, value=4).grid(row=agmatine_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp2_frame, text='1 tsp', padx=5, variable=agmatine, bg='tan', pady=5, value=8).grid(row=agmatine_row, column=6, sticky = tk.E+tk.W)


##################
## supplements3 - creating 3 frames in lieu of scrolling
##########################################################
data3 = {}
def submit_data3_current():
    data3['magnesium'] = decimal.Decimal(zma.get()*150)
    data3['vitaminB6'] = decimal.Decimal(zma.get()*3.5)
    data3['zinc'] = decimal.Decimal(zma.get()*10)
    data3['ashwagandha'] = decimal.Decimal(ash.get()*300)
    data3['phosphatidylserine'] = decimal.Decimal(pserine.get()*100)
    data3['potassium'] = decimal.Decimal(pot.get()*99)
    data3['passion-flower'] = decimal.Decimal(passflow.get()*619)
    data3['theanine'] = decimal.Decimal(thea.get()*100)
    data3['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
    data3['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
    data3['hmb'] = decimal.Decimal(hmb.get()*500)
    data3['eliteprominerals'] = decimal.Decimal(elite_min.get())
    data3['aspirin'] = decimal.Decimal(aspirin.get()*81)
    data3['bromelain'] = decimal.Decimal(brom.get()*500)
    data3['taurine'] = decimal.Decimal(taurine.get()*1.25)
    for key in list(data3.keys()):  ## creates a list of all keys
        if data3[key] == 0:
            del data3[key]

    realm = 'supplements'
    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    required_hash_data3 = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data3 = data3.copy()
    final_input_data3.update(required_hash_data3)
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data3)
    #print result
    result = "PutItem succeeded"
    t3.insert(tk.END, result)
    t3.after(10000, lambda: t1.delete(1.0, tk.END))


def submit_data3_historical():
    data3['magnesium'] = decimal.Decimal(zma.get()*150)
    data3['vitaminB6'] = decimal.Decimal(zma.get()*3.5)
    data3['zinc'] = decimal.Decimal(zma.get()*10)
    data3['ashwagandha'] = decimal.Decimal(ash.get())
    data3['phosphatidylserine'] = decimal.Decimal(pserine.get()*100)
    data3['potassium'] = decimal.Decimal(pot.get()*99)
    data3['passion-flower'] = decimal.Decimal(passflow.get()*619)
    data3['theanine'] = decimal.Decimal(thea.get()*100)
    data3['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
    data3['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
    data3['hmb'] = decimal.Decimal(hmb.get()*500)
    data3['eliteprominerals'] = decimal.Decimal(elite_min.get())
    data3['aspirin'] = decimal.Decimal(aspirin.get()*81)
    data3['bromelain'] = decimal.Decimal(brom.get()*500)
    data3['taurine'] = decimal.Decimal(taurine.get()*1.25)
    for key in list(data3.keys()):  ## creates a list of all keys
        if data3[key] == 0:
            del data3[key]

    realm = 'supplements'
    timestamp = hist_input.get()
    required_hash_data3 = {
        'realm': realm,
        'timestamp': timestamp
    }
    #combine dicts
    final_input_data3 = data3.copy()
    final_input_data3.update(required_hash_data3)
    #write to wellness table
    with table.batch_writer() as batch:
        batch.put_item(final_input_data3)
    #print result
    result = "PutItem succeeded"
    t3.insert(tk.END, result)
    t3.after(10000, lambda: t1.delete(1.0, tk.END))
# entry width wag
ENTRY_WIDTH = 20

# adding Label and Text Entry widgets
#----------------------------------------

zma_row = 3
pserine_row = 5
taurine_row = 7
ash_row = 9
pot_row = 11
passflow_row = 13
thea_row = 15
hmb_row = 17
green_tea_row = 19
elite_min_row = 21
asp_row = 23
brom_row = 22

#add the submit and cancel buttons
tk.Button(supp3_frame, text='Submit Current', command=submit_data3_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
tk.Button(supp3_frame, text='Submit Historical', command=submit_data3_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
hist_input = tk.StringVar(value='2018-05-07 08:00:00')
tk.Entry(supp3_frame, text='what', textvariable=hist_input).grid(row=1, column=2, columnspan=2)
t3=tk.Text(supp3_frame, height=1, width=20)
t3.grid(row=1, column=4,columnspan=2, padx=(1,2),pady=(1,2))
tk.Button(supp3_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)

#ZMA
ttk.Label(supp3_frame, text='ZMA').grid(row=zma_row, column=0, sticky = 'E')
zma = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=zma, bg='tan', pady=5, value=0).grid(row=zma_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', variable=zma, padx=5,  bg='tan', pady=5, value=3).grid(row=zma_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=zma, bg='tan', pady=5, value=4).grid(row=zma_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='5 pills', padx=5, variable=zma, bg='tan', pady=5, value=5).grid(row=zma_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='6 pills', padx=5, variable=zma, bg='tan', pady=5, value=6).grid(row=zma_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='7 pills', padx=5, variable=zma, bg='tan', pady=5, value=7).grid(row=zma_row, column=6, sticky = tk.E+tk.W)
#----------------------------------------------------
#Taurine Powder
ttk.Label(supp3_frame, text='Taurine powder').grid(row=taurine_row, column=0, sticky = 'E')
taurine = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=taurine, bg='tan', pady=5, value=0).grid(row=taurine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 scoops', padx=5, variable=taurine, bg='tan', pady=5, value=1).grid(row=taurine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 scoops', padx=5, variable=taurine, bg='tan', pady=5, value=2).grid(row=taurine_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 scoops', padx=5, variable=taurine, bg='tan', pady=5, value=3).grid(row=taurine_row, column=4, sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=taurine_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=taurine_row, column=6,sticky = tk.E+tk.W)

# Ashwagandha
ttk.Label(supp3_frame, text='Ashwagandha').grid(row=ash_row, column=0, sticky = 'E')
ash = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, pady=5, bg='tan', variable=ash, value=0).grid(row=ash_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=ash, value=1).grid(row=ash_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=ash, value=2).grid(row=ash_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=ash_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=ash_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=ash_row, column=6,sticky = tk.E+tk.W)

# Jarrow PS100 Phosphatidylserine
ttk.Label(supp3_frame, text='Phosphatidylserine').grid(row=pserine_row, column=0, sticky = 'E')
pserine = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, pady=5, bg='tan', variable=pserine, value=0).grid(row=pserine_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=pserine, value=1).grid(row=pserine_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=pserine, value=2).grid(row=pserine_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=pserine_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=pserine_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=pserine_row, column=6,sticky = tk.E+tk.W)

# Potassium
ttk.Label(supp3_frame, text='Potassium').grid(row=pot_row, column=0, sticky = 'E')
pot = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=pot, bg='tan', pady=5, value=0).grid(row=pot_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, variable=pot, bg='tan', pady=5, value=1).grid(row=pot_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=pot, bg='tan', pady=5, value=2).grid(row=pot_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=pot, bg='tan', pady=5, value=3).grid(row=pot_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=pot, bg='tan', pady=5, value=4).grid(row=pot_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='5 pills', padx=5, variable=pot, bg='tan', pady=5, value=5).grid(row=pot_row, column=6, sticky = tk.E+tk.W)

#Passion flower Herb Pharm
ttk.Label(supp3_frame, text='PassionFlower liq').grid(row=passflow_row, column=0, sticky = 'E')
passflow = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=passflow, bg='tan', pady=5, value=0).grid(row=passflow_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=passflow, bg='tan', pady=5, value=1800).grid(row=passflow_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=passflow, bg='tan', pady=5, value=2250).grid(row=passflow_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=passflow, bg='tan', pady=5, value=3000).grid(row=passflow_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=passflow_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=passflow_row, column=6,sticky = tk.E+tk.W)

# Theanine
ttk.Label(supp3_frame, text='Theanine').grid(row=thea_row, column=0, sticky = 'E')
thea = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=thea, bg='tan', pady=5, value=0).grid(row=thea_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, variable=thea, bg='tan', pady=5, value=1).grid(row=thea_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=thea, bg='tan', pady=5, value=2).grid(row=thea_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=thea, bg='tan', pady=5, value=3).grid(row=thea_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=thea, bg='tan', pady=5, value=4).grid(row=thea_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='5 pills', padx=5, variable=thea, bg='tan', pady=5, value=5).grid(row=thea_row, column=6, sticky = tk.E+tk.W)

#Bayer Aspirin
ttk.Label(supp3_frame, text='Aspirin').grid(row=asp_row, column=0, sticky = 'E')
aspirin = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, pady=5, bg='tan', variable=aspirin, value=0).grid(row=asp_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=aspirin, value=1).grid(row=asp_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=aspirin, value=2).grid(row=asp_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=asp_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=asp_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=asp_row, column=6,sticky = tk.E+tk.W)

#Bromelain
ttk.Label(supp3_frame, text='Bromelain').grid(row=brom_row, column=0, sticky = 'E')
brom = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, pady=5, bg='tan', variable=brom, value=0).grid(row=brom_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=brom, value=1).grid(row=brom_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=brom, value=2).grid(row=brom_row, column=3, sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=brom_row, column=4,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=brom_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=brom_row, column=6,sticky = tk.E+tk.W)

#vitamonk HMB
ttk.Label(supp3_frame, text='HMB').grid(row=hmb_row, column=0, sticky = 'E')
hmb = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=hmb, bg='tan', pady=5, value=0).grid(row=hmb_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, variable=hmb, bg='tan', pady=5, value=1).grid(row=hmb_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=hmb, bg='tan', pady=5, value=2).grid(row=hmb_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=hmb, bg='tan', pady=5, value=3).grid(row=hmb_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=hmb, bg='tan', pady=5, value=4).grid(row=hmb_row, column=5,sticky = tk.E+tk.W)
tk.Label(supp3_frame, background='tan', padx=5, pady=5).grid(row=hmb_row, column=6,sticky = tk.E+tk.W)
#
#Biotest ElitePro Mineral supp3ort
ttk.Label(supp3_frame, text='ElitePro Minerals').grid(row=elite_min_row, column=0, sticky = 'E')
elite_min = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=elite_min, bg='tan', pady=5, value=0).grid(row=elite_min_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, variable=elite_min, bg='tan', pady=5, value=1).grid(row=elite_min_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=2).grid(row=elite_min_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=3).grid(row=elite_min_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=4).grid(row=elite_min_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='5 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=5).grid(row=elite_min_row, column=6, sticky = tk.E+tk.W)

#Buddha's Herbs Green Tea decaffeinated
ttk.Label(supp3_frame, text='Green Tea Extract').grid(row=green_tea_row, column=0, sticky = 'E')
green_tea = tk.IntVar()
tk.Radiobutton(supp3_frame, text='None', padx=5, variable=green_tea, bg='tan', pady=5, value=0).grid(row=green_tea_row, column=1,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='1 pill', padx=5, variable=green_tea, bg='tan', pady=5, value=1).grid(row=green_tea_row, column=2,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='2 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=2).grid(row=green_tea_row, column=3, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='3 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=3).grid(row=green_tea_row, column=4,sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='4 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=4).grid(row=green_tea_row, column=5, sticky = tk.E+tk.W)
tk.Radiobutton(supp3_frame, text='5 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=5).grid(row=green_tea_row, column=6, sticky = tk.E+tk.W)


win.mainloop()
#
##################
## supplements2 - creating 2 frames in lieu of scrolling
##########################################################
#
#
#
## supplement2 submit function, it generally will contain things taken in the evening
## or several times a day
#
#data = {}
#def submit_data_current():
#    data['taurine'] = decimal.Decimal(taurine.get())
#    data['liver'] = decimal.Decimal(liver.get())
#    data['boron'] = decimal.Decimal(boron.get())
#    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
#    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
#    data['garlic'] = decimal.Decimal(garlic.get()*500)
#    data['parsley'] = decimal.Decimal(garlic.get()*150)
#    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
##    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
#    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
#    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
#    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
#    data['tyrosine'] = decimal.Decimal(tyrosine.get())
#    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
#    data['creatine'] = decimal.Decimal(creatine.get()*5000)
##    data['rez-v'] = decimal.Decimal(rezV.get()*200)
#    data['hmb'] = decimal.Decimal(hmb.get()*500)
#    data['tongkat-ali'] = decimal.Decimal(tongkatali.get()*40)
#    data['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
#    data['tribulus'] = decimal.Decimal(trib.get()*250)
#    data['eliteprominerals'] = decimal.Decimal(elite_min.get())
#    data['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
#    data['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
##    data['forskolin'] = decimal.Decimal(forskolin.get()*20)
#    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
#    data['alpha-lipoic-acid'] = decimal.Decimal(ala.get()*300)
##    data['rhodiola-rosea'] = decimal.Decimal(rhodiola.get()*500)
#    data['nicotinamide-riboside'] = decimal.Decimal(basis.get()*125)
#    data['pterostilbene'] = decimal.Decimal(basis.get()*25)
#    data['k2'] = decimal.Decimal(k2.get()*5)
#    for key in list(data.keys()):  ## creates a list of all keys
#        if data[key] == 0:
#            del data[key]
#
#    realm = 'supplements'
#    timestamp = str(time.strftime("%Y-%m-%d %H:%M:%S"))
#    required_hash_data = {
#        'realm': realm,
#        'timestamp': timestamp
#    }
#    #combine dicts
#    final_input_data = data.copy()
#    final_input_data.update(required_hash_data)
#    #write to wellness table
#    with table.batch_writer() as batch:
#        batch.put_item(final_input_data)
#    #print result
#    result = "PutItem succeeded"
#    t1.insert(tk.END, result)
#    t1.after(10000, lambda: t1.delete(1.0, tk.END))
#
#
#def submit_data_historical():
#    data['taurine'] = decimal.Decimal(taurine.get())
#    data['liver'] = decimal.Decimal(liver.get())
n#    data['boron'] = decimal.Decimal(boron.get())
#    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
#    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
#    data['garlic'] = decimal.Decimal(garlic.get()*500)
#    data['parsley'] = decimal.Decimal(garlic.get()*150)
#    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
##    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
#    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
#    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
#    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
#    data['tyrosine'] = decimal.Decimal(tyrosine.get())
#    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
#    data['creatine'] = decimal.Decimal(creatine.get()*5000)
##    data['niacin'] = decimal.Decimal(niacin.get()*100) #not in current
#    data['msm'] = decimal.Decimal(msm.get()*100)
##    data['rez-v'] = decimal.Decimal(rezV.get()*200)
#    data['hmb'] = decimal.Decimal(hmb.get()*500)
#    data['tongkat-ali'] = decimal.Decimal(tongkatali.get()*40)
#    data['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
#    data['tribulus'] = decimal.Decimal(trib.get()*250)
#    data['eliteprominerals'] = decimal.Decimal(elite_min.get())
#    data['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
#    data['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
##    data['forskolin'] = decimal.Decimal(forskolin.get()*20)
#    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
#    data['alpha-lipoic-acid'] = decimal.Decimal(ala.get()*300)
##    data['rhodiola-rosea'] = decimal.Decimal(rhodiola.get()*500)
#    data['nicotinamide-riboside'] = decimal.Decimal(basis.get()*125)
#    data['pterostilbene'] = decimal.Decimal(basis.get()*25)
#    data['k2'] = decimal.Decimal(k2.get()*5)
#    for key in list(data.keys()):  ## creates a list of all keys
#        if data[key] == 0:
#            del data[key]
#
#    realm = 'supplements'
#    timestamp = hist_input.get()
#    required_hash_data = {
#        'realm': realm,
#        'timestamp': timestamp
#    }
#    #combine dicts
#    final_input_data = data.copy()
#    final_input_data.update(required_hash_data)
#    #write to wellness table
#    with table.batch_writer() as batch:
#        batch.put_item(final_input_data)
#    #print result
#    result = "PutItem succeeded"
#    t1.insert(tk.END, result)
#    t1.after(10000, lambda: t1.delete(1.0, tk.END))
## entry width wag
#ENTRY_WIDTH = 20
#
## adding Label and Text Entry widgets
##----------------------------------------
##add the submit and cancel buttons
#tk.Button(supp_frame, text='Submit Current', command=submit_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
#tk.Button(supp_frame, text='Submit Historical', command=submit_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
#hist_input = tk.StringVar(value='2017-05-07 08:00:00')
#tk.Entry(supp_frame, text='what', textvariable=hist_input).grid(row=1, column=2, columnspan=2)
#t1=tk.Text(supp_frame, height=1, width=20)
#t1.grid(row=1, column=4,columnspan=2, padx=(1,2),pady=(1,2))
#tk.Button(supp_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)
#
##vitaminD
#ttk.Label(supp_frame, text='VitaminD (liquid)').grid(row=3, column=0, sticky = 'E')
#vitaminD = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=vitaminD, bg='tan', pady=5, value=0).grid(row=3, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 drop', variable=vitaminD, padx=5,  bg='tan', pady=5, value=400).grid(row=3, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=800).grid(row=3, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=1200).grid(row=3, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=1600).grid(row=3, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 drops', padx=5, variable=vitaminD, bg='tan', pady=5, value=2000).grid(row=3, column=6, sticky = tk.E+tk.W)
##----------------------------------------------------
##beta alanine MUST FIX for ON brand powder
#ttk.Label(supp_frame, text='beta-alanine').grid(row=4, column=0, sticky = 'E')
#betaAlanine = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=betaAlanine, bg='tan', pady=5, value=0).grid(row=4, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=1800).grid(row=4, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=2250).grid(row=4, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=betaAlanine, bg='tan', pady=5, value=3000).grid(row=4, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=4, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=4, column=6,sticky = tk.E+tk.W)
#
## vitamin k2
#ttk.Label(supp_frame, text='Vitamin K2').grid(row=5, column=0, sticky = 'E')
#k2 = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=k2, bg='tan', pady=5, value=0).grid(row=5, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=k2, bg='tan', pady=5, value=1).grid(row=5, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=k2, bg='tan', pady=5, value=2).grid(row=5, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=k2, bg='tan', pady=5, value=3).grid(row=5, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=k2, bg='tan', pady=5, value=4).grid(row=5, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=k2, bg='tan', pady=5, value=5).grid(row=5, column=6, sticky = tk.E+tk.W)
#
#
###rhodiola-rosea
##ttk.Label(supp_frame, text='Rhodiola-rosea').grid(row=5, column=0, sticky = 'E')
##rhodiola = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=rhodiola, bg='tan', pady=5, value=0).grid(row=5, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=rhodiola, bg='tan', pady=5, value=1).grid(row=5, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=2).grid(row=5, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=3).grid(row=5, column=4,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=4).grid(row=5, column=5, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=rhodiola, bg='tan', pady=5, value=5).grid(row=5, column=6, sticky = tk.E+tk.W)
###liver pills
##ttk.Label(supp_frame, text='Liver pills').grid(row=5, column=0, sticky = 'E')
##liver = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=liver, bg='tan', pady=5, value=0).grid(row=5, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=liver, bg='tan', pady=5, value=750).grid(row=5, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=liver, bg='tan', pady=5, value=1500).grid(row=5, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=liver, bg='tan', pady=5, value=2250).grid(row=5, column=4,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=liver, bg='tan', pady=5, value=3000).grid(row=5, column=5, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=liver, bg='tan', pady=5, value=3750).grid(row=5, column=6, sticky = tk.E+tk.W)
##curcumin
#ttk.Label(supp_frame, text='2mg Boron').grid(row=6, column=0, sticky = 'E')
#boron = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=boron, value=0).grid(row=6, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=boron, value=2).grid(row=6, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=boron, value=4).grid(row=6, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=6,sticky = tk.E+tk.W)
##Jarrow QH/PQQ
#ttk.Label(supp_frame, text='QH-absorb/PQQ').grid(row=7, column=0, sticky = 'E')
#qh_pqq = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=qh_pqq, value=0).grid(row=7, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=qh_pqq, value=1).grid(row=7, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=qh_pqq, value=2).grid(row=7, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=7, column=6,sticky = tk.E+tk.W)
##garlic BR Nutrition
#ttk.Label(supp_frame, text='Garlic').grid(row=8, column=0, sticky = 'E')
#garlic = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=garlic, bg='tan', pady=5, value=0).grid(row=8, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=garlic, bg='tan', pady=5, value=1).grid(row=8, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=garlic, bg='tan', pady=5, value=2).grid(row=8, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=garlic, bg='tan', pady=5, value=3).grid(row=8, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=garlic, bg='tan', pady=5, value=4).grid(row=8, column=5, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=8, column=6, sticky = tk.E+tk.W)
##Jarrow Pantothenic Acid B5
#ttk.Label(supp_frame, text='Pantothenic Acid B5').grid(row=9, column=0, sticky = 'E')
#pant_acid = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=pant_acid, value=0).grid(row=9, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=pant_acid, value=500).grid(row=9, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=pant_acid, value=1000).grid(row=9, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=9, column=6,sticky = tk.E+tk.W)
##BR Nutrition Acetyl-L-Carnitine
##ttk.Label(supp_frame, text='Acetyl-l-Carnitine').grid(row=10, column=0, sticky = 'E')
##acetylCarnitine = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=0).grid(row=10, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=1).grid(row=10, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=acetylCarnitine, value=2).grid(row=10, column=3, sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=4,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=5,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=10, column=6,sticky = tk.E+tk.W)
##Biotest Flameout Fish oil
#ttk.Label(supp_frame, text='Fish Oil').grid(row=11, column=0, sticky = 'E')
#fishoil = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=fishoil, bg='tan', pady=5, value=0).grid(row=11, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=fishoil, bg='tan', pady=5, value=1).grid(row=11, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=2).grid(row=11, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=3).grid(row=11, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=4).grid(row=11, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=fishoil, bg='tan', pady=5, value=5).grid(row=11, column=6, sticky = tk.E+tk.W)
##Bayer Aspirin
#ttk.Label(supp_frame, text='Aspirin').grid(row=12, column=0, sticky = 'E')
#aspirin = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=aspirin, value=0).grid(row=12, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=aspirin, value=1).grid(row=12, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=aspirin, value=2).grid(row=12, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=12, column=6,sticky = tk.E+tk.W)
##Biotest Micronized Creatine
#ttk.Label(supp_frame, text='Creatine').grid(row=13, column=0, sticky = 'E')
#creatine = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=creatine, bg='tan', pady=5, value=0).grid(row=13, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 scoops', padx=5, variable=creatine, bg='tan', pady=5, value=1).grid(row=13, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 scoops', padx=5, variable=creatine, bg='tan', pady=5, value=2).grid(row=13, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=13, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=13, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=13, column=6,sticky = tk.E+tk.W)
##BR Nutrition L-Tyrosine
#ttk.Label(supp_frame, text='L-Tyrosine').grid(row=14, column=0, sticky = 'E')
#tyrosine = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=tyrosine, value=0).grid(row=14, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=tyrosine, value=500).grid(row=14, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=tyrosine, value=1000).grid(row=14, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=14, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=14, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=14, column=6,sticky = tk.E+tk.W)
##Jarrow MSM
#ttk.Label(supp_frame, text='MSM').grid(row=15, column=0, sticky = 'E')
#msm = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=msm, bg='tan', pady=5, value=0).grid(row=15, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=1).grid(row=15, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1/2 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=2).grid(row=15, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3/4 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=3).grid(row=15, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 Tsp', padx=5, variable=msm, bg='tan', pady=5, value=4).grid(row=15, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1/5 TBS', padx=5, variable=msm, bg='tan', pady=5, value=6).grid(row=15, column=6, sticky = tk.E+tk.W)
#
###Biotest RezV
##ttk.Label(supp_frame, text='Resveratrol').grid(row=16, column=0, sticky = 'E')
##rezV = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=rezV, bg='tan', pady=5, value=0).grid(row=16, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=rezV, bg='tan', pady=5, value=1).grid(row=16, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=rezV, bg='tan', pady=5, value=2).grid(row=16, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=rezV, bg='tan', pady=5, value=3).grid(row=16, column=4,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=16, column=5,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=16, column=6,sticky = tk.E+tk.W)
#
##vitamonk HMB
#ttk.Label(supp_frame, text='HMB').grid(row=17, column=0, sticky = 'E')
#hmb = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=hmb, bg='tan', pady=5, value=0).grid(row=17, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=hmb, bg='tan', pady=5, value=1).grid(row=17, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=hmb, bg='tan', pady=5, value=2).grid(row=17, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=hmb, bg='tan', pady=5, value=3).grid(row=17, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=hmb, bg='tan', pady=5, value=4).grid(row=17, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=17, column=6,sticky = tk.E+tk.W)
#
###Source Naturals Niacin
##ttk.Label(supp_frame, text='Niacin').grid(row=18, column=0, sticky = 'E')
##niacin = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=niacin, bg='tan', pady=5, value=0).grid(row=18, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=niacin, bg='tan', pady=5, value=1).grid(row=18, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=niacin, bg='tan', pady=5, value=2).grid(row=18, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=niacin, bg='tan', pady=5, value=3).grid(row=18, column=4,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=niacin, bg='tan', pady=5, value=4).grid(row=18, column=5, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=niacin, bg='tan', pady=5, value=5).grid(row=18, column=6, sticky = tk.E+tk.W)
##
##ttk.Label(supp_frame, text='Taurine').grid(row=19, column=0, sticky = 'E')
##taurine = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=taurine, value=0).grid(row=19, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=taurine, value=500).grid(row=19, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=taurine, value=1000).grid(row=19, column=3, sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=19, column=4,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=19, column=5,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=19, column=6,sticky = tk.E+tk.W)
#
#ttk.Label(supp_frame, text='tongkatali').grid(row=20, column=0, sticky = 'E')
#tongkatali = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=tongkatali, value=0).grid(row=20, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='.5 pill', padx=5, pady=5, bg='tan', variable=tongkatali, value=1).grid(row=20, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pills', padx=5, pady=5, bg='tan', variable=tongkatali, value=2).grid(row=20, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=20, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=20, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=20, column=6,sticky = tk.E+tk.W)
#
##Biotest ElitePro Mineral Support
#ttk.Label(supp_frame, text='ElitePro Minerals').grid(row=25, column=0, sticky = 'E')
#elite_min = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=elite_min, bg='tan', pady=5, value=0).grid(row=25, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=elite_min, bg='tan', pady=5, value=1).grid(row=25, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=2).grid(row=25, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=3).grid(row=25, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=4).grid(row=25, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=elite_min, bg='tan', pady=5, value=5).grid(row=25, column=6, sticky = tk.E+tk.W)
#
##Jarrow Alpha Lipoic Sustain
#ttk.Label(supp_frame, text='Alpha Lipoic').grid(row=26, column=0, sticky = 'E')
#ala = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=ala, bg='tan', pady=5, value=0).grid(row=26, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=ala, bg='tan', pady=5, value=1).grid(row=26, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=ala, bg='tan', pady=5, value=2).grid(row=26, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=ala, bg='tan', pady=5, value=3).grid(row=26, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=ala, bg='tan', pady=5, value=4).grid(row=26, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=ala, bg='tan', pady=5, value=5).grid(row=26, column=6, sticky = tk.E+tk.W)
#
#
##Buddha's Herbs Green Tea decaffeinated
#ttk.Label(supp_frame, text='Green Tea Extract').grid(row=27, column=0, sticky = 'E')
#green_tea = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=green_tea, bg='tan', pady=5, value=0).grid(row=27, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=green_tea, bg='tan', pady=5, value=1).grid(row=27, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=2).grid(row=27, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=3).grid(row=27, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=4).grid(row=27, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=green_tea, bg='tan', pady=5, value=5).grid(row=27, column=6, sticky = tk.E+tk.W)
#
###Jarrow L-Carnitine Tartrate
#ttk.Label(supp_frame, text='Carnitine Tartrate').grid(row=28, column=0, sticky = 'E')
#carnitine = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=carnitine, bg='tan', pady=5, value=0).grid(row=28, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=carnitine, bg='tan', pady=5, value=1).grid(row=28, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=2).grid(row=28, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=3).grid(row=28, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=4).grid(row=28, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=carnitine, bg='tan', pady=5, value=5).grid(row=28, column=6, sticky = tk.E+tk.W)
#
###Biotest Carbolin 19
##ttk.Label(supp_frame, text='Carbolin 19').grid(row=29, column=0, sticky = 'E')
##forskolin = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=forskolin, bg='tan', pady=5, value=0).grid(row=29, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=forskolin, bg='tan', pady=5, value=1).grid(row=29, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=2).grid(row=29, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=3).grid(row=29, column=4,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=4).grid(row=29, column=5, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=forskolin, bg='tan', pady=5, value=5).grid(row=29, column=6, sticky = tk.E+tk.W)
#
## Elysium Basis
#ttk.Label(supp_frame, text='Basis').grid(row=29, column=0, sticky = 'E')
#basis = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, variable=basis, bg='tan', pady=5, value=0).grid(row=29, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=basis, bg='tan', pady=5, value=1).grid(row=29, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=basis, bg='tan', pady=5, value=2).grid(row=29, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=basis, bg='tan', pady=5, value=3).grid(row=29, column=4,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=basis, bg='tan', pady=5, value=4).grid(row=29, column=5, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=basis, bg='tan', pady=5, value=5).grid(row=29, column=6, sticky = tk.E+tk.W)
#
#
#ttk.Label(supp_frame, text='Red Ginseng').grid(row=30, column=0, sticky = 'E')
#r_ginseng = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=r_ginseng, value=0).grid(row=30, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=r_ginseng, value=1).grid(row=30, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=r_ginseng, value=2).grid(row=30, column=3, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=30, column=4,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=30, column=5,sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=30, column=6,sticky = tk.E+tk.W)
#
#ttk.Label(supp_frame, text='Tribulus').grid(row=31, column=0, sticky = 'E')
#trib = tk.IntVar()
#tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=trib, value=0).grid(row=31, column=1,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=trib, value=1).grid(row=31, column=2,sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=trib, value=2).grid(row=31, column=3, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='3 pills', padx=5, pady=5, bg='tan', variable=trib, value=3).grid(row=31, column=4, sticky = tk.E+tk.W)
#tk.Radiobutton(supp_frame, text='4 pills', padx=5, pady=5, bg='tan', variable=trib, value=4).grid(row=31, column=5, sticky = tk.E+tk.W)
#tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=31, column=6,sticky = tk.E+tk.W)
#
#
#win.mainloop()
#
#
###liver pills
##ttk.Label(supp_frame, text='Liver pills').grid(row=5, column=0, sticky = 'E')
##liver = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, variable=liver, bg='tan', pady=5, value=0).grid(row=5, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, variable=liver, bg='tan', pady=5, value=750).grid(row=5, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, variable=liver, bg='tan', pady=5, value=1500).grid(row=5, column=3, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='3 pills', padx=5, variable=liver, bg='tan', pady=5, value=2250).grid(row=5, column=4,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='4 pills', padx=5, variable=liver, bg='tan', pady=5, value=3000).grid(row=5, column=5, sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='5 pills', padx=5, variable=liver, bg='tan', pady=5, value=3750).grid(row=5, column=6, sticky = tk.E+tk.W)
##curcumin
##ttk.Label(supp_frame, text='2mg Boron').grid(row=6, column=0, sticky = 'E')
##boron = tk.IntVar()
##tk.Radiobutton(supp_frame, text='None', padx=5, pady=5, bg='tan', variable=boron, value=0).grid(row=6, column=1,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='1 pill', padx=5, pady=5, bg='tan', variable=boron, value=2).grid(row=6, column=2,sticky = tk.E+tk.W)
##tk.Radiobutton(supp_frame, text='2 pills', padx=5, pady=5, bg='tan', variable=boron, value=4).grid(row=6, column=3, sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=4,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=5,sticky = tk.E+tk.W)
##tk.Label(supp_frame, background='tan', padx=5, pady=5).grid(row=6, column=6,sticky = tk.E+tk.W)
#
##night_data = {}
#
##def submit_data_current():
##    data['taurine'] = decimal.Decimal(taurine.get())
##    data['vitaminD'] = decimal.Decimal(vitaminD.get())
##    data['beta-alanine'] = decimal.Decimal(betaAlanine.get())
##    data['liver'] = decimal.Decimal(liver.get())
##    data['curcumin'] = decimal.Decimal(curcumin.get())
##    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
##    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
##    data['garlic'] = decimal.Decimal(garlic.get()*500)
##    data['parsley'] = decimal.Decimal(garlic.get()*150)
##    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
##    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
##    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
##    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
##    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
##    data['tyrosine'] = decimal.Decimal(tyrosine.get())
##    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
##    data['creatine'] = decimal.Decimal(creatine.get()*5000)
###    data['rez-v'] = decimal.Decimal(rezV.get()*200)
##    data['hmb'] = decimal.Decimal(hmb.get()*500)
##    data['tongkat-ali'] = decimal.Decimal(tongkatali.get()*80)
###    data['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
##    data['tribulus'] = decimal.Decimal(trib.get()*250)
##    data['eliteprominerals'] = decimal.Decimal(elite_min.get())
##    data['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
##    data['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
##    data['forskolin'] = decimal.Decimal(forskolin.get()*20)
##    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
##    for key in list(data.keys()):  ## creates a list of all keys
##        if data[key] == 0:
##            del data[key]
##
##    realm = 'supplements'
##    timestamp = str(datetime.today()) #update to time
##    required_hash_data = {
##        'realm': realm,
##        'timestamp': timestamp
##    }
##    #combine dicts
##    final_input_data = data.copy()
##    final_input_data.update(required_hash_data)
##    #write to wellness table
##    with table.batch_writer() as batch:
##        batch.put_item(final_input_data)
##    #print result
##    result = "PutItem succeeded"
##    t1.insert(tk.END, result)
##    t1.after(10000, lambda: t1.delete(1.0, tk.END))
##
##
##def submit_data_historical():
##    data['taurine'] = decimal.Decimal(taurine.get())
##    data['vitaminD'] = decimal.Decimal(vitaminD.get())
##    data['beta-alanine'] = decimal.Decimal(betaAlanine.get())
##    data['liver'] = decimal.Decimal(liver.get())
##    data['curcumin'] = decimal.Decimal(curcumin.get())
##    data['pqq'] = decimal.Decimal(qh_pqq.get()*10)
##    data['ubiquinol'] = decimal.Decimal(qh_pqq.get()*100)
##    data['garlic'] = decimal.Decimal(garlic.get()*500)
##    data['parsley'] = decimal.Decimal(garlic.get()*150)
##    data['pantothenic-acid'] = decimal.Decimal(pant_acid.get())
##    data['acetyl-carnitine'] = decimal.Decimal(acetylCarnitine.get()*500)
##    data['fishoil(dha)'] = decimal.Decimal(fishoil.get()*550)
##    data['fishoil(epa)'] = decimal.Decimal(fishoil.get()*220)
##    data['fishoil(cla)'] = decimal.Decimal(fishoil.get()*90)
##    data['tyrosine'] = decimal.Decimal(tyrosine.get())
##    data['aspirin'] = decimal.Decimal(aspirin.get()*81)
##    data['creatine'] = decimal.Decimal(creatine.get()*5000)
###    data['niacin'] = decimal.Decimal(niacin.get()*100) #not in current
##    data['msm'] = decimal.Decimal(msm.get()*100)
###    data['rez-v'] = decimal.Decimal(rezV.get()*200)
##    data['hmb'] = decimal.Decimal(hmb.get()*500)
##    data['tongkat-ali'] = decimal.Decimal(tongkatali.get()*80)
###    data['red-ginseng'] = decimal.Decimal(r_ginseng.get()*300)
##    data['tribulus'] = decimal.Decimal(trib.get()*250)
##    data['eliteprominerals'] = decimal.Decimal(elite_min.get())
##    data['greenTeaECGC'] = decimal.Decimal(green_tea.get()*200)
##    data['greenTeaCatequins'] = decimal.Decimal(green_tea.get()*320)
##    data['forskolin'] = decimal.Decimal(forskolin.get()*20)
##    data['carnitine'] = decimal.Decimal(carnitine.get()*500)
##    for key in list(data.keys()):  ## creates a list of all keys
##        if data[key] == 0:
##            del data[key]
##
##    realm = 'supplements'
##    timestamp = hist_input.get()
##    required_hash_data = {
##        'realm': realm,
##        'timestamp': timestamp
##    }
##    #combine dicts
##    final_input_data = data.copy()
##    final_input_data.update(required_hash_data)
##    #write to wellness table
##    with table.batch_writer() as batch:
##        batch.put_item(final_input_data)
##    #print result
##    result = "PutItem succeeded"
##    t1.insert(tk.END, result)
##    t1.after(10000, lambda: t1.delete(1.0, tk.END))
#
###add the submit and cancel buttons
###tk.Button(shake_frame, text='Submit Current', command=submit_shake_data_current, pady=4, padx=7, relief='raised',bd=4).grid(row=1, column=0)
###tk.Button(shake_frame, text='Submit Historical', command=submit_shake_data_historical, pady=5, padx=7, relief='raised',bd=4).grid(row=1, column=1)
##hist_shake_input = tk.StringVar(value='2017-05-07 08:00:00')
##tk.Entry(shake_frame, text='what', textvariable=hist_shake_input).grid(row=1, column=2, columnspan=2)
##tk.Button(shake_frame, text='Quit', command=_quit, pady=4, padx=7, relief='sunken').grid(row=1,column=6)
##
###inputs
##ttk.Label(shake_frame, text='Protein').grid(row=11, column=0, sticky = 'E')
##temp_input = tk.StringVar(value='0.0')
##tk.Entry(shake_frame, textvariable=temp_input).grid(row=11, column=1,sticky = tk.E+tk.W)
