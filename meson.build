project('nautilus-code',
  version: '0.6.alpha',
)

dependency('nautilus-python', required:true)

extensions_dir = get_option('datadir') / 'nautilus-python/extensions'

install_data(
  files('nautilus-code.py'),
  install_dir: extensions_dir,
)

subdir('NautilusCode')
