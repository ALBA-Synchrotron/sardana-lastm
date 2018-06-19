#!/usr/bin/env python

###############################################################################
#     STM laboratory Sardana Controllers.
#
#     Copyright (C) 2018  ALBA Synchrotron, Cerdanyola del Valles, Spain.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

from setuptools import setup, find_packages


def main():
    """Main method collecting all the parameters to setup."""
    name = "sardana-ctrl-lastm"

    version = "0.0.1"

    description = "Sardana controllers for STM laboratory."

    author = "Zbigniew Reszela"

    author_email = "zreszela@cells.es"

    license = "GPLv3"

    url = "http://www.albasynchrotron.es"

    packages = find_packages()

    provides = ['aldtgctrl']

    requires = ['sardana']

    setup(
        name=name,
        version=version,
        description=description,
        author=author,
        author_email=author_email,
        license=license,
        url=url,
        packages=packages,
    )

if __name__ == "__main__":
    main()