# coding=utf-8
"""
Test client for the streamer
"""
from streamer import Streamer

streamer = Streamer()
streamer.main(language="tr", track="ankara, istanbul, gezi, AKP, CHP, siyaset, hatay, diren, antakya, armutlu, polis,"
                                   "adliye, bakan, tayyip")


