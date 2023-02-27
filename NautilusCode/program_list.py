from gettext import gettext as _

from .types import ProgramList, Program, Native, Flatpak

progs = ProgramList()

progs += Program('code-oss', _('Code-OSS'),
                 Native('code-oss'),
                 Flatpak('com.visualstudio.code-os'))

progs += Program('vscode', _('VSCode'),
                 Flatpak('com.visualstudio.code'))

# Code-OSS also has a binary named 'code'. If Code-OSS is installed, the
# command 'code' refers to Code-OSS instead of Microsoft VSCode. So, in
# that case, we shouldn't show a menu entry for Microsft 'VSCode'.
if not progs['code-oss']['Native'].is_installed:
    progs['vscode'] += Native('code')

progs += Program('code_insiders', _('VSCode (Insiders)'),
                 Native('code-insiders'),
                 Flatpak('com.visualstudio.code.insiders'))

progs += Program('vscodium', _('VSCodium'),
                 Native('vscodium', 'codium'),
                 Flatpak('com.vscodium.codium'))

progs += Program('gnome-builder', _('Builder'),
                 Flatpak('org.gnome.Builder'),
                 Native('gnome-builder'),
                 arguments=['--project'])

progs += Program('sublime', _("Sublime"),
                 Flatpak("com.sublimetext.three"),
                 Native("subl"))

progs += Program('phpstorm', _("PhpStorm"),
                 Flatpak("com.jetbrains.PhpStorm"),
                 Native("phpstorm"))

progs += Program('phpstorm-eap', _("PhpStorm (EAP)"),
                 Native("phpstorm-eap"))
