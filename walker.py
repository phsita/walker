#!/usr/bin/python -tt

import os
import time
import re
import sys
import math
import traceback
import magic
import hashlib

# VERSION 0.2 Of the Application

BUF_SIZE = 65536
DIR="'-'.join(TARGET_DIR.split(os.sep)).strip('-')"
SIGNATURE="Directory_Files_Record"
COUNTER=1
TARGET_DIR=str()
TIME="time.ctime().replace(' ','-').replace('--','-').replace(':','-')"
FILE_NAME='"{}_{}-{}-{}.csv".format(SIGNATURE, eval(DIR), COUNTER, eval(TIME))'

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

def get_target_size(size):
    units=dict()
    units[0]="Bytes"
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

def get_target_type(target_path):
    target_type=magic.from_file(target_path, mime=True)
    return target_type

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

def write(data):
    if os.path.getsize(os.path.join(os.getcwd(),CURRENT_FILE))>=1048576:
        global COUNTER
        COUNTER+=1
        global CURRENT_FILE
        CURRENT_FILE=eval(FILE_NAME)
    out=open(CURRENT_FILE,"a+")
    fname=data.get("name")
    fpath=data.get("path")
    ttype=data.get("type")
    fsize=data.get("fsize")
    checksum=data.get("checksum")
    rsize=data.get("rsize")
    string="{}\t{}\t{}\t{}\t{}\t{}\n".format(
        fname,fpath,ttype,fsize,checksum,rsize)

#    print(string)
    out.write(string)
    out.close()

def start_app():
    try:
        global CURRENT_FILE
        CURRENT_FILE=eval(FILE_NAME)
        out=open(CURRENT_FILE,"a+")
        out.close()
        start_time=time.time()
        print("Walking through the directory tree \""+TARGET_DIR+"\"")
        for root, dirs, files in os.walk(TARGET_DIR):
            if files is not None:
                for target_name in files:
                    try:
                        target_path = os.path.join(root,target_name)
                        target_data=get_target_data(target_name,target_path)
                        write(target_data)

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
                        time.sleep(0.2)

        end_time=time.time()
        print("Done. Records stored in the current directory.")
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
                print(sys.argv[1]+\
                    " is a file. Directory expected.\nTry again.")
        
            elif (os.path.exists(sys.argv[1])):
                print("Directory expected.\nTry again.")

            else:
                print("Directory \""+sys.argv[1]+"\" does not exist.\nTry again.")

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
