#!/usr/bin/python
# -*- coding: UTF-8 -*-

import re
import json
import random
import urllib2
import cipher

class fingerprint:

    userAgentdb = []

    def __init__(self, userAgentPath, fingerprintPath):
        self.fingerprintdb = {}
        self.fingerCount = 0
        if not self.userAgentdb:
            self.loadUserAgent(userAgentPath)
        self.loadFingerprint(fingerprintPath)

    def loadUserAgent(self, path):
        file = open(path)
        items = file.readlines()
        file.close()
        for item in items:
            self.userAgentdb.append(item)

    def loadFingerprint(self, file):
        file = open(file)
        list = json.load(file, encoding="utf-8")
        for finger in list:
            key = finger['url']
            values = self.fingerprintdb.setdefault(key, [])
            values.append(finger)
        file.close()
        self.fingerCount = len(list)

    def check(self, body, header, fingerdb, fastMode):
        rs=[]

	charset_reg =r'<meta.*charset="?([\w|-]*)"?\s*/?>'
	patten = re.compile(charset_reg)
	match_patten_code = patten.search(body)
	if match_patten_code is None:
		code = 'UTF-8'
	else:
		code = match_patten_code.group(1)

        for finger in fingerdb:
            if finger["md5"]:
                md5 = cipher.getmd5(body)
                if (finger["md5"] !=md5):
                    continue
            elif finger["pattern"]:
                isMatch = False
                if (finger["mode"] == 'body'):
                    isMatch = re.search(finger['pattern'], body.decode(encoding=code), re.IGNORECASE)
                elif (finger["mode"] == 'header'):
                    isMatch = re.search(finger['pattern'], header.decode(encoding='UTF-8'), re.IGNORECASE)
                if (not isMatch):
                    continue
            elif finger['regex']:
                isMatch = False
                if (finger["mode"] == 'body'):
                    isMatch = re.search(finger['regex'], body.decode(encoding=code), re.IGNORECASE)
                elif (finger["mode"] == 'header'):
                    isMatch = re.search(finger['regex'], header.decode(encoding='UTF-8'), re.IGNORECASE)
                if (not isMatch):
                    continue
            rs.append(finger)
            if fastMode:
                break
        return rs

    def scan(self, url, fastMode):
        rs = []
        for path_url in self.fingerprintdb:
            test_url = url.rstrip('/') + path_url
            request = urllib2.Request(test_url)
            request.add_header('User-Agent', random.choice(self.userAgentdb).rstrip('\n'))
            try:
                response = urllib2.urlopen(request)
                body = response.read()
                header = str(response.info())
                if not body is None:
                    matched = self.check(body, header, self.fingerprintdb[path_url], fastMode)
                    if matched:
                        rs.extend(matched)
                        if fastMode:
                            break
            except urllib2.HTTPError:
                pass
        return rs
