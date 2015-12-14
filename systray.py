#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from sys import argv, platform

USAGE = "USAGE: {} SPACEAPI_URL [ REFRESH_RATE (in seconds) ]"

if __name__ == "__main__":
    if 'linux' in platform:
        from linux.systray import main
    elif 'darwin' in platform:
        from osx.systray import main
    else:
        print("Your platform is not (yet ?) supported.")

    if len(argv) < 2:
        print(USAGE.format(argv[0]))
    else:
        refresh_rate = 60 if len(argv) < 3 else int(argv[2])
        main(argv[1], refresh_rate)
