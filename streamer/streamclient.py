# coding=utf-8
"""
Test client for the streamer
"""
import logging
from datetime import datetime
from streamer import Streamer
from utils import get_kw_from_file


logging.basicConfig(filename="../logs/twcrawl_log_%s.log" % datetime.now().strftime("%Y%m%d_%H%M"),
    format='%(asctime)-15s %(levelname)s : %(message)s',
    level=logging.INFO)

streamer = Streamer()
streamer.main(language="tr", track=get_kw_from_file())



