import os
import pkg_resources

alternative_packages = {
    "tflite-runtime": ["tensorflow-cpu", "tensorflow"]
}

# Get a list of currently installed packages
installed_distributions = {pkg.key for pkg in pkg_resources.working_set}

with open("requirements.txt", "r") as file:
    installed_packages = []
    for line in file:
        package = line.strip()
        if package:
            # Check if the package is already installed
            if package in installed_distributions:
                print(f"Package {package} is already installed.")
                installed_packages.append(package)
                continue

            success = os.system(f"pip install {package}")
            if success == 0:
                print(f"Successfully installed {package}")
                installed_packages.append(package)
            else:
                print(f"Package {package} failed to install. Trying alternative package...")
                if package in alternative_packages:
                    counter = 0
                    for alternative_package in alternative_packages[package]:
                        success = os.system(f"pip install {alternative_package}")
                        counter += 1
                        if success == 0:
                            print(f"Successfully installed alternative package {alternative_package} for failed package {package}")
                            installed_packages.append(alternative_package)
                            break
                    if counter == len(alternative_packages[package]):
                        print(f"Alternatives for package {package} failed to install.")
                else:
                    print(f"Package {package} failed to install. No alternative packages listed.")

print("All packages installed successfully")
print(f"Installed packages: {installed_packages}")
with open("requirements.txt", "w") as file:
    for package in installed_packages:
        file.write(package + "\n")