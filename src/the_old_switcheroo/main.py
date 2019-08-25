# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re, os, random
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from anki.hooks import addHook

from .callback import Callback
from .utils import cacheImg
from .const import *


class Switcheroo:
    tiffCB=Callback()
    replaced=0

    def __init__(self):
        addHook("prepareQA", self.onPrepareQA)
        if not CCBC:
            mw.addonManager._webExports[MOD_DIR] = '.*\.png$'


# TODO: Known Bugs
# Can't get instance of clayout to attach a callback/js script


    def onPrepareQA(self, txt, card, state):
        txt=self.inline_media(txt)
        if not CCBC or state.startswith("review"):
            #qt5 requires CB tobe attached before initialization on Q side
            self.tiffCB.attachCallback(state)
        else:
            #qt4 and previewer requires timer
            mw.progress.timer(10,lambda:self.tiffCB.attachCallback(state),False)
        return txt


    def _testErrors(self, tif, attr):
        mal=RE_MAL_PG.search(attr)
        if mal:
            showInfo("Malformed: Please remove 'data-pg' attribute in image tag")
            return True
        mal=RE_MAL_SRC.search(attr)
        if mal:
            showInfo("Malformed: Please remove 'data-src' attribute in image tag")
            return True


    def _getPageNum(self, tif, attr):
        saved=self.tiffCB.dict.get(tif,-1)
        if saved>-1:
            return saved
        target=RE_TARGET.search(attr)
        if target:
            return int(target.group(1))
        search=RE_RAND.search(attr)
        if search:
            pg=int(search.group(1))
            return random.randint(0,pg)
        return 0


    def inline_media(self, html):
        def subEmbedTag(r):
            tif=r.group(2)
            self._testErrors(tif,r.group(0))
            pg=self._getPageNum(tif,r.group(0))
            self.tiffCB.dict[tif]=pg
            png,_=cacheImg(tif,pg)
            if not png:
                return r.group(0)
            return r.group(1) + r.group(3) + u"""\
onmousedown="handleTIFF(event,this);" \
src="%s" data-src="%s" data-pg="%s">\
"""%(png,tif,pg)

        s,cnt=RE_MEDIA.subn(subEmbedTag,html)
        self.replaced=cnt
        if not cnt:
            return html
        return s + """<script>
function handleTIFF(e,el){
  el=$(el);
  src=el.attr('data-src');
  pg=el.attr('data-pg');
  r=el.attr('data-rand');
  if(e.shiftKey){
    pg=parseInt(prompt("Jump to page: (0-based)",pg));
    if(isNaN(pg)) return;
  }else if(r){
    pg=Math.random()*r;
  }else{
    pg++;
  }
  tiffcmd.update(src,pg,tiffParentFrame);
  return false;
}
function updateTIFF(src,png,pg){
  el=$("[data-src='"+src+"']");
  el.attr('src',png).attr('data-pg',pg);
}
</script>"""

