#!/usr/bin/python -SO
import sys,runpy
sys.path.insert(0,"tron-win32-support.zip")
globals().update(runpy.run_module("tron",run_name=__name__))
