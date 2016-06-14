# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# Copyright 2016 Florian Bruhin (The Compiler) <mail@qutebrowser.org>
#
# This file is part of qutebrowser.
#
# qutebrowser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# qutebrowser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with qutebrowser.  If not, see <http://www.gnu.org/licenses/>.

"""Wrapper over a QWebEngineView."""

from PyQt5.QtCore import pyqtSlot

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
except ImportError:
    QWebEngineView = None
    QWebEnginePage = None

from qutebrowser.browser import tab
from qutebrowser.utils import usertypes, qtutils


class WebEngineScroller(tab.AbstractScroller):

    ## TODO

    pass


class WebEngineHistory(tab.AbstractHistory):

    def __iter__(self):
        return iter(self.history.items())

    def current_idx(self):
        return self.history.currentItemIndex()

    def back(self):
        self.history.back()

    def forward(self):
        self.history.forward()

    def can_go_back(self):
        return self.history.canGoBack()

    def can_go_forward(self):
        return self.history.canGoForward()

    def serialize(self):
        return qtutils.serialize(self.history)

    def deserialize(self, data):
        return qtutils.deserialize(data, self.history)

    def load_items(self, items):
        # TODO
        raise NotImplementedError


class WebEngineViewTab(tab.AbstractTab):

    def __init__(self, win_id, parent=None):
        super().__init__(win_id)
        widget = QWebEngineView()
        self.history = WebEngineHistory(self)
        self.scroll = WebEngineScroller(parent=self)
        self._set_widget(widget)
        self._connect_signals()

    def openurl(self, url):
        self._widget.load(url)

    @property
    def cur_url(self):
        return self._widget.url()

    @property
    def progress(self):
        return 0  # FIXME:refactor

    @property
    def load_status(self):
        return usertypes.LoadStatus.success

    def set_zoom_factor(self, factor):
        self._widget.setZoomFactor(factor)

    def zoom_factor(self):
        return self._widget.zoomFactor()

    def dump_async(self, callback=None, *, plain=False):
        if plain:
            self._widget.page().toPlainText(callback)
        else:
            self._widget.page().toHtml(callback)

    def shutdown(self):
        # TODO
        pass

    def reload(self, *, force=False):
        if force:
            action = QWebEnginePage.ReloadAndBypassCache
        else:
            action = QWebEnginePage.Reload
        self._widget.triggerPageAction(action)

    def stop(self):
        self._widget.stop()

    def title(self):
        return self._widget.title()

    def icon(self):
        return self._widget.icon()

    def _connect_signals(self):
        view = self._widget
        page = view.page()
        page.windowCloseRequested.connect(self.window_close_requested)
        page.linkHovered.connect(self.link_hovered)
        page.loadProgress.connect(self.load_progress)
        page.loadStarted.connect(self.load_started)
        view.titleChanged.connect(self.title_changed)
        page.loadFinished.connect(self.load_finished)
        # FIXME:refactor
        # view.iconChanged.connect(self.icon_changed)
        # view.scroll.pos_changed.connect(self.scroll.perc_changed)
        # view.url_text_changed.connect(self.url_text_changed)
        # view.load_status_changed.connect(self.load_status_changed)