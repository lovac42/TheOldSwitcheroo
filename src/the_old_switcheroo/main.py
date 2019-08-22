# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re, os, random
from aqt import mw
from aqt.qt import *
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
# Can't attach callback to previewer on Answer side for CCBC.
# Or when "show both sides" is selected for 2.1.
# Can't get instance of clayout to attach a callback/js script

    def onPrepareQA(self, txt, card, state):
        if state.endswith("Question"):
            getPage=self._getInitPageNum
        else:
            getPage=self._getSavedPageNum
        txt=self.inline_media(txt,getPage)
        if self.replaced and state.endswith("Question"):
            self.tiffCB.attachCallback(state)
        return txt


    def _getSavedPageNum(self, tif, group):
        return self.tiffCB.dict.get(tif,0)

    def _getInitPageNum(self, tif, group):
        search=RE_TARGET.search(group)
        if search:
            pg=int(search.group(1))
            self.tiffCB.dict[tif]=pg
            return pg
        search=RE_RAND.search(group)
        if search:
            pg=random.randint(0,int(search.group(1)))
            self.tiffCB.dict[tif]=pg
            return pg
        return 0


    def inline_media(self, html, getPage):
        def subEmbedTag(r):
            tif=r.group(2)
            pg=getPage(tif,r.group(0))
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

