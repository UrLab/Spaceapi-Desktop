#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sys import argv, platform

if __name__ == "__main__":
    if 'linux' in platform:
        from linux.systray import main
    elif 'darwin' in platform:
        from osx.systray import main
    else:
        print("Your platform is not (yet ?) supported.")

    main("http://urlab.space", 60)
