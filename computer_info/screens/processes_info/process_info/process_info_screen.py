from functools import partial
from typing import Callable, Dict, List, Union
from psutil import AccessDenied
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.screen import Screen
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.tab import MDTabs
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp

from computer_info.screens.processes_info.processes_info_screen import (
    ProcessesInfoScreen,
)
from computer_info.utils.process_info import ProcessInfo


class ProcessInfoContent(MDBoxLayout):
    def __init__(self, **kwargs):
        data: Union[Dict, List[Dict]] = kwargs.get("data")
        type: str = kwargs.get("type")
        super().__init__()
        for (info_key, info_value) in data:
            self.fork(self.add_content, info_key, str(info_value), type)

    def add_content(self, info_key: str, info_value: str, type: str, *args):
        text = info_key if type == "memory_info" else f"Caminho: {info_key}"
        secondary_text = (
            info_value if type == "memory_info" else f"RSS: {info_value}"
        )
        self.add_widget(
            TwoLineListItem(
                text=text,
                secondary_text=secondary_text,
            )
        )

    def fork(self, function: Callable, *args):
        Clock.schedule_once(partial(function, *args), 0.1)


class ProcessInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.set_process_info_list()

    def on_pre_enter(self, *args):
        self.ids.spinner.active = True

        header = MDApp.get_running_app().root.ids.header
        self.toolbar: MDToolbar = header.ids.toolbar
        self.tabs: MDTabs = header.ids.tabs

        processes_info_screen: ProcessesInfoScreen = self.manager.get_screen(
            "processes_info"
        )

        pid = processes_info_screen.process_pid
        name = processes_info_screen.process_name

        self.process_info = ProcessInfo(pid)
        self.change_header(name, pid)

    def hide_widget(self, widget, do_hide=True):
        if hasattr(widget, "saved_attributes"):
            if not do_hide:
                (
                    widget.height,
                    widget.opacity,
                    widget.disabled,
                ) = widget.saved_attributes
                del widget.saved_attributes
        elif do_hide:
            saved_attributes = (widget.height, widget.opacity, widget.disabled)
            widget.saved_attributes = saved_attributes
            values = (0, 0, True)
            widget.height, widget.opacity, widget.disabled = values

    def change_header(self, name: str, pid: int):
        self.toolbar.title = f"{name} - PID: {pid}"
        self.toolbar.left_action_items = [
            [
                "arrow-left",
                lambda x: self.navigation_back(x),
            ]
        ]
        self.hide_widget(self.tabs)

    def change_header_back(self, *args):
        self.toolbar.title = "Informações"
        self.toolbar.left_action_items = []
        self.hide_widget(self.tabs, False)

    def on_pre_leave(self, *args):
        self.change_header_back()
        self.ids.process_info_box.clear_widgets()

        if hasattr(self, "error"):
            self.remove_widget(self.error)

    def navigation_back(self, *args):
        self.manager.current = "processes_info"

    def set_process_info_list(self):
        try:
            for info_key, info_value in self.process_info.get_info().items():
                if info_key not in ["memory_maps", "memory_info"]:
                    self.add_row_widget(info_key, str(info_value))
                    continue
                self.add_expandable_row_widget(info_key, info_value)

        except AccessDenied:
            self.ids.spinner.active = False
            self.add_error_widget()

        finally:
            self.ids.spinner.active = False

    def add_error_widget(self):
        self.error = MDLabel(
            text="Você não tem acesso para visualizar esse processo!",
            halign="center",
            theme_text_color="Error",
        )
        self.add_widget(self.error)

    def add_expandable_row_widget(
        self, info_key: str, info_value: Union[Dict, List[Dict]], *args
    ):
        data = (
            info_value if isinstance(info_value, list) else info_value.items()
        )

        content = ProcessInfoContent(data=data, type=info_key)
        expandable_row = MDExpansionPanel(
            content=content,
            panel_cls=MDExpansionPanelOneLine(
                text=info_key,
            ),
        )
        self.ids.process_info_box.add_widget(expandable_row)

    def add_row_widget(self, info_key: str, info_value: str):
        row = TwoLineListItem(
            _txt_left_pad=0,
            text=info_key,
            secondary_text=info_value,
        )
        self.ids.process_info_box.add_widget(row)
