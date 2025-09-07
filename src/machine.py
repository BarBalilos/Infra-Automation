from dataclasses import dataclass
from typing import Dict

_ALLOWED_OSES = {
    "ubuntu": "Ubuntu",
    "centos": "CentOS",
}


@dataclass
class Machine:
    name: str
    os: str
    cpu: int    
    ram_gb: int

    def __post_init__(self):
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Machine name cannot be empty.")
        if self.os not in _ALLOWED_OSES.values():
            raise ValueError(f"OS must be one of: {','.join(_ALLOWED_OSES.values())}")
        if not (isinstance(self.cpu, int) and 1 <= self.cpu <= 64):
            raise ValueError("CPU must be an integer between 1 and 64.")
        if not (isinstance(self.ram_gb, int) and 1 <= self.ram_gb <= 512):
            raise ValueError("RAM must be an integer between 1 and 512 GB.")
        
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "os": self.os,
            "cpu": self.cpu,
            "ram_gb": self.ram_gb,
        }


ALLOWED_OSES = _ALLOWED_OSES