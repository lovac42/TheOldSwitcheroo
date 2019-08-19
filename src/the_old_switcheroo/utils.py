# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import os
from aqt import mw
from .const import *

from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


def cacheImg(src, pg):
    f=os.path.join(mw.col.media.dir(),src)
    if os.path.exists(f):
        try:
            img=Image.open(f)
        except OSError as e:
            print(e)
        else:
            if img.format=='TIFF':
                try:
                    img.seek(pg)
                except EOFError:
                    pg=0
                    img.seek(0)
                fn=src+'_%d.png'%pg
                fp=os.path.join(CACHE_DIR,fn)
                if not os.path.exists(fp):
                    img.save(fp,'png')

                if CCBC:
                    return 'file:///'+fp.replace('\\','/'), pg
                return webBundlePath(fn), pg
    return "",0


def webBundlePath(path):
    return "http://127.0.0.1:%d/_addons/%s/.cache/%s"%(
            mw.mediaServer.getPort(),MOD_DIR,path)
