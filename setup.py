#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-lbtc.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum-lbtc.png'])
    ]

setup(
    name="Electrum-LBTC",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require={
        'full': requirements_hw + ['pycryptodomex', 'scrypt>=0.6.0'],
    },
    packages=[
        'electrum_lbtc',
        'electrum_lbtc_gui',
        'electrum_lbtc_gui.qt',
        'electrum_lbtc_plugins',
        'electrum_lbtc_plugins.audio_modem',
        'electrum_lbtc_plugins.cosigner_pool',
        'electrum_lbtc_plugins.email_requests',
        'electrum_lbtc_plugins.hw_wallet',
        'electrum_lbtc_plugins.keepkey',
        'electrum_lbtc_plugins.labels',
        'electrum_lbtc_plugins.ledger',
        'electrum_lbtc_plugins.trezor',
        'electrum_lbtc_plugins.digitalbitbox',
        'electrum_lbtc_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_lbtc': 'lib',
        'electrum_lbtc_gui': 'gui',
        'electrum_lbtc_plugins': 'plugins',
    },
    package_data={
        'electrum_lbtc': [
            'servers.json',
            'servers_testnet.json',
            'servers_regtest.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-lbtc'],
    data_files=data_files,
    description="Lightweight LiteBitcoin Wallet",
    author="Team LBTC",
    author_email="litebitcoins@gmail.com",
    license="MIT Licence",
    url="http://lbtc.info",
    long_description="""Lightweight LiteBitcoin Wallet"""
)
