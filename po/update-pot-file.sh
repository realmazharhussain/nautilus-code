#!/bin/bash
po_dir=$(dirname "$(realpath "$0")")

options=(
  -f "${po_dir}"/POTFILES.in
  -o "${po_dir}"/nautilus-code.pot
  --add-comments=Translators
  --keyword=_
  --keyword=C_:1c,2
  --from-code=UTF-8

  --package-name="nautilus-code"
  --package-version="3.alpha"
  --msgid-bugs-address="realmazharhussain@gmail.com"
)

xgettext "${options[@]}"
