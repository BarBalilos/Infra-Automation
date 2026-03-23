# 🚀 Infra-Automation

A Python-based **infrastructure provisioning simulator** for a DevOps rolling project.

This project simulates infrastructure provisioning by allowing users to define virtual machines (VMs), validate them using **Pydantic**, save configurations, and execute a Bash script to install and configure Nginx.

Future stages will integrate **AWS** and **Terraform** for real infrastructure automation.

---

## ✨ Features

- 🖥️ Interactive VM creation  
- ✅ Validation using **Pydantic** (strict typing & constraints)  
- 🏗️ Object-oriented design with a `Machine` class  
- 📝 JSON and TXT configuration output  
- ⚙️ Bash-based Nginx installation  
- 🔗 Python `subprocess` integration  
- 📊 Central logging (`logs/provisioning.log`)  
- 🛡️ Error handling in both Python and Bash  

---

## 📂 Project Structure

```text
infra-automation/
├── configs/
│   ├── instances.json
│   └── instances.txt
├── logs/
│   └── provisioning.log
├── scripts/
│   └── service_installer.sh
├── src/
│   ├── __init__.py
│   ├── input_helpers.py
│   ├── logger.py
│   └── machine.py
├── infra_simulator.py
├── README.md
└── requirements.txt
```

---

## 📦 Requirements

### 🐍 Python
- Python 3.10+
- pydantic>=2.0.0,<3.0.0

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### 💻 System Requirements

| OS | Requirement |
|----|------------|
| Linux / macOS | Bash shell (default) |
| Windows | Git Bash or WSL (Ubuntu recommended) |

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/BarBalilos/Infra-Automation.git
cd Infra-Automation
```

---

### 2. Create virtual environment

#### Linux / macOS / WSL
```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

---

### 3. Run the simulator

```bash
python infra_simulator.py
```

---

## 🧪 Example Input

```text
Machine name (or 'done'): web-server
OS (Ubuntu/CentOS): Ubuntu
CPU (integer only, 1-64): 2
RAM in GB (integer only, 1-512): 4
```

---

## 📄 Example JSON Output

**configs/instances.json**

```json
[
  {
    "name": "web-server",
    "os": "Ubuntu",
    "cpu": 2,
    "ram_gb": 4
  }
]
```

---

## 📄 Example TXT Output

**configs/instances.txt**

```text
web-server: Ubuntu | 2 vCPU | 4 GB RAM
```

---

## 📊 Example Logs

**logs/provisioning.log**

```text
2026-03-21 12:00:00 | INFO | === Provisioning session START ===
2026-03-21 12:00:12 | INFO | Machine created: web-server (Ubuntu, 2 vCPU, 4 GB RAM)
2026-03-21 12:00:20 | INFO | Running installer script
2026-03-21 12:00:25 | INFO | Installer completed successfully
```

---

## 🧠 Validation Rules

- CPU: integer (1–64)
- RAM: integer (1–512)
- OS: Ubuntu / CentOS only
- No duplicate machine names

✔ Validation is handled using **Pydantic models**.

---

## 🚀 Future Enhancements

- ☁️ AWS EC2 provisioning
- 🏗️ Terraform integration
- 🔧 Additional services (DB, monitoring, etc.)
- 📥 Load configs from external files

---

## 📖 Notes

- Logs are stored in `logs/provisioning.log`
- Both Python and Bash scripts include logging
- This is a **simulation project** (no real VMs yet)
- Designed for **easy extension in future DevOps stages**
