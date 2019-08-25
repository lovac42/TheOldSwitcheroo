# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from anki.hooks import addHook
from .utils import cacheImg
from .const import CCBC


class Callback(QObject):
    dict={}

    def __init__(self):
        QObject.__init__(self)
        addHook("browser.setupMenus", self._setBrowser)
        addHook("showAnswer", self._clearData)
        addHook('beforeStateChange', self._clearData)

    def _setBrowser(self, bws):
        "Save ref to browser instance"
        self.browser=bws

    def _clearData(self, *args):
        self.dict={}

    def _getWeb(self, parent):
        if parent.startswith("review"):
            return mw.web
        if parent.startswith("preview"):
            return self.browser._previewWeb


    def attachCallback(self, state):
        web=self._getWeb(state)
        if not web:
            return
        web.eval('var tiffParentFrame="%s";'%state)
        if CCBC:
            web.page().mainFrame().addToJavaScriptWindowObject("tiffcmd", self)
        else:
            web.page()._channel.registerObject("tiffcmd", self)
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
            web.page().profile().scripts().insert(script)


    @pyqtSlot(str, int, str)
    def update(self, src, pg, parent):
        png,pg=cacheImg(src,pg)
        if not png:
            return
        web=self._getWeb(parent)
        if not web:
            return
        web.eval('updateTIFF("%s","%s","%s");'%(src,png,pg))
        self.dict[src]=int(pg)
