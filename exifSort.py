#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 16:09:57 2020

@author: navneethkrishna
"""

#Sorting a directory based on the exif data.
#The EXIF file format returns an object similar to json which can be accessed via a dictionary.
#Once the entire media is sorted, we create subdirectories for the mentioned date.
import os
import shutil
import progressbar
import colorama
#from time import sleep
#for i in xrange(20):
    #bar.update(i+1)
    #sleep(0.1)
parent = input("Enter the absolute path of the directory:")
if(parent[-1] != '/'):
    parent = parent + '/'
entries = os.listdir(parent)
#print(entries)
import PIL.Image
PIL.Image.MAX_IMAGE_PIXELS = None
from datetime import datetime 
count = 0
supported_types = ".png .jpg .jpeg .gif .psd .epf .JPG .PNG .JPEG .GIF .PSD .EPF"
for file in entries:
    filename, file_extension = os.path.splitext(str(file))
    if str(file_extension)[1:] in supported_types and str(file)[0]!='.':
        count = count + 1
totalCount = count
percentage = 0
#bar = progressbar.ProgressBar(maxval=count, \
    #widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
#bar.start()
count = 0
for file in entries:
    print(colorama.Fore.WHITE+"Currently working on file: "+str(file))
    #print(file)
    count = count + 1
    filename, file_extension = os.path.splitext(str(file))
    #print(file_extension)
    if (str(file_extension)[1:] in supported_types) and os.path.isdir(parent+str(file)) == False and str(file)[0]!='.':
        img = PIL.Image.open(parent+str(file))
        exif_data = img._getexif()
        #print(exif_data)
        #print(str(entries).find("exif"))
        #print(len(str(entries)))
        #result2010 = exif_data.find("201")
        #result2020 = exif_data.find("202")
        #meta_data =  ImageMetaData(path_name)
        if(str(exif_data) != "None"):
            #print("Passed exif empty check.")
            result = 0
            dates_obtained = []
            exif_text = str(exif_data)
            #print(exif_text)
            #result = 0
            #exif_text = str(exif_data)
            while(result!=-1):
                #print("Trying 2000")
                result = exif_text.find("\'200")
                if(result!=-1):
                    dates_obtained.append(exif_text[result+1:result+20])
                    exif_text = exif_text[result+19:]
            result = 0
            exif_text = str(exif_data)
            while(result!=-1):
                #print("Trying 2010")
                result = exif_text.find("\'201")
                if(result!=-1):
                    dates_obtained.append(exif_text[result+1:result+20])
                    exif_text = exif_text[result+19:]
            result = 0
            exif_text = str(exif_data)
            while(result!=-1):
                result = exif_text.find("\'202")
                if(result!=-1):
                    dates_obtained.append(exif_text[result+1:result+20])
                    exif_text = exif_text[result+19:]
            #print(dates_obtained)
            if(len(dates_obtained)>0):
                datetime_objects = []
                for i in dates_obtained:
                    datetime_object = datetime.strptime(i, '%Y:%m:%d %H:%M:%S')
                    datetime_objects.append(datetime_object)
                #print(datetime_objects)
                datetime_objects.sort()
                createdTime = datetime_objects[0]
                folder = createdTime.strftime('%d-%b-%Y')
                #print(folder)
                if(os.path.exists(folder) == False):
                    path = os.path.join(parent, folder)
                    os.mkdir(path)
                dest = shutil.move(parent+str(file), parent+folder+"/")
                print(colorama.Back.GREEN+"Image: "+str(file)+" successfully moved to "+dest)
                #bar.update(count)
                percentage = count * 100 / totalCount
                print(colorama.Fore.GREEN+"Completed "+str(percentage)+"% out of 100%")
    
#bar.finish()        
        

        
    