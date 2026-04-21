from __future__ import annotations

from PyQt6.QtGui import QIcon, QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from src.sprite_sheet import get_frames
from src.window import CatWindow


class CatTray:
    def __init__(self, app: QApplication, window: CatWindow) -> None:
        self._app = app
        self._window = window

        self._tray = QSystemTrayIcon()
        self._tray.setIcon(self._build_tray_icon())

        self._menu = QMenu()
        self._toggle_action = self._menu.addAction("Poka\u017c / ukryj kota")
        self._toggle_action.triggered.connect(self._toggle_window_visibility)
        self._menu.addSeparator()
        self._quit_action = self._menu.addAction("Zamknij")
        self._quit_action.triggered.connect(self._app.quit)

        self._tray.setContextMenu(self._menu)
        self._tray.activated.connect(self._on_tray_activated)

        self._update_toggle_action_text()
        self._tray.show()

    def _build_tray_icon(self) -> QIcon:
        try:
            frame = get_frames("rest_sit")[0]
            data = frame.tobytes("raw", "RGBA")
            qimage = QImage(data, 64, 64, QImage.Format.Format_RGBA8888)
            pixmap = QPixmap.fromImage(qimage)
            return QIcon(pixmap)
        except Exception:
            return QIcon()

    def _toggle_window_visibility(self) -> None:
        if self._window.isVisible():
            self._window.hide()
        else:
            self._window.show()
        self._update_toggle_action_text()

    def _update_toggle_action_text(self) -> None:
        self._toggle_action.setText("Ukryj kota" if self._window.isVisible() else "Poka\u017c kota")

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self._toggle_window_visibility()
