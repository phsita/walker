#!/usr/bin/python -tt

import hashlib
import magic
import math
import os
import re
import sys
import time
import traceback

# For Faster Writing to Files
BUF_SIZE = 65536

# Directory Root to be looked up for finding duplicates 
DIR="'-'.join(TARGET_DIR.split(os.sep)).strip('-')"

# Banner appearing in File Names
BN="Files_Index"

# Stored Files Index Counter for keeping counts of number of SFI Files Created
SFI_COUNTER=1

# Deleted Files Index Counter for keeping counts of number of DFI Files Created
DFI_COUNTER=1

# Target Directory 
TARGET_DIR=str()
STATUS=""
TIME="time.ctime().replace(' ','_').replace('--','-').replace(':','-')"

# SFI_FILE --> STORED FILES INDEX File Containing Index of Files Stored
# in Disk
SFI_FILE_NAME='"{}_{}-{}-({}).txt".format(BN, eval(DIR), eval(TIME),\
 SFI_COUNTER)'

# Dfi_FILE --> DELETED FILES INDEX File Containing Index of Files Deleted
# from Disk
DFI_FILE_NAME='"Deleted_{}_{}-{}-({}).txt".format(BN, eval(DIR),\
 eval(TIME), DFI_COUNTER)'

# print("DIR: "+DIR+"\t\tTARGET_DIR: "+TARGET_DIR)

SFI_FILE=str()
DFI_FILE=str()

# Return Checksum of Target
def get_target_checksum(target_path):
    sha512 = hashlib.sha512()
    with open(target_path, 'rb') as target:
        while True:
            data = target.read(BUF_SIZE)
            if not data:
                break
            sha512.update(data)
    target_checksum=sha512.hexdigest()
    target.close()
    return target_checksum

# Returns Size of Target File in Human Readable Format
def get_target_size(size):
    units=dict()
    units[0]="B"
    units[1]="KB"
    units[2]="MB"
    units[3]="GB"
    units[4]="TB"
    if size<100:
        fsize=str(size)+" "+units.get(0)
    else:
        i=int(math.floor(math.log(size,1024)))
        p=math.pow(1024,i)
        fsize=round(size/p,2)
        fsize=str(fsize)+" "+units.get(i)
    return fsize

# Gives MIME Type of the Target File
def get_target_type(target_path):
    target_type=magic.from_file(target_path, mime=True)
    return target_type

# Collect all data regarding Target File and store in a Dictionary
def get_target_data(target_name,target_path):
    data=dict()
    f=open(target_path,'rb')
    contents=f.read()
    checksum=get_target_checksum(target_path)
    rsize=os.path.getsize(target_path)
    fsize=get_target_size(rsize)
    ttype=get_target_type(target_path)
    data["name"]=target_name
    data["path"]=target_path
    data["checksum"]=checksum
    data["fsize"]=fsize
    data["type"]=ttype
    data["rsize"]=rsize
    f.close()
    return data

# Write Data separated by Tab to a File
def write_target_data(data,f_status):

    global SFI_FILE
    global DFI_FILE
    global SFI_COUNTER
    global DFI_COUNTER
   
    if os.path.getsize(os.path.join(os.getcwd(),SFI_FILE))>=1048576:
        SFI_COUNTER+=1
        SFI_FILE=eval(SFI_FILE_NAME)

    if os.path.getsize(os.path.join(os.getcwd(),DFI_FILE))>=1048576:
        DFI_COUNTER+=1
        DFI_FILE=eval(DFI_FILE_NAME)
    
    if f_status is 0:
        output_file=open(SFI_FILE,"a+")
    else:
        output_file=open(DFI_FILE,"a+")
    
    fname=data.get("name")
    fpath=data.get("path")
    ttype=data.get("type")
    fsize=data.get("fsize")
    checksum=data.get("checksum")
    rsize=data.get("rsize")
    string="{}\t{}\t{}\t{}\t{}\t{}\n".format(
        fname,fpath,ttype,fsize,checksum,rsize)
    # print(string)
    output_file.write(string)
    output_file.close()

def validate_data(target_file):

    
    # STATUS = 0    -->    KEEP FILE
    # STATUS = 1    -->    DELETE FILE
    target_checksum=target_file.get("checksum")
    target_rsize=target_file.get("rsize")
    status=-1
    f=open(SFI_FILE,"a+")
    check_sha=f.read().find(target_checksum)
    f.close()
    if ( check_sha is -1 or target_rsize is 0 ):
        status=0
    else:
        status=1

    return status

