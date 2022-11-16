project('nautilus-code', 'c',
  version: '0.6.alpha',
  default_options: [
    'prefix=/usr',
  ]
)

shared_module(meson.project_name(),
  ['nautilus-code-module.c', 'nautilus-code.c'],
  dependencies : dependency('libnautilus-extension-4'),
  install_dir: get_option('prefix') / get_option('libdir') / 'nautilus/extensions-4',
  install: true,
)
