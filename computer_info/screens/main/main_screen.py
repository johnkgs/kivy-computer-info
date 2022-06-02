from typing import Tuple
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.tab import MDTabs, MDTabsBase, MDTabsLabel

from computer_info.utils.path import get_kv_file_path


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        self.title = "Visualizador de informações do computador"
        return Builder.load_file(get_kv_file_path(__file__, "main_screen.kv"))

    def on_tab_switch(
        self,
        instance_tabs: MDTabs,
        instance_tab: MDTabsBase,
        *args: Tuple[MDTabsLabel, str],
    ):
        pass
