
from skpy import Skype
from getpass import getpass
from extractor import allgchistory, singlegchistory
import re
from quickstart import updatefile
from uploadtogdrive import uploadfile
import os

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    sentinel = input("\nPress 1 to proceed Generate GC History:\nPress 3 to Upload or Update file in G Drive:\nPress 0 to exit: ")
    while sentinel != '0':
        if sentinel == '1':
            print('\nEnter password to login:\n')
            sk = Skype('katranjikamote@gmail.com', getpass())
            if sk.conn.connected:
                gcid = sk.chats.recent()
                groupid(gcid)     
                
                param = input("Enter GC ID, or Press Enter to Generate all GC History: ")            

                if param:                
                    singlegchistory(sk, gcid, param)
                    del gcid[param]
                elif not param:
                    allgchistory(sk, gcid)   

                groupid(gcid)


        elif sentinel == '3':
            updateuploadinGDrive()

        elif sentinel == "0":
            exit()
        
        sentinel = input("\nPress 1 to proceed Generate GC History:\nPress 3 to Upload or Update file in G Drive:\nPress 0 to exit: ")


def groupid(gcid):
    for x in gcid:
            if re.findall("19", x):
                print("Group Name: ", gcid[x].topic,"Group ID: ", x)
    print("\n")



def updateuploadinGDrive():
    os.system('cls' if os.name == 'nt' else 'clear')
    uploadupdate = input("\nPress 1 to upload file to G Drive,\nPress 3 to Update file in G Drive,\nPress 0 to exit: ") 

    if uploadupdate == "1":  
        filename = input("Enter file name: ")
        if filename:
            uploadfile('./docs/', filename+'.xlsx')  
        else:
            print("Must profie file name.\n")
            return
    elif uploadupdate == '3':
        filename = input("Enter file name: ")
        if filename:
            updatefile(filename+'.xlsx')
        else:
            print("Must provide file.\n")
            return
        # updateinGDrive(filename+'.xlsx')  

main()