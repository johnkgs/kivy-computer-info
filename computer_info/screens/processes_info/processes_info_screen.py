from typing import List
from kivy.metrics import dp
from kivy.input.providers.mouse import (
    MouseMotionEvent,
)
from kivymd.uix.screen import Screen
from kivymd.uix.datatables import (
    MDDataTable,
    CellRow,
    TableData,
)
from kivymd.uix.label import MDLabel

from computer_info.utils.decorators.debounce import (
    debounce,
)
from computer_info.utils.process_info import (
    ProcessInfo,
)

column_header = [
    ["PID", dp(32)],
    ["Nome", dp(48)],
    ["Linha de comando", dp(1200)],
]

row_data = ProcessInfo.get_processes_list()


class ProcessesInfoScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def filter(
        self,
        text: str,
        data: List[List[str]],
    ):
        new_data: List[List[str]] = []
        for item in data:
            line = " ".join(item)
            if text.lower() in line.lower():
                new_data.append(item)
        return new_data

    @debounce(0.1)
    def set_processes_list(self, text="", search=False):
        if search:
            if len(text) > 0:
                self.data_table.row_data = self.filter(text, row_data)
                return

            self.data_table.row_data = row_data

    def add_processes_data_table_widget(
        self,
    ):
        self.data_table = MDDataTable(
            rows_num=32,
            use_pagination=True,
            pagination_menu_pos="auto",
            column_data=column_header,
            row_data=row_data,
        )

        pagination_label: MDLabel = self.data_table.pagination.children[-1]
        pagination_label.text = "Linhas por página"

        self.data_table.bind(on_row_press=self.on_row_press)
        self.ids.recycle_view.add_widget(self.data_table)

    def on_row_press(
        self,
        instance_table: MDDataTable,
        instance_row: CellRow,
    ):
        last_touch: MouseMotionEvent = instance_row.last_touch

        if not last_touch.is_double_tap:
            return

        table: TableData = instance_row.table
        (start_index, end_index,) = table.recycle_data[
            instance_row.index
        ]["range"]
        pid = table.recycle_data[start_index]["text"]
        name = table.recycle_data[end_index - 1]["text"]
