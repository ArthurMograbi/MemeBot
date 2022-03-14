from __future__ import print_function
from PIL import Image
from random import randint
from random import seed
import os, os.path
from datetime import datetime
import time




def try_mkdir(dirName):
    try:
        os.mkdir(dirName)
        print("Directory %s Created " % dirName) 
    except FileExistsError:
        pass

def try_mkfile(fileName):
    try:
        open(fileName,'x')
        print("File %s Created " % fileName) 
    except FileExistsError:
        pass


try_mkdir("./Object")
try_mkdir("./Template")
try_mkdir("./TemplateBack")
try_mkdir("./OUTPUT")

try_mkfile("./data.txt")
try_mkfile("./existing.txt")

seed(datetime.now())

dataFile =open("./data.txt","r")
data = dataFile.read().split("\n")

dataFile.close()

data = [i.split(",") for i in data]
data = [ [int(j) for j in i if j!="" if i[0][0]!="M"] for i in data]



def craft(chotemp,choobj):
    tem2=False
    obj = Image.open('./Object/'+str(choobj)+'.png').convert("RGBA")
    if data[chotemp][5]==1:
        filetype='.jpg'
    else:
        filetype='.png'
        tem2= Image.open('./TemplateBack/'+str(chotemp)+filetype).convert("RGBA")
    tem = Image.open('./Template/'+str(chotemp)+filetype).convert("RGBA")
    box = (data[chotemp][0],data[chotemp][1],data[chotemp][2],data[chotemp][3])
    region = obj.resize((data[chotemp][2]-data[chotemp][0],data[chotemp][3]-data[chotemp][1]))
    region = region.rotate(data[chotemp][4])
    tem.paste(region,box,mask=region)
    if tem2:
        width, height = tem.size
        tem.paste(tem2,(0,0,width,height),mask=tem2)
    tem.save('./OUTPUT/'+str(len(os.listdir('./OUTPUT')))+'.png')
        


def gen(num):
    print("Processing\n|",end='')
    for i in range(num):
        eFile =open("./existing.txt","r+")
        exis = eFile.read()
        exisM = exis.split(",")
        objLen=len(os.listdir('./Object'))
        tempLen=len(os.listdir('./Template'))
        if len(exisM) >= objLen*tempLen:
           raise Exception("All possible combinations exausted!")
        oNum= randint(1,objLen)
        tNum= randint(1,tempLen)
        while (str(oNum)+"-"+str(tNum)) in exisM:
            oNum= randint(1,objLen)
            tNum= randint(1,tempLen)
        if i % (num//5) ==0:
            print('**',end='')
        craft(tNum,oNum)
        eFile.write(","+str(oNum)+"-"+str(tNum))
        eFile.close()
    print('|')
    time.sleep(1)
    

gen(int(input("How many would you like to generate?\n")))
#craft(5,2)

