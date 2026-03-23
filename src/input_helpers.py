from logging import Logger
from typing import List

from pydantic import ValidationError

from src.machine import Machine


def get_vm_details(logger: Logger) -> List[Machine]:
    """
    Interactively collects VM data from the user.
    Validation is performed by the Pydantic Machine model.
    """
    vms: List[Machine] = []
    seen_names = set()

    logger.info("Interactive VM entry started. Type 'done' as machine name to finish.")

    while True:
        name = input("Machine name (or 'done'): ").strip()

        if name.lower() == "done":
            break

        if name in seen_names:
            logger.warning("Duplicate machine name '%s'. Re-asking.", name)
            print("Machine name already exists. Please enter a unique name.")
            continue

        os_name = input("OS (Ubuntu/CentOS): ").strip()
        cpu = input("CPU (integer only, 1-64, e.g. 2): ").strip()
        ram_gb = input("RAM in GB (integer only, 1-512, e.g. 4): ").strip()

        raw_data = {
            "name": name,
            "os": os_name,
            "cpu": cpu,
            "ram_gb": ram_gb,
        }

        try:
            vm = Machine(**raw_data)
            vms.append(vm)
            seen_names.add(vm.name)
            logger.info(vm.log_creation_message())
            print(f"Added: {vm.name}")
        except ValidationError as exc:
            logger.error("Validation failed for VM input: %s", raw_data)

            for err in exc.errors():
                field_name = ".".join(str(x) for x in err["loc"])
                logger.error("Field '%s': %s", field_name, err["msg"])
                print(f"Invalid {field_name}: {err['msg']}")

            print("Please try entering the machine again.\n")

    logger.info("Interactive VM entry finished. Total machines: %d.", len(vms))
    return vms