# Main script for rolling project.
import json
import sys
from pathlib import Path
import subprocess


#Project root for further use

project_root = Path(__file__).resolve().parent
    
#----------Paths----------

CONFIGS = project_root / "configs"
LOGS = project_root / "logs"
SCRIPTS = project_root / "scripts"

JSON_PATH = CONFIGS / "instances.json"
TXT_PATH = CONFIGS / "instances.txt"
LOG_FILE = LOGS / "provisioning.log"
INSTALLER = SCRIPTS / "service_installer.sh"

#Ensure directories exist

CONFIGS.mkdir(parents=True, exist_ok=True)
LOGS.mkdir(parents=True, exist_ok=True)
SCRIPTS.mkdir(parents=True, exist_ok=True)


# --- Ensure 'src' is importable even if run from elsewhere ---

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))


#----------Logger----------

from src.logger import setup_logger
infra_logger = setup_logger(LOG_FILE)
infra_logger.info("Logger initiated. Provisioning session starting...")


# --- Input helpers ---

from src.input_helpers import get_vm_details

# --- Save to files (logs only) ---
def save_instances(instances) -> None:
    data = [m.to_dict() for m in instances]
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    TXT_PATH.write_text(
        "\n".join(f"{m.name}: {m.os} | {m.cpu} vCPU | {m.ram_gb} GB RAM" for m in instances),
        encoding="utf-8",
    )
    infra_logger.info("Saved %d instance(s) to %s and %s", len(instances), JSON_PATH, TXT_PATH)

# --- Service installer ---
def run_installer():
    if not INSTALLER.exists():
        infra_logger.error("Installer script not found: %s", INSTALLER)
        raise FileNotFoundError(INSTALLER)

    infra_logger.info("Running installer: %s", INSTALLER)

    process = subprocess.Popen(
        ["bash", str(INSTALLER)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    # stream installer output into the Python logger (ends up in logs/provisioning.log)
    for line in process.stdout:
        line = line.rstrip()
        if line:
            infra_logger.info("[INSTALLER] %s", line)

    process.wait()

    if process.returncode == 0:
        infra_logger.info("Installer completed successfully")
    else:
        infra_logger.error("Installer failed with exit code %s", process.returncode)
        raise subprocess.CalledProcessError(process.returncode, process.args)

# --- Main orchestration ---
if __name__ == "__main__":
    infra_logger.info("=== Session START ===")
    try:
        vms = get_vm_details(infra_logger)   # interactive; re-prompts on invalid input
        if vms:
            save_instances(vms)              # write JSON + TXT
            for vm in vms:
                infra_logger.info("Provisioned VM (simulated): %s", vm.to_dict())

            try:
                run_installer()
            except subprocess.CalledProcessError as e:
                infra_logger.error("Installer failed with exit code %s", e.returncode)
        else:
            infra_logger.info("No machines entered; nothing to save.")
    except KeyboardInterrupt:
        infra_logger.warning("Operation cancelled by user.")
    except Exception as e:
        infra_logger.exception("Unexpected error: %s", e)
    finally:
        infra_logger.info("=== Session END ===")
