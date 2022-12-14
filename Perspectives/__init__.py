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
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load PerspectivesPlugin class from file PerspectivesPlugin.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PerspectivesPlugin import PerspectivesPlugin

    return PerspectivesPlugin(iface)
