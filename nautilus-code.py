import os
from gi.repository import Nautilus, GObject, GLib

user_data_dir = GLib.get_user_data_dir()


class NamedList (dict):
    def __iter__ (self):
        return self.values().__iter__()

    def names (self):
        return self.keys()


class Package:
    run_command: tuple[str]
    is_installed: bool

    @property
    def type_string (self):
        return self.__class__.__name__

    def __str__ (self):
        return f"{self.type_string}:\n  installed = {self.is_installed}"


class Native (Package):
    cmd_path = ''

    def __init__ (self, *commands):
      self.commands = commands
      for cmd in commands:
        if cmd_path := GLib.find_program_in_path(cmd):
          self.cmd_path = cmd_path
          break

    @property
    def run_command (self) -> tuple[str]:
        '''The command that should be executed in order to
           run a program using this type of package'''
        return (self.cmd_path,)

    @property
    def is_installed (self):
        return bool(self.cmd_path)

    def __str__ (self):
        lines = super().__str__().splitlines()
        if self.cmd_path:
          lines.insert(-1, f"  command = {os.path.basename(self.cmd_path)}")
        elif self.commands:
          lines.insert(-1, f"  command(s) = " + ', '.join(self.commands))
        return  '\n'.join(lines)


class Flatpak (Package):
    flatpak_path = GLib.find_program_in_path('flatpak') or ''
    flatpak_bin_dirs = None

    def __init__ (self, app_id: str):
      self.app_id = app_id
      self._calculate_bin_dirs()

    def _calculate_bin_dirs(self):
        if self.flatpak_bin_dirs is not None:
            return

        if self.__class__.flatpak_bin_dirs is not None:
            self.flatpak_bin_dirs = self.__class__.flatpak_bin_dirs
            return

        self.flatpak_bin_dirs = self.__class__.flatpak_bin_dirs = []

        postfix = '/flatpak/exports/bin'
        for bin_dir in [
          user_data_dir + postfix,
          *os.environ.get('PATH', '').split(':'),
          '/var/lib' + postfix
          ]:
          if (postfix in bin_dir
          and bin_dir not in self.flatpak_bin_dirs):
            self.flatpak_bin_dirs.append(bin_dir)

    @property
    def run_command (self) -> tuple[str]:
        '''The command that should be executed in order to
           run a program using this type of package'''
        return (self.flatpak_path, 'run', self.app_id)

    @property
    def is_installed (self) -> bool:
        if not self.flatpak_path:
            return False

        for bin_dir in self.flatpak_bin_dirs:
            if os.path.exists (os.path.join (bin_dir, self.app_id)):
                return True

        return False

    def __str__ (self):
        lines = super().__str__().splitlines()
        lines.insert(-1, f"  app_id = {self.app_id}")
        return  '\n'.join(lines)


class Edition:
    edition_id: str
    packages: NamedList[Package]

    def __init__ (self, edition_id:str, *packages):
        self.edition_id = edition_id
        self.packages = NamedList()
        for pkg in packages:
            self.add_package(pkg)

    def add_package (self, pkg):
        self.packages[pkg.type_string] = pkg

    def __getitem__ (self, type_string):
        return self.packages[type_string]

    def __str__ (self):
        _str = self.edition_id + ':'
        for pkg in self.packages:
          for line in str(pkg).splitlines():
            _str += '\n  ' + line
        return _str


class Program:
    def __init__ (self, name:str, *packages_and_editions, arguments:list[str]=None):
        self.name = name
        self.arguments = arguments or []
        self.editions = NamedList()
        self._default_edition = Edition('default')

        for item in packages_and_editions:
            if isinstance(item, Package):
                self.add_package(item)
            else:
                self.add_edition(item)

    @property
    def packages (self):
        return self._default_edition.packages

    def add_edition (self, edition):
        self.editions[edition.edition_id] = edition

    def add_package (self, pkg):
        self._default_edition.add_package(pkg)

    def __getitem__ (self, identifier, /):
        if identifier in self.packages.names():
            return self.packages[identifier]
        return self.editions[identifier]

    def __str__ (self):
        _str  =  'Program:'
        _str += f'\n  Name: {self.name}'
        if self.arguments:
          _str += f'\n  Arguments: ' + ' '.join(repr(x) for x in self.arguments)
        _str +=  '\n  Packages:'
        for pkg in self.packages:
          for line in str(pkg).splitlines():
            _str += '\n    ' + line
        if self.editions:
          _str +=  '\n  Editions:'
          for vrt in self.editions:
            for line in str(vrt).splitlines():
              _str += '\n    ' + line
        return _str


code_oss = Program('Code-OSS',
                   Native('code-oss'),
                   Flatpak('com.visualstudio.code-os'))

vscode = Program('VSCode',
                 Flatpak('com.visualstudio.code'),
                 Edition('Insiders',
                         Native('code-insiders')))

if not code_oss['Native'].is_installed:
    vscode.add_package(Native('code'))

vscodium = Program('VSCodium',
                   Native('vscodium', 'codium'),
                   Flatpak('com.vscodium.codium'))

gnome_builder = Program('Builder',
                        Flatpak('org.gnome.Builder'),
                        Native('gnome-builder'),
                        arguments=['--project'])


sublime_text = Program("Sublime Text",
                       Flatpak("com.sublimetext.three"),
                       Native("subl"))

phpstorm = Program("PhpStorm",
                   Flatpak("com.jetbrains.PhpStorm"),
                   Native("phpstorm"),
                   Edition("EAP",
                           Native("phpstorm-eap")))

#class ProgramList (list):
#    def append (self, program):
#        if Program.found_any_package:
#            super().append(prog)
#
#    def __iadd__ (self, prog: Program):
#        self.append(prog)
#
#class NautilusCode (GObject.Object, Nautilus.MenuProvider):
#  def get_background_items (self, *args):
#    current_folder = args[-1]
#
#  def get_file_items (self, *args):
#    selected_files = args[-1]
#    first_selection = selected_files[0]
#
#    if len(selected_files) > 1 or not first_selection.is_directory():
#      return
#
#    return self.get_background_items(first_selection)
