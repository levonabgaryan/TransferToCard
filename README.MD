# 🚀 Getting Started

## 1. ✅ Install Python

Download and install **Python for Windows** from the official site:  
👉 [https://www.python.org/downloads/](https://www.python.org/downloads/)

Make sure to install **Python 3.13 or higher** and check the option **“Add Python to PATH”** during installation.

---

## 2. 📦 Create and Activate Virtual Environment

Open a terminal (**PowerShell** or **Command Prompt**) and run:

```bash
    python3.13 -m venv .venv
```

Then activate the virtual environment:
CMD
```bash
    .venv\Scripts\activate.bat
```

POWERSHELL
```bash
    .venv\Scripts\Activate.ps1
```

⚠️ If you get a permission error in PowerShell, run:
```bash
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
🧐 How to check if the virtual environment is activated
When the virtual environment is activated successfully, your terminal prompt will show the environment name as a prefix, like this
```
(.venv) C:\path\to\your\project>
```

## 3. 📥 Install Dependencies
```bash
    pip install -r requirements.txt
```

## 4. ⚙️ Set Environment Variables
Create a .env file by copying the template:

1) copy env_template .env
2) Open .env and fill in the required variables.

## 5. ▶️ Run the Application
```bash
    python main.py
```