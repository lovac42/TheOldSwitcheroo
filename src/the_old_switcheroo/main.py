# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import re, os
from aqt import mw
from aqt.qt import *
from anki.hooks import addHook

from .callback import Callback
from .utils import cacheImg
from .const import *


class Switcheroo:
    tiffCB=Callback()

    def __init__(self):
        addHook("mungeQA", self.inline_media)
        addHook("showQuestion", self.onShowQuestion)

        if CCBC:
            self.addCallback=mw.reviewer.web.page().mainFrame().addToJavaScriptWindowObject
        else:
            self.addCallback=mw.reviewer.web.page()._channel.registerObject
            self.insert=mw.reviewer.web.page().profile().scripts().insert
            mw.addonManager._webExports[MOD_DIR] = '.*\.png$'


    def onShowQuestion(self):
        self.addCallback("tiffcmd", self.tiffCB)
        if not CCBC:
            js = QFile(':/qtwebchannel/qwebchannel.js')
            assert js.open(QIODevice.ReadOnly)
            js = bytes(js.readAll()).decode('utf-8')

            script=QWebEngineScript()
            script.setInjectionPoint(QWebEngineScript.DocumentCreation)
            script.setWorldId(QWebEngineScript.MainWorld)
            script.setName("qwebchannel.js");
            script.setRunsOnSubFrames(False)

            # TODO: fix channel error
            # Uncaught TypeError: channel.execCallbacks[message.id]
            # is not a function
            script.setSourceCode(js+'''
var tiffcmd;
var update;
new QWebChannel(qt.webChannelTransport, function(channel) {
    try{
        tiffcmd=channel.objects.tiffcmd;
        update=channel.objects.tiffcmd.update;
    }catch(TypeError){;}
});
        ''')
            self.insert(script)


    def inline_media(self, html, *args, **kwargs):
        def subEmbedTag(r):
            tif=r.group(2)
            png,_=cacheImg(tif,0)
            if not png:
                return r.group(0)
            return r.group(1) + r.group(3) + u"""\
onmousedown="handleTIFF(event,this);" \
src="%s" data-src="%s" data-pg="0">\
"""%(png,tif)

        html=RE_MEDIA.sub(subEmbedTag,html)
        return html + """<script>
function handleTIFF(e,el){
  src=$(el).attr('data-src');
  pg=$(el).attr('data-pg');
  if(e.shiftKey){
    pg=parseInt(prompt("Jump to page:",pg));
    if(isNaN(pg)) return;
  }else{
    pg++;
  }
  tiffcmd.update(src,pg);
  return false;
}
function updateTIFF(src,png,pg){
  el=$("[data-src='"+src+"']");
  el.attr('src',png).attr('data-pg',pg);
}
</script>"""
