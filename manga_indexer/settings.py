import os, sys

APPLICATION_ROOT = os.path.dirname(os.path.abspath(__file__))

DATA_ROOT = os.path.join(
    APPLICATION_ROOT,
    'data'
)

SUPPORT_ROOT = os.path.join(
    APPLICATION_ROOT,
    'support'
)

MANGA_DOWNLOAD_ROOT = DATA_ROOT
CRAWLING_PROCESS_ROOT = DATA_ROOT
LOG_ROOT = DATA_ROOT

sys.path.append(APPLICATION_ROOT)