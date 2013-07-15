import logging
import traceback

def get_kw_from_file():
    tracks=[]
    try:
        fo = open("./.tracklist", "r")
        for t in fo:
            tracks.append(t.strip())
        return ",".join(tracks)
    except IOError:
        logging.getLogger(__name__).error("Encountered IOError while loading tracklist")
        logging.getLogger(__name__).error("Printing stacktrace: %s" % traceback.format_exc())





