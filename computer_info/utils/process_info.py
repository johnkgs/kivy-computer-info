from typing import List
from psutil import Process, process_iter

from computer_info.types.process_info import ProcessInfoType, MemoryInfoType


class ProcessInfo:
    def __init__(self, pid: int):
        self.process = Process(pid)

    def get_info(self) -> ProcessInfoType:
        return {
            "cpu_affinity": self.process.cpu_affinity(),
            "cpu_percent": self.process.cpu_percent(),
            "num_threads": self.process.num_threads(),
            "memory_percent": self.process.memory_percent(),
            "memory_maps": self.process.memory_maps(),
            "memory_info": self._get_memory_info(),
        }

    def _get_memory_info(self) -> MemoryInfoType:
        memory_info = self.process.memory_info()._asdict()
        return {
            "vms": memory_info["vms"],
            "num_page_faults": memory_info["num_page_faults"],
            "paged_pool": memory_info["paged_pool"],
            "nonpaged_pool": memory_info["nonpaged_pool"],
            "pagefile": memory_info["pagefile"],
            "private": memory_info["private"],
        }

    def get_processes_list():
        iterable_processes = process_iter()
        processes: List[List[str]] = []
        for process in iterable_processes:
            process_info = [str(process.pid), process.name()]
            try:
                cmd = process.cmdline()
                process_info.append(" ".join(cmd))
            except:
                process_info.append("")
            processes.append(process_info)
        return processes
