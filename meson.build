project('nautilus-code', 'c', # lang-name e.g. 'c', 'cpp', etc
  version: '1.0.alpha',
  default_options: [
    'prefix=/usr',
  ]
)

sources = files('nautilus-code-module.c', 'nautilus-code.c')

shared_module('nautilus-code', sources,
  install: true,
  install_dir: get_option('prefix') / get_option('libdir') / 'nautilus/extensions-3.0',
  dependencies : dependency('libnautilus-extension'),
)
