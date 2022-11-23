from .types import ProgramList, Program, Native, Flatpak, Edition

progs = ProgramList()

progs += Program('Code-OSS',
                   Native('code-oss'),
                   Flatpak('com.visualstudio.code-os'))

progs += Program('VSCode',
                 Flatpak('com.visualstudio.code'),
                 Edition('Insiders',
                         Native('code-insiders')))

if not progs['Code-OSS']['Native'].is_installed:
    progs['VSCode'].add_package(Native('code'))

progs += Program('VSCodium',
                 Native('vscodium', 'codium'),
                 Flatpak('com.vscodium.codium'))

progs += Program('Builder',
                 Flatpak('org.gnome.Builder'),
                 Native('gnome-builder'),
                 arguments=['--project'])

progs += Program("Sublime Text",
                 Flatpak("com.sublimetext.three"),
                 Native("subl"))

progs += Program("PhpStorm",
                 Flatpak("com.jetbrains.PhpStorm"),
                 Native("phpstorm"),
                 Edition("EAP",
                         Native("phpstorm-eap")))
