from utils import *

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

        if args.inventory:
            im = temp.crop(CROP_SIZE_INVENTORY)
            im = ImageOps.invert(im)
            white_nontext(im)
        else:
            im = temp.crop(CROP_SIZE).convert('L')
            # --psm 11 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvw\ xyz
        text = pytesseract.image_to_string(im, config="--psm 11")
        for d in text.lower().split('\n'):
            line = sent_tokenize(d.strip())
            if len(line) > 0:
                fname = "villagerdb/data/items/{}.json".format(line[0].lower().replace(' ', '-'))
                if os.path.exists(fname):
                    if fname not in all_json:

                        with open(fname, 'r') as f:
                            jdata = json.loads(f.read())
                            if add_to_list(args, jdata):
                                all_text.append(jdata['name'])
                                all_data.append(json.dumps(jdata))
                                print(jdata['name'])

                        all_json.append(fname)

                else:
                    if args.debug:
                        if not os.path.exists(fname):
                            print("NOT FOUND: {}".format(line))

    all_text = sorted(list(set(all_text)))

    if not os.path.exists('catalogs'):
        os.mkdir('catalogs')

    fname = args.filename.split("/")[-1]
    with open(f"catalogs/{fname}.txt", "w") as f: f.write("\n".join(all_text))
    with open(f"catalogs/{fname}.ndjson", "w") as f: f.write("\n".join(all_data))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Extract AC catalog from video.')
    parser.add_argument('filename', type=str, help='a video, recorded from switch')
    parser.add_argument('--start', dest='start', type=int, default=0,
        help='Specify (in seconds) where to start in the video')
    parser.add_argument('--orderable', dest='orderable', action='store_true',
        help='Only get items from the catalog that are orderable')
    parser.add_argument('--categories', dest='categories', nargs='+', type=str,
        help='Categories of items from the catalog (default: all)')
    parser.add_argument('--categories_exclude', dest='categories_exclude', nargs='+', type=str,
        help='Categories to exclude from the catalog (default: none)')
    parser.add_argument('--inventory', dest='inventory', action='store_true',
        help='Parse text from the inventory menu (work in progress)')
    parser.add_argument('--debug', dest='debug', action='store_true',
        help='Debug')
    args = parser.parse_args()
    main(args)






