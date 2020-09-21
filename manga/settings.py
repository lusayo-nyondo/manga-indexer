import os, sys

APPLICATION_ROOT = os.path.dirname(os.path.abspath(__file__))
MANGA_DOWNLOAD_ROOT = os.path.join(APPLICATION_ROOT, 'data/manga')
LOG_ROOT = os.path.join(APPLICATION_ROOT, 'logs')

sys.path.append(APPLICATION_ROOT)

if not os.path.exists(MANGA_DOWNLOAD_ROOT):
    os.makedirs(MANGA_DOWNLOAD_ROOT)

if not os.path.exists(LOG_ROOT):
    os.makedirs(LOG_ROOT)

