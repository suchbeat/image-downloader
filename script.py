from gevent import monkey; monkey.patch_all()
import argparse
import gevent
import gevent.pool
import logging
import os
import requests


def download_image(url, dir_name):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            f = open(os.path.join(dir_name, url.split('/')[-1]), 'w')
            f.write(response.content)
            f.close()
        else:
            logging.debug('Unsucessful download for %s. Status code: %s. '
                          'Reason: %s', (url,
                                         response.status_code,
                                         response.reason))
    except Exception:
        logging.exception('Failed download for %s' % url)


def main():
    parser = argparse.ArgumentParser(
        description='Image downloader.')
    parser.add_argument('-f', '--file',
                        metavar='INPUT_FILE', required=True,
                        help='Path to input file with image links')
    parser.add_argument('-d', '--dir',
                        metavar='DIR', required=True,
                        help='Download directory')
    args = parser.parse_args()

    urls = [url.rstrip('\n') for url in open(args.file) if url != '\n']

    pool = gevent.pool.Pool(2)
    [pool.spawn(download_image, url, args.dir) for url in urls]
    pool.join()

if __name__ == '__main__':
    main()
