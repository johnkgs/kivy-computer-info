from functools import partial
from typing import Any, Callable, Dict, List, Tuple, Union
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

from computer_info.utils.computer_info import ComputerInfo


class ComputerInfoContent(MDBoxLayout):
    def __init__(self, **kwargs):
        data: Union[Dict, List[Dict]] = kwargs.get("data")
        super().__init__()

        if isinstance(data, list):
            for info in data:
                partition_key = f"Partition {info['device']}"
                items = {partition_key: str(info)}.items()
                self.add_row_widgets(items)
            return

        self.add_row_widgets(data)

    def add_row_widgets(self, items: Tuple[str, Any]):
        for (
            key,
            value,
        ) in items:
            self.add_widget(
                TwoLineListItem(
                    text=key,
                    secondary_text=str(value),
                )
            )


class ComputerInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.computer_info = ComputerInfo()

    def on_pre_leave(self, *args):
        if hasattr(self, "error"):
            self.remove_widget(self.error)

    def set_computer_info_list(self):
        try:
            for info_key, info_value in self.computer_info.get_info().items():
                if info_key == "cpu_count":
                    self.add_row_widget(info_key, str(info_value))
                    continue
                self.fork(self.add_expandable_row_widget, info_key, info_value)
        except:
            self.add_error_widget()

    def add_error_widget(self):
        self.error = MDLabel(
            text="Um erro inesperado aconteceu!",
            halign="center",
            theme_text_color="Error",
        )
        self.add_widget(self.error)

    def add_row_widget(self, info_key: str, info_value: str):
        row = TwoLineListItem(
            _txt_left_pad=0,
            text=info_key,
            secondary_text=info_value,
        )
        self.ids.computer_info_box.add_widget(row)

    def add_expandable_row_widget(
        self, info_key: str, info_value: Union[Dict, List[Dict]], *args
    ):
        data = (
            info_value if isinstance(info_value, list) else info_value.items()
        )

        content = ComputerInfoContent(data=data)
        expandable_row = MDExpansionPanel(
            content=content,
            panel_cls=MDExpansionPanelOneLine(
                text=info_key,
            ),
        )
        self.ids.computer_info_box.add_widget(expandable_row)

    def fork(self, function: Callable, *args):
        Clock.schedule_once(partial(function, *args), 0.1)
