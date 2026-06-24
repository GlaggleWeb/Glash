#!/usr/bin/env python3
"""
Glash Browser 2.0 — by Glaggle
A modern glassmorphism browser with Glaggle Blue design.
Homepage: glaggle.ch | Search: Google
"""

import sys
import os
import json
from datetime import datetime
from urllib.parse import quote_plus

from PyQt6.QtCore import (
    Qt, QUrl, QTimer, QSize, pyqtSignal, QObject,
    QPropertyAnimation, QEasingCurve, QPoint, QRect,
    QAbstractTableModel, QSortFilterProxyModel, QModelIndex
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTabWidget, QTabBar, QLabel, QToolBar,
    QStatusBar, QMenu, QMenuBar, QDialog, QListWidget, QListWidgetItem,
    QSplitter, QFrame, QScrollArea, QTextEdit, QCheckBox, QSlider,
    QComboBox, QMessageBox, QProgressBar, QSizePolicy, QGraphicsOpacityEffect,
    QStackedWidget, QToolButton, QInputDialog, QTableWidget, QTableWidgetItem,
    QHeaderView, QGroupBox, QRadioButton, QSpinBox, QSystemTrayIcon,
    QStyle, QTreeWidget, QTreeWidgetItem, QSplashScreen
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEnginePage, QWebEngineSettings,
    QWebEngineDownloadRequest, QWebEngineScript, QWebEngineCertificateError
)
from PyQt6.QtGui import (
    QIcon, QPixmap, QColor, QPalette, QFont, QAction,
    QLinearGradient, QPainter, QBrush, QPen, QCursor,
    QKeySequence, QShortcut, QFontDatabase, QGradient,
    QGuiApplication, QPainterPath
)
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog

# ─────────────────────────────────────────────
#  GLAGGLE DESIGN TOKENS
# ─────────────────────────────────────────────
GLAGGLE_BLUE       = "#70C4F7"
GLAGGLE_BLUE_DARK  = "#2E94D1"
GLAGGLE_BLUE_MID   = "#4AAEE8"
GLAGGLE_BG_LIGHT   = "#EBF6FE"
GLAGGLE_BG_MID     = "#D4ECFB"
GLAGGLE_BG_DARK    = "#C2E3F8"
GLAGGLE_GREEN      = "#34A853"
GLAGGLE_RED        = "#EA4335"
GLAGGLE_YELLOW     = "#FBBC05"
HOME_URL           = "https://glaggle.ch"
APP_NAME           = "Glash"
VERSION            = "2.0.0"

# ─────────────────────────────────────────────
#  STYLESHEET  (Glaggle Design System)
# ─────────────────────────────────────────────
STYLESHEET = """
/* ── Global ── */
* { box-sizing: border-box; }

QMainWindow, QWidget {
    background: transparent;
    color: #1a1a2e;
    font-family: -apple-system, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 14px;
}

/* ── Central Widget Gradient ── */
#centralWidget {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:1,
        stop:0 #EBF6FE, stop:0.45 #D4ECFB, stop:1 #C2E3F8
    );
}

/* ── Main Chrome Frame ── */
#chromeFrame {
    background: rgba(255,255,255,0.88);
    border-bottom: 1px solid rgba(112,196,247,0.3);
}

/* ── Tab Bar Strip ── */
#tabStrip {
    background: rgba(240,250,255,0.85);
    border-bottom: 1px solid rgba(112,196,247,0.25);
    min-height: 40px;
    max-height: 40px;
}

/* ── Navigation Bar ── */
#navBar {
    background: rgba(255,255,255,0.96);
    border-bottom: 1px solid rgba(112,196,247,0.3);
    min-height: 52px;
    max-height: 52px;
}

/* ── URL Bar ── */
#urlBar {
    background: rgba(255,255,255,0.9);
    border: 1.5px solid rgba(112,196,247,0.45);
    border-radius: 20px;
    padding: 5px 16px;
    font-size: 14px;
    color: #1a1a2e;
    selection-background-color: #70C4F7;
}
#urlBar:focus {
    background: #FFFFFF;
    border: 2px solid #70C4F7;
    outline: none;
}
#urlBar:hover:!focus {
    border: 1.5px solid #70C4F7;
    background: #FFFFFF;
}

/* ── Nav Buttons ── */
#navBtn {
    background: transparent;
    border: none;
    border-radius: 16px;
    color: #2E94D1;
    font-size: 17px;
    font-weight: 600;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0;
}
#navBtn:hover  { background: rgba(112,196,247,0.2); }
#navBtn:pressed{ background: rgba(112,196,247,0.4); }
#navBtn:disabled { color: rgba(112,196,247,0.35); }

/* ── Action Buttons ── */
#actionBtn {
    background: transparent;
    border: none;
    border-radius: 16px;
    color: #2E94D1;
    font-size: 15px;
    min-width: 34px; max-width: 34px;
    min-height: 34px; max-height: 34px;
    padding: 0;
}
#actionBtn:hover  { background: rgba(112,196,247,0.22); }
#actionBtn:pressed{ background: rgba(112,196,247,0.42); }

/* Bookmarked star */
#actionBtn[bookmarked="true"] {
    color: #F4A400;
}

/* ── Tab Widget ── */
QTabWidget::pane { border: none; background: transparent; }
QTabBar {
    background: rgba(240,250,255,0.85);
}
QTabBar::tab {
    background: rgba(255,255,255,0.45);
    color: #666;
    border: none;
    border-right: 1px solid rgba(112,196,247,0.15);
    padding: 7px 36px 7px 14px;
    min-width: 130px;
    max-width: 210px;
    font-size: 13px;
}
QTabBar::tab:selected {
    background: rgba(255,255,255,0.92);
    color: #1a1a2e;
    border-bottom: 2.5px solid #70C4F7;
    font-weight: 600;
}
QTabBar::tab:hover:!selected {
    background: rgba(112,196,247,0.14);
    color: #2E94D1;
}
QTabBar::tab[private="true"] {
    background: rgba(100,60,160,0.15);
    color: #8B5CF6;
}
QTabBar::tab[private="true"]:selected {
    background: rgba(139,92,246,0.18);
    border-bottom: 2.5px solid #8B5CF6;
    color: #7C3AED;
}
QTabBar::close-button {
    image: none;
    subcontrol-position: right;
    subcontrol-origin: padding;
    width: 14px; height: 14px;
    border-radius: 7px;
    background: rgba(200,200,200,0.5);
    margin-right: 4px;
}
QTabBar::close-button:hover { background: rgba(234,67,53,0.8); }

/* ── New Tab Button ── */
#newTabBtn {
    background: rgba(255,255,255,0.55);
    border: 1px solid rgba(112,196,247,0.3);
    border-radius: 13px;
    color: #2E94D1;
    font-size: 18px;
    font-weight: 300;
    min-width: 26px; max-width: 26px;
    min-height: 26px; max-height: 26px;
    padding: 0;
    margin: 5px 4px;
}
#newTabBtn:hover {
    background: rgba(112,196,247,0.35);
    border: 1px solid #70C4F7;
}

/* ── Progress Bar ── */
QProgressBar {
    border: none;
    background: transparent;
    max-height: 2px; min-height: 2px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #70C4F7, stop:0.5 #4AAEE8, stop:1 #2E94D1);
    border-radius: 1px;
}

/* ── Status Bar ── */
QStatusBar {
    background: rgba(255,255,255,0.75);
    color: #666;
    font-size: 11px;
    border-top: 1px solid rgba(112,196,247,0.2);
    min-height: 18px; max-height: 18px;
}

/* ── Menu Bar ── */
QMenuBar {
    background: rgba(255,255,255,0.97);
    color: #1a1a2e;
    border-bottom: 1px solid rgba(112,196,247,0.2);
    font-size: 13px;
    min-height: 22px; max-height: 22px;
    padding: 0 4px;
}
QMenuBar::item {
    padding: 3px 10px;
    border-radius: 4px;
}
QMenuBar::item:selected { background: rgba(112,196,247,0.22); }
QMenuBar::item:pressed  { background: rgba(112,196,247,0.4); }

/* ── Menus ── */
QMenu {
    background: rgba(248,253,255,0.98);
    border: 1px solid rgba(112,196,247,0.4);
    border-radius: 10px;
    padding: 5px 3px;
    font-size: 13px;
}
QMenu::item {
    padding: 6px 22px 6px 14px;
    border-radius: 6px;
    margin: 1px 3px;
    color: #1a1a2e;
}
QMenu::item:selected { background: rgba(112,196,247,0.25); }
QMenu::item:disabled { color: #aaa; }
QMenu::separator {
    height: 1px;
    background: rgba(112,196,247,0.2);
    margin: 4px 10px;
}
QMenu::indicator { width: 16px; height: 16px; }

/* ── Dialogs ── */
QDialog {
    background: rgba(238,250,255,0.98);
    border-radius: 14px;
}
QDialog QLabel { color: #1a1a2e; font-size: 13px; }

/* ── List Widgets ── */
QListWidget {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(112,196,247,0.3);
    border-radius: 10px;
    color: #1a1a2e;
    font-size: 13px;
    padding: 4px;
    outline: none;
}
QListWidget::item {
    padding: 8px 12px;
    border-radius: 7px;
    margin: 1px 2px;
}
QListWidget::item:selected { background: rgba(112,196,247,0.28); color: #1a1a2e; }
QListWidget::item:hover:!selected { background: rgba(112,196,247,0.12); }

/* ── Scrollbars ── */
QScrollBar:vertical {
    background: transparent; width: 8px; border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: rgba(112,196,247,0.5); border-radius: 4px; min-height: 30px;
}
QScrollBar::handle:vertical:hover { background: rgba(112,196,247,0.8); }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal {
    background: transparent; height: 8px; border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: rgba(112,196,247,0.5); border-radius: 4px; min-width: 30px;
}
QScrollBar::handle:horizontal:hover { background: rgba(112,196,247,0.8); }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Input Fields ── */
QLineEdit, QTextEdit {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(112,196,247,0.4);
    border-radius: 8px;
    padding: 6px 10px;
    color: #1a1a2e;
    font-size: 13px;
}
QLineEdit:focus, QTextEdit:focus {
    border: 1.5px solid #70C4F7;
    background: #FFFFFF;
}

/* ── Buttons ── */
QPushButton {
    background: rgba(112,196,247,0.18);
    border: 1px solid rgba(112,196,247,0.5);
    border-radius: 8px;
    color: #1a3a5c;
    font-size: 13px;
    font-weight: 600;
    padding: 7px 18px;
}
QPushButton:hover   { background: rgba(112,196,247,0.38); border: 1px solid #70C4F7; }
QPushButton:pressed { background: rgba(46,148,209,0.42); }
QPushButton#primaryBtn {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #70C4F7, stop:1 #2E94D1);
    color: white;
    border: none;
}
QPushButton#primaryBtn:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #5BB8F5, stop:1 #2580BE);
}
QPushButton#dangerBtn {
    background: rgba(234,67,53,0.12);
    border: 1px solid rgba(234,67,53,0.4);
    color: #c0392b;
}
QPushButton#dangerBtn:hover { background: rgba(234,67,53,0.25); }

/* ── Checkboxes ── */
QCheckBox { color: #1a1a2e; spacing: 6px; font-size: 13px; }
QCheckBox::indicator {
    width: 16px; height: 16px;
    border-radius: 4px;
    border: 1.5px solid rgba(112,196,247,0.6);
    background: rgba(255,255,255,0.8);
}
QCheckBox::indicator:checked {
    background: #70C4F7;
    border-color: #2E94D1;
    image: none;
}

/* ── Sliders ── */
QSlider::groove:horizontal {
    height: 4px;
    background: rgba(112,196,247,0.25);
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #70C4F7;
    border: none;
    width: 16px; height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}
QSlider::sub-page:horizontal { background: #70C4F7; border-radius: 2px; }

/* ── ComboBox ── */
QComboBox {
    background: rgba(255,255,255,0.85);
    border: 1px solid rgba(112,196,247,0.4);
    border-radius: 8px;
    padding: 5px 10px;
    color: #1a1a2e;
    font-size: 13px;
}
QComboBox:hover { border-color: #70C4F7; }
QComboBox::drop-down { border: none; width: 22px; }
QComboBox QAbstractItemView {
    background: rgba(248,253,255,0.98);
    border: 1px solid rgba(112,196,247,0.4);
    border-radius: 8px;
    selection-background-color: rgba(112,196,247,0.25);
    outline: none;
    padding: 4px;
}

/* ── Splitter ── */
QSplitter::handle {
    background: rgba(112,196,247,0.3);
    width: 2px;
}
QSplitter::handle:hover { background: #70C4F7; }

/* ── Dialog Title ── */
#dialogTitle {
    font-size: 16px;
    font-weight: 700;
    color: #1a3a5c;
}

/* ── Glass Cards ── */
#glassCard {
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(112,196,247,0.3);
    border-radius: 14px;
    padding: 14px;
}

/* ── Security Labels ── */
#secureLabel {
    color: #34A853; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 8px;
    background: rgba(52,168,83,0.1);
    border: 1px solid rgba(52,168,83,0.25);
}
#insecureLabel {
    color: #EA4335; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 8px;
    background: rgba(234,67,53,0.1);
    border: 1px solid rgba(234,67,53,0.25);
}
#localLabel {
    color: #666; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 8px;
    background: rgba(100,100,100,0.08);
    border: 1px solid rgba(100,100,100,0.2);
}
#privateLabel {
    color: #8B5CF6; font-size: 11px; font-weight: 600;
    padding: 2px 8px; border-radius: 8px;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.3);
}

/* ── Status / Info labels ── */
#zoomLabel, #readerModeLabel {
    color: #666; font-size: 11px;
    padding: 2px 8px; border-radius: 8px;
    background: rgba(255,255,255,0.7);
    border: 1px solid rgba(112,196,247,0.2);
}
#readerModeBtn[active="true"] {
    color: #34A853;
    background: rgba(52,168,83,0.12);
    border: 1px solid rgba(52,168,83,0.3);
}

/* ── Sidebar Panel ── */
#sidebarPanel {
    background: rgba(245,252,255,0.98);
    border-right: 1px solid rgba(112,196,247,0.25);
    min-width: 260px;
    max-width: 260px;
}
#sidebarPanel QLabel#panelTitle {
    font-size: 14px;
    font-weight: 700;
    color: #1a3a5c;
    padding: 4px 0;
}

/* ── Reader Mode ── */
#readerWidget {
    background: #FAFAFA;
    border-left: 1px solid rgba(112,196,247,0.2);
}
#readerTitle {
    font-size: 22px;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1.3;
}
#readerContent {
    background: #FAFAFA;
    border: none;
    color: #333;
    font-size: 16px;
    line-height: 1.75;
    selection-background-color: #70C4F7;
}

/* ── Download Item ── */
#downloadItem {
    background: rgba(255,255,255,0.8);
    border: 1px solid rgba(112,196,247,0.2);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 3px 0;
}
#downloadItem:hover {
    background: rgba(255,255,255,0.95);
    border-color: rgba(112,196,247,0.5);
}

/* ── Find Bar ── */
#findBar {
    background: rgba(255,255,255,0.97);
    border-bottom: 1px solid rgba(112,196,247,0.3);
    border-top: 1px solid rgba(112,196,247,0.1);
    padding: 5px 12px;
}

/* ── Table Widgets ── */
QTableWidget {
    background: rgba(255,255,255,0.75);
    border: 1px solid rgba(112,196,247,0.25);
    border-radius: 8px;
    gridline-color: rgba(112,196,247,0.15);
    selection-background-color: rgba(112,196,247,0.25);
    outline: none;
}
QTableWidget::item { padding: 6px 10px; }
QHeaderView::section {
    background: rgba(240,250,255,0.9);
    border: none;
    border-right: 1px solid rgba(112,196,247,0.2);
    border-bottom: 1px solid rgba(112,196,247,0.2);
    padding: 6px 10px;
    font-weight: 600;
    color: #1a3a5c;
}
QHeaderView::section:hover { background: rgba(112,196,247,0.15); }
"""

