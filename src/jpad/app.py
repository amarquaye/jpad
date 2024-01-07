"""
Text editor written using beeware!
"""
import toga
from toga import Key
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.style.pack import *


class Jpad(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        main_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        toga.Font.register("MerriWeather", "resources/fonts/Merriweather-Regular.ttf")
        # Main box for typing 
        text_box = toga.Box(style=Pack(flex=1))
        self.typing_area = toga.MultilineTextInput(style=Pack(flex=1, font_family="MerriWeather", font_size=11))
        main_scroll = toga.ScrollContainer(content=self.typing_area, style=Pack(flex=1))
        
        text_box.add(main_scroll)
        
        # Add groups and commands 
        self.file_group = toga.Group("File")
        # New 
        self.new_file_command = toga.Command(self.new_file_func, text="New", tooltip="New File",
                                        shortcut=Key.MOD_1+Key.N, group=self.file_group)
        # New Window 
        self.new_window_command = toga.Command(self.new_window_func, text="New Window", tooltip="Open New Window",
                                          shortcut=Key.MOD_1+Key.SHIFT+Key.N, group=self.file_group)
        # Save As 
        self.save_as_command = toga.Command(self.save_as_func, text="Save As...", tooltip="Save file as...",
                                       shortcut=Key.MOD_1+Key.S, group=self.file_group)
        # Open 
        self.open_file_command = toga.Command(self.open_file_func, text="Open...", tooltip="Open file",
                                         shortcut=Key.MOD_1+Key.O, group=self.file_group)
        
        # Add widgets 
        main_box.add(text_box)
        
        # Configurations 
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.toolbar.add(self.new_file_command, self.new_window_command, self.save_as_command, self.open_file_command)
        self.main_window.content = main_box
        self.main_window.show()
        
    def new_file_func(self, widget):
        """Function to create a new or empty file"""
        self.typing_area.value = ""
        self.main_window.title = "Jpad"
        
        
    
    async def new_window_func(self, widget):
        """Function to open a new window for typing"""
        self.new_window = toga.Window(title="Jpad")
        # Features to be used on new windows 
        main_box = toga.Box(style=Pack(flex=1, direction=COLUMN))
        toga.Font.register("MerriWeather", "resources/fonts/Merriweather-Regular.ttf")
        # Main box for typing 
        text_box = toga.Box(style=Pack(flex=1))
        typing_area = toga.MultilineTextInput(style=Pack(flex=1, font_family="MerriWeather", font_size=11))
        main_scroll = toga.ScrollContainer(content=typing_area, style=Pack(flex=1))
        text_box.add(main_scroll)
        main_box.add(text_box)
        
        # Add groups and commands 
        self.file_group = toga.Group("File")
        # New 
        # DeprecationWarning 
        # Removed new file command since it only works on the main window(app) and has no effect on the current window 
        # self.new_file_command = toga.Command(self.new_file_func, text="New", tooltip="New File",
        #                                 shortcut=Key.MOD_1+Key.N, group=self.file_group)
        # New Window 
        self.new_window_command = toga.Command(self.new_window_func, text="New Window", tooltip="Open New Window",
                                          shortcut=Key.MOD_1+Key.SHIFT+Key.N, group=self.file_group)
        # Save As 
        self.save_as_command = toga.Command(self.save_as_func, text="Save As...", tooltip="Save file as...",
                                       shortcut=Key.MOD_1+Key.S, group=self.file_group)
        # Open 
        self.open_file_command = toga.Command(self.open_file_func, text="Open...", tooltip="Open file",
                                         shortcut=Key.MOD_1+Key.O, group=self.file_group)
        
        self.new_window.toolbar.add(self.new_window_command, self.save_as_command, self.open_file_command)
        self.new_window.content = main_box 
        self.new_window.show()
     
    async def save_as_func(self, widget):
        """Function to display save as dialog and save file"""
        self.file_name = await self.main_window.save_file_dialog(title="Save As", suggested_filename="Untitled.txt",
                                                                 file_types=["txt", "py", "cpp", 'c', "js"])
        try:
            with open(self.file_name, "w") as fn:
                contents = fn.write(self.typing_area.value)
            # Do nothing if user doesn't open any file 
            if self.file_name is None:
                pass
        except Exception as e:
            self.main_window.error_dialog(title="Unexpected Error",
                                          message="An error prevented your file from being saved.\nPlease try again!")
            
    async def open_file_func(self, widget):
        """Function to open file contents in textarea"""
        self.file_to_open = await self.main_window.open_file_dialog(title="Select file to open")
        try:
            # Open file contents 
            with open(self.file_to_open, "r") as rf:
                content = rf.read()
            self.typing_area.value = content
            self.main_window.title = f"{self.file_to_open} - Jpad" 
            # Do nothing if user doesn't open any file 
            if self.file_to_open is None:
                pass
        except Exception as e:
            self.main_window.error_dialog(title="Unexpected Error", 
                                          message="An error prevented your file from opening.\nPlease try again!")


def main():
    return Jpad()
