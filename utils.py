from PIL import Image, ImageOps
import subprocess, base64, sys
from io import BytesIO, StringIO
import io
import ffmpeg
import numpy as np
import pytesseract
import argparse
from nltk.tokenize import sent_tokenize
import nltk
import os.path
from os import path
import os
import json

CROP_SIZE = (630, 130, 1050, 645)
CROP_SIZE_INVENTORY = (200, 0, 1150, 400)
height = 720
width = 1280
time_amount = 30
fps = 30

def white_nontext(img):
    img.convert("RGB")
    pixdata = img.load()
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if sum(pixdata[x, y]) < 100:
                pixdata[x, y] = (0, 0, 0)
            else:
                pixdata[x, y] = (255, 255, 255)

def is_orderable(data):
    try:
        if data["games"]["nh"]["orderable"]: return True
    except:
        pass

    return False

def add_to_list(args, data):
    if args.orderable:
        if not is_orderable(data):
            return False

    if args.categories is not None:
        try:
            if not data['category'].lower() in args.categories:
                return False

        except:
            return False

    if args.categories_exclude is not None:
        try:
            if data['category'].lower() in args.categories:
                return False

        except:
            return False

    return True





