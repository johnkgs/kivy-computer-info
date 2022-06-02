from typing import List, Union, TypedDict
from psutil._pswindows import pmmap_grouped as MemoryMapGrouped


class MemoryInfoType(TypedDict):
    vms: int
    num_page_faults: int
    paged_pool: int
    nonpaged_pool: int
    pagefile: int
    private: int


class ProcessInfoType(TypedDict):
    cpu_affinity: Union[List[int], None]
    cpu_percent: float
    num_threads: int
    memory_percent: float
    memory_maps: List[MemoryMapGrouped]
    memory_info: MemoryInfoType
