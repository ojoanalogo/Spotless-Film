# Building SpotlessFilm Executable

This guide shows you how to create a standalone executable that your friends can run without installing Python.

## Prerequisites

### Install uv (Recommended)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or download from: https://github.com/astral-sh/uv/releases

## Quick Build (Recommended)

1. **Navigate to the project root:**
   ```bash
   cd /path/to/Spotless-Film
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Run the build script:**
   ```bash
   cd src
   uv run python build_executable.py
   ```

The script will:
- ✅ Sync all dependencies with uv
- ✅ Install PyInstaller if needed
- ✅ Clean previous builds
- ✅ Create the executable
- ✅ Package everything in a `distribution/` folder

## Manual Build (Advanced)

If you prefer manual control:

1. **Install dependencies:**
   ```bash
   uv sync
   uv pip install pyinstaller
   ```

2. **Build the executable:**
   ```bash
   cd src
   uv run pyinstaller --clean spotless_film.spec
   ```

## Without uv (pip fallback)

If you don't have uv, the build script will fall back to pip:

```bash
cd src
pip install pyinstaller torch torchvision pillow customtkinter opencv-python numpy tkinterdnd2 tqdm
python build_executable.py
```

## Output Files

After building, you'll find:

### macOS:
- `distribution/SpotlessFilm.app` - The application bundle
- Double-click to run, or drag to Applications folder

### Windows:
- `distribution/SpotlessFilm.exe` - The executable
- Just double-click to run

### Linux:
- `distribution/SpotlessFilm` - The executable
- Make executable: `chmod +x SpotlessFilm`

## Sharing with Friends

1. **Zip the distribution folder:**
   ```bash
   cd distribution
   zip -r SpotlessFilm.zip .
   ```

2. **Send the zip file to your friend**

3. **Your friend should:**
   - Extract the zip file
   - Double-click the executable to run
   - No Python installation needed!

## File Size Expectations

- **macOS**: ~500MB - 1GB (includes all dependencies)
- **Windows**: ~300MB - 800MB
- **Linux**: ~400MB - 900MB

The large size is normal - it includes Python, PyTorch, and all dependencies.

## Troubleshooting

### Build Fails
- Make sure you're in the `src/` directory when running the build script
- Try reinstalling dependencies: `uv sync --reinstall`
- Clean and retry: `rm -rf build dist __pycache__`

### Executable Won't Start
- Run from terminal to see error messages
- Check system requirements (4GB+ RAM recommended)
- Make sure model weights are in the `weights/` folder

### Large File Size
- This is normal for PyTorch applications
- Consider using file compression for distribution
- Size can be reduced by excluding unused dependencies

## Model Weights

**Important**: Make sure your model weights (`.pth` files) are in the `src/weights/` directory before building. The executable will include them automatically.

## Platform-Specific Notes

### macOS
- The app may show "unidentified developer" warning
- Right-click → Open → Open to bypass security warning
- Or run: `sudo xattr -rd com.apple.quarantine SpotlessFilm.app`

### Windows
- Windows Defender may flag the executable initially
- Add exception if needed

### Linux
- Make sure the executable has run permissions
- Some distributions may need additional system libraries

## Advanced Options

Edit `spotless_film.spec` to customize:
- Add application icon
- Include/exclude specific modules
- Adjust console visibility for debugging
- Change app bundle settings

## Development

Run the app directly without building:

```bash
cd /path/to/Spotless-Film
uv run python src/spotless_film_modern.py
```
