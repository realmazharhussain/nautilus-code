# nautilus-code (legacy)
An extension for Nautilus (GNOME Files) File Manager (version 42 and earlier) which adds right-click menu options to open current/selected folder in Code Editors and IDEs like VSCode or GNOME Builder (if they are installed)

## How to install?
- Make sure `wget`, `tar`, `gz`, `meson` and `libnautilus-extension` are installed on your system
- Run the following commands in terminal
  
  ```bash
  wget https://github.com/realmazharhussain/nautilus-code/archive/legacy.tar.gz -O nautilus-code-legacy.tar.gz
  tar xf nautilus-code-legacy.tar.gz
  cd nautilus-code-legacy
  meson setup build
  meson install -C build
  ```

**Note:** To uninstall (if installed manually) just remove the file `/usr/lib/nautilus/extensions-3.0/libnautilus-code.so`.

## Supported Code Editors and IDEs

### Currently Supported
**Note:** Both native and flatpak versions of these apps are supported.

- GNOME Builder
- VSCode
  - Official/Proprietary version from Microsoft
  - Insiders
  - VSCodium
  - Code - OSS
- Sublime Text
- PhpStorm

### Request support for your favorite IDE or Code Editor
You can [create a GitHub issue](https://github.com/realmazharhussain/nautilus-code/issues/new) to request support for your favorite IDE or Code Editor.
