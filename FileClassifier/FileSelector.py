#! /usr/bin/env python
#coding=utf-8

import os
import shutil

from OptionKey import OptionKey
from MyFile import MyFile

class FileSelector(object):
    def initialize(self, config):
        self.mInputDir = config[OptionKey.INPUT]
        self.mOutputDir = config[OptionKey.OUTPUT]
        self.mCheckSumType = config[OptionKey.CHECKSUM_TYPE]
        self.mClassifyType = config[OptionKey.CLASSIFY_TYPE]
    
    def __generateOutputDir(self, classifyType):
        if classifyType is OptionKey.date:
            #the data format is YYYY-MM-DD hh:mm:ss,we need years and month only
            return [(self.mOutputDir +  str(sourceFile.createtimeStr[:sourceFile.createtimeStr.rfind("-")])
                     + os.sep) for sourceFile in self.mOutputList]
        else:
            #the mime format is general-type/detail-type,we need general type only
            return [(self.mOutputDir +  sourceFile.mime[:sourceFile.mime.find('/') + 1]) for sourceFile in self.mOutputList]
    
    def __renameDumplicateFiles(self, file, counterDic):
        fileName = file.name
        
        """
        create the key as the output parent dir + filename
        """
        key = fileName
        if self.mClassifyType is OptionKey.date:
            key = key + str(file.createtimeStr[:file.createtimeStr.rfind("-")])
        else:
            key = key + file.mime[:file.mime.find('/') + 1]
        
        """
        rename the filename which is already to be the target dir
        casue all the files in the same layer
        """
        if counterDic.get(key, 0) == 0:
            counterDic[key] = 1
            return fileName;
        else:
            name, ext = os.path.splitext(fileName) 
            newName = name + "_" + str(counterDic[key]) + ext
            counterDic[key] = counterDic.get(key) + 1
            return newName
    
    def __warpperCopy(self, sourcePath, destPath):
        self.mCounter += 1
        print("ClassFile process in {0}/{1}".format(self.mCounter, self.mTotal))
        shutil.copy(sourcePath, destPath)
        
    def outputToTarget(self):
        if(len(self.mOutputList) == 0):
            print("There is valid file")
            return
        
        """create output dor if needed"""
        if not os.path.exists(self.mOutputDir):
            os.mkdir(self.mOutputDir)
        outputDir = self.__generateOutputDir(self.mClassifyType)
        for path in outputDir:
            if not os.path.exists(path):
                os.mkdir(path)
        
        """copy the files to the output dir"""
        dupNamesCounterDic = dict()
        self.mCounter = 0
        self.mTotal = len(self.mOutputList)
        
        map(self.__warpperCopy,
            [sourceFile.fullPathName for sourceFile in self.mOutputList],
            [(dir + self.__renameDumplicateFiles(sourceFile, dupNamesCounterDic))
                for dir,sourceFile in zip(outputDir, self.mOutputList)])
        
    def processPickoutFiles(self):
        fileDic,outputDic,self.mOutputList, fileList = dict(),dict(),list(),list()
        
        for root, dirs, files in os.walk(self.mInputDir):
            for file in files:
                fileList.append(MyFile(root, file))
        
        """
        classify the files into  different list bu its file size
        """
        for file in fileList:
            listBySize = fileDic.get(file.size, list())
            listBySize.append(file)
            fileDic[file.size] = listBySize
                
        """
        copute the checksum which filelist's length is not 0 in outputDic and then insert them
        into the outputDic which key as the checksum,for the key's unique of dictionary,it can
        fileter the duplicate file
        """
        for key in fileDic.keys():
            if len(fileDic[key]) == 1:
                for file in fileDic[key]:
                    self.mOutputList.append(file)
            else:
                for file in fileDic[key]:
                    outputDic[file.getCheckSum(self.mCheckSumType)] = file
        """
        merge the valid file into the outputFileList
        """
        self.mOutputList.extend([outputDic[key] for  key in outputDic.keys()])
        
    def start(self):
        self.processPickoutFiles()
        self.outputToTarget()