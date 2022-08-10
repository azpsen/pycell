import statistics

import imgui
import imgui.core
from imgui.integrations.pyglet import create_renderer
import array


class UI:
    def __init__(self, window, config):

        self.config = config

        # Initial GUI setup
        imgui.create_context()
        self.renderer = create_renderer(window)
        imgui.new_frame()
        imgui.end_frame()

        # Set font
        io = imgui.get_io()
        io.fonts.clear()
        io.fonts.add_font_from_file_ttf(self.config.font, 14, )
        self.renderer.refresh_font_texture()

        self.update_font = False
        self.current_font = 2
        self.font_sizes = ["8", "11", "14", "16", "18", "24", "32", "48"]

        self.center = (0, 0)

        # Window visibility variables
        self.show_stats = False
        self.show_parameters = False
        self.show_controls = True
        self.show_settings = False
        self.show_demo = False

        self.show_save_quit_modal = False
        self.show_save_modal = False
        self.show_clear_modal = False

        self.show_menu = True
        self.show_gui = True

        self.file_saved = False
        self.ask_next = True

        # Window variables
        self.render_count = 0
        self.fps_history = array.array('f', [0])
        self.fps = 0
        self.avg_fps = 0
        self.update_history = array.array('f', [0])
        self.update_time = 0
        self.avg_update = 0
        self.cells_updated = "No"
        self.mouse_pos = (0, 0)
        self.focus = False

        # App signals
        self.update_grid = False
        self.change_grid_color = False
        self.quit = False
        self.clear_board = False
        self.step = False
        self.stepping = False
        self.step_freq = 1

    def update(self):
        """
        Mainly used to update statistic values (FPS, update time, etc.)
        :return:
        """
        if self.show_stats:
            self.fps_history.append(self.fps)
            if len(self.fps_history) <= 100:
                self.avg_fps = round(statistics.mean(self.fps_history), 2)
            if len(self.fps_history) > 100:
                self.avg_fps = round((len(self.fps_history) * self.avg_fps - self.fps_history[0]
                                      + self.fps_history[-1]) / len(self.fps_history), 2)
                self.fps_history = self.fps_history[1:]
            self.update_history.append(self.update_time)
            if len(self.update_history) <= 100:
                self.avg_update = round(statistics.mean(self.update_history))
            if len(self.update_history) > 100:
                self.avg_update = round((len(self.update_history) * self.avg_update - self.update_history[0]
                                         + self.update_history[-1]) / len(self.update_history))
                self.update_history = self.update_history[1:]

    def render(self):
        """
        Draws GUI elements to the screen
        :return:
        """
        imgui.render()
        self.renderer.render(imgui.get_draw_data())
        imgui.new_frame()

        if self.show_menu:
            if imgui.begin_main_menu_bar():
                if imgui.begin_menu("File"):
                    if imgui.menu_item("New Sheet", "Ctrl+N")[0]:
                        pass
                    if imgui.menu_item("Save Cells...", "Ctrl+S")[0]:
                        pass
                    imgui.separator()
                    _, self.show_settings = imgui.menu_item("Settings", None, self.show_settings)
                    imgui.separator()
                    if imgui.menu_item("Quit", "Ctrl+Q")[0]:
                        self.exit()
                    imgui.end_menu()
                if imgui.begin_menu("Edit"):
                    if imgui.menu_item("Undo", "Ctrl+Z")[0]:
                        pass
                    if imgui.menu_item("Redo", "Ctrl+Y")[0]:
                        pass
                    imgui.separator()
                    if imgui.menu_item("Clear", "Ctrl+Esc")[0]:
                        self.show_clear_modal = True
                    if imgui.begin_menu("Rules"):
                        if imgui.menu_item("Conway's Game of Life", None, True):
                            pass
                        imgui.end_menu()
                    imgui.end_menu()
                if imgui.begin_menu("View"):
                    _, self.config.show_grid = imgui.menu_item("Show Grid", None, self.config.show_grid)
                    imgui.separator()
                    if imgui.begin_menu("Tool Windows"):
                        _, self.show_stats = imgui.menu_item("Stats", None, self.show_stats)
                        _, self.show_parameters = imgui.menu_item("Parameters", None, self.show_parameters)
                        _, self.show_controls = imgui.menu_item("Controls", None, self.show_controls)
                        _, self.show_demo = imgui.menu_item("Demo Window", None, self.show_demo)
                        imgui.end_menu()
                    if imgui.begin_menu("Appearance"):
                        _, self.show_gui = imgui.menu_item("Tool Windows", "Ctrl+H", self.show_gui)
                        _, self.show_menu = imgui.menu_item("Menu Bar", "Ctrl+M", self.show_menu)
                        imgui.end_menu()
                    imgui.end_menu()
                imgui.separator()
                imgui.text(str(self.mouse_pos))
                imgui.end_main_menu_bar()

        if not self.show_gui:
            return

        if self.show_stats:
            _, self.show_stats = imgui.begin("Statistics", closable=True)
            imgui.text("Rendered Cells: " + str(self.render_count))
            imgui.text("FPS: " + str(self.fps))
            imgui.plot_lines("avg: " + str(self.avg_fps), self.fps_history)
            imgui.text("Update Duration: " + str(self.update_time) + "ms")
            imgui.plot_lines("avg: " + str(self.avg_update) + "ms", self.update_history)
            imgui.text("Cells Updated? " + self.cells_updated)
            imgui.text("Any window focused? " + str(self.focus))
            imgui.text("Stepping? " + str(self.stepping))

            imgui.end()

        if self.show_parameters:
            _, self.show_parameters = imgui.begin("Parameters", closable=True)

            imgui.text("Test text")

            imgui.end()

        if self.show_controls:
            _, self.show_controls = imgui.begin("Controls", closable=True)

            if imgui.button("Step"):
                self.step = True
            imgui.same_line()
            if imgui.button("Start/Stop"):
                self.stepping = not self.stepping
            if imgui.is_item_hovered():
                imgui.set_tooltip("Space")
            _, self.config.step_speed = imgui.slider_int("Steps / Second", self.config.step_speed,
                                                         min_value=self.config.min_step,
                                                         max_value=self.config.max_step)
            _, self.config.steps_per_frame = imgui.slider_int("Steps / Frame", self.config.steps_per_frame,
                                                              min_value=self.config.min_step_per_frame,
                                                              max_value=self.config.max_step_per_frame)
            imgui.end()

        if self.show_settings:
            _, self.show_settings = imgui.begin("Settings", closable=True)

            _, self.config.ask_clear = imgui.checkbox("Ask Before Clearing", self.config.ask_clear)
            if not self.show_clear_modal and not self.config.ask_clear == self.ask_next:
                self.ask_next = self.config.ask_clear

            changed, self.current_font = imgui.combo("Font Size", self.current_font, self.font_sizes)
            if changed:
                self.update_font = True

            imgui.end()

        if self.show_demo:
            imgui.show_demo_window()

        if self.show_save_quit_modal:
            imgui.open_popup("Save Changes?")
            imgui.set_next_window_position(self.center[0], self.center[1], imgui.APPEARING, 0.5, 0.5)
            if imgui.begin_popup_modal("Save Changes?", True,
                                       imgui.WINDOW_ALWAYS_AUTO_RESIZE |
                                       imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_MOVE):
                imgui.text("Save changes to your open sheet?")
                if imgui.button("Save"):
                    imgui.close_current_popup()
                    self.show_save_quit_modal = False
                    self.show_save_modal = True
                imgui.same_line()
                if imgui.button("Discard"):
                    self.quit = True
                imgui.same_line()
                if imgui.button("Cancel"):
                    imgui.close_current_popup()
                    self.show_save_quit_modal = False
            imgui.end_popup()

        if self.show_save_modal:
            imgui.open_popup("Save...")
            imgui.set_next_window_position(self.center[0], self.center[1], imgui.APPEARING, 0.5, 0.5)
            if imgui.begin_popup_modal("Save..."):#, True, imgui.WINDOW_ALWAYS_AUTO_RESIZE | imgui.WINDOW_NO_MOVE):
                imgui.text("Save Changes")
            imgui.end_popup()

        if self.show_clear_modal:
            if self.config.ask_clear:
                imgui.open_popup("Clear?")
                imgui.set_next_window_position(self.center[0], self.center[1], imgui.APPEARING, 0.5, 0.5)
                if imgui.begin_popup_modal("Clear?"):
                    imgui.text("Clear the entire board?")
                    _, self.ask_next = imgui.checkbox("Ask every time", self.ask_next)
                    if imgui.button("Clear"):
                        self.clear_board = True
                        imgui.close_current_popup()
                        self.show_clear_modal = False
                        if not self.ask_next == self.config.ask_clear:
                            self.config.ask_clear = self.ask_next
                    imgui.same_line()
                    if imgui.button("Cancel"):
                        imgui.close_current_popup()
                        self.show_clear_modal = False
                imgui.end_popup()
            else:
                self.show_clear_modal = False
                self.clear_board = True

        self.focus = imgui.is_window_focused(imgui.FOCUS_ANY_WINDOW)

        imgui.end_frame()

        if self.update_font:
            io = imgui.get_io()
            io.fonts.clear()
            io.fonts.add_font_from_file_ttf(self.config.font, int(self.font_sizes[self.current_font]), )
            self.renderer.refresh_font_texture()
            self.update_font = False

    def exit(self):
        if self.file_saved:
            self.quit = True
            return
        self.show_save_quit_modal = True
