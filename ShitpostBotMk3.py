from __future__ import print_function
from PIL import Image
from random import randint
from random import seed
import os, os.path
from datetime import datetime
import time
seed(datetime.now())
file_path=os.getcwd()
#objnumb=len(os.listdir(file_path+'\\object'))
#tempnumb=len(os.listdir(file_path+'\\template'))

dataFile =open(file_path+"\\data.txt","r")
data = dataFile.read().split("\n")
data = [i.split(",") for i in data]
data = [ [int(j) for j in i if j!="" if i[0][0]!="M"] for i in data]
#print(data)
#seed(os.time())

def craft(chotemp,choobj):
    tem2=False
    obj = Image.open(file_path+'\\Object/'+str(choobj)+'.png').convert("RGBA")
    if data[chotemp][5]==1:
        filetype='.jpg'
    else:
        filetype='.png'
        tem2= Image.open(file_path+'\\TemplateBack/'+str(chotemp)+filetype).convert("RGBA")
    tem = Image.open(file_path+'\\Template/'+str(chotemp)+filetype).convert("RGBA")
    box = (data[chotemp][0],data[chotemp][1],data[chotemp][2],data[chotemp][3])
    region = obj.resize((data[chotemp][2]-data[chotemp][0],data[chotemp][3]-data[chotemp][1]))
    region = region.rotate(data[chotemp][4])
    tem.paste(region,box,mask=region)
    if tem2:
        width, height = tem.size
        tem.paste(tem2,(0,0,width,height),mask=tem2)
    tem.save(file_path+'\\OUTPUT/'+str(len(os.listdir(file_path+'\\OUTPUT')))+'.png')
        


def gen(num):
    print("Processing\n|",end='')
    for i in range(num):
        eFile =open(file_path+"\\existing.txt","r+")
        exis = eFile.read()
        exisM = exis.split(",")
        objLen=len(os.listdir(file_path+'\\Object'))
        tempLen=len(os.listdir(file_path+'\\Template'))
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
dataFile.close()