# ─────────────────────────────────────────────
#  DATA STORE
# ─────────────────────────────────────────────
class DataStore:
    def __init__(self):
        self.data_file = os.path.expanduser("~/.glash_v2_data.json")
        self.bookmarks: list[dict] = []
        self.history:   list[dict] = []
        self.downloads: list[dict] = []
        self.settings: dict = {
            "homepage":        HOME_URL,
            "search_engine":   "google",  # google | glaggle | bing | duckduckgo
            "zoom":            100,
            "js_enabled":      True,
            "block_popups":    True,
            "smooth_scroll":   True,
            "reader_font_size":18,
            "reader_font":     "Georgia",
            "sidebar_default": "none",
        }
        self.load()

    def load(self):
        try:
            with open(self.data_file, "r") as f:
                d = json.load(f)
                self.bookmarks = d.get("bookmarks", [])
                self.history   = d.get("history",   [])
                self.settings.update(d.get("settings", {}))
        except Exception:
            pass

    def save(self):
        try:
            with open(self.data_file, "w") as f:
                json.dump({
                    "bookmarks": self.bookmarks[-1000:],
                    "history":   self.history[-5000:],
                    "settings":  self.settings,
                }, f, indent=2)
        except Exception:
            pass

    def add_history(self, url: str, title: str):
        if url and not url.startswith("about:") and url != "about:blank":
            self.history.append({
                "url": url, "title": title,
                "time": datetime.now().isoformat()
            })
            if len(self.history) > 5000:
                self.history = self.history[-5000:]
            self.save()

    def add_bookmark(self, url: str, title: str, folder: str = ""):
        if not any(b["url"] == url for b in self.bookmarks):
            self.bookmarks.append({
                "url": url, "title": title, "folder": folder,
                "added": datetime.now().isoformat()
            })
            self.save()
            return True
        return False

    def remove_bookmark(self, url: str):
        self.bookmarks = [b for b in self.bookmarks if b["url"] != url]
        self.save()

    def is_bookmarked(self, url: str) -> bool:
        return any(b["url"] == url for b in self.bookmarks)

    def get_search_url(self, query: str) -> str:
        q = quote_plus(query)
        engines = {
            "google":    f"https://www.google.com/search?q={q}",
            "glaggle":   f"https://glaggle.ch/search?q={q}",
            "bing":      f"https://www.bing.com/search?q={q}",
            "duckduckgo":f"https://duckduckgo.com/?q={q}",
        }
        return engines.get(self.settings.get("search_engine", "google"),
                           f"https://www.google.com/search?q={q}")


STORE = DataStore()


# ─────────────────────────────────────────────
#  CUSTOM WEB PAGE
# ─────────────────────────────────────────────
class GlashWebPage(QWebEnginePage):
    new_tab_requested = pyqtSignal(QUrl)

    def __init__(self, profile, is_private=False, parent=None):
        super().__init__(profile, parent)
        self.is_private = is_private

    def createWindow(self, _type):
        temp = GlashWebPage(self.profile(), self.is_private, self.parent())
        temp.urlChanged.connect(lambda url: self.new_tab_requested.emit(url))
        return temp

    def javaScriptConsoleMessage(self, level, msg, line, src):
        pass

    def certificateError(self, error):
        return False  # Show errors normally


