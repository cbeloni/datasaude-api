class DrawConter:
    def __init__(self):
        self._counter = 0

    @property
    def draw(self):
        self._counter += 1
        return self._counter