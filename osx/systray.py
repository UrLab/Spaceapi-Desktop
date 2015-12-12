#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import rumps
import requests


class SystrayIconApp(rumps.App):

    def __init__(self, title, spaceapiUrl, refresh_rate):
        super(SystrayIconApp, self).__init__(title)
        self._spaceapiUrl = spaceapiUrl
        self.people_now_present = []
        self.is_open = None
        self.timer = rumps.Timer(self._refresh, refresh_rate)
        self.timer.start()

    @rumps.clicked("Who's there ?")
    def prefs(self, _):
        if len(self.people_now_present) > 0:
            res = ""
            for p in self.people_now_present:
                res += "-" + str(p) + "\n"
        else:
            res = "Nobody is there .. for the moment ! \n"
        rumps.alert(res)

    def _refresh(self, trash):
        was_open = self.is_open
        space = requests.get(self._spaceapiUrl).json()
        try:
            space = requests.get(self._spaceapiUrl).json()
        except:
            space = {}
        is_open = space.get('state', {}).get('open', None)
        if is_open != was_open:
            new_title = "UrLaB:Open" if is_open else "UrLaB:Close"
            self.title = new_title
        self.is_open = is_open

        try:
            self.people_now_present = space['sensors']['people_now_present'][0]['names']
        except:
            self.people_now_present = []


if __name__ == "__main__":
    from sys import argv

    if len(argv) < 2:
        print("USAGE: {} SPACEAPI_URL [ REFRESH_RATE (in seconds) ]".format(
            argv[0]))
    else:
        refresh_rate = 120 if len(argv) < 3 else int(argv[2])
        sia = SystrayIconApp("UrLaB:fetching...", argv[1], refresh_rate)
        sia.run()
