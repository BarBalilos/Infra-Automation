from typing import List
from src.machine import Machine, ALLOWED_OSES
from logging import Logger

def _ask_nonempty(prompt: str, logger: Logger) -> str:
    while True:
        val = input(prompt).strip()
        if val:
            return val
        logger.warning("Empty value for '%s'. Re-asking.", prompt)

def _ask_choice_os(prompt: str, logger: Logger) -> str:
    while True:
        raw = input(prompt).strip().lower()
        if raw in ALLOWED_OSES:
            return ALLOWED_OSES[raw]
        match = next((canon for k, canon in ALLOWED_OSES.items() if raw and k.startswith(raw)), None)
        if match:
            return match
        logger.warning("Invalid OS '%s'. Allowed: %s. Re-asking.",
                       raw, ", ".join(ALLOWED_OSES.values()))
        
def _ask_int_range(prompt: str, min_v: int, max_v: int, logger: Logger) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if min_v <= val <= max_v:
                return val
            logger.warning("Out-of-range value %s for '%s'. Allowed %s..%s. Re-asking.",
                           val, prompt, min_v, max_v)
        except ValueError:
            logger.warning(
                "Invalid input '%s' for '%s'. Must be an integer only (no units like 'GB' or 'vCPU'). Re-asking.",
                raw, prompt
            )
        

def get_vm_details(logger: Logger) -> List[Machine]:
    vms: List[Machine] = []
    seen_names = set()

    logger.info("Interactive VM entry started. Type 'done' as machine name to finish.")
    while True:
        name = input("Machine name (or 'done'): ").strip()
        if name.lower() == "done":
            break
        if not name:
            logger.warning("Machine name empty. Re-asking.")
            continue
        if name in seen_names:
            logger.warning("Duplicate machine name '%s'. Re-asking.", name)
            continue

        os_name = _ask_choice_os("OS (Ubuntu/CentOS): ", logger)
        cpu     = _ask_int_range("CPU (integer only, 1–64, e.g., 2): ", 1, 64, logger)
        ram_gb  = _ask_int_range("RAM in GB (integer only, 1–512, e.g., 4): ", 1, 512, logger)

        try:
            vm = Machine(name=name, os=os_name, cpu=cpu, ram_gb=ram_gb)
        except ValueError as ve:
            logger.error("Construction error for VM %s/%s/%s/%s -> %s",
                         name, os_name, cpu, ram_gb, ve)
            continue

        vms.append(vm)
        seen_names.add(name)
        logger.info("Added VM: %s | %s | %s vCPU | %s GB RAM",
                    vm.name, vm.os, vm.cpu, vm.ram_gb)

    logger.info("Interactive VM entry finished. Total machines: %d.", len(vms))
    return vms

