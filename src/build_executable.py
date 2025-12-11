#!/usr/bin/env python3
"""
Build script for creating SpotlessFilm executable
This script handles the entire build process including dependency checks.
Supports both uv (preferred) and pip as fallback.
"""

import subprocess
import sys
import os
import shutil
from pathlib import Path


def has_uv():
    """Check if uv is available"""
    try:
        subprocess.run(["uv", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(cmd, check=True):
    """Run a command and return success status"""
    try:
        subprocess.check_call(cmd)
        return True
    except subprocess.CalledProcessError:
        return False


def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        print("✅ PyInstaller is already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        if has_uv():
            run_command(["uv", "pip", "install", "pyinstaller"])
        else:
            run_command([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")


def check_dependencies():
    """Check and install required dependencies"""
    required_packages = [
        "torch",
        "torchvision",
        "pillow",
        "customtkinter",
        "opencv-python",
        "numpy",
        "tkinterdnd2",
        "tqdm"
    ]

    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        if has_uv():
            run_command(["uv", "pip", "install"] + missing_packages)
        else:
            run_command([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ All dependencies installed")


def sync_dependencies():
    """Sync dependencies using uv if available (preferred method)"""
    if has_uv():
        print("📦 Syncing dependencies with uv...")
        # Check if we're in project root or src directory
        project_root = Path(__file__).parent.parent
        if (project_root / "pyproject.toml").exists():
            result = subprocess.run(
                ["uv", "sync"],
                cwd=project_root,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print("✅ Dependencies synced with uv")
                return True
            else:
                print(f"⚠️  uv sync failed, falling back to manual install")
                print(result.stderr)
    return False


def clean_build():
    """Clean previous build artifacts"""
    dirs_to_clean = ["build", "dist", "__pycache__"]
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"🧹 Cleaning {dir_name}...")
            shutil.rmtree(dir_name)


def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")

    # Check if we're on Windows, macOS, or Linux
    import platform
    system = platform.system()

    # Determine the pyinstaller command
    if has_uv():
        cmd_prefix = ["uv", "run"]
    else:
        cmd_prefix = []

    if system == "Darwin":  # macOS
        print("🍎 Building for macOS...")
        cmd = cmd_prefix + ["pyinstaller", "--clean", "spotless_film.spec"]
    elif system == "Windows":
        print("🪟 Building for Windows...")
        cmd = cmd_prefix + ["pyinstaller", "--clean", "spotless_film.spec"]
    else:  # Linux
        print("🐧 Building for Linux...")
        cmd = cmd_prefix + ["pyinstaller", "--clean", "spotless_film.spec"]

    try:
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")

        # Show output location
        if system == "Darwin":
            print("📦 App bundle created: dist/SpotlessFilm.app")
        else:
            print(f"📦 Executable created: dist/SpotlessFilm{'.exe' if system == 'Windows' else ''}")

    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

    return True


def create_distribution():
    """Create a distribution folder with all necessary files"""
    print("📂 Creating distribution package...")

    # Create distribution directory
    dist_dir = Path("distribution")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Copy executable/app
    import platform
    system = platform.system()

    if system == "Darwin":
        # Copy the .app bundle
        if Path("dist/SpotlessFilm.app").exists():
            shutil.copytree("dist/SpotlessFilm.app", dist_dir / "SpotlessFilm.app")
    else:
        # Copy the executable
        exe_name = f"SpotlessFilm{'.exe' if system == 'Windows' else ''}"
        if Path(f"dist/{exe_name}").exists():
            shutil.copy2(f"dist/{exe_name}", dist_dir / exe_name)

    # Copy model weights if they exist
    weights_dir = Path("weights")
    if weights_dir.exists():
        shutil.copytree(weights_dir, dist_dir / "weights")
        print("📦 Model weights included")

    # Create README for distribution
    readme_content = """# SpotlessFilm - AI-Powered Dust Removal

## Quick Start
1. Double-click the SpotlessFilm executable to launch the application
2. Click "Choose Image" to load a photo with dust/scratches
3. Click "Detect Dust" to identify dust particles
4. Use brush/eraser tools to refine the dust mask if needed
5. Click "Remove Dust" to clean the image
6. Click "Export" to save the cleaned image

## System Requirements
- 4GB+ RAM recommended
- GPU support optional but recommended for faster processing

## Troubleshooting
- If the app doesn't start, try running it from terminal/command prompt to see error messages
- Make sure your system has sufficient RAM and disk space
- Contact support if you encounter issues

Generated with PyInstaller
"""

    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme_content)

    print(f"✅ Distribution package created in: {dist_dir}")


def main():
    """Main build process"""
    print("🚀 Starting SpotlessFilm executable build process...")
    print(f"📍 Working directory: {os.getcwd()}")

    # Check package manager
    if has_uv():
        print("📦 Using uv package manager (fast)")
    else:
        print("📦 Using pip package manager (uv not found)")

    # Check if we're in the right directory
    if not os.path.exists("spotless_film_modern.py"):
        print("❌ Error: spotless_film_modern.py not found!")
        print("Please run this script from the src/ directory")
        return

    try:
        # Step 1: Try to sync with uv first (if pyproject.toml exists)
        if not sync_dependencies():
            # Fallback to manual dependency check
            check_dependencies()

        # Step 2: Check PyInstaller
        check_pyinstaller()

        # Step 3: Clean previous builds
        clean_build()

        # Step 4: Build executable
        if build_executable():
            # Step 5: Create distribution package
            create_distribution()
            print("\n🎉 Build process completed successfully!")
            print("📦 Your executable is ready for distribution")
        else:
            print("\n❌ Build process failed")

    except KeyboardInterrupt:
        print("\n⚠️  Build process interrupted by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
