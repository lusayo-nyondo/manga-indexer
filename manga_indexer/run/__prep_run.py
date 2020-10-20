import os, datetime
from pathlib import Path

from manga_indexer.settings import DATA_ROOT

def prep_filesystem(args, site):
    process_instance = str(
        datetime.datetime.utcnow().timestamp()
    )

    site_dir = os.path.join(
        DATA_ROOT,
        site['sitename']
    )

    data_dir = os.path.join(
        site_dir,
        process_instance
    )

    job_dir = __get_job_dir(data_dir, args)
    scrapy_log = __get_scrapy_log(job_dir)

    event_log = __get_event_log(data_dir, args)
    process_log = __get_process_log(data_dir, args)
    output_file = __get_output_file(data_dir, args)

    for file in ( scrapy_log, event_log, process_log, output_file ):
        if not os.path.exists(
            os.path.abspath(
                os.path.dirname(file)
            )
        ):
            os.makedirs(
                os.path.dirname(file)
            )
    
    Path(scrapy_log).touch()

    return process_log, event_log, output_file, job_dir, scrapy_log

def __get_job_dir(data_dir, args):
    if args.crawl_dir:
        return args.crawl_dir
    else:
        return os.path.join(
            data_dir,
            'scrapy_job'
        )

def __get_event_log(data_dir, args):
    if args.log_file:
        return args.log_file
    else: return os.path.join(
            data_dir,
            'events.log'
        )

def __get_scrapy_log(job_dir):
    return os.path.join(
        job_dir,
        'scrapy_proc.log'
    )

def __get_output_file(data_dir, args):
    rawpath = None

    if args.output:
        rawpath = args.output
    else:
        rawpath = os.path.join(
            data_dir,
            'index'
        )

    base_filename = os.path.basename(rawpath)
    dirname = os.path.dirname(
        os.path.abspath(rawpath)
    )

    output_format = args.format

    if len(base_filename.split('.')) == 1:
        formatted_filename = '{base_filename}.{output_format}'.format(
            base_filename=base_filename,
            output_format=output_format
        )

    return os.path.join(
        dirname,
        formatted_filename
    )

def __get_process_log(data_dir, args):
    return os.path.join(
        data_dir,
        'proc.log'
    )

def __prep_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

