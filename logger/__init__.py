#coding=utf-8
import logging
import logging.config
import os
 
logging.config.fileConfig(os.path.abspath(os.path.dirname(__file__)) + "/logging.conf")
logger = logging.getLogger("main")