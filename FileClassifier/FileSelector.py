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
            
    def outputToTarget(self):
        if(len(self.mOutputList) == 0):
            print("There is valid file")
            return
        
        """create output dor if needed"""
        if not os.path.exists(self.mOutputDir):
            os.mkdir(self.mOutputDir)
        outputDir = [(self.mOutputDir +  sourceFile.mime[:sourceFile.mime.find('/') + 1]) for sourceFile in self.mOutputList]
        for path in outputDir:
            if not os.path.exists(path):
                os.mkdir(path)
        
        """copy the files to the output dir"""
        map(shutil.copy,
            [sourceFile.fullPathName for sourceFile in self.mOutputList],
            [(dir + sourceFile.name) for dir,sourceFile in zip(outputDir, self.mOutputList)])
        
    def processPickoutFiles(self):
        fileList = [MyFile(self.mInputDir, name) for name in os.listdir(self.mInputDir)]
        fileDic,outputDic,self.mOutputList = dict(),dict(),list()
        
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