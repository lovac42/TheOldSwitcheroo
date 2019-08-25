# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re, os
from anki import version
CCBC=version.endswith("ccbc")


MOD_ABS,_ = os.path.split(__file__)
MOD_DIR = os.path.basename(MOD_ABS)

CACHE_DIR = os.path.join(MOD_ABS,".cache")
os.makedirs(CACHE_DIR,exist_ok=True)

RE_MEDIA=re.compile(r"""(\<img .*)src=['"](.*?\.tiff?)['"](.*?)/?\>""", re.I)

RE_RAND=re.compile(r'''data-rand=['"](\d+)['"]''',re.I)

RE_TARGET=re.compile(r'''data-target=['"](\d+)['"]''',re.I)

RE_MAL_PG=re.compile(r'''data-pg=['"](\d+)['"]''',re.I)

RE_MAL_SRC=re.compile(r'''data-src=['"].*?['"]''',re.I)
