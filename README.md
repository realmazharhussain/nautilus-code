# nautilus-code
An extension for Nautilus (GNOME Files) File Manager which adds right-click menu options to open current/selected folder in Code Editors and IDEs like VSCode or GNOME Builder (if they are installed)

## How to install?

### On ArchLinux/Manjaro (and other ArchLinux-based distributions)
This nautilus extension is available in the AUR as [nautilus-code](https://aur.archlinux.org/packages/nautilus-code) and [nautilus-code-git](https://aur.archlinux.org/packages/nautilus-code-git). Use your favorite AUR helper to install it.

### Manual Installation
- Make sure `git`, `meson` and [NautilusPython](https://wiki.gnome.org/Projects/NautilusPython) are installed on your system
- Run the following commands in terminal
  
  ```bash
  git clone --depth=1 https://github.com/realmazharhussain/nautilus-code.git
  cd nautilus-code
  meson setup build
  meson install -C build
  ```

**Note:** To uninstall (if installed manually), run the following command in the same directory where you ran the `meson install` command

```bash
ninja uninstall -C build
```

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
- Android Studio
- Aqua
- CLion
- DataGrip
- DataSpell
- Fleet
- GoLand
- IntelliJ
- MPS
- PhpStorm
- PyCharm
- Rider
- RubyMine
- WebStorm

### Request support for your favorite IDE or Code Editor
You can [open a GitHub issue](https://github.com/realmazharhussain/nautilus-code/issues/new) to request support for your favorite IDE or Code Editor.
