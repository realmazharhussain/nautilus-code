from .types import ProgramList, Program, Native, Flatpak

progs = ProgramList()

progs += Program('Code-OSS',
                 Native('code-oss'),
                 Flatpak('com.visualstudio.code-os'))

progs += Program('VSCode', Flatpak('com.visualstudio.code'))

# Code-OSS also has a binary named 'code'. If Code-OSS is installed, the
# command 'code' refers to Code-OSS instead of Microsoft VSCode. So, in
# that case, we shouldn't show a menu entry for Microsft 'VSCode'.
if not progs['Code-OSS']['Native'].is_installed:
    progs['VSCode'] += Native('code')

progs += Program('VSCode (Insiders)',
                 Native('code-insiders'),
                 Flatpak('com.visualstudio.code.insiders'))

progs += Program('VSCodium',
                 Native('vscodium', 'codium'),
                 Flatpak('com.vscodium.codium'))

progs += Program('Builder',
                 Flatpak('org.gnome.Builder'),
                 Native('gnome-builder'),
                 arguments=['--project'])

progs += Program("Sublime",
                 Flatpak("com.sublimetext.three"),
                 Native("subl"))

progs += Program("PhpStorm",
                 Flatpak("com.jetbrains.PhpStorm"),
                 Native("phpstorm"))

progs += Program("PhpStorm (EAP)", Native("phpstorm-eap"))
