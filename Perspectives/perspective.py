class Perspective():
    def __init__(self, name, state):
        self._name = name
        self._state = state

    def name(self):
        return self._name

    def setName(self, value):
        self._name = value

    def state(self):
        return self._state

    def setState(self, value):
        self._state = value

    def __str__(self):
        return f"Perspective(name={self._name})"
