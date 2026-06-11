import json
import os
from gettext import gettext as _

from gi.repository import Nautilus
from gi.repository import GLib


user_data_dir = GLib.get_user_data_dir()


class NamedList (dict):
    def __iter__ (self):
        return self.values().__iter__()

    @property
    def names (self):
        return self.keys()


class Priority:
    '''Named priority levels for package deduplication.  Higher value wins on
     an identity collision, so the base default (FALLBACK) is the lowest and
     any package type added without an explicit priority safely loses.  Values
     are spaced so new levels can be slotted in between without renumbering.'''
    FALLBACK = 0
    NORMAL = 10
    PREFERRED = 20


class Package:
    run_command: tuple[str]
    is_installed: bool
    type_name = _('Unknown')
    priority = Priority.FALLBACK
    show_type_name = True

    def menu_label (self, program_name, *, disambiguate=False):
        '''Build the menu label for launching `program_name` via this package.
           When `disambiguate` is set (more than one install of the program is
           shown) and this package type wants it, the type name is appended so
           the entries can be told apart.'''
        label = _('Open in %s') % program_name
        if disambiguate and self.show_type_name:
            label += f' ({self.type_name})'
        return label

    @property
    def identity (self):
        '''The set of values that identify the actual program being launched.
           Each package describes only itself; two installed packages are
           considered the same install when their identity sets intersect.  On
           a collision the one with the higher priority wins and the other is
           dropped by _dedupe.  Return an empty set to opt out of dedup.'''
        return frozenset()

    @property
    def type_name_raw (self):
        return self.__class__.__name__

    def __str__ (self):
        return f"{self.type_name}:\n  installed = {self.is_installed}"


class Native (Package):
    type_name = _('Native')
    priority = Priority.PREFERRED
    show_type_name = False
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

    @property
    def identity (self):
        '''The real executable this command resolves to.  Knows nothing about
           any other package type; it is up to e.g. Toolbox to declare that it
           also owns a launcher on PATH that resolves here.'''
        if not self.cmd_path:
            return frozenset()
        return frozenset({os.path.realpath(self.cmd_path)})

    def __str__ (self):
        lines = super().__str__().splitlines()
        if self.cmd_path:
          lines.insert(-1, f"  command = {os.path.basename(self.cmd_path)}")
        elif self.commands:
          lines.insert(-1, f"  command(s) = " + ', '.join(self.commands))
        return  '\n'.join(lines)


class Toolbox (Package):
    type_name = _('Toolbox')
    toolbox_dir = os.path.join(user_data_dir, 'JetBrains', 'Toolbox')
    state_file = os.path.join(toolbox_dir, 'state.json')
    settings_file = os.path.join(toolbox_dir, '.settings.json')
    _tools = None
    _scripts_dir = None

    @classmethod
    def _load_tools (cls):
        if cls._tools is None:
            try:
                with open(cls.state_file, encoding='utf-8') as f:
                    cls._tools = json.load(f).get('tools', []) or []
            except (OSError, ValueError):
                cls._tools = []
        return cls._tools

    @classmethod
    def scripts_dir (cls):
        '''Directory where Toolbox writes the shell-script launchers it adds
           to PATH. The location is user-configurable in Toolbox settings and
           defaults to the "scripts" folder next to state.json.'''
        if cls._scripts_dir is None:
            cls._scripts_dir = os.path.normpath(cls._read_scripts_location())
        return cls._scripts_dir

    @classmethod
    def _read_scripts_location (cls):
        '''Read the configured shell-scripts location from Toolbox settings,
           falling back to the default "scripts" folder next to state.json
           when the settings file is missing, unreadable, or unset.'''
        default = os.path.join(cls.toolbox_dir, 'scripts')
        try:
            with open(cls.settings_file, encoding='utf-8') as f:
                settings = json.load(f)
        except (OSError, ValueError):
            return default
        return (settings.get('shell_scripts') or {}).get('location') or default

    def __init__ (self, *tool_ids):
      self.tool_ids = tool_ids
      self.launch_command = ''
      self.install_location = ''
      for tool in self._load_tools():
        if tool.get('toolId') in tool_ids:
          cmd = tool.get('launchCommand', '')
          if cmd and os.path.exists(cmd):
            self.launch_command = cmd
            self.install_location = tool.get('installLocation', '')
            break

    @property
    def run_command (self) -> tuple[str]:
        '''The command that should be executed in order to
           run a program using this type of package'''
        return (self.launch_command,)

    @property
    def is_installed (self) -> bool:
        return bool(self.launch_command)

    @property
    def identity (self):
        '''The launcher executable plus every launcher Toolbox dropped on PATH
           that points at this install.  By declaring the PATH launchers it
           owns, a Native command that resolves to one of them collides with
           this entry without Native needing to know Toolbox exists.'''
        if not self.launch_command:
            return frozenset()
        ids = {os.path.realpath(self.launch_command)}
        ids.update(self._owned_scripts())
        return frozenset(ids)

    def _owned_scripts (self):
        '''Real paths of launchers in the Toolbox scripts dir that start this
           install.  Toolbox writes either a symlink into the install dir or a
           wrapper shell script that execs the launchCommand, so both forms are
           recognised here.'''
        owned = set()
        install = os.path.realpath(self.install_location) if self.install_location else ''
        try:
            entries = list(os.scandir(self.scripts_dir()))
        except OSError:
            return owned
        for entry in entries:
            real = os.path.realpath(entry.path)
            # Symlink launcher resolving into this install dir.
            if install and (real == install or real.startswith(install + os.sep)):
                owned.add(real)
                continue
            # Wrapper script launcher that execs this install's launchCommand.
            try:
                with open(entry.path, encoding='utf-8', errors='ignore') as f:
                    if self.launch_command in f.read():
                        owned.add(real)
            except OSError:
                pass
        return owned

    def __str__ (self):
        lines = super().__str__().splitlines()
        if self.launch_command:
          lines.insert(-1, f"  command = {self.launch_command}")
        elif self.tool_ids:
          lines.insert(-1, f"  tool_id(s) = " + ', '.join(self.tool_ids))
        return  '\n'.join(lines)