# ─────────────────────────────────────────────
#  BROWSER TAB
# ─────────────────────────────────────────────
class BrowserTab(QWebEngineView):
    title_updated   = pyqtSignal(str)
    url_updated     = pyqtSignal(QUrl)
    load_progress   = pyqtSignal(int)
    new_tab_url     = pyqtSignal(QUrl)
    favicon_updated = pyqtSignal(QIcon)
    reader_ready    = pyqtSignal(str, str)  # title, html

    def __init__(self, profile: QWebEngineProfile, is_private=False, parent=None):
        super().__init__(parent)
        self.is_private = is_private
        page = GlashWebPage(profile, is_private, self)
        page.new_tab_requested.connect(self.new_tab_url)
        self.setPage(page)

        self.titleChanged.connect(self.title_updated)
        self.urlChanged.connect(self.url_updated)
        self.loadProgress.connect(self.load_progress)
        self.iconChanged.connect(self.favicon_updated)
        self.loadStarted.connect(self._on_load_started)
        self.loadFinished.connect(self._on_load_finished)

        s = self.settings()
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.ScrollAnimatorEnabled, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.JavascriptCanOpenWindows, not STORE.settings.get("block_popups", True))
        s.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        s.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, not is_private)
        s.setAttribute(QWebEngineSettings.WebAttribute.WebGLEnabled, True)

        self._reader_mode = False

    def _on_load_started(self):
        pass

    def _on_load_finished(self, ok):
        pass

    def zoom_in(self):
        new = min(self.zoomFactor() + 0.1, 3.0)
        self.setZoomFactor(new)
        return int(new * 100)

    def zoom_out(self):
        new = max(self.zoomFactor() - 0.1, 0.25)
        self.setZoomFactor(new)
        return int(new * 100)

    def zoom_reset(self):
        self.setZoomFactor(1.0)
        return 100

    def extract_reader_content(self):
        """Extract readable content from the page."""
        js = """
        (function() {
            var title = document.title || '';
            var article = document.querySelector('article') ||
                          document.querySelector('main') ||
                          document.querySelector('[role="main"]') ||
                          document.querySelector('.post-content') ||
                          document.querySelector('.article-body') ||
                          document.querySelector('.entry-content') ||
                          document.body;
            var html = article ? article.innerHTML : document.body.innerHTML;
            return JSON.stringify({title: title, html: html});
        })();
        """
        self.page().runJavaScript(js, 0, self._reader_callback)

    def _reader_callback(self, result):
        if result:
            try:
                data = json.loads(result)
                self.reader_ready.emit(data.get("title", ""), data.get("html", ""))
            except Exception:
                pass

    def scroll_to_top(self):
        self.page().runJavaScript("window.scrollTo(0, 0);")

    def scroll_to_bottom(self):
        self.page().runJavaScript("window.scrollTo(0, document.body.scrollHeight);")


# ─────────────────────────────────────────────
#  FIND BAR
# ─────────────────────────────────────────────
class FindBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("findBar")
        self.setFixedHeight(44)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 6, 14, 6)
        layout.setSpacing(8)

        lbl = QLabel("🔍")
        lbl.setFixedWidth(22)
        layout.addWidget(lbl)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Text auf Seite suchen…")
        self.input.returnPressed.connect(self.find_next)
        self.input.textChanged.connect(self._on_text_changed)
        self.input.setFixedWidth(260)
        layout.addWidget(self.input)

        self.count_lbl = QLabel("")
        self.count_lbl.setObjectName("zoomLabel")
        self.count_lbl.setFixedWidth(70)
        layout.addWidget(self.count_lbl)

        self.case_cb = QCheckBox("Aa")
        self.case_cb.setToolTip("Groß-/Kleinschreibung")
        layout.addWidget(self.case_cb)

        prev_btn = QPushButton("↑")
        prev_btn.setFixedSize(28, 28)
        prev_btn.setToolTip("Vorheriger Treffer (Shift+Enter)")
        prev_btn.clicked.connect(self.find_prev)
        layout.addWidget(prev_btn)

        next_btn = QPushButton("↓")
        next_btn.setFixedSize(28, 28)
        next_btn.setToolTip("Nächster Treffer (Enter)")
        next_btn.clicked.connect(self.find_next)
        layout.addWidget(next_btn)

        layout.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.clicked.connect(self.hide_and_clear)
        layout.addWidget(close_btn)

        self.web_view = None
        self.hide()

    def _on_text_changed(self, text):
        if self.web_view and not text:
            self.web_view.findText("")
            self.count_lbl.setText("")

    def set_view(self, view):
        self.web_view = view

    def _flags(self):
        flags = QWebEnginePage.FindFlag(0)
        if self.case_cb.isChecked():
            flags |= QWebEnginePage.FindFlag.FindCaseSensitively
        return flags

    def find_next(self):
        if self.web_view and self.input.text():
            self.web_view.findText(self.input.text(), self._flags())

    def find_prev(self):
        if self.web_view and self.input.text():
            flags = self._flags() | QWebEnginePage.FindFlag.FindBackward
            self.web_view.findText(self.input.text(), flags)

    def show_and_focus(self):
        self.show()
        self.input.setFocus()
        self.input.selectAll()

    def hide_and_clear(self):
        if self.web_view:
            self.web_view.findText("")
        self.hide()


# ─────────────────────────────────────────────
#  READER MODE WIDGET
# ─────────────────────────────────────────────
class ReaderWidget(QWidget):
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("readerWidget")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Toolbar
        toolbar = QWidget()
        toolbar.setObjectName("navBar")
        toolbar.setFixedHeight(48)
        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(16, 6, 16, 6)
        tb_layout.setSpacing(8)

        title_lbl = QLabel("📖  Reader Mode")
        title_lbl.setObjectName("dialogTitle")
        tb_layout.addWidget(title_lbl)
        tb_layout.addStretch()

        # Font size
        tb_layout.addWidget(QLabel("Schrift:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(12, 32)
        self.font_size_spin.setValue(STORE.settings.get("reader_font_size", 18))
        self.font_size_spin.valueChanged.connect(self._update_style)
        tb_layout.addWidget(self.font_size_spin)

        # Font family
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Georgia", "Arial", "Times New Roman", "Helvetica", "Verdana"])
        saved_font = STORE.settings.get("reader_font", "Georgia")
        idx = self.font_combo.findText(saved_font)
        if idx >= 0:
            self.font_combo.setCurrentIndex(idx)
        self.font_combo.currentTextChanged.connect(self._update_style)
        tb_layout.addWidget(self.font_combo)

        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Hell", "Sepia", "Dunkel"])
        self.theme_combo.currentTextChanged.connect(self._update_style)
        tb_layout.addWidget(self.theme_combo)

        close_btn = QPushButton("✕ Schließen")
        close_btn.clicked.connect(self.closed.emit)
        tb_layout.addWidget(close_btn)

        layout.addWidget(toolbar)

        # Scrollable reader area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("readerWidget")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.content_widget = QWidget()
        self.content_widget.setObjectName("readerWidget")
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)

        # Inner container for max width
        inner = QWidget()
        inner.setObjectName("readerWidget")
        inner_layout = QVBoxLayout(inner)
        inner_layout.setContentsMargins(60, 40, 60, 60)
        inner_layout.setSpacing(20)

        self.title_label = QLabel("")
        self.title_label.setObjectName("readerTitle")
        self.title_label.setWordWrap(True)
        inner_layout.addWidget(self.title_label)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("background: rgba(112,196,247,0.4); max-height: 1px;")
        inner_layout.addWidget(separator)

        self.content_view = QTextEdit()
        self.content_view.setObjectName("readerContent")
        self.content_view.setReadOnly(True)
        self.content_view.setFrameStyle(QFrame.Shape.NoFrame)
        inner_layout.addWidget(self.content_view)

        content_layout.addWidget(inner)
        content_layout.addStretch()

        scroll.setWidget(self.content_widget)
        layout.addWidget(scroll)

        self._current_theme = "Hell"
        self._update_style()

    def load_content(self, title: str, html: str):
        self.title_label.setText(title)
        self.content_view.setHtml(self._clean_html(html))

    def _clean_html(self, html: str) -> str:
        # Remove scripts and styles for clean reading
        import re
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL|re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL|re.IGNORECASE)
        html = re.sub(r'<(nav|header|footer|aside|iframe|form|button)[^>]*>.*?</\1>', '', html, flags=re.DOTALL|re.IGNORECASE)
        return html

    def _update_style(self):
        theme = self.theme_combo.currentText()
        font = self.font_combo.currentText()
        size = self.font_size_spin.value()
        self._current_theme = theme

        themes = {
            "Hell":   ("#FAFAFA", "#222222"),
            "Sepia":  ("#F8F0E3", "#3B2F2F"),
            "Dunkel": ("#1E1E2E", "#E0E0E0"),
        }
        bg, fg = themes.get(theme, ("#FAFAFA", "#222222"))
        self.content_widget.setStyleSheet(f"background: {bg};")
        self.content_view.setStyleSheet(
            f"background: {bg}; color: {fg}; "
            f"font-family: '{font}'; font-size: {size}px; "
            f"line-height: 1.8; padding: 0;"
        )
        self.title_label.setStyleSheet(f"color: {fg}; font-size: {size + 8}px;")

        STORE.settings["reader_font_size"] = size
        STORE.settings["reader_font"] = font
        STORE.save()


