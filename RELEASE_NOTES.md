# Hopplo 1.0.1

## What's new

- Added automated GitHub Releases packaging for Linux, Windows, and macOS
- Added a PyInstaller release build configuration
- Fixed bundled-app resource loading for `LICENSE` and `version.txt`
- Fixed update checking to use the correct GitHub Releases API endpoint
- Improved update downloads by selecting the most relevant asset for the current platform

## Release process

```bash
git add .
git commit -m "Prepare 1.0.1 release build"
git tag v1.0.1
git push origin main
git push origin v1.0.1
```
