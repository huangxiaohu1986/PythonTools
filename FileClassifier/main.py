#! /usr/bin/env python
#coding=utf-8

import getopt,sys
import json

from FileSelector import FileSelector
from OptionKey import OptionKey

config = {OptionKey.INPUT:"E:/test/",
    OptionKey.OUTPUT:"E:/testResult/",
    OptionKey.CHECKSUM_TYPE:"md5",
    OptionKey.CLASSIFY_TYPE:"date",
    OptionKey.VERBOSE:False
    }

def usage():
    print("File classfier useage:\n")

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:c:v", ["help", "input=", 
            "output=", "type=", "classify=", "verbose"])
        for option, value in opts: 
            if option in ["-h", "--help"]:
                usage()
            elif option in ["-i", "--input"]:
                config[OptionKey.INPUT] = value
            elif option in ["-o", "--output"]:
                config[OptionKey.OUTPUT] = value
            elif option in ["-t", "--type"]:
                config[OptionKey.CHECKSUM_TYPE] = value
            elif option in ["-c", "--classify"]:
                config[OptionKey.CLASSIFY_TYPE] = value
            elif option in ["-v", "--verbose"]:
                config[OptionKey.VERBOSE] = True
            else:
                print("Can't found the option")
    except getopt.GetoptError:
        print("option error!\n");
        usage();
    
    if config[OptionKey.VERBOSE]:
        print("config:" + json.dumps(config))
    fileSelector = FileSelector()
    fileSelector.initialize(config)
    fileSelector.start()
            
if __name__ == '__main__':
    main()