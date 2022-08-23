from qgis.PyQt.QtCore import QSettings

from Perspectives.perspective import Perspective


class Settings():

    GROUP = 'PerspectivesPlugin'

    def __init__(self):
        self._qsettings = QSettings()
        self._qsettings.beginGroup(self.GROUP)

    def currentPerspective(self):
        return self._qsettings.value("currentPerspective")

    def setCurrentPerspective(self, value):
        self._qsettings.setValue("currentPerspective", value)

    def writePerspectives(self, perspectives):
        self._qsettings.beginGroup("perspectives")
        self._qsettings.remove("")
        self._qsettings.endGroup()

        self._qsettings.beginWriteArray("perspectives", len(perspectives))
        for i, perspective in enumerate(perspectives):
            self._qsettings.setArrayIndex(i)
            self._qsettings.setValue("name", perspective.name())
            self._qsettings.setValue("state", perspective.state())
        self._qsettings.endArray()

    def readPerspectives(self):
        perspectives = []
        count = self._qsettings.beginReadArray("perspectives")
        for i in range(count):
            self._qsettings.setArrayIndex(i)
            perspectives.append(
                Perspective(
                    name=self._qsettings.value("name"),
                    state=self._qsettings.value("state"),
                )
            )
        self._qsettings.endArray()
        return perspectives


settings = Settings()
