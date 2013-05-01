from PyQt4.QtGui import QDialog, QWidget


class SettingDialog():
    def __init__(self, settingManager, setValuesOnDialogAccepted=True, setValueOnWidgetUpdate=False):
        if isinstance(self, QDialog) and setValuesOnDialogAccepted:
            self.accepted.connect(self.acceptDialog)

        self._settings = []
        for setting in settingManager.settings:
            widget = self.findChild(QWidget, setting.name)
            if widget:
                setting.setWidget(widget)
                if setValueOnWidgetUpdate:
                    setting.setValueOnWidgetUpdateSignal()
                self._settings.append(setting)

        # just in case the widget has no showEvent
        self.setWidgetsFromValues()

    """
    you can override this method in the PluginSettings subclass
    """
    def onBeforeAcceptDialog(self):
        return True

    def widgetList(self):
        wl = []
        for setting in self._settings:
            wl.append(setting.name)
        return wl

    def acceptDialog(self):
        if self.onBeforeAcceptDialog():
            self.setValuesFromWidgets()

    def showEvent(self, e):
        self.setWidgetsFromValues()

    def setValuesFromWidgets(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setValueFromWidget()

    def setWidgetsFromValues(self):
        for setting in self._settings:
            if setting.widget is not None:
                setting.setWidgetFromValue()