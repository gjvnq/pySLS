#!/usr/bin/env python3

import pkgutil
from io import StringIO

from typing import Optional

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QMainWindow, QSizePolicy
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import Qt, QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QScreen
from PySide6.QtMultimedia import QMediaDevices, QCamera, QMediaCaptureSession, QImageCapture, QCameraDevice
from PySide6.QtMultimediaWidgets import QVideoWidget

from .utils import load_ui, qsize2area

from icecream import ic

class DataCollection(QMainWindow):
    camimg: QImageCapture
    display_options: list[tuple[str, QScreen]]
    camera_options: list[tuple[str, QCameraDevice]]
    camera_view: Optional[QVideoWidget]

    def __init__(self, app: QtWidgets.QApplication):
        self.app = app
        super().__init__()
        load_ui("data_collection.ui", self)
        self.camera_view = None

    def showEvent(self, evt):
        self.input_video_src.currentIndexChanged.connect(self.changed_video_src)
        self.input_display.currentIndexChanged.connect(self.changed_display)

        self.reload_displays()
        self.reload_cameras()

    def make_camera_view(self):
        if self.camera_view is None:
            self.camera_view = QVideoWidget()
            layout = self.camera_view_placeholder.parent().layout()
            # ic(layout.replaceWidget(self.camera_view_placeholder, self.camera_view))
            # self.camera_view.resize(200,200)
            # self.camera_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


    def reload_displays(self):
        self.display_options = [("Resizable Window", None)]
        for screen in self.app.screens():
            size = screen.size()
            ic(screen)
            title = f"{screen.name()} by {screen.manufacturer()} ({size.width()}x{size.height()})"
            self.display_options += ((title, screen),)
        
        self.input_display.clear()
        for (title, screen) in self.display_options:
            self.input_display.addItem(title)

        # self.changed_display()

    def changed_display(self):
        if self.input_display is None:
            return
        print("func has been called!")
        ic(self.input_display.currentIndex())

    def changed_video_src(self):
        if self.input_video_src is None:
            return
        idx = self.input_video_src.currentIndex()
        ic(idx)
        camname, camdev = self.camera_options[idx]
        ic(camname, camdev)
        cam = QCamera(camdev)
        ic(cam)

        best_fmt = None
        for fmt in camdev.videoFormats():
            ic(fmt, fmt.resolution(), fmt.pixelFormat())
            if best_fmt is None or qsize2area(best_fmt.resolution()) < qsize2area(fmt.resolution()):
                best_fmt = fmt
        cam.setCameraFormat(best_fmt)

        cam.setExposureMode(QCamera.ExposureManual)
        cam.setFocusMode(QCamera.FocusModeManual)
        cam.setWhiteBalanceMode(QCamera.WhiteBalanceManual)

        ic(cam.cameraDevice())
        ic(cam.cameraFormat())
        ic(cam.cameraFormat().resolution())
        ic(cam.cameraFormat().pixelFormat())
        ic(cam.cameraFormat().minFrameRate())
        ic(cam.cameraFormat().maxFrameRate())
        ic(cam.captureSession())
        ic(cam.colorTemperature())
        ic(cam.customFocusPoint())
        ic(cam.error())
        ic(cam.errorString())
        ic(cam.exposureCompensation())
        ic(cam.exposureMode())
        ic(cam.exposureTime())
        ic(cam.flashMode())
        ic(cam.focusDistance())
        ic(cam.focusMode())
        ic(cam.focusPoint())
        ic(cam.isActive())
        ic(cam.isAvailable())
        ic(cam.isExposureModeSupported(QCamera.ExposureManual))
        ic(cam.isFlashModeSupported(QCamera.FlashOn))
        ic(cam.isFlashReady())
        ic(cam.isFocusModeSupported(QCamera.FocusModeManual))
        ic(cam.isFocusModeSupported(QCamera.FocusModeInfinity))
        ic(cam.isTorchModeSupported(QCamera.TorchOn))
        ic(cam.isWhiteBalanceModeSupported(QCamera.WhiteBalanceManual))
        ic(cam.isoSensitivity())
        ic(cam.manualExposureTime())
        ic(cam.manualIsoSensitivity())
        ic(cam.maximumExposureTime())
        ic(cam.maximumIsoSensitivity())
        ic(cam.maximumZoomFactor())
        ic(cam.minimumExposureTime())
        ic(cam.minimumIsoSensitivity())
        ic(cam.minimumZoomFactor())
        ic(cam.torchMode())
        ic(cam.whiteBalanceMode())
        ic(cam.zoomFactor())

        ic(cam.captureSession())

        
        camrec = QMediaCaptureSession()
        camrec.setCamera(cam)
        cam.start()
        
        # ic(...) is just a pretty print from package icecream

        # This doesn't work
        # ic(self.camera_view)
        # ic(camrec.setVideoOutput(self.camera_view))
        # self.camera_view.show()

        # This works (albeit slow)
        # camview = QVideoWidget()
        # ic(camrec.setVideoOutput(camview))
        # camview.show()

        # This doesn't work
        # self.camview = QVideoWidget()
        # ic(camrec.setVideoOutput(self.camview))
        # self.camview.show()

        # And this works (WTF!?)
        # (note no show(), yet it works)
        # camview = QVideoWidget()
        # layout = self.camera_view_placeholder.parent().layout()
        # ic(layout.replaceWidget(self.camera_view_placeholder, camview))
        # ic(camrec.setVideoOutput(camview))

        # And this also works (WTF²!?)
        # self.camview = QVideoWidget()
        # layout = self.camera_view_placeholder.parent().layout()
        # ic(layout.replaceWidget(self.camera_view_placeholder, self.camview))
        # ic(camrec.setVideoOutput(self.camview))

        # And this doesn't work
        # layout = self.camera_view_placeholder.parent().layout()
        # ic(layout.replaceWidget(self.camera_view_placeholder, self.camera_view))
        # ic(camrec.setVideoOutput(self.camera_view))

        # self.make_camera_view()
        # self.camera_view.show()
        # ic(camrec.setVideoOutput(self.camera_view))



        ic(camrec)
        ic(cam.captureSession())


    def reload_cameras(self):
        self.camera_options = []
        cameras_raw = QMediaDevices.videoInputs()
        for cameraDevice in cameras_raw:
            self.camera_options += ((cameraDevice.description(), cameraDevice),)
            ic(cameraDevice.photoResolutions())
            ic(cameraDevice.position())
            ic(cameraDevice.videoFormats())
        ic(self.camera_options)

        self.input_video_src.clear()
        for (title, screen) in self.camera_options:
            self.input_video_src.addItem(title)
        
        self.changed_video_src()

