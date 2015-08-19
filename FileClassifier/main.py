#! /usr/bin/env python
#coding=utf-8

import getopt,sys
import json

from FileSelector import FileSelector
from OptionKey import OptionKey

config = {OptionKey.INPUT:"E:/test/",
    OptionKey.OUTPUT:"E:/testResult/",
    OptionKey.CHECKSUM_TYPE:"md5"}

def usage():
    print("File classfier useage:\n")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:", ["help", "input=", 
            "output=", "type="])
        for option, value in opts: 
            if option in ["-h", "--help"]:
                usage()
            elif option in ["-i", "--input"]:
                config["input"] = value
            elif option in ["-o", "--output"]:
                config["output"] = value
            elif option in ["-t", "--type"]:
                config["type"] = value
            else:
                print("Can't found the option")
    except getopt.GetoptError:
        print("option error!\n");
        usage();
    
    print("config:" + json.dumps(config))
    fileSelector = FileSelector()
    fileSelector.initialize(config)
    fileSelector.start()
            
if __name__ == '__main__':
    main()