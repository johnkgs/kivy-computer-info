from typing import Tuple
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabs, MDTabsBase, MDTabsLabel
from computer_info.screens.computer_info.computer_info_screen import (
    ComputerInfoScreen,
)
from computer_info.screens.processes_info.process_info.process_info_screen import (
    ProcessInfoScreen,
)
from computer_info.screens.processes_info.processes_info_screen import (
    ProcessesInfoScreen,
)

from computer_info.utils.path import get_kv_file_path

screen_manager = ScreenManager()
screen_manager.add_widget(ComputerInfoScreen(name="computer_info"))
screen_manager.add_widget(ProcessesInfoScreen(name="processes_info"))
screen_manager.add_widget(ProcessInfoScreen(name="process_info"))


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Visualizador de informações do computador"
        return Builder.load_file(get_kv_file_path(__file__, "main_screen.kv"))

    def on_start(self):
        self.initialize_widgets()

    def initialize_widgets(self):
        sm: ScreenManager = self.root.ids.screen_manager
        computer_info_screen: ComputerInfoScreen = sm.get_screen(
            "computer_info"
        )
        processes_info_screen: ProcessesInfoScreen = sm.get_screen(
            "processes_info"
        )
        computer_info_screen.set_computer_info_list()
        processes_info_screen.add_processes_data_table_widget()

    def on_tab_switch(
        self,
        instance_tabs: MDTabs,
        instance_tab: MDTabsBase,
        *args: Tuple[MDTabsLabel, str],
    ):
        if instance_tab.name == "computer":
            self.root.ids.screen_manager.current = "computer_info"
            return
        self.root.ids.screen_manager.current = "processes_info"
