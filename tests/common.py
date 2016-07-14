#!/usr/bin/python
# -*- coding: utf-8 -*-


def read(path):
    f = open(path, "r")
    data = f.read()
    f.close()
    return data


def write(path, data):
    f = open(path, "w")
    f.write(data)
    f.close()
