from psutil import (
    cpu_count,
    cpu_freq,
    disk_partitions,
    disk_io_counters,
    disk_usage,
    virtual_memory,
    swap_memory,
)
from computer_info.types.computer_info import ComputerInfoType
from computer_info.utils.path import get_root_path


class ComputerInfo:
    def get_info(self) -> ComputerInfoType:
        disk_partitions_list = list(
            map(lambda partition: partition._asdict(), disk_partitions())
        )

        return {
            "cpu_count": cpu_count(),
            "cpu_freq": cpu_freq()._asdict(),
            "disk_io_counters": disk_io_counters()._asdict(),
            "disk_usage": disk_usage(get_root_path())._asdict(),
            "disk_partitions": disk_partitions_list,
            "virtual_memory": virtual_memory()._asdict(),
            "swap_memory": swap_memory()._asdict(),
        }
