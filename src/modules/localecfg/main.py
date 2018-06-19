#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# === This file is part of Calamares - <https://github.com/calamares> ===
#
#   Copyright 2014, Anke Boersma <demm@kaosx.us>
#   Copyright 2015, Philip Müller <philm@manjaro.org>
#   Copyright 2016, Teo Mrnjavac <teo@kde.org>
#   Copyright 2018, AlmAck <gluca86@gmail.com>
#   Copyright 2018, Adriaan de Groot <groot@kde.org>
#
#   Calamares is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Calamares is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Calamares. If not, see <http://www.gnu.org/licenses/>.

import os
import shutil

import libcalamares


def run():
    """ Create locale """
    en_us_locale = 'en_US.UTF-8'
    locale_conf = libcalamares.globalstorage.value("localeConf")

    if not locale_conf:
        locale_conf = {
            'LANG': 'en_US.UTF-8',
            'LC_NUMERIC': 'en_US.UTF-8',
            'LC_TIME': 'en_US.UTF-8',
            'LC_MONETARY': 'en_US.UTF-8',
            'LC_PAPER': 'en_US.UTF-8',
            'LC_NAME': 'en_US.UTF-8',
            'LC_ADDRESS': 'en_US.UTF-8',
            'LC_TELEPHONE': 'en_US.UTF-8',
            'LC_MEASUREMENT': 'en_US.UTF-8',
            'LC_IDENTIFICATION': 'en_US.UTF-8'
        }

    install_path = libcalamares.globalstorage.value("rootMountPoint")
    target_locale_gen = "{!s}/etc/locale.gen".format(install_path)
    target_locale_gen_bak = target_locale_gen + ".bak"
    target_locale_conf_path = "{!s}/etc/locale.conf".format(install_path)
    target_etc_default_path = "{!s}/etc/default".format(install_path)

    # restore backup if available
    if os.path.exists('/etc/locale.gen.bak'):
        shutil.copy2(target_locale_gen_bak,
                     target_locale_gen)

    # run locale-gen if detected
    if os.path.exists('/etc/locale.gen'):
        text = []

        with open(target_locale_gen, "r") as gen:
            text = gen.readlines()

        # we want unique values, so locale_values should have 1 or 2 items
        locale_values = set(locale_conf.values())

        with open(target_locale_gen, "w") as gen:
            for line in text:
                # always enable en_US
                if line.startswith("#" + en_us_locale):
                    # uncomment line
                    line = line[1:].lstrip()

                for locale_value in locale_values:
                    if line.startswith("#" + locale_value):
                        # uncomment line
                        line = line[1:].lstrip()

                gen.write(line)

        libcalamares.utils.target_env_call(['locale-gen'])
        print('locale.gen done')

    # write /etc/locale.conf
    with open(target_locale_conf_path, "w") as lcf:
        for k, v in locale_conf.items():
            lcf.write("{!s}={!s}\n".format(k, v))

    # write /etc/default/locale if /etc/default exists and is a dir
    if os.path.isdir(target_etc_default_path):
        with open(os.path.join(target_etc_default_path, "locale"), "w") as edl:
            for k, v in locale_conf.items():
                edl.write("{!s}={!s}\n".format(k, v))

    return None
