#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 09:31:41 2018

@author: davidhagan
"""
import string
import secrets

N = 32
this = ''.join(secrets.choice(string.printable) for _ in range(N))
print(this)
#print(string.printable)