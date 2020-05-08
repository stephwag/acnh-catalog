from PIL import Image
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
import json

CROP_SIZE = (630, 130, 1050, 645)
height = 720
width = 1280
time_amount = 30
fps = 30

def main(args):
    print(args)

    all_text = []
    all_json = []
    all_data = []

    num_frames = (fps * (time_amount - args.start)) 

    out, _ = (
        ffmpeg
        .input(args.filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24', vframes=num_frames, ss=f'00:00:{str(args.start).zfill(2)}')
        .run(capture_stdout=True)
        )

    video = np.frombuffer(out, np.uint8).reshape([-1, height, width, 3])

    for frame_num in range(num_frames):
        try:
            temp = Image.fromarray(video[frame_num])
        except IndexError:
            break

        im = temp.crop(CROP_SIZE).convert('L')
        text = pytesseract.image_to_string(im, config='--psm 11')

        for d in text.split('\n'):
            line = sent_tokenize(d.strip())
            if len(line) > 0:
                fname = "villagerdb/data/items/{}.json".format(line[0].lower().replace(' ', '-'))
                if path.exists(fname) and fname not in all_json:
                    all_json.append(fname)
                    with open(fname, 'r') as f:
                        jdata = json.loads(f.read())
                        all_text.append(jdata['name'])
                        all_data.append(json.dumps(jdata))
                        print(jdata['name'])


    all_text = sorted(list(set(all_text)))
    with open("catalog.txt", "w") as f: f.write("\n".join(all_text))
    with open("catalog.ndjson", "w") as f: f.write("\n".join(all_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract AC catalog from video.')
    parser.add_argument('filename', type=str, help='a video, recorded from switch')
    parser.add_argument('--start', dest='start', type=int, default=0,
        help='Specify (in seconds) where to start in the video')
    args = parser.parse_args()
    main(args)