# ─────────────────────────────────────────────
#  DOWNLOAD MANAGER DIALOG
# ─────────────────────────────────────────────
class DownloadDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Downloads — Glash")
        self.setMinimumSize(600, 420)
        self.setWindowFlags(Qt.WindowType.Sheet)
        self._build()
        self._refresh()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        header = QHBoxLayout()
        title = QLabel("⬇  Downloads")
        title.setObjectName("dialogTitle")
        header.addWidget(title)
        header.addStretch()
        clr_btn = QPushButton("🗑 Liste leeren")
        clr_btn.setObjectName("dangerBtn")
        clr_btn.clicked.connect(self._clear)
        header.addWidget(clr_btn)
        layout.addLayout(header)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Dateiname", "Ordner", "Grösse", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        layout.addWidget(self.table)

        btns = QHBoxLayout()
        open_folder_btn = QPushButton("📂 Downloads öffnen")
        open_folder_btn.clicked.connect(self._open_folder)
        btns.addWidget(open_folder_btn)
        btns.addStretch()
        close_btn = QPushButton("Schließen")
        close_btn.setObjectName("primaryBtn")
        close_btn.clicked.connect(self.close)
        btns.addWidget(close_btn)
        layout.addLayout(btns)

    def _refresh(self):
        self.table.setRowCount(0)
        for d in reversed(STORE.downloads):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(d.get("name", "")))
            self.table.setItem(row, 1, QTableWidgetItem(d.get("path", "")[:40]))
            size = d.get("size", 0)
            self.table.setItem(row, 2, QTableWidgetItem(
                f"{size/1024/1024:.1f} MB" if size > 1024*1024 else
                f"{size/1024:.0f} KB" if size > 1024 else f"{size} B"
            ))
            status_item = QTableWidgetItem(d.get("state", ""))
            if "Fertig" in d.get("state", ""):
                status_item.setForeground(QColor("#34A853"))
            elif "Fehler" in d.get("state", ""):
                status_item.setForeground(QColor("#EA4335"))
            self.table.setItem(row, 3, status_item)

    def _clear(self):
        STORE.downloads.clear()
        self._refresh()

    def _open_folder(self):
        import subprocess
        folder = os.path.expanduser("~/Downloads")
        try:
            if sys.platform == "darwin":
                subprocess.Popen(["open", folder])
            elif sys.platform.startswith("linux"):
                subprocess.Popen(["xdg-open", folder])
            elif sys.platform == "win32":
                os.startfile(folder)
        except Exception:
            pass


# ─────────────────────────────────────────────
#  HISTORY / BOOKMARKS DIALOG
# ─────────────────────────────────────────────
class SidePanelDialog(QDialog):
    navigate_to = pyqtSignal(str)

    def __init__(self, mode: str, parent=None):
        super().__init__(parent)
        self.mode = mode
        self.setWindowTitle("Lesezeichen" if mode == "bookmarks" else "Verlauf")
        self.setMinimumSize(560, 600)
        self.setWindowFlags(Qt.WindowType.Sheet)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 16)
        layout.setSpacing(12)

        title = QLabel("⭐  Lesezeichen" if self.mode == "bookmarks" else "🕐  Verlauf")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        search = QLineEdit()
        search.setPlaceholderText("Suchen…")
        search.textChanged.connect(self._filter)
        layout.addWidget(search)
        self.search_bar = search

        self.table = QTableWidget()
        if self.mode == "bookmarks":
            self.table.setColumnCount(2)
            self.table.setHorizontalHeaderLabels(["Titel", "URL"])
        else:
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(["Titel", "URL", "Zeit"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.doubleClicked.connect(self._open_selected)
        layout.addWidget(self.table)

        btns = QHBoxLayout()
        if self.mode == "bookmarks":
            del_btn = QPushButton("🗑 Entfernen")
            del_btn.setObjectName("dangerBtn")
            del_btn.clicked.connect(self._delete_item)
            btns.addWidget(del_btn)
        else:
            clr_btn = QPushButton("🗑 Verlauf löschen")
            clr_btn.setObjectName("dangerBtn")
            clr_btn.clicked.connect(self._clear_history)
            btns.addWidget(clr_btn)
        btns.addStretch()
        open_btn = QPushButton("↗ Öffnen")
        open_btn.setObjectName("primaryBtn")
        open_btn.clicked.connect(self._open_selected)
        btns.addWidget(open_btn)
        close_btn = QPushButton("Schließen")
        close_btn.clicked.connect(self.close)
        btns.addWidget(close_btn)
        layout.addLayout(btns)

        self._populate()

    def _populate(self, filter_text=""):
        self.table.setRowCount(0)
        items = STORE.bookmarks if self.mode == "bookmarks" else list(reversed(STORE.history))
        for item in items:
            title = item.get("title", "") or item.get("url", "")
            url   = item.get("url", "")
            if filter_text and filter_text.lower() not in title.lower() and \
               filter_text.lower() not in url.lower():
                continue
            row = self.table.rowCount()
            self.table.insertRow(row)
            t_item = QTableWidgetItem(title)
            t_item.setData(Qt.ItemDataRole.UserRole, url)
            self.table.setItem(row, 0, t_item)
            self.table.setItem(row, 1, QTableWidgetItem(url))
            if self.mode == "history":
                ts = item.get("time", "")
                if ts:
                    try:
                        dt = datetime.fromisoformat(ts)
                        self.table.setItem(row, 2, QTableWidgetItem(dt.strftime("%d.%m.%Y %H:%M")))
                    except Exception:
                        self.table.setItem(row, 2, QTableWidgetItem(ts))

    def _filter(self, text): self._populate(text)

    def _get_selected_url(self):
        row = self.table.currentRow()
        if row >= 0:
            item = self.table.item(row, 0)
            if item:
                return item.data(Qt.ItemDataRole.UserRole)
        return None

    def _open_selected(self):
        url = self._get_selected_url()
        if url:
            self.navigate_to.emit(url)
            self.close()

    def _delete_item(self):
        url = self._get_selected_url()
        if url:
            STORE.remove_bookmark(url)
            self._populate(self.search_bar.text())

    def _clear_history(self):
        if QMessageBox.question(
            self, "Verlauf löschen", "Gesamten Verlauf löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            STORE.history.clear()
            STORE.save()
            self._populate()


# ─────────────────────────────────────────────
#  SETTINGS DIALOG
# ─────────────────────────────────────────────
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Einstellungen — Glash")
        self.setMinimumSize(520, 560)
        self.setWindowFlags(Qt.WindowType.Sheet)
        self._build()

    def _build(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 22, 24, 18)
        layout.setSpacing(14)

        title = QLabel("⚙️  Einstellungen")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        # ── Allgemein ──
        gen_group = QGroupBox("Allgemein")
        gen_layout = QVBoxLayout(gen_group)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("Startseite:"))
        self.hp_edit = QLineEdit(STORE.settings.get("homepage", HOME_URL))
        row1.addWidget(self.hp_edit)
        gen_layout.addLayout(row1)

        row2 = QHBoxLayout()
        row2.addWidget(QLabel("Suchmaschine:"))
        self.engine_combo = QComboBox()
        engines = [("Google", "google"), ("Glaggle", "glaggle"),
                   ("Bing", "bing"), ("DuckDuckGo", "duckduckgo")]
        for name, key in engines:
            self.engine_combo.addItem(name, key)
        current = STORE.settings.get("search_engine", "google")
        for i, (_, k) in enumerate(engines):
            if k == current:
                self.engine_combo.setCurrentIndex(i)
        row2.addWidget(self.engine_combo)
        gen_layout.addLayout(row2)
        layout.addWidget(gen_group)

        # ── Anzeige ──
        disp_group = QGroupBox("Anzeige")
        disp_layout = QVBoxLayout(disp_group)

        zoom_row = QHBoxLayout()
        zoom_row.addWidget(QLabel("Standard-Zoom:"))
        self.zoom_slider = QSlider(Qt.Orientation.Horizontal)
        self.zoom_slider.setRange(50, 200)
        self.zoom_slider.setValue(STORE.settings.get("zoom", 100))
        self.zoom_lbl = QLabel(f"{self.zoom_slider.value()}%")
        self.zoom_lbl.setFixedWidth(42)
        self.zoom_slider.valueChanged.connect(lambda v: self.zoom_lbl.setText(f"{v}%"))
        zoom_row.addWidget(self.zoom_slider)
        zoom_row.addWidget(self.zoom_lbl)
        disp_layout.addLayout(zoom_row)
        layout.addWidget(disp_group)

        # ── Reader Mode ──
        reader_group = QGroupBox("Reader Mode")
        reader_layout = QVBoxLayout(reader_group)

        reader_font_row = QHBoxLayout()
        reader_font_row.addWidget(QLabel("Schrift:"))
        self.reader_font_combo = QComboBox()
        self.reader_font_combo.addItems(["Georgia", "Arial", "Times New Roman", "Helvetica", "Verdana"])
        saved_font = STORE.settings.get("reader_font", "Georgia")
        idx = self.reader_font_combo.findText(saved_font)
        if idx >= 0:
            self.reader_font_combo.setCurrentIndex(idx)
        reader_font_row.addWidget(self.reader_font_combo)
        reader_font_row.addWidget(QLabel("Größe:"))
        self.reader_size_spin = QSpinBox()
        self.reader_size_spin.setRange(12, 32)
        self.reader_size_spin.setValue(STORE.settings.get("reader_font_size", 18))
        reader_font_row.addWidget(self.reader_size_spin)
        reader_layout.addLayout(reader_font_row)
        layout.addWidget(reader_group)

        # ── Datenschutz ──
        priv_group = QGroupBox("Datenschutz & Sicherheit")
        priv_layout = QVBoxLayout(priv_group)
        self.popup_cb = QCheckBox("Pop-ups blockieren")
        self.popup_cb.setChecked(STORE.settings.get("block_popups", True))
        priv_layout.addWidget(self.popup_cb)
        self.js_cb = QCheckBox("JavaScript aktiviert")
        self.js_cb.setChecked(STORE.settings.get("js_enabled", True))
        priv_layout.addWidget(self.js_cb)
        layout.addWidget(priv_group)

        layout.addStretch()

        info = QLabel(
            f"<b>Glash</b> v{VERSION} — powered by Glaggle<br>"
            f"<small style='color:#888'>PyQt6 + Chromium WebEngine | © 2026 Glaggle Inc.</small>"
        )
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        btns = QHBoxLayout()
        save_btn = QPushButton("✅ Speichern")
        save_btn.setObjectName("primaryBtn")
        save_btn.clicked.connect(self._save)
        cancel_btn = QPushButton("Abbrechen")
        cancel_btn.clicked.connect(self.close)
        btns.addWidget(save_btn)
        btns.addWidget(cancel_btn)
        layout.addLayout(btns)

    def _save(self):
        STORE.settings["homepage"]        = self.hp_edit.text().strip() or HOME_URL
        STORE.settings["search_engine"]   = self.engine_combo.currentData()
        STORE.settings["zoom"]            = self.zoom_slider.value()
        STORE.settings["js_enabled"]      = self.js_cb.isChecked()
        STORE.settings["block_popups"]    = self.popup_cb.isChecked()
        STORE.settings["reader_font"]     = self.reader_font_combo.currentText()
        STORE.settings["reader_font_size"]= self.reader_size_spin.value()
        STORE.save()
        self.close()


# ─────────────────────────────────────────────
#  KEYBOARD SHORTCUTS HELP DIALOG
# ─────────────────────────────────────────────
class ShortcutsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tastenkürzel — Glash")
        self.setMinimumSize(480, 520)
        self.setWindowFlags(Qt.WindowType.Sheet)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 20, 22, 16)

        title = QLabel("⌨️  Tastenkürzel")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)

        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(["Aktion", "Kürzel"])
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)

        shortcuts = [
            ("Neuer Tab",           "Ctrl+T"),
            ("Tab schließen",       "Ctrl+W"),
            ("Nächster Tab",        "Ctrl+Tab"),
            ("Vorheriger Tab",      "Ctrl+Shift+Tab"),
            ("Neues Fenster",       "Ctrl+N"),
            ("Privater Tab",        "Ctrl+Shift+P"),
            ("URL-Leiste fokus",    "Ctrl+L"),
            ("Seite suchen",        "Ctrl+F"),
            ("Neu laden",           "Ctrl+R"),
            ("Hard Reload",         "Ctrl+Shift+R"),
            ("Zurück",              "Alt+← / Ctrl+["),
            ("Vorwärts",            "Alt+→ / Ctrl+]"),
            ("Startseite",          "Ctrl+H"),
            ("Lesezeichen",         "Ctrl+D"),
            ("Verlauf",             "Ctrl+Shift+H"),
            ("Reader Mode",         "Ctrl+Shift+R"),
            ("Vergrößern",          "Ctrl++"),
            ("Verkleinern",         "Ctrl+-"),
            ("Zoom zurücksetzen",   "Ctrl+0"),
            ("Vollbild",            "F11"),
            ("DevTools",            "F12"),
            ("Downloads",           "Ctrl+Shift+J"),
            ("Einstellungen",       "Ctrl+,"),
            ("Seite drucken",       "Ctrl+P"),
            ("Seite speichern",     "Ctrl+S"),
            ("Seitenquelltext",     "Ctrl+U"),
            ("Nach oben",           "Ctrl+↑"),
            ("Nach unten",          "Ctrl+↓"),
            ("Glash beenden",       "Ctrl+Q"),
        ]
        table.setRowCount(len(shortcuts))
        for i, (action, key) in enumerate(shortcuts):
            table.setItem(i, 0, QTableWidgetItem(action))
            k_item = QTableWidgetItem(key)
            k_item.setForeground(QColor(GLAGGLE_BLUE_DARK))
            k_item.setFont(QFont("Courier New", 12))
            table.setItem(i, 1, k_item)

        layout.addWidget(table)
        close_btn = QPushButton("Schließen")
        close_btn.setObjectName("primaryBtn")
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)


