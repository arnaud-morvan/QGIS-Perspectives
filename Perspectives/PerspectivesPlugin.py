# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PerspectivesPlugin
                             -------------------
        begin                : 2022-08-23
        copyright            : (C) 2022 by Arnaud Morvan
        email                : arnaud.morvan@camptocamp.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os.path
from functools import partial

from qgis.core import QgsSettings
from qgis.PyQt import QtCore, QtGui, QtWidgets
from qgis.utils import iface

from Perspectives.perspective import Perspective
from Perspectives.settings import settings


class PerspectivesPlugin(QtCore.QObject):
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        super(PerspectivesPlugin, self).__init__()
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QtCore.QSettings().value("locale/userLocale")[0:2]
        locale_path = os.path.join(
            self.plugin_dir, "i18n", "PerspectivesPlugin_{}.qm".format(locale)
        )

        if os.path.exists(locale_path):
            self.translator = QtCore.QTranslator()
            self.translator.load(locale_path)

            if QtCore.qVersion() > "4.3.3":
                QtCore.QCoreApplication.installTranslator(self.translator)

        self.perspectives = settings.readPerspectives()
        self.actions = {}

    def initGui(self):
        self.toolbar = QtWidgets.QToolBar("Perspectives toolbar", iface.mainWindow())
        self.toolbar.setObjectName("PerspectivesPluginToolbar")

        # self.tool_button = QtWidgets.QToolButton(iface.mainWindow())
        # self.tool_button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        # self.perspectives_menu = QtWidgets.QMenu()
        # self.tool_button.setMenu(self.perspectives_menu)
        # self.toolbar.addWidget(self.tool_button)

        # For exclusivity of actions
        self.action_group = QtWidgets.QActionGroup(self.toolbar)

        self.separator = self.toolbar.addSeparator()

        self.new_perspective_line_edit = QtWidgets.QLineEdit(self.toolbar)
        self.new_perspective_line_edit.setFixedWidth(80)
        self.new_perspective_line_edit_action = self.toolbar.addWidget(self.new_perspective_line_edit)
        self.new_perspective_line_edit_action.setVisible(True)

        self.create_perspective_action = QtWidgets.QAction(
            # self.tr("Create new perspective"),
            self.tr("+"),
            self,
        )
        self.create_perspective_action.triggered.connect(self.createPerspective)
        self.toolbar.addAction(self.create_perspective_action)

        self.clear_perspectives_action = QtWidgets.QAction(
            self.tr("Clear"),
            self,
        )
        self.clear_perspectives_action.triggered.connect(self.clearPerspectives)
        self.toolbar.addAction(self.clear_perspectives_action)

        for perspective in self.perspectives:
            self.addPerspectiveButton(perspective)

        iface.mainWindow().addToolBar(self.toolbar)

        current_perspective = self.currentPerspective()
        if current_perspective is not None:
            self.openPerspective(current_perspective)

    def addPerspectiveButton(self, perspective):
        action = QtWidgets.QAction(perspective.name(), self.toolbar)
        action.triggered.connect(partial(self.openPerspective, perspective))

        self.action_group.addAction(action)

        action.setCheckable(True)
        widget = self.toolbar.widgetForAction(action)
        self.toolbar.insertAction(self.separator, action)

        # self.perspectives_menu.addAction(action)
        # self.tool_button.setText(perspective.name())

        self.actions[perspective.name()] = action

    def createPerspective(self):
        name = self.new_perspective_line_edit.text()
        perspective = self.perspectiveByName(name)
        if perspective is None:
            perspective = Perspective(
                name=name,
                state=iface.mainWindow().saveState(),
            )
            self.perspectives.append(perspective)
            settings.writePerspectives(self.perspectives)
            self.addPerspectiveButton(perspective)
        else:
            perspective.setState(iface.mainWindow().state())
        self.new_perspective_line_edit.clear()
        self.openPerspective(perspective)

    def clearPerspectives(self):
        for action in self.actions.values():
            self.toolbar.removeAction(action)
        self.perspectives = []
        settings.writePerspectives(self.perspectives)

    def openPerspective(self, perspective):
        self.saveCurrentPerspective()
        self.actions[perspective.name()].setChecked(True)
        iface.mainWindow().restoreState(perspective.state())
        settings.setCurrentPerspective(perspective.name())

    def currentPerspective(self):
        return self.perspectiveByName(settings.currentPerspective())

    def perspectiveByName(self, name):
        return next(filter(lambda p: p.name() == name, self.perspectives), None)

    def saveCurrentPerspective(self):
        p = self.currentPerspective()
        if p is None:
            return
        p.setState(iface.mainWindow().saveState())
        settings.writePerspectives(self.perspectives)

    def unload(self):
        if hasattr(self, "toolbar"):
            iface.mainWindow().removeToolBar(self.toolbar)
            self.toolbar.deleteLater()