def start_app():
    global SFI_FILE
    global DFI_FILE
    try:
#        global CURRENT_FILE
#        CURRENT_FILE=eval(FILE_NAME)
#        out=open(CURRENT_FILE,"a+")
#        out.close()
        # CREATING INDEX FILES
        SFI_FILE=eval(SFI_FILE_NAME)
        DFI_FILE=eval(DFI_FILE_NAME)

#        BN="Files_Index"        SFI_COUNTER=1        DFI_COUNTER=1        TARGET_DIR=str()
#        STATUS=""        TIME="time.ctime().replace(' ','-').replace('--','-').replace(':','-')"
#        SFI_FILE_NAME='"{}_{}-{}-({}).txt".format(BN, eval(DIR), eval(TIME), SFI_COUNTER)'
#        DFI_FILE_NAME='"Deleted_{}_{}-{}-({}).txt".format(BN, eval(DIR), eval(TIME), DFI_COUNTER)'
#        SFI_FILE=str()
#        DFI_FILE=str()

        
#        print("DIR: '{}'\tBN: '{}'\tTARGET_DIR: '{}'\nSTATUS: '{}'\tTIME: '{}'".format(DIR, BN, TARGET_DIR, STATUS, TIME))
#        print("SFI_COUNTER: '{}'\tDFI_COUNTER: '{}'\nSFI_FILE_NAME: '{}'\nDFI_FILE_NAME: '{}'\t".format(SFI_COUNTER,DFI_COUNTER,SFI_FILE_NAME,DFI_FILE_NAME))
#        print("SFI_FILE: '{}'\tDFI_FILE: '{}'".format(SFI_FILE,DFI_FILE))

        FILE=open(SFI_FILE,"a+")
        FILE.close()

        FILE=open(DFI_FILE,"a+")
        FILE.close()
        
        start_time=time.time()
        print("Walking through the directory tree \""+TARGET_DIR+"\"")
        for root, dirs, files in os.walk(TARGET_DIR):
            if files is not None:
                for target_name in files:
                    try:
                        target_path=os.path.join(root,target_name)
                        target_data=get_target_data(target_name,target_path)
                        f_status=validate_data(target_data)
                        write_target_data(target_data,f_status)
                        if f_status:
                            # print("Deleting File \""+target_path+"\"")
                            os.remove(target_path)

                    except IOError as ie:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print("Error Occured:")
                        traceback.print_exception(exc_type, exc_value,
                            exc_traceback, limit=2, file=sys.stdout)
                        print("Skipping File "+target_path)
                        continue

                    except KeyboardInterrupt as ki:
                        raise

                    except:
                        exc_type, exc_value, exc_traceback = sys.exc_info()
                        print("Error Occured:")
                        traceback.print_exception(exc_type, exc_value, 
                            exc_traceback, limit=2, file=sys.stdout)

                    finally:
                        time.sleep(0.002)

        end_time=time.time()
        print("Done. Records are stored in current directory.")
        proc_time=int(end_time-start_time)
        hrs=(proc_time/(3600*1.0))
        mins=(hrs%1)*60
        secs=((mins%1)*60)
        print("Processing Time - {} hrs : {} mins : {} secs".format(
            int(hrs),int(mins),int(secs)))

    except KeyboardInterrupt as ki:
        raise

def main():

    try:
        if len(sys.argv) is 1:
            print('Enter directory root.')
        elif len(sys.argv) is 2:
            if (os.path.isdir(sys.argv[1])):
                global TARGET_DIR
                TARGET_DIR=sys.argv[1]
                start_app()
            elif (os.path.isfile(sys.argv[1])):
                print("\""+sys.argv[1]+
                    "\" is a file. Directory expected.\nTry again.")
        
            elif (os.path.exists(sys.argv[1])):
                print("Directory expected.\nTry again.")

            else:
                print("Directory \""+
                    sys.argv[1]+"\" does not exist.\nTry again.")

        else:
            print("Provide the directory tree as the argument.\nTry Again.")

    except KeyboardInterrupt as ki:
        print("Aborting Program.")
        sys.exit(0)

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        print "Error Occured:"
        traceback.print_exception(exc_type, exc_value, exc_traceback,
            limit=2, file=sys.stdout)

if __name__=='__main__':
    main()
