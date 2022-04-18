# nautilus-code
An extension for Nautilus (GNOME Files) File Manager which adds right-click menu options to open current folder in VSCode or GNOME Builder

## How to install/use?

### On ArchLinux/Manjaro (and other ArchLinux-based distributions)
This nautilus extension is available in the AUR as `nautilus-code` and `nautilus-code-git`. Use your favorite AUR helper to install it.

### Manual Installation
- Make sure `git`, `meson` and `libnautilus-extension` are installed on your system
- Run the following commands in terminal
  
  ```bash
  git clone --depth=1 https://github.com/realmazharhussain/nautilus-code.git
  cd nautilus-code
  meson build
  sudo meson install -C build
  ```