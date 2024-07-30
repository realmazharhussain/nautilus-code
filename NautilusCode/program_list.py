from gettext import gettext as _

from .types import ProgramList, Program, Native, Flatpak

progs = ProgramList()

progs += Program('code-oss', _('Code-OSS'),
                 Native('code-oss'),
                 Flatpak('com.visualstudio.code-os'),
                 supports_files=True)

progs += Program('vscode', _('VSCode'),
                 Flatpak('com.visualstudio.code'),
                 supports_files=True)

# Code-OSS also has a binary named 'code'. If Code-OSS is installed, the
# command 'code' refers to Code-OSS instead of Microsoft VSCode. So, in
# that case, we shouldn't show a menu entry for Microsft 'VSCode'.
if not progs['code-oss']['Native'].is_installed:
    progs['vscode'] += Native('code')

progs += Program('code_insiders', _('VSCode (Insiders)'),
                 Native('code-insiders'),
                 Flatpak('com.visualstudio.code.insiders'),
                 supports_files=True)

progs += Program('vscodium', _('VSCodium'),
                 Native('vscodium', 'codium'),
                 Flatpak('com.vscodium.codium'),
                 supports_files=True)

progs += Program('gnome-builder', _('Builder'),
                 Flatpak('org.gnome.Builder'),
                 Native('gnome-builder'),
                 arguments=['--project'])

progs += Program('sublime', _("Sublime"),
                 Flatpak("com.sublimetext.three"),
                 Native("subl"))

progs += Program('android-studio', _('Android Studio'),
                 Native('studio'),
                 Flatpak('com.google.AndroidStudio'))

progs += Program('aqua', _('Aqua'),
                 Native('aqua'))

progs += Program('clion', _('CLion'),
                 Native('clion'),
                 Flatpak('com.jetbrains.CLion'),)

progs += Program('clion-eap', _('CLion (EAP)'),
                 Native('clion-eap'))

progs += Program('datagrip', _('DataGrip'),
                 Native('datagrip'),
                 Flatpak('com.jetbrains.DataGrip'))

progs += Program('datagrip-eap', _('DataGrip (EAP)'),
                 Native('datagrip-eap'))

progs += Program('dataspell', _('DataSpell'),
                 Native('dataspell'))

progs += Program('dataspell-eap', _('DataSpell (EAP)'),
                 Native('dataspell-eap'))

progs += Program('fleet', _('Fleet'),
                 Native('fleet'))

progs += Program('goland', _('GoLand'),
                 Native('goland'),
                 Flatpak('com.jetbrains.GoLand'))

progs += Program('goland-eap', _('GoLand (EAP)'),
                 Native('goland-eap'))

# IntelliJ IDEA has multiple editions that default to the same command but
# prioritise the highest-paying edition. Therefore the native version has been
# treated as a separate program due to the uncertainty around edition.
progs += Program('idea', _('IntelliJ IDEA'),
                 Native('idea'))

progs += Program('idea-eap', _('IntelliJ IDEA (EAP)'),
                 Native('idea-eap'))

progs += Program('idea-community', _('IntelliJ IDEA Community'),
                 Flatpak('com.jetbrains.IntelliJ-IDEA-Community'))

progs += Program('idea-professional', _('IntelliJ IDEA Ultimate'),
                 Flatpak('com.jetbrains.IntelliJ-IDEA-Ultimate'))

progs += Program('mps', _('MPS'),
                 Native('mps'))

progs += Program('phpstorm', _("PhpStorm"),
                 Flatpak("com.jetbrains.PhpStorm"),
                 Native("phpstorm"))

progs += Program('phpstorm-eap', _("PhpStorm (EAP)"),
                 Native("phpstorm-eap"))

# PyCharm has multiple editions that default to the same command but
# prioritise the highest-paying edition. Therefore the native version has been
# treated as a separate program due to the uncertainty around edition.
progs += Program('pycharm', _('PyCharm'),
		 Native('pycharm'))

progs += Program('pycharm-eap', _('PyCharm (EAP)'),
		 Native('pycharm-eap'))

progs += Program('pycharm-professional', _('PyCharm Professional'),
		 Flatpak('com.jetbrains.PyCharm-Professional'))

progs += Program('pycharm-community', _('PyCharm Community'),
		 Flatpak('com.jetbrains.PyCharm-Community'))

progs += Program('rider', _('Rider'),
                 Native('rider'),
                 Flatpak('com.jetbrains.Rider'))

progs += Program('rubymine', _('RubyMine'),
                 Native('rubymine'),
                 Flatpak('com.jetbrains.RubyMine'))

progs += Program('rubymine-eap', _('RubyMine (EAP)'),
                 Native('rubymine-eap'))

progs += Program('webstorm', _('WebStorm'),
                 Native('webstorm'),
                 Flatpak('com.jetbrains.WebStorm'))

progs += Program('webstorm-eap', _('WebStorm (EAP)'),
                 Native('webstorm-eap'))

progs += Program('zed', _('Zed'),
                 Native('zeditor', 'zedit'),
                 Flatpak('dev.zed.Zed'))
