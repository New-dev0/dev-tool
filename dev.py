import sys
import os
import subprocess

from devtemplate import TEMPLATE

if len(sys.argv) < 2:
    print("❌ No Arguments were provided.")
    sys.exit()

_default = "-y" in sys.argv

if "create" in sys.argv:
    files = [
        "main.py",
        ("requirements.txt", "python-decouple"),
        ("settings.ini", "[settings]"),
    ]

    if "heroku" in sys.argv:
        if "docker" in sys.argv:
            files.append(("Dockerfile", "FROM python:latest"))
        else:
            files.extend(
                [
                    ("Procfile", "worker: python main.py"),
                    ("runtime.txt", "python-3.10.6"),
                ]
            )
    elif len(sys.argv) > 1 and sys.argv[2] in list(TEMPLATE.keys()):

        files[0] = (
            "main.py",
            TEMPLATE[sys.argv[2]],
        )
    for file in files:
        content = ""
        if isinstance(file, tuple):
            file, content = file
        if os.path.exists(file):
            ask = (
                _default
                if _default is True
                else input(f"{file} already exists. OverWrite y/N? ").lower()
                in ["y", "yes"]
            )
            if not ask:
                continue
        with open(file, "w") as f:
            f.write(content)

    print("✅ Created template.")
elif "install" in sys.argv:
    try:
        package = sys.argv[sys.argv.index("install") + 1:]
    except IndexError:
        print("😵 Package name was not provided.")
        sys.exit()
    subprocess.run(["pip", "install", "-U", *package])
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "a") as file:
            file.write("\n".join(package))
    print("Completed Task!")
elif "run" in sys.argv:
    get = sys.argv.index("run")
    try:
        file = os.path.abspath(sys.argv[get + 1])
    except IndexError:
        print("❌ File not specified.")
        sys.exit()
    notify =  "--notify" in sys.argv
    if notify:
        try:
            import pyttsx3
        except ImportError:
            pyttsx3 = None
            print("😵 pyttsx3 is not installed!")
            notify = False
    cmds = ["python"]
    if os.path.isdir(file):
        cmds.append("-m")
    cmds.append(file)
    process = subprocess.run(cmds)
    if notify:
        pyttsx3.speak(f"Command Execution finished with return code {process.returncode}.")
