#! /usr/bin/env python
#coding=utf-8

import os
import stat
import hashlib
import urllib 
from mimetypes import MimeTypes
from OptionKey import OptionKey

class MyFile(object):
    __READBUFFSIZE = 4096
    mMd5Checksum = None
    mSha1Checksum = None
    mMimeType = None
    
    def __init__(self, path, name):
        self.mPath = path
        self.mName = name
        self.mFullPathName = path + name
    
    @property
    def path(self):
        return self.mPath
    
    @property
    def name(self):
        return self.mName
    
    @property
    def fullPathName(self):
        return self.mFullPathName;
    
    @property
    def atime(self):
        return os.stat(self.mFullPathName)[stat.ST_ATIME]
    
    @property
    def size(self):
        return os.stat(self.mFullPathName)[stat.ST_SIZE]
    
    @property
    def mime(self):
        if self.mMimeType is not None:
            return self.mMimeType
        
        mime = MimeTypes()
        url = urllib.pathname2url(self.mFullPathName)
        self.mMimeType = mime.guess_type(url)[0]
        if self.mMimeType is None:
            self.mMimeType = "Unkown/None"
        return self.mMimeType
    
    def __getMd5CheckSum(self):
        if self.mMd5Checksum is not None:
            return self.mMd5Checksum
        
        md5 = hashlib.md5()
        with open(self.mFullPathName, "rb") as handler:
            while(True):
                bulk = handler.read(self.__READBUFFSIZE)
                if not bulk:
                    break
                md5.update(bulk)
        self.mMd5Checksum = md5.hexdigest()
        return self.mMd5Checksum
    
    def __getSha1CheckSum(self):
        if self.mSha1Checksum is not None:
            return self.mSha1Checksum
        
        sha1 = hashlib.sha1()
        with open(fileName, "rb") as handler:
            while(True):
                bulk = handler.read(self.__READBUFFSIZE)
                if not bulk:
                    break
                sha1.update(bulk)
        self.mSha1Checksum = sha1.hexdigest()
        return self.mSha1Checksum
    
    def getCheckSum(self, type):
        print("File {0} Generate checksum by {1}".format(self.mFullPathName, type))
        if OptionKey.MD5 is type:
            return self.__getMd5CheckSum()
        elif OptionKey.SHA1 is type:
            return self.__getSha1CheckSum()
        else:
            return self.__getMd5CheckSum()
    
