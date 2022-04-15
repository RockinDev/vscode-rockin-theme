#!/usr/bin/env python3

import json
import os
import shutil
import sys

from os.path import expanduser

HOME_DIR = expanduser('~')
CWD = os.getcwd()

THEME_FILES = [
  'package.json',
  'themes/apsis-light.json',
  'themes/apsis-dark.json'
]

def install_theme(extension_dir, extension_name):
  if os.path.exists(extension_dir):
    print('Extension directory found: "{}"'.format(extension_dir))

    # delete extension if already present
    theme_dir = os.path.join(extension_dir, extension_name)
    if os.path.exists(theme_dir):
      print('Deleting existing theme directory "{}"'.format(theme_dir))
      shutil.rmtree(theme_dir, ignore_errors=True)

    print('Installing theme to "{}"'.format(theme_dir))
    os.makedirs(theme_dir)
    os.makedirs(os.path.join(theme_dir, 'themes'))

    for f in THEME_FILES:
      shutil.copy(os.path.join(CWD, f), os.path.join(theme_dir, f))

  else:
    print('No extension directory found at {}'.format(extension_dir))

if __name__ == '__main__':
  try:
    with open('package.json', 'r') as f:
      p = json.load(f)
      EXTENSION_NAME = '{}.{}-{}'.format(
        p['publisher'],
        p['name'],
        p['version']
      ).lower()

    # extension dir(s)
    VS_CODE_EXTENSION_DIR = os.path.join(HOME_DIR, '.vscode/extensions/')
    CODIUM_EXTENSION_DIR = os.path.join(HOME_DIR, '.vscode-oss/extensions/')
    FLATPAK_EXTENSION_DIR = os.path.join(HOME_DIR, '.var/app/com.visualstudio.code/data/vscode/extensions/')

    print('Attempting to install standard Visual Studio Code installation...')
    install_theme(VS_CODE_EXTENSION_DIR, EXTENSION_NAME)
    print('Attempting to install Codium...')
    install_theme(CODIUM_EXTENSION_DIR, EXTENSION_NAME)
    print('Attempting to install Flatpak-based VSCode installation...')
    install_theme(FLATPAK_EXTENSION_DIR, EXTENSION_NAME)

  except Exception as e:
    print(e)
    sys.exit(1)