# ─────────────────────────────────────────────
#  MAIN WINDOW
# ─────────────────────────────────────────────
class GlashWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} — Glaggle Browser")
        self.setMinimumSize(1024, 700)
        self.resize(1360, 860)

        # Shared profile (regular)
        self.profile = QWebEngineProfile("GlashProfile_v2", self)
        self.profile.setHttpUserAgent(
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/124.0.0.0 Safari/537.36 Glash/{VERSION}"
        )
        self.profile.downloadRequested.connect(self._handle_download)

        # Private profile (no persistence)
        self.private_profile = QWebEngineProfile(self)
        self.private_profile.setHttpUserAgent(self.profile.httpUserAgent())
        self.private_profile.downloadRequested.connect(self._handle_download)

        self._extra_windows = []
        self._devtools_views = []
        self._reader_mode_active = False
        self._sidebar_visible = False

        self._build_ui()
        self._build_menu()
        self._build_shortcuts()

        # Open first tab
        self.new_tab(STORE.settings.get("homepage", HOME_URL))

    # ──────────────────────────────────────────
    #  UI CONSTRUCTION
    # ──────────────────────────────────────────

    def _build_ui(self):
        central = QWidget()
        central.setObjectName("centralWidget")
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── 1. Navigation Bar (ALWAYS at the very top) ──
        nav_bar = self._build_nav_bar()
        main_layout.addWidget(nav_bar)

        # ── 2. Thin progress bar sits just below nav ──
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(2)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        # ── 3. Find bar (hidden by default) ──
        self.find_bar = FindBar()
        main_layout.addWidget(self.find_bar)

        # ── 4. Horizontal splitter: sidebar | tabs | reader ──
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_splitter.setHandleWidth(1)

        # Sidebar panel (hidden initially)
        self.sidebar_panel = self._build_sidebar_panel()
        self.sidebar_panel.setVisible(False)
        self.main_splitter.addWidget(self.sidebar_panel)

        # Tab widget — tabs appear at TOP via TabPosition.North (default)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.setDocumentMode(False)   # False = proper tab frame on macOS
        self.tab_widget.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self._on_tab_changed)
        self.main_splitter.addWidget(self.tab_widget)

        # Reader mode panel (hidden initially)
        self.reader_panel = ReaderWidget()
        self.reader_panel.closed.connect(self._toggle_reader_mode)
        self.reader_panel.setVisible(False)
        self.main_splitter.addWidget(self.reader_panel)

        self.main_splitter.setStretchFactor(0, 0)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setStretchFactor(2, 0)
        main_layout.addWidget(self.main_splitter)

        # "+" new-tab button in top-right corner of tab bar
        new_tab_btn = QPushButton("+")
        new_tab_btn.setObjectName("newTabBtn")
        new_tab_btn.setToolTip("Neuer Tab (Ctrl+T)")
        new_tab_btn.clicked.connect(lambda: self.new_tab())
        self.tab_widget.setCornerWidget(new_tab_btn, Qt.Corner.TopRightCorner)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Bereit — Glash v2.0")

    def _build_nav_bar(self) -> QWidget:
        nav = QWidget()
        nav.setObjectName("navBar")
        nav.setFixedHeight(52)
        layout = QHBoxLayout(nav)
        layout.setContentsMargins(10, 7, 10, 7)
        layout.setSpacing(4)

        def nav_btn(text, tip):
            b = QPushButton(text)
            b.setObjectName("navBtn")
            b.setToolTip(tip)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            return b

        def action_btn(text, tip):
            b = QPushButton(text)
            b.setObjectName("actionBtn")
            b.setToolTip(tip)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            return b

        # Sidebar toggle
        self.sidebar_btn = action_btn("☰", "Seitenleiste (Ctrl+B)")
        self.sidebar_btn.clicked.connect(self._toggle_sidebar)
        layout.addWidget(self.sidebar_btn)

        # Nav buttons
        self.back_btn    = nav_btn("◀", "Zurück (Alt+←)")
        self.forward_btn = nav_btn("▶", "Vorwärts (Alt+→)")
        self.reload_btn  = nav_btn("↻", "Neu laden (Ctrl+R)")
        self.stop_btn    = nav_btn("✕", "Laden stoppen (Esc)")
        self.stop_btn.hide()

        self.back_btn.clicked.connect(self._nav_back)
        self.forward_btn.clicked.connect(self._nav_forward)
        self.reload_btn.clicked.connect(self._nav_reload)
        self.stop_btn.clicked.connect(self._nav_stop)

        for b in (self.back_btn, self.forward_btn, self.reload_btn, self.stop_btn):
            layout.addWidget(b)

        # Home
        home_btn = action_btn("⌂", "Startseite (Ctrl+H)")
        home_btn.clicked.connect(self._nav_home)
        layout.addWidget(home_btn)

        # Security
        self.security_label = QLabel("🔒")
        self.security_label.setObjectName("secureLabel")
        self.security_label.setToolTip("Verbindung")
        self.security_label.setCursor(Qt.CursorShape.PointingHandCursor)
        layout.addWidget(self.security_label)

        # URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setPlaceholderText("URL oder Suchbegriff…")
        self.url_bar.returnPressed.connect(self._url_entered)
        self.url_bar.setMinimumWidth(300)
        layout.addWidget(self.url_bar, stretch=1)

        # Reader mode
        self.reader_btn = action_btn("📖", "Reader Mode (Ctrl+Shift+R)")
        self.reader_btn.clicked.connect(self._toggle_reader_mode)
        layout.addWidget(self.reader_btn)

        # Bookmark
        self.bookmark_btn = action_btn("☆", "Lesezeichen (Ctrl+D)")
        self.bookmark_btn.clicked.connect(self._toggle_bookmark)
        layout.addWidget(self.bookmark_btn)

        # Zoom label
        self.zoom_label = QLabel("100%")
        self.zoom_label.setObjectName("zoomLabel")
        self.zoom_label.setToolTip("Zoom — Ctrl+ / Ctrl-")
        self.zoom_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.zoom_label.mousePressEvent = lambda e: self._current_view() and \
            (self._current_view().zoom_reset(), self._update_zoom_label(100))
        layout.addWidget(self.zoom_label)

        # Private tab indicator
        self.private_label = QLabel("🕶 Privat")
        self.private_label.setObjectName("privateLabel")
        self.private_label.setVisible(False)
        layout.addWidget(self.private_label)

        # Downloads
        dl_btn = action_btn("⬇", "Downloads (Ctrl+Shift+J)")
        dl_btn.clicked.connect(self._show_downloads)
        layout.addWidget(dl_btn)

        # Extensions/Settings menu
        settings_btn = action_btn("⚙", "Einstellungen")
        settings_btn.clicked.connect(self._show_settings)
        layout.addWidget(settings_btn)

        return nav

    def _build_sidebar_panel(self) -> QWidget:
        panel = QWidget()
        panel.setObjectName("sidebarPanel")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 12, 10, 10)
        layout.setSpacing(8)

        # Tabs for sidebar content
        self.sidebar_tabs = QTabWidget()
        self.sidebar_tabs.setDocumentMode(True)
        self.sidebar_tabs.setTabPosition(QTabWidget.TabPosition.North)

        # Bookmarks tab
        bm_widget = QWidget()
        bm_layout = QVBoxLayout(bm_widget)
        bm_layout.setContentsMargins(4, 4, 4, 4)
        bm_layout.setSpacing(6)
        bm_search = QLineEdit()
        bm_search.setPlaceholderText("Lesezeichen suchen…")
        bm_search.textChanged.connect(self._filter_sidebar_bm)
        bm_layout.addWidget(bm_search)
        self.sidebar_bm_list = QListWidget()
        self.sidebar_bm_list.itemDoubleClicked.connect(self._sidebar_open_item)
        bm_layout.addWidget(self.sidebar_bm_list)
        bm_add_btn = QPushButton("✚ Aktuell hinzufügen")
        bm_add_btn.clicked.connect(self._toggle_bookmark)
        bm_layout.addWidget(bm_add_btn)
        self.sidebar_tabs.addTab(bm_widget, "⭐ Lesezeichen")

        # History tab
        hist_widget = QWidget()
        hist_layout = QVBoxLayout(hist_widget)
        hist_layout.setContentsMargins(4, 4, 4, 4)
        hist_layout.setSpacing(6)
        hist_search = QLineEdit()
        hist_search.setPlaceholderText("Verlauf suchen…")
        hist_search.textChanged.connect(self._filter_sidebar_hist)
        hist_layout.addWidget(hist_search)
        self.sidebar_hist_list = QListWidget()
        self.sidebar_hist_list.itemDoubleClicked.connect(self._sidebar_open_item)
        hist_layout.addWidget(self.sidebar_hist_list)
        hist_layout.addWidget(QLabel("<small style='color:#888'>Doppelklick zum Öffnen</small>"))
        self.sidebar_tabs.addTab(hist_widget, "🕐 Verlauf")

        layout.addWidget(self.sidebar_tabs)
        self._refresh_sidebar()
        return panel

    def _refresh_sidebar(self):
        # Bookmarks
        self.sidebar_bm_list.clear()
        for bm in STORE.bookmarks:
            item = QListWidgetItem(bm.get("title", bm["url"])[:50])
            item.setData(Qt.ItemDataRole.UserRole, bm["url"])
            item.setToolTip(bm["url"])
            self.sidebar_bm_list.addItem(item)

        # History
        self.sidebar_hist_list.clear()
        for h in reversed(STORE.history[-200:]):
            item = QListWidgetItem(h.get("title", h["url"])[:50])
            item.setData(Qt.ItemDataRole.UserRole, h["url"])
            item.setToolTip(h["url"])
            self.sidebar_hist_list.addItem(item)

    def _filter_sidebar_bm(self, text):
        for i in range(self.sidebar_bm_list.count()):
            item = self.sidebar_bm_list.item(i)
            match = text.lower() in item.text().lower() or \
                    text.lower() in (item.data(Qt.ItemDataRole.UserRole) or "").lower()
            item.setHidden(not match if text else False)

    def _filter_sidebar_hist(self, text):
        for i in range(self.sidebar_hist_list.count()):
            item = self.sidebar_hist_list.item(i)
            match = text.lower() in item.text().lower() or \
                    text.lower() in (item.data(Qt.ItemDataRole.UserRole) or "").lower()
            item.setHidden(not match if text else False)

    def _sidebar_open_item(self, item):
        url = item.data(Qt.ItemDataRole.UserRole)
        if url:
            v = self._current_view()
            if v:
                v.setUrl(QUrl(url))

    def _toggle_sidebar(self):
        self._sidebar_visible = not self._sidebar_visible
        self.sidebar_panel.setVisible(self._sidebar_visible)
        if self._sidebar_visible:
            self.main_splitter.setSizes([260, self.width() - 260, 0])
            self._refresh_sidebar()

    # ──────────────────────────────────────────
    #  MENU
    # ──────────────────────────────────────────

    def _add_action(self, menu, text, slot, shortcut=None, checkable=False, checked=False):
        a = QAction(text, self)
        if shortcut:
            a.setShortcut(QKeySequence(shortcut))
        a.setCheckable(checkable)
        if checkable:
            a.setChecked(checked)
        a.triggered.connect(slot)
        menu.addAction(a)
        return a

    def _build_menu(self):
        mb = self.menuBar()

        # Glash
        app_menu = mb.addMenu(f"  {APP_NAME}  ")
        self._add_action(app_menu, "Einstellungen…",   self._show_settings,  "Ctrl+,")
        self._add_action(app_menu, "Tastenkürzel…",    self._show_shortcuts)
        app_menu.addSeparator()
        self._add_action(app_menu, "Glash beenden",    self.close,           "Ctrl+Q")

        # Datei
        file_menu = mb.addMenu("  Datei  ")
        self._add_action(file_menu, "Neuer Tab",       lambda: self.new_tab(),      "Ctrl+T")
        self._add_action(file_menu, "Privater Tab",    self._new_private_tab,       "Ctrl+Shift+P")
        self._add_action(file_menu, "Neues Fenster",   self._new_window,            "Ctrl+N")
        file_menu.addSeparator()
        self._add_action(file_menu, "Tab schließen",
            lambda: self.close_tab(self.tab_widget.currentIndex()),                "Ctrl+W")
        file_menu.addSeparator()
        self._add_action(file_menu, "Seite drucken…",  self._print_page,    "Ctrl+P")
        self._add_action(file_menu, "Als PDF…",        self._save_as_pdf)
        self._add_action(file_menu, "Seite speichern…",self._save_page,     "Ctrl+S")

        # Bearbeiten
        edit_menu = mb.addMenu("  Bearbeiten  ")
        self._add_action(edit_menu, "Rückgängig",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.Undo), "Ctrl+Z")
        self._add_action(edit_menu, "Wiederholen",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.Redo), "Ctrl+Shift+Z")
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Kopieren",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.Copy), "Ctrl+C")
        self._add_action(edit_menu, "Ausschneiden",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.Cut), "Ctrl+X")
        self._add_action(edit_menu, "Einfügen",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.Paste), "Ctrl+V")
        self._add_action(edit_menu, "Alles auswählen",
            lambda: self._current_view() and
            self._current_view().page().triggerAction(QWebEnginePage.WebAction.SelectAll), "Ctrl+A")
        edit_menu.addSeparator()
        self._add_action(edit_menu, "Auf Seite suchen…", self._show_find, "Ctrl+F")

        # Darstellung
        view_menu = mb.addMenu("  Darstellung  ")
        self._add_action(view_menu, "Vergrößern",
            lambda: self._zoom_by(+1), "Ctrl++")
        self._add_action(view_menu, "Verkleinern",
            lambda: self._zoom_by(-1), "Ctrl+-")
        self._add_action(view_menu, "Originalansicht",
            lambda: self._zoom_by(0), "Ctrl+0")
        view_menu.addSeparator()
        self._add_action(view_menu, "Seitenleiste",    self._toggle_sidebar, "Ctrl+B")
        self._add_action(view_menu, "Reader Mode",     self._toggle_reader_mode, "Ctrl+Shift+R")
        view_menu.addSeparator()
        self._add_action(view_menu, "Vollbild",        self._toggle_fullscreen, "F11")
        view_menu.addSeparator()
        self._add_action(view_menu, "Seitenquelltext", self._view_source,   "Ctrl+U")
        self._add_action(view_menu, "Entwicklerwerkzeuge", self._toggle_devtools, "F12")

        # Verlauf
        history_menu = mb.addMenu("  Verlauf  ")
        self._add_action(history_menu, "Zurück",       self._nav_back,    "Ctrl+[")
        self._add_action(history_menu, "Vorwärts",     self._nav_forward, "Ctrl+]")
        history_menu.addSeparator()
        self._add_action(history_menu, "Startseite",   self._nav_home,    "Ctrl+H")
        history_menu.addSeparator()
        self._add_action(history_menu, "Gesamten Verlauf…", self._show_history, "Ctrl+Shift+H")
        self._add_action(history_menu, "Verlauf löschen…",  self._clear_history_prompt)

        # Lesezeichen
        bm_menu = mb.addMenu("  Lesezeichen  ")
        self._add_action(bm_menu, "Lesezeichen hinzufügen/entfernen",
                         self._toggle_bookmark, "Ctrl+D")
        self._add_action(bm_menu, "Alle Lesezeichen…", self._show_bookmarks)
        bm_menu.addSeparator()
        bm_menu.aboutToShow.connect(lambda: self._populate_bm_menu(bm_menu))

        # Fenster
        win_menu = mb.addMenu("  Fenster  ")
        self._add_action(win_menu, "Minimieren",     self.showMinimized,  "Ctrl+M")
        self._add_action(win_menu, "Maximieren",     self.showMaximized)
        win_menu.addSeparator()
        self._add_action(win_menu, "Nächster Tab",   lambda: self._switch_tab(+1), "Ctrl+Tab")
        self._add_action(win_menu, "Vorheriger Tab", lambda: self._switch_tab(-1), "Ctrl+Shift+Tab")
        win_menu.addSeparator()
        self._add_action(win_menu, "Downloads",      self._show_downloads,  "Ctrl+Shift+J")

        # Hilfe
        help_menu = mb.addMenu("  Hilfe  ")
        self._add_action(help_menu, "Glaggle öffnen",   lambda: self.new_tab(HOME_URL))
        self._add_action(help_menu, "Tastenkürzel…",    self._show_shortcuts)
        self._add_action(help_menu, "Über Glash…",      self._show_about)
        help_menu.addSeparator()
        self._add_action(help_menu, "Fehler melden",
                         lambda: self.new_tab("https://glaggle.ch/faq"))

    def _build_shortcuts(self):
        QShortcut(QKeySequence("Ctrl+L"),   self, self._focus_url_bar)
        QShortcut(QKeySequence("Escape"),   self, self._escape_pressed)
        QShortcut(QKeySequence("Ctrl+R"),   self, self._nav_reload)
        QShortcut(QKeySequence("Ctrl+Shift+R"), self, self._hard_reload)
        QShortcut(QKeySequence("F5"),        self, self._nav_reload)
        QShortcut(QKeySequence("F11"),       self, self._toggle_fullscreen)
        QShortcut(QKeySequence("F12"),       self, self._toggle_devtools)
        QShortcut(QKeySequence("Alt+Left"),  self, self._nav_back)
        QShortcut(QKeySequence("Alt+Right"), self, self._nav_forward)
        QShortcut(QKeySequence("Ctrl+Up"),   self,
                  lambda: self._current_view() and self._current_view().scroll_to_top())
        QShortcut(QKeySequence("Ctrl+Down"), self,
                  lambda: self._current_view() and self._current_view().scroll_to_bottom())
        QShortcut(QKeySequence("Ctrl+1"),    self, lambda: self._go_to_tab(0))
        QShortcut(QKeySequence("Ctrl+2"),    self, lambda: self._go_to_tab(1))
        QShortcut(QKeySequence("Ctrl+3"),    self, lambda: self._go_to_tab(2))
        QShortcut(QKeySequence("Ctrl+4"),    self, lambda: self._go_to_tab(3))
        QShortcut(QKeySequence("Ctrl+5"),    self, lambda: self._go_to_tab(4))
        QShortcut(QKeySequence("Ctrl+9"),    self,
                  lambda: self._go_to_tab(self.tab_widget.count() - 1))

    # ──────────────────────────────────────────
    #  TAB MANAGEMENT
    # ──────────────────────────────────────────

    def new_tab(self, url: str = None, private: bool = False, background: bool = False):
        if url is None:
            url = STORE.settings.get("homepage", HOME_URL)

        profile = self.private_profile if private else self.profile
        view = BrowserTab(profile, is_private=private)
        view.title_updated.connect(lambda t, v=view: self._on_title_changed(t, v))
        view.url_updated.connect(lambda u, v=view: self._on_url_changed(u, v))
        view.load_progress.connect(self._on_load_progress)
        view.new_tab_url.connect(lambda u: self.new_tab(u.toString()))
        view.favicon_updated.connect(lambda ico, v=view: self._on_favicon(ico, v))
        view.loadStarted.connect(self._on_load_started)
        view.loadFinished.connect(self._on_load_finished)
        view.reader_ready.connect(self._on_reader_ready)

        if STORE.settings.get("zoom", 100) != 100:
            view.setZoomFactor(STORE.settings["zoom"] / 100)

        idx = self.tab_widget.addTab(view, "Neuer Tab")

        if private:
            self.tab_widget.tabBar().setTabData(idx, {"private": True})
            self.tab_widget.tabBar().setTabToolTip(idx, "🕶 Privater Tab")

        if not background:
            self.tab_widget.setCurrentIndex(idx)

        view.setUrl(QUrl(url))
        self.find_bar.set_view(view)
        return view

    def _new_private_tab(self):
        self.new_tab(STORE.settings.get("homepage", HOME_URL), private=True)

    def close_tab(self, index: int):
        if self.tab_widget.count() == 1:
            self.new_tab()
        widget = self.tab_widget.widget(index)
        self.tab_widget.removeTab(index)
        if widget:
            widget.deleteLater()

    def _current_view(self) -> BrowserTab | None:
        w = self.tab_widget.currentWidget()
        return w if isinstance(w, BrowserTab) else None

    def _switch_tab(self, delta: int):
        count = self.tab_widget.count()
        if count:
            idx = (self.tab_widget.currentIndex() + delta) % count
            self.tab_widget.setCurrentIndex(idx)

    def _go_to_tab(self, idx: int):
        if 0 <= idx < self.tab_widget.count():
            self.tab_widget.setCurrentIndex(idx)

    # ──────────────────────────────────────────
    #  NAVIGATION
    # ──────────────────────────────────────────

    def _url_entered(self):
        text = self.url_bar.text().strip()
        if not text:
            return

        # Detect if it's a URL or a search query
        if text.startswith(("http://", "https://", "file://", "about:", "view-source:")):
            url = text
        elif "." in text and " " not in text and not text.startswith("www") == False or \
             text.count(".") >= 1 and " " not in text:
            # Looks like a domain
            if "." in text and " " not in text:
                url = "https://" + text if not text.startswith("http") else text
            else:
                url = STORE.get_search_url(text)
        else:
            url = STORE.get_search_url(text)

        v = self._current_view()
        if v:
            v.setUrl(QUrl(url))

    def _nav_back(self):
        v = self._current_view()
        if v: v.back()

    def _nav_forward(self):
        v = self._current_view()
        if v: v.forward()

    def _nav_reload(self):
        v = self._current_view()
        if v: v.reload()

    def _hard_reload(self):
        v = self._current_view()
        if v: v.page().triggerAction(QWebEnginePage.WebAction.ReloadAndBypassCache)

    def _nav_stop(self):
        v = self._current_view()
        if v: v.stop()

    def _nav_home(self):
        v = self._current_view()
        if v: v.setUrl(QUrl(STORE.settings.get("homepage", HOME_URL)))

    def _focus_url_bar(self):
        self.url_bar.setFocus()
        self.url_bar.selectAll()

    def _escape_pressed(self):
        if self.find_bar.isVisible():
            self.find_bar.hide_and_clear()
        elif self._reader_mode_active:
            self._toggle_reader_mode()
        else:
            self._nav_stop()

    def _zoom_by(self, direction: int):
        v = self._current_view()
        if not v:
            return
        if direction > 0:
            pct = v.zoom_in()
        elif direction < 0:
            pct = v.zoom_out()
        else:
            pct = v.zoom_reset()
        self._update_zoom_label(pct)

    def _update_zoom_label(self, pct: int):
        self.zoom_label.setText(f"{pct}%")
        if pct != 100:
            self.zoom_label.setStyleSheet("color: #2E94D1; font-weight: 600;")
        else:
            self.zoom_label.setStyleSheet("")

    # ──────────────────────────────────────────
    #  SIGNAL HANDLERS
    # ──────────────────────────────────────────

    def _on_title_changed(self, title: str, view: BrowserTab):
        idx = self.tab_widget.indexOf(view)
        if idx >= 0:
            short = (title[:26] + "…") if len(title) > 28 else title
            prefix = "🕶 " if view.is_private else ""
            self.tab_widget.setTabText(idx, prefix + (short or "Neuer Tab"))
        if view == self._current_view():
            self.setWindowTitle(f"{title} — {APP_NAME}")

    def _on_url_changed(self, url: QUrl, view: BrowserTab):
        if view != self._current_view():
            return
        url_str = url.toString()
        self.url_bar.setText(url_str)

        # Security
        if view.is_private:
            self.security_label.setText("🕶")
            self.security_label.setObjectName("privateLabel")
            self.private_label.setVisible(True)
        elif url_str.startswith("https://"):
            self.security_label.setText("🔒")
            self.security_label.setObjectName("secureLabel")
            self.private_label.setVisible(False)
        elif url_str.startswith("http://"):
            self.security_label.setText("⚠️")
            self.security_label.setObjectName("insecureLabel")
            self.private_label.setVisible(False)
        else:
            self.security_label.setText("ℹ️")
            self.security_label.setObjectName("localLabel")
            self.private_label.setVisible(False)
        self.security_label.setStyleSheet("")

        self._update_bookmark_btn(url_str)
        self.back_btn.setEnabled(view.history().canGoBack())
        self.forward_btn.setEnabled(view.history().canGoForward())

        pct = int(view.zoomFactor() * 100)
        self._update_zoom_label(pct)

        if url_str and not url_str.startswith("about:") and not view.is_private:
            title = self.tab_widget.tabText(self.tab_widget.currentIndex())
            STORE.add_history(url_str, title)

    def _on_load_started(self):
        self.reload_btn.hide()
        self.stop_btn.show()
        self.progress_bar.setValue(0)
        self.progress_bar.show()
        self.status_bar.showMessage("Lädt…")

    def _on_load_finished(self, ok: bool):
        self.stop_btn.hide()
        self.reload_btn.show()
        self.progress_bar.hide()
        v = self._current_view()
        if v:
            msg = v.url().toString() if ok else f"⚠ Fehler beim Laden"
            self.status_bar.showMessage(msg, 4000)

    def _on_load_progress(self, progress: int):
        self.progress_bar.setValue(progress)

    def _on_tab_changed(self, idx: int):
        view = self.tab_widget.widget(idx)
        if not isinstance(view, BrowserTab):
            return
        url_str = view.url().toString()
        self.url_bar.setText(url_str)
        self.back_btn.setEnabled(view.history().canGoBack())
        self.forward_btn.setEnabled(view.history().canGoForward())
        self.find_bar.set_view(view)
        pct = int(view.zoomFactor() * 100)
        self._update_zoom_label(pct)
        self._update_bookmark_btn(url_str)
        self.setWindowTitle(f"{view.title() or 'Neuer Tab'} — {APP_NAME}")
        self.private_label.setVisible(view.is_private)

        # Reader mode security indicator
        if view.is_private:
            self.security_label.setText("🕶")
            self.security_label.setObjectName("privateLabel")
        elif url_str.startswith("https://"):
            self.security_label.setText("🔒")
            self.security_label.setObjectName("secureLabel")
        elif url_str.startswith("http://"):
            self.security_label.setText("⚠️")
            self.security_label.setObjectName("insecureLabel")
        else:
            self.security_label.setText("ℹ️")
            self.security_label.setObjectName("localLabel")
        self.security_label.setStyleSheet("")

    def _on_favicon(self, icon: QIcon, view: BrowserTab):
        idx = self.tab_widget.indexOf(view)
        if idx >= 0 and not icon.isNull():
            self.tab_widget.setTabIcon(idx, icon)

    def _on_reader_ready(self, title: str, html: str):
        self.reader_panel.load_content(title, html)

    # ──────────────────────────────────────────
    #  BOOKMARKS
    # ──────────────────────────────────────────

    def _update_bookmark_btn(self, url: str):
        if STORE.is_bookmarked(url):
            self.bookmark_btn.setText("★")
            self.bookmark_btn.setToolTip("Lesezeichen entfernen (Ctrl+D)")
            self.bookmark_btn.setProperty("bookmarked", "true")
        else:
            self.bookmark_btn.setText("☆")
            self.bookmark_btn.setToolTip("Lesezeichen hinzufügen (Ctrl+D)")
            self.bookmark_btn.setProperty("bookmarked", "false")
        self.bookmark_btn.setStyleSheet("")

    def _toggle_bookmark(self):
        v = self._current_view()
        if not v:
            return
        url = v.url().toString()
        title = v.title() or url
        if STORE.is_bookmarked(url):
            STORE.remove_bookmark(url)
            self.status_bar.showMessage("Lesezeichen entfernt", 2000)
        else:
            STORE.add_bookmark(url, title)
            self.status_bar.showMessage("✨ Lesezeichen gespeichert!", 2000)
        self._update_bookmark_btn(url)
        self._refresh_sidebar()

    def _populate_bm_menu(self, menu: QMenu):
        actions = menu.actions()
        for a in actions[3:]:
            menu.removeAction(a)
        if STORE.bookmarks:
            for bm in reversed(STORE.bookmarks[-25:]):
                title = (bm.get("title", bm["url"]) or bm["url"])[:55]
                a = QAction(f"⭐  {title}", self)
                a.triggered.connect(lambda checked, u=bm["url"]: self.new_tab(u, background=True))
                menu.addAction(a)
        else:
            a = QAction("Keine Lesezeichen", self)
            a.setEnabled(False)
            menu.addAction(a)

    # ──────────────────────────────────────────
    #  READER MODE
    # ──────────────────────────────────────────

    def _toggle_reader_mode(self):
        v = self._current_view()
        if not v:
            return
        self._reader_mode_active = not self._reader_mode_active
        self.reader_panel.setVisible(self._reader_mode_active)

        if self._reader_mode_active:
            self.reader_btn.setProperty("active", "true")
            self.main_splitter.setSizes([
                260 if self._sidebar_visible else 0,
                self.width() // 2,
                self.width() // 2
            ])
            v.extract_reader_content()
            self.status_bar.showMessage("Reader Mode aktiviert", 2000)
        else:
            self.reader_btn.setProperty("active", "false")
            self.main_splitter.setSizes([
                260 if self._sidebar_visible else 0,
                self.width(),
                0
            ])
            self.status_bar.showMessage("Reader Mode deaktiviert", 2000)
        self.reader_btn.setStyleSheet("")

    # ──────────────────────────────────────────
    #  VIEW ACTIONS
    # ──────────────────────────────────────────

    def _view_source(self):
        v = self._current_view()
        if v:
            self.new_tab(f"view-source:{v.url().toString()}")

    def _toggle_devtools(self):
        v = self._current_view()
        if not v:
            return
        dev_view = QWebEngineView()
        dev_view.setWindowTitle(f"DevTools — {v.title() or 'Glash'}")
        dev_view.resize(1000, 650)
        v.page().setDevToolsPage(dev_view.page())
        dev_view.show()
        self._devtools_views.append(dev_view)

    def _toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def _print_page(self):
        v = self._current_view()
        if not v:
            return
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dlg = QPrintDialog(printer, self)
        if dlg.exec() == QPrintDialog.DialogCode.Accepted:
            self.status_bar.showMessage("Druckt…", 3000)

    def _save_as_pdf(self):
        v = self._current_view()
        if v:
            path = os.path.expanduser(
                f"~/Desktop/Glash_{v.title()[:30].replace('/', '_')}_{int(datetime.now().timestamp())}.pdf"
            )
            v.page().printToPdf(path)
            self.status_bar.showMessage(f"PDF gespeichert: {path}", 4000)

    def _save_page(self):
        v = self._current_view()
        if v:
            path = os.path.expanduser(
                f"~/Desktop/Glash_Page_{int(datetime.now().timestamp())}.html"
            )
            v.page().save(path, QWebEnginePage.SavePageFormat.SingleHtmlSavedPage)
            self.status_bar.showMessage(f"Seite gespeichert: {path}", 3000)

    def _new_window(self):
        w = GlashWindow()
        w.show()
        self._extra_windows.append(w)

    def _hard_reload(self):
        v = self._current_view()
        if v:
            v.page().triggerAction(QWebEnginePage.WebAction.ReloadAndBypassCache)

    # ──────────────────────────────────────────
    #  DIALOGS
    # ──────────────────────────────────────────

    def _show_bookmarks(self):
        dlg = SidePanelDialog("bookmarks", self)
        dlg.navigate_to.connect(lambda u: self._current_view() and self._current_view().setUrl(QUrl(u)))
        dlg.exec()

    def _show_history(self):
        dlg = SidePanelDialog("history", self)
        dlg.navigate_to.connect(lambda u: self._current_view() and self._current_view().setUrl(QUrl(u)))
        dlg.exec()

    def _show_settings(self):
        dlg = SettingsDialog(self)
        dlg.exec()

    def _show_find(self):
        self.find_bar.show_and_focus()

    def _show_downloads(self):
        dlg = DownloadDialog(self)
        dlg.exec()

    def _show_shortcuts(self):
        dlg = ShortcutsDialog(self)
        dlg.exec()

    def _show_about(self):
        QMessageBox.information(
            self, f"Über {APP_NAME}",
            f"<b style='font-size:20px'>⚡ Glash Browser v{VERSION}</b><br><br>"
            f"powered by <b>Glaggle</b><br><br>"
            f"<b>Neu in v2.0:</b><br>"
            f"• Reader Mode<br>"
            f"• Private Tabs<br>"
            f"• Download Manager<br>"
            f"• Seitenleiste (Bookmarks + Verlauf)<br>"
            f"• Google Suche<br>"
            f"• Wählbare Suchmaschine<br>"
            f"• Hard Reload<br>"
            f"• Tab-Shortcuts (Ctrl+1–9)<br>"
            f"• Verbessertes Design<br><br>"
            f"<small style='color:#888'>Built with PyQt6 + Chromium WebEngine<br>"
            f"© 2026 Glaggle Inc. — Glaggle your life!</small>"
        )

    def _clear_history_prompt(self):
        if QMessageBox.question(
            self, "Verlauf löschen", "Gesamten Verlauf löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        ) == QMessageBox.StandardButton.Yes:
            STORE.history.clear()
            STORE.save()
            self._refresh_sidebar()
            self.status_bar.showMessage("Verlauf gelöscht.", 2000)

    # ──────────────────────────────────────────
    #  DOWNLOAD HANDLER
    # ──────────────────────────────────────────

    def _handle_download(self, dl: QWebEngineDownloadRequest):
        dl_dir = os.path.expanduser("~/Downloads")
        os.makedirs(dl_dir, exist_ok=True)
        fname = dl.suggestedFileName() or "download"
        path = os.path.join(dl_dir, fname)
        dl.setDownloadDirectory(dl_dir)
        dl.setDownloadFileName(fname)
        dl.accept()

        entry = {"name": fname, "path": path, "state": "Lädt…", "size": 0}
        STORE.downloads.append(entry)
        self.status_bar.showMessage(f"⬇ Download gestartet: {fname}", 3000)

        def _on_finished():
            ok = dl.state() == QWebEngineDownloadRequest.DownloadState.DownloadCompleted
            entry["state"] = "Fertig ✅" if ok else "Fehler ❌"
            entry["size"]  = dl.receivedBytes()
            STORE.save()
            self.status_bar.showMessage(
                f"{'✅' if ok else '❌'} {fname} — {'fertig' if ok else 'Fehler'}", 5000
            )

        dl.isFinishedChanged.connect(_on_finished)
        dl.receivedBytesChanged.connect(lambda: entry.update({"size": dl.receivedBytes()}))

    # ──────────────────────────────────────────
    #  WINDOW CLOSE
    # ──────────────────────────────────────────

    def closeEvent(self, event):
        STORE.save()
        super().closeEvent(event)


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
def main():
    os.environ.setdefault("QTWEBENGINE_CHROMIUM_FLAGS",
        "--enable-features=NetworkServiceInProcess "
        "--disable-web-security=false "
        "--enable-smooth-scrolling")

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    app.setOrganizationName("Glaggle Inc.")
    app.setApplicationDisplayName(f"{APP_NAME} Browser")
    app.setDesktopFileName("glash")
    app.setStyleSheet(STYLESHEET)

    font = QFont()
    font.setFamily("-apple-system")
    font.setPointSize(13)
    app.setFont(font)

    window = GlashWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
