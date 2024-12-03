#!/usr/bin/env python3

import subprocess
import sys
import importlib
import importlib.metadata

# List of scripts to choose from
scripts = {
    "1": ("Default", "default.py"),
    "2": ("Visual", "visual.py"),
    "3": ("Batch", "fast.py"),
    "4": ("Angles", "angles.py"),
}

# List of required packages for each script
dependencies = {
    "default.py": ["numpy"],
    "visual.py": ["numpy", "matplotlib"],
    "fast.py": ["numpy", "numba"],
    "angles.py": ["numpy", "matplotlib"],
}


def check_dependencies(script_name):
    missing_packages = []
    for package in dependencies.get(script_name, []):
        try:
            # Attempt to get the package version
            version = importlib.metadata.version(package)
            print(f"{package} ({version}) is installed.")
        except importlib.metadata.PackageNotFoundError:
            missing_packages.append(package)
    return missing_packages


def install_packages(packages):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
    except subprocess.CalledProcessError:
        print("Failed to install packages:", ", ".join(packages))
        sys.exit(1)


def main():
    print("Welcome to the Monte Carlo Simulation Menu!")
    print("-------------------------------------------")
    for key, (description, _) in scripts.items():
        print(f"{key}. {description}")
    print("q. Quit")

    choice = input("Please select an option: ").strip()

    if choice.lower() == "q":
        print("Exiting the program.")
        sys.exit(0)

    if choice not in scripts:
        print("Invalid selection. Please try again.")
        sys.exit(1)

    script_description, script_name = scripts[choice]
    print(f"\nYou have selected: {script_description} ({script_name})")

    # Check for missing dependencies
    print("Checking for required dependencies...")
    missing_packages = check_dependencies(script_name)
    if missing_packages:
        print("The following packages are missing or outdated:")
        for pkg in missing_packages:
            print(f"- {pkg}")
        install = (
            input("Would you like to install/update them now? (y/n): ").strip().lower()
        )
        if install == "y":
            print("Installing missing packages...")
            install_packages(missing_packages)
            print("Dependencies installed successfully.")
        else:
            print("Cannot proceed without installing dependencies. Exiting.")
            sys.exit(1)
    else:
        print("All dependencies are satisfied.")

    # Run the selected script
    print(f"Running {script_name}...\n")
    try:
        subprocess.run([sys.executable, script_name])
    except FileNotFoundError:
        print(f"Error: {script_name} not found in the current directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
