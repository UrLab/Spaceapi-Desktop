#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import gtk
import gobject
import requests


class SystrayIconApp:
    def __init__(self, spaceapi_url, refresh_rate_seconds=30):
        self.url = spaceapi_url
        self.tray = gtk.StatusIcon()
        self.people_now_present = []
        self.refresh()
        self.tray.connect('popup-menu', self.on_right_click)
        self.tray.connect('button-press-event', self.on_left_click)
        gobject.timeout_add(refresh_rate_seconds*1000, self.refresh)

    def refresh(self):
        was_open = getattr(self, 'is_open', None)
        try:
            space = requests.get(self.url).json()
        except:
            space = {}

        is_open = space.get('state', {}).get('open', None)
        if is_open != was_open:
            self.render(space.get('space', None), is_open)
        self.is_open = is_open

        try:
            self.people_now_present = sorted(space['sensors']['people_now_present'][0]['names'])
        except:
            self.people_now_present = []

        try:
            self.people_count = int(space['sensors']['people_now_present'][0]['value'])
        except:
            self.people_count = len(self.people_now_present)

        return True

    def render(self, name, is_open):
        icon = gtk.STOCK_STOP
        if is_open is True:
            icon = gtk.STOCK_YES
        elif is_open is False:
            icon = gtk.STOCK_NO
        self.tray.set_from_stock(icon)

        if name is None:
            self.tray.set_tooltip('Connection error')
        else:
            text = "open \\o/" if is_open else "closed /o\\"
            self.tray.set_tooltip(name + " is " + text)

    def on_left_click(self, receiver, evt):
        if evt.button != 1:
            return
        menu = gtk.Menu()

        for people in self.people_now_present:
            item = gtk.MenuItem(people)
            item.show()
            menu.append(item)

        hidden = self.people_count - len(self.people_now_present)
        if hidden > 0:
            text = "%i other" % hidden
            if hidden > 1:
                text += "s"
            item = gtk.MenuItem(text)
            item.show()
            menu.append(item)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   evt.button, evt.time, self.tray)

    def on_right_click(self, icon, event_button, event_time):
        menu = gtk.Menu()

        # show about dialog
        about = gtk.MenuItem("About")
        about.show()
        menu.append(about)
        about.connect('activate', self.show_about_dialog)

        # add quit item
        quit = gtk.MenuItem("Quit")
        quit.show()
        menu.append(quit)
        quit.connect('activate', gtk.main_quit)

        menu.popup(None, None, gtk.status_icon_position_menu,
                   event_button, event_time, self.tray)

    def show_about_dialog(self, widget):
        about_dialog = gtk.AboutDialog()
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_icon_name("SpaceAPI Desktop")
        about_dialog.set_name('SpaceAPI Desktop')
        about_dialog.set_version('0.2')
        about_dialog.set_copyright("Made at UrLab, ULB's hackerspace")
        about_dialog.set_website("https://github.com/urlab/spaceapi-desktop")
        about_dialog.set_comments(
            "A system tray icon to display your local hackerspace status")
        about_dialog.set_authors(['iTitou', 'C4', 'infected', 'piR'])
        about_dialog.run()
        about_dialog.destroy()


def main(url, refresh_rate):
    SystrayIconApp(url, refresh_rate)
    gtk.main()
