import pyglet
import pyglet.gl as gl

from grid import Grid
from configuration import Configuration
from ui import UI
import rules


class App(pyglet.window.Window):
    def __init__(self, width=1280, height=720):
        super().__init__(width, height, "Cellular Automata", resizable=False, config=gl.Config(factor=True))#, config=gl.Config(double_buffer=True))
        pyglet.clock.schedule_interval(self.update, 1/60)
        self.set_vsync(True)

        self.settings = Configuration()

        self.gui = UI(self, self.settings)
        self.gui.center = (self.width / 2, self.height / 2)

        self.set_minimum_size(300, 200)
        gl.glOrtho(0, width, 0, height, 0, 1)
        gl.glClearColor(self.settings.bg_color[0], self.settings.bg_color[1], self.settings.bg_color[2], 1)

        self.grid = Grid(self.settings, self)
        self.ruleset = rules.ConwayLife()

        self.step_count = 0.0

        self.placing = False
        self.removing = False
        self.placing_value = 1
        self.prev_mouse_cell = (0, 0)
        self.just_pressed = 0

        self.mouse_pos = (0, 0)

    def step(self):
        self.grid = self.ruleset.step(self.grid)
        self.grid.draw_cells()

    def on_resize(self, w, h):
        gl.glViewport(0, 0, w, h)
        self.grid.w_x, self.grid.w_y = w, h
        self.grid.draw_cells()
        self.gui.render_count = self.grid.cell_count
        self.gui.center = (self.width / 2, self.height / 2)

    def on_draw(self):
        pass
        # self.flip()

    def update(self, dt):
        if self.gui.quit:
            pyglet.app.exit()

        self.gui.render_count = self.grid.cell_count
        self.gui.fps = round(pyglet.clock.get_fps(), 2)
        self.gui.update_time = round(dt * 1000)
        if self.grid.cells_updated:
            self.gui.cells_updated = "Yes"
            self.grid.cells_updated = False
        else:
            self.gui.cells_updated = "No"

        if self.gui.update_grid:
            self.grid.draw_cells()
            self.gui.update_grid = False

        # if self.gui.change_grid_color:
        #     if self.settings.show_grid:
        #         gl.glClearColor(self.settings.grid_color[0], self.settings.grid_color[1], self.settings.grid_color[2], 1)
        #     else:
        #         gl.glClearColor(self.settings.cell_color_off[0], self.settings.cell_color_off[1], self.settings.cell_color_off[2], 1)

        if self.gui.clear_board:
            self.grid.clear()
            self.gui.clear_board = False

        if self.gui.step:
            self.step()
            self.gui.step = False

        if self.gui.stepping:
            for i in range(0, self.settings.steps_per_frame):
                self.step_count += dt
                if self.step_count >= 1 / self.settings.step_speed:
                    self.step()
                    self.step_count = 0.0

        self.gui.update()
        self.grid.update(self.mouse_pos)

        # Only allow placing/removing if the UI is not focused
        if self.gui.focus:
            self.placing = self.removing = False

        if self.just_pressed >= 3:
            if self.placing:
                self.grid.set_cell(self.gui.mouse_pos, self.placing_value)
            if self.removing:
                self.grid.set_cell(self.gui.mouse_pos, 0)
            self.just_pressed = 0
        if self.just_pressed >= 1:
            self.just_pressed += 1

        # Clear the screen, dispatch events to prevent lag
        self.clear()
        self.dispatch_events()

        # -- Draw to the screen -- #
        # Must go in update() to prevent UI flickering
        self.grid.cell_batch.draw()
        if self.settings.show_grid:
            self.grid.line_batch.draw()
        self.gui.render()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.H and modifiers & pyglet.window.key.MOD_CTRL:
            print("Hiding GUI..." if self.gui.show_gui else "Showing GUI...")
            self.gui.show_gui = not self.gui.show_gui
        if symbol == pyglet.window.key.M and modifiers & pyglet.window.key.MOD_CTRL:
            print("Hiding Menu..." if self.gui.show_gui else "Showing Menu...")
            self.gui.show_menu = not self.gui.show_menu

        if symbol == pyglet.window.key.Q and modifiers & pyglet.window.key.MOD_CTRL:
            self.gui.exit()

        if symbol == pyglet.window.key.S and modifiers & pyglet.window.key.MOD_CTRL:
            pass

        if symbol == pyglet.window.key.ESCAPE and modifiers & pyglet.window.key.MOD_CTRL:
            self.gui.show_clear_modal = True

        if symbol == pyglet.window.key.SPACE:
            self.gui.stepping = not self.gui.stepping

    def on_key_release(self, symbol, modifiers):
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        self.gui.mouse_pos = self.grid.screen_to_cell((x, y))
        self.prev_mouse_cell = self.gui.mouse_pos
        self.grid.mouse_pos = (x, y)
        self.mouse_pos = (x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.gui.mouse_pos = self.grid.screen_to_cell((x, y))
        self.mouse_pos = (x, y)
        if self.gui.focus:
            return
        if not self.prev_mouse_cell == self.gui.mouse_pos:
            if self.placing:
                self.grid.set_cell(self.grid.screen_to_cell((x, y)), self.placing_value)
            if self.removing:
                self.grid.set_cell(self.grid.screen_to_cell((x, y)), 0)
        if buttons & pyglet.window.mouse.MIDDLE:
            self.grid.pan_offset((dx, dy))
            # self.grid.update_line_offset()

    def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if self.gui.focus:
            return
        self.grid.inc_zoom(1 + (scroll_y * self.settings.zoom_speed))

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            self.removing = False
            self.placing = True
        elif button == pyglet.window.mouse.RIGHT:
            self.placing = False
            self.removing = True
        self.just_pressed = 1

    def on_mouse_release(self, x, y, button, modifiers):
        self.just_pressed = 0
        self.placing = False
        self.removing = False
