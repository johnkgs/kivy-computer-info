from typing import List, TypedDict


class FrequencyType(TypedDict):
    current: int
    min: int
    max: int


class DiskIOCountersType(TypedDict):
    read_count: int
    write_count: int
    read_bytes: int
    write_bytes: int
    read_time: int
    write_time: int


class DiskUsageType(TypedDict):
    total: int
    used: int
    free: int
    percent: float


class DiskPartitionType(TypedDict):
    device: str
    mountpoint: str
    fstype: str
    opts: str
    maxfile: int
    maxpath: int


class VirtualMemoryType(TypedDict):
    total: int
    available: int
    percent: float
    used: int
    free: int


class SwapMemoryType(TypedDict):
    total: int
    used: int
    free: int
    percent: float
    sin: float
    sout: float


class ComputerInfoType(TypedDict):
    cpu_count: int
    cpu_freq: FrequencyType
    disk_io_counters: DiskIOCountersType
    disk_usage: DiskUsageType
    disk_partitions: List[DiskPartitionType]
    virtual_memory: VirtualMemoryType
    swap_memory: SwapMemoryType
