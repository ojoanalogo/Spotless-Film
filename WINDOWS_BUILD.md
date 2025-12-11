# Building SpotlessFilm for Windows

## Prerequisites

1. **Install uv** (fast Python package manager):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   Or download from: https://github.com/astral-sh/uv/releases

2. **Python 3.10+** will be automatically managed by uv

## Build Steps

1. **Download the source code** (get the entire project folder)

2. **Open Command Prompt** (cmd) or PowerShell

3. **Navigate to the project root:**
   ```cmd
   cd path\to\Spotless-Film
   ```

4. **Install dependencies and build tools:**
   ```cmd
   uv sync
   uv pip install pyinstaller
   ```

5. **Build the executable:**
   ```cmd
   cd src
   uv run python build_executable.py
   ```

6. **Find the .exe file:**
   - Look in `distribution\SpotlessFilm.exe`
   - This is the Windows executable!

## Alternative: Quick Build (One-liner)

If you have uv installed:
```cmd
cd path\to\Spotless-Film
uv sync && cd src && uv run python build_executable.py
```

## Alternative: Manual PyInstaller Build

If the automated script doesn't work:

```cmd
cd src
uv run pyinstaller --onefile --windowed --name SpotlessFilm spotless_film_modern.py
```

The .exe will be in `dist\SpotlessFilm.exe`

## File Size

Expect ~300-800MB for the Windows executable (includes PyTorch and all dependencies).

## GPU Support

- **NVIDIA GPU**: CUDA support is automatic if you have NVIDIA drivers installed
- **CPU only**: Works fine, just slower processing

## Sharing

Once built, just send the `SpotlessFilm.exe` file - no installation needed!

## Troubleshooting

### uv not found
- Restart your terminal after installing uv
- Or add uv to your PATH manually

### Build fails with missing dependencies
```cmd
uv sync --reinstall
```

### Executable won't start
- Run from command prompt to see error messages:
  ```cmd
  distribution\SpotlessFilm.exe
  ```
