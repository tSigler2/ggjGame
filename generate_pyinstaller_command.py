import os

# Base directory where your project resides
base_dir = "GameLib"

# File extensions to include in the bundle
include_extensions = (
    ".png",
    ".jpg",
    ".jpeg",
    ".mp3",
    ".wav",
    ".ttf",
    ".otf",
    ".py",
)  # Add more if needed

# Collect all assets with their paths
assets = []
for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith(include_extensions):
            # Full path of the file
            full_path = os.path.join(root, file)
            # Relative path for PyInstaller
            relative_path = os.path.relpath(full_path, base_dir)
            # Add-data format: "source;destination"
            assets.append(
                f'"{full_path};{os.path.join(".", os.path.dirname(relative_path))}"'
            )

# Generate the PyInstaller command
assets_str = " ".join([f"--add-data {asset}" for asset in assets])
command = f"pyinstaller --onefile {assets_str} {os.path.join(base_dir, 'Main.py')}"

# Output the command
print("Run the following command to build your project:")
print(command)
