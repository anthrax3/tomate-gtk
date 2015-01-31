from locale import gettext as _

from gi.repository import AppIndicator3, Gtk

from tomate.profile import ProfileManagerSingleton
from tomate.signals import tomate_signals
from tomate.base import ConnectSignalMixin

profile = ProfileManagerSingleton.get()


class IndicatorMenu(Gtk.Menu):

    def __init__(self):
        Gtk.Menu.__init__(self, halign=Gtk.Align.CENTER)

        self.show_menu = Gtk.MenuItem(_('Show'), visible=False)
        self.show_menu.connect('activate', self.on_show_menu_activate)
        self.append(self.show_menu)
        self.show_all()

    def on_show_menu_activate(self, widget):
        tomate_signals.emit('window hid')


class Indicator(ConnectSignalMixin):

    signals = (
        ('session_ended', 'hide'),
        ('window_showed', 'hide'),
        ('window_hid', 'show'),
    )

    def __init__(self):
        self.indicator = AppIndicator3.Indicator.new_with_path(
                'tomate',
                'tomate-indicator',
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
                profile.get_icon_paths()[0]
            )
        self.indicator.set_menu(IndicatorMenu())

        self.connect_signals()

    def show(self):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    def hide(self, *args, **kwargs):
        self.indicator.set_status(AppIndicator3.IndicatorStatus.PASSIVE)