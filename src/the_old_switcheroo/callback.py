# -*- coding: utf-8 -*-
# Copyright: (C) 2019 Lovac42
# Support: https://github.com/lovac42/TheOldSwitcheroo
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.qt import *
from .utils import cacheImg


class Callback(QObject):
    @pyqtSlot(str, int)
    def update(self, src, pg):
        png,pg=cacheImg(src,pg)
        if not png:
            return
        mw.web.eval('updateTIFF("%s","%s","%s");'%(src,png,pg))