class Flatpak (Package):
    type_name = _('Flatpak')
    priority = Priority.FALLBACK
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

    @property
    def identity (self):
        # Flatpak apps are sandboxed; their identity can never collide with a
        # filesystem path used by Native or Toolbox packages.
        return frozenset({('flatpak', self.app_id)})

    def __str__ (self):
        lines = super().__str__().splitlines()
        lines.insert(-1, f"  app_id = {self.app_id}")
        return  '\n'.join(lines)


class Program:
    def __init__ (self, id:str, name:str, *packages, arguments:list[str]=None, supports_files=False):
        self.id = id
        self.name = name
        self.arguments = arguments or []
        self.supports_files = supports_files
        self.packages = NamedList()
        for pkg in packages:
            self.add(pkg)

    @property
    def installed_packages (self):
        pkgs = []
        for pkg in self.packages:
            if pkg.is_installed:
                pkgs.append(pkg)
        return self._dedupe(pkgs)

    @staticmethod
    def _dedupe (pkgs):
        '''Remove packages that are merely a different "view" of an install
           already represented by another package, so the same IDE is not
           offered twice in the menu.

           Each Package subclass declares an `identity` set (the things it
           launches) and a `priority` (which representation wins on a
           collision).  Two installed packages are duplicates when their
           identity sets intersect; the lower-priority one is dropped.  An
           empty identity set never collides with anything.'''
        kept = []
        kept_identities = []
        for pkg in sorted(pkgs, key=lambda p: -p.priority):
            ident = pkg.identity
            if ident and any(ident & seen for seen in kept_identities):
                continue
            kept.append(pkg)
            if ident:
                kept_identities.append(ident)
        return [p for p in pkgs if p in kept]

    def add (self, pkg):
        self.packages[pkg.type_name_raw] = pkg
        return self

    def __iadd__ (self, pkg):
        return self.add(pkg)

    def __getitem__ (self, type_name_raw):
        return self.packages[type_name_raw]

    def __str__ (self):
        _str  =  'Program:'
        _str += f'\n  Id: {self.id}'
        _str += f'\n  Name: {self.name}'
        if self.arguments:
          _str += f'\n  Arguments: ' + ' '.join(repr(x) for x in self.arguments)
        for pkg in self.packages:
          for line in str(pkg).splitlines():
            _str += '\n  ' + line
        return _str


class ProgramList (NamedList):

    @staticmethod
    def _activate_item (item, command: list[str]):
        pid, *io = GLib.spawn_async(command)
        GLib.spawn_close_pid(pid)

    def get_menu_items (self, path, *, id_prefix='', is_file=False):
        items = []

        for program in self:
            if is_file and not program.supports_files:
                continue

            installed_pkgs = program.installed_packages
            include_type_name = True if len(installed_pkgs) > 1 else False
            for pkg in installed_pkgs:

                name = id_prefix + program.id
                command = [*pkg.run_command, *program.arguments, path]
                label = pkg.menu_label(program.name, disambiguate=include_type_name)

                item = Nautilus.MenuItem.new(name, label)
                item.connect('activate', self._activate_item, command)
                items.append(item)

        return items

    def __iadd__ (self, value, /):
        self[value.id] = value
        return self
