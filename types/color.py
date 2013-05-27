#-----------------------------------------------------------
#
# QGIS setting manager is a python module to easily manage read/write
# settings and set/get corresponding widgets.
#
# Copyright    : (C) 2013 Denis Rouzaud
# Email        : denis.rouzaud@gmail.com
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this progsram; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------


# options:
# dialogTitle: show in color dialog

from PyQt4.QtCore import QSettings, QStringList, SIGNAL
from PyQt4.QtGui import QColor
from qgis.core import QgsProject
from qgis.gui import QgsColorButton

from ..setting import Setting


class Color(Setting):

    def __init__(self, pluginName, name, scope, defaultValue, options={}):

        setGlobal = lambda(value): QSettings(pluginName, pluginName).setValue(name, [value.red(),
                                                                                     value.green(),
                                                                                     value.blue()])
        setProject = lambda(value): QgsProject.instance().writeEntry(pluginName, name,
                                                                     QStringList(["%u" % value.red(),
                                                                                  "%u" % value.green(),
                                                                                  "%u" % value.blue()]))
        getGlobal = lambda: self.list2color(QSettings(pluginName, pluginName).value(name, defaultValue).toStringList())
        getProject = lambda: self.list2color(QgsProject.instance().readListEntry(pluginName, name, defaultValue))

        Setting.__init__(self, pluginName, name, scope, defaultValue, options,
                         setGlobal, setProject, getGlobal, getProject)

    def check(self, color):
        if type(color) != QColor:
            raise NameError("Color setting %s must be a QColor." % self.name)

    def setWidget(self, widget):
        txt = self.options.get("dialogTitle", "")
        self.widget = QgsColorButton(widget, txt)
        self.signal = SIGNAL("colorChanged(color)")  # TODO: check if signal is working
        self.widgetSetMethod = self.widget.setColor
        self.widgetGetMethod = self.widget.color

    def list2color(self, color):
        if type(color) != list or len(color) != 3:
            return self.defaultValue
        else:
            r = color[0].toInt()[0]
            g = color[1].toInt()[0]
            b = color[2].toInt()[0]
        return QColor(r, g, b)
