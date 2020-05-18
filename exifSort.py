#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Sorting a directory based on the exif data.
#The EXIF file format returns an object similar to json which can be accessed via a dictionary.
#Once the entire media is sorted, we create subdirectories for the mentioned date.

import os
import shutil
import colorama
import PIL.Image
from datetime import datetime 
PIL.Image.MAX_IMAGE_PIXELS = None
supported_types = ".png .jpg .jpeg .gif .psd .epf .JPG .PNG .JPEG .GIF .PSD .EPF"

def appendSlash(parent):
    if(parent[-1] != '/'):
        parent = parent + '/'
    return parent    

def getDirName(parent):
    reversedDir = str(parent[::-1])
    reversedDir = reversedDir[1:]
    dirNameStartsWith = reversedDir.find("/")
    dirNameReversed = reversedDir[:dirNameStartsWith]
    dirName = dirNameReversed[::-1]
    return dirName

def countLegitFiles(entries):
    count = 0
    for file in entries:
        filename, file_extension = os.path.splitext(str(file))
        if str(file_extension)[1:] in supported_types and str(file)[0]!='.':
            count = count + 1
    return count

def recurse(dirPath, dirName, entries):
    
    def searchDates(x):
        result = 0
        exif_text = str(exif_data)
        if(x == "2000"):
            y = "\'200"
        elif(x == "2010"):
            y = "\'201"
        else:
            y = "\'202"
        while(result!=-1):
            result = exif_text.find(y)
            if(result!=-1):
                dates_obtained.append(exif_text[result+1:result+20])
                exif_text = exif_text[result+19:]
    
    for file in entries:
        print(colorama.Fore.WHITE+"Currently working on file: "+str(file)+" in dir: "+str(dirName))
        filename, file_extension = os.path.splitext(str(file))
        if(os.path.isdir(dirPath+str(file)) == True and str(file)[0]!='.'):
            subdirPath = dirPath + str(file) + "/"
            subdirName = getDirName(subdirPath)
            subEntries = os.listdir(subdirPath)
            recurse(subdirPath, subdirName, subEntries)    
        elif (str(file_extension)[1:] in supported_types and str(file)[0]!='.'):
            img = PIL.Image.open(dirPath+str(file))
            exif_data = img._getexif()
            readFiles = ''
            with open(parent+'.settings.txt', 'r') as myfile:
                readFiles = myfile.read()
            myfile.close()
            if(str(exif_data) != "None" and str(file) not in readFiles):
                dates_obtained = []
                searchDates("2000")
                searchDates("2010")
                searchDates("2020")
                if(len(dates_obtained)>0):
                    datetime_objects = []
                    for i in dates_obtained:
                        datetime_object = datetime.strptime(i, '%Y:%m:%d %H:%M:%S')
                        datetime_objects.append(datetime_object)
                    datetime_objects.sort()
                    createdTime = datetime_objects[0]
                    folder = createdTime.strftime('%d-%b-%Y')
                    if(os.path.exists(folder) == False):
                        path = os.path.join(dirPath, folder)
                        os.mkdir(path)
                    dest = shutil.move(dirPath+str(file), dirPath+folder+"/")
                    print(colorama.Back.GREEN+"Image: "+str(file)+" successfully moved to "+dest)
                    with open(parent+".settings.txt", "a") as myfile:
                        myfile.write(str(file)+"\n")
                    myfile.close()

def main():
    parentDir = input("Enter the absolute path of the directory:")
    if(os.path.isdir(parentDir)) == False:
        print("Invalid directory.\nPlease ensure that you have entered the absolute path.\n")    
    else:
        global parent
        parent = appendSlash(parentDir)
        if(os.path.isfile(parent+".settings.txt") == False):
            f = open(parent+".settings.txt", "w+")
            f.write("***List of read files***\n")
            f.close()
        entries = os.listdir(parent)
        totalCount = countLegitFiles(entries)
        dirName = getDirName(parent)
        recurse(parent, dirName, entries)
        print("Process complete.")
            
if __name__ == "__main__":
    main()
                