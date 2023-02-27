project('nautilus-code',
  version: '0.6.alpha',
  default_options: [
    'prefix=~/.local',
  ]
)

dependency('nautilus-python', required: true)

extensions_dir = get_option('datadir') / 'nautilus-python/extensions'

configure_file(
  input: 'nautilus-code.py.in',
  output: 'nautilus-code.py',
  install: true,
  install_dir: extensions_dir,
  configuration: configuration_data({
    'localedir': get_option('prefix') / get_option('localedir'),
  })
)

subdir('NautilusCode')
subdir('po')
