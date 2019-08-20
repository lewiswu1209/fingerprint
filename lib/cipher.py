#!/usr/bin/python
# -*- coding: UTF-8 -*-

import hashlib

def getmd5(plain):
    m2 = hashlib.md5()
    m2.update(plain)
    return m2.hexdigest()
