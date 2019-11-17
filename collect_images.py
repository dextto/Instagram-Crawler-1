import os
import shutil

from docopt import docopt


def collect(name, followers):
    root = f'./data/{name}'
    image_dir = f'./data/{name}_{followers}'
    if not os.path.isdir(image_dir):
        os.mkdir(image_dir)

    cnt = 1
    for d in os.listdir(root):
        with open(f'{root}/{d}/info.txt') as f:
            f.readline()
            likes = f.readline().replace(',', '').replace('\n', '')
        _cnt = str('%06d' % cnt)
        shutil.copy(f'{root}/{d}/image.jpg', f'{image_dir}/{_cnt}_{likes}.jpg')
        cnt = cnt + 1


def main():
    args = docopt("""
        Usage:
            crawl.py [-q QUERY] [-f FOLLOWERS]

        Options:
            -q QUERY  username, add '#' to search for hashtags, e.g. 'username' or '#hashtag'
                      For multiple query seperate with comma, e.g. 'username1, username2, #hashtag'
            -f FOLLOWERS    followers
        """)
    query = args.get('-q', '')
    followers = args.get('-f', 0)
    collect(query, followers)


main()
