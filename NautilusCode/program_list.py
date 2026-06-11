from gettext import gettext as _

from .types import ProgramList, Program, Native, Flatpak, Toolbox

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

progs += Program('codium_insiders', _('VSCodium (Insiders)'),
                 Native('vscodium-insiders', 'codium-insiders'),
                 Flatpak('com.vscodium.codium-insiders'),
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

progs += Program('air', _('Air'),
                 Native('air'),
                 Toolbox('Air'))

progs += Program('aqua', _('Aqua'),
                 Native('aqua'),
                 Toolbox('Aqua'))

progs += Program('clion', _('CLion'),
                 Native('clion'),
                 Flatpak('com.jetbrains.CLion'),
                 Toolbox('CLion'))

progs += Program('clion-eap', _('CLion (EAP)'),
                 Native('clion-eap'))

progs += Program('cursor', _('Cursor'),
                 Native('cursor'))

progs += Program('datagrip', _('DataGrip'),
                 Native('datagrip'),
                 Flatpak('com.jetbrains.DataGrip'),
                 Toolbox('DataGrip'))

progs += Program('datagrip-eap', _('DataGrip (EAP)'),
                 Native('datagrip-eap'))

progs += Program('dataspell', _('DataSpell'),
                 Native('dataspell'),
                 Toolbox('DataSpell'))

progs += Program('dataspell-eap', _('DataSpell (EAP)'),
                 Native('dataspell-eap'))

progs += Program('fleet', _('Fleet'),
                 Native('fleet'),
                 Toolbox('Fleet'))

progs += Program('goland', _('GoLand'),
                 Native('goland'),
                 Flatpak('com.jetbrains.GoLand'),
                 Toolbox('GoLand'))

progs += Program('goland-eap', _('GoLand (EAP)'),
                 Native('goland-eap'))

# IntelliJ IDEA has multiple editions that default to the same command but
# prioritise the highest-paying edition. Therefore the native version has been
# treated as a separate program due to the uncertainty around edition.
# Toolbox uses one toolId per product and cannot cleanly separate EAP from
# stable, so only the stable entry carries the Toolbox toolId.
progs += Program('idea', _('IntelliJ IDEA'),
                 Native('idea'),
                 Toolbox('IntelliJ-IDEA', 'IntelliJIdea', 'IDEA', 'IDEA-U', 'IDEA-C'))

progs += Program('idea-eap', _('IntelliJ IDEA (EAP)'),
                 Native('idea-eap'))

progs += Program('idea-community', _('IntelliJ IDEA Community'),
                 Flatpak('com.jetbrains.IntelliJ-IDEA-Community'))

progs += Program('idea-professional', _('IntelliJ IDEA Ultimate'),
                 Flatpak('com.jetbrains.IntelliJ-IDEA-Ultimate'))

progs += Program('mps', _('MPS'),
                 Native('mps'),
                 Toolbox('MPS'))

progs += Program('phpstorm', _("PhpStorm"),
                 Flatpak("com.jetbrains.PhpStorm"),
                 Native("phpstorm"),
                 Toolbox('PhpStorm'))

progs += Program('phpstorm-eap', _("PhpStorm (EAP)"),
                 Native("phpstorm-eap"))

# PyCharm has multiple editions that default to the same command but
# prioritise the highest-paying edition. Therefore the native version has been
# treated as a separate program due to the uncertainty around edition.
progs += Program('pycharm', _('PyCharm'),
                 Native('pycharm'),
                 Toolbox('PyCharm', 'PyCharm-P', 'PyCharm-C'))

progs += Program('pycharm-eap', _('PyCharm (EAP)'),
                 Native('pycharm-eap'))

progs += Program('pycharm-professional', _('PyCharm Professional'),
                 Flatpak('com.jetbrains.PyCharm-Professional'))

progs += Program('pycharm-community', _('PyCharm Community'),
                 Flatpak('com.jetbrains.PyCharm-Community'))

progs += Program('rider', _('Rider'),
                 Native('rider'),
                 Flatpak('com.jetbrains.Rider'),
                 Toolbox('Rider'))

progs += Program('rubymine', _('RubyMine'),
                 Native('rubymine'),
                 Flatpak('com.jetbrains.RubyMine'),
                 Toolbox('RubyMine'))

progs += Program('rubymine-eap', _('RubyMine (EAP)'),
                 Native('rubymine-eap'))

progs += Program('rustrover', _('RustRover'),
                 Native('rustrover'),
                 Flatpak('com.jetbrains.RustRover'),
                 Toolbox('RustRover'))

progs += Program('rustrover-eap', _('RustRover (EAP)'),
                 Native('rustrover-eap'))

progs += Program('webstorm', _('WebStorm'),
                 Native('webstorm'),
                 Flatpak('com.jetbrains.WebStorm'),
                 Toolbox('WebStorm'))

progs += Program('webstorm-eap', _('WebStorm (EAP)'),
                 Native('webstorm-eap'))

progs += Program('zed', _('Zed'),
                 Native('zed', 'zedit', 'zeditor', 'zed-editor'),
                 Flatpak('dev.zed.Zed'))

progs += Program('zed-preview', _('Zed (Preview)'),
                  Flatpak('dev.zed.Zed-Preview'))
