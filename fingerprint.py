#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
from lib.fingerprint import *



def _banner():
    print('''  
      __ _                                  _       _   
     / _(_)                                (_)     | |  
    | |_ _ _ __   __ _  ___ _ __ _ __  _ __ _ _ __ | |_ 
    |  _| | '_ \ / _` |/ _ \ '__| '_ \| '__| | '_ \| __|
    | | | | | | | (_| |  __/ |  | |_) | |  | | | | | |_ 
    |_| |_|_| |_|\__, |\___|_|  | .__/|_|  |_|_| |_|\__|
                  __/ |         | |                     
                 |___/          |_|                     
    ''')

def _usage():
    print("    Usage : python fingerprint.py http://www.baidu.com/")

if __name__ == '__main__':
    _banner()
    
    if len(sys.argv) < 2:
        _usage()
    else:
        langFingerPath = 'data/fingerprint/lang.json'
        webFingerPath  = 'data/fingerprint/web.json'
        cmsFingerPath  = 'data/fingerprint/cms.json'

        userAgentPath  = 'data/UserAgent/user-agents.txt'

        lang = fingerprint(userAgentPath, langFingerPath)
        web  = fingerprint(userAgentPath, webFingerPath)
        cms  = fingerprint(userAgentPath, cmsFingerPath)

        print(u'\t[-]\t指纹库已加载%d个语言特征' % lang.fingerCount)
        print(u'\t[-]\t指纹库已加载%d个Web容器特征' % web.fingerCount)
        print(u'\t[-]\t指纹库已加载%d个CMS特征' % cms.fingerCount)

        start = time.clock()
        rs_lang = lang.scan(sys.argv[1], True)
        if (len(rs_lang)>0):
            print(u'\t[-]\t识别到:%s, 在位置:%s' % (rs_lang[0]['tag'], rs_lang[0]['url']))
        rs_web  = web.scan(sys.argv[1], True)
        if (len(rs_web)>0):
            print(u'\t[-]\t识别到:%s, 在位置:%s' % (rs_web[0]['tag'], rs_web[0]['url']))
        rs_cms  = cms.scan(sys.argv[1], True)
        if (len(rs_cms)>0):
            print(u'\t[-]\t识别到:%s, 在位置:%s' % (rs_cms[0]['tag'], rs_cms[0]['url']))
        end = time.clock()
        print (u"\t[-]\t识别完成, 耗时: %f s" % (end - start))