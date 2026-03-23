import json
import subprocess
import sys
from pathlib import Path

# -----------------------------
# Project paths
# -----------------------------
project_root = Path(__file__).resolve().parent

CONFIGS = project_root / "configs"
LOGS = project_root / "logs"
SCRIPTS = project_root / "scripts"

JSON_PATH = CONFIGS / "instances.json"
TXT_PATH = CONFIGS / "instances.txt"
LOG_FILE = LOGS / "provisioning.log"
INSTALLER = SCRIPTS / "service_installer.sh"

# Ensure required folders exist
CONFIGS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
SCRIPTS.mkdir(parents=True, exist_ok=True)

# Ensure src package is importable
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.input_helpers import get_vm_details
from src.logger import setup_logger

infra_logger = setup_logger(LOG_FILE)


def save_instances(instances) -> None:
    """
    Saves machine data into:
    1. configs/instances.json
    2. configs/instances.txt
    """
    data = [machine.to_dict() for machine in instances]

    with open(JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    TXT_PATH.write_text(
        "\n".join(
            f"{machine.name}: {machine.os} | {machine.cpu} vCPU | {machine.ram_gb} GB RAM"
            for machine in instances
        ),
        encoding="utf-8",
    )

    infra_logger.info(
        "Saved %d instance(s) to %s and %s",
        len(instances),
        JSON_PATH,
        TXT_PATH,
    )


def run_installer() -> None:
    """
    Runs the Bash installer script using subprocess.
    Logs script output into the Python log.
    """
    if not INSTALLER.exists():
        infra_logger.error("Installer script not found: %s", INSTALLER)
        raise FileNotFoundError(f"Installer script not found: {INSTALLER}")

    infra_logger.info("Running installer script: %s", INSTALLER)

    process = subprocess.Popen(
        ["bash", str(INSTALLER)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    if process.stdout is not None:
        for line in process.stdout:
            line = line.rstrip()
            if line:
                infra_logger.info("[INSTALLER] %s", line)

    process.wait()

    if process.returncode == 0:
        infra_logger.info("Installer completed successfully.")
    else:
        infra_logger.error("Installer failed with exit code %s", process.returncode)
        raise subprocess.CalledProcessError(process.returncode, process.args)


def main() -> None:
    infra_logger.info("=== Provisioning session START ===")

    try:
        machines = get_vm_details(infra_logger)

        if not machines:
            infra_logger.info("No machines entered. Nothing to provision.")
            print("No machines were entered.")
            return

        save_instances(machines)

        for machine in machines:
            infra_logger.info("Provisioned VM (simulated): %s", machine.to_dict())

        run_installer()

        print("\nProvisioning completed successfully.")
        print(f"JSON saved to: {JSON_PATH}")
        print(f"TXT saved to:  {TXT_PATH}")
        print(f"Logs saved to: {LOG_FILE}")

    except KeyboardInterrupt:
        infra_logger.warning("Operation cancelled by user.")
        print("\nOperation cancelled by user.")

    except subprocess.CalledProcessError as exc:
        infra_logger.exception("Subprocess execution failed: %s", exc)
        print("\nInstaller failed. Check logs/provisioning.log for details.")

    except Exception as exc:
        infra_logger.exception("Unexpected error: %s", exc)
        print("\nUnexpected error occurred. Check logs/provisioning.log for details.")

    finally:
        infra_logger.info("=== Provisioning session END ===")


if __name__ == "__main__":
    main()