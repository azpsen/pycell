import pyglet


class Camera(pyglet.graphics.Group):
    def __init__(self, window):
        super().__init__()
        self.win = window
        self.offset = (0, 0)
        self.zoom = 1

    def set_offset(self, offset):
        self.offset = offset

    def set_zoom(self, zoom):
        self.zoom = zoom

    def set_state(self):
        pyglet.gl.glPushMatrix()
        x, y = self.offset[0], self.offset[1]
        pyglet.gl.glTranslatef(x, y, 0.0)
        pyglet.gl.glScalef(self.zoom, self.zoom, 1.0)

    def unset_state(self):
        pyglet.gl.glPopMatrix()
