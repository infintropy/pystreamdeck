from ElGateau import ElGateau, Icon
import time
import webbrowser
import uuid
import profile_manager

eg = ElGateau(do_boot=False)
BUTTON_COUNT = 15
BUTTON_RANGE = range( 1, BUTTON_COUNT+1 )


class Action(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.id = str(uuid.uuid4())
        self._icon = Icon.text("Action")

    def run(self):
        #implement in subclass
        print("button clicked")

    def _run(self):
        self.run()

class BackAction(Action):
    def __init__(self, *args, **kwargs):
        super(BackAction, self).__init__(*args, **kwargs)
        self._icon = Icon.text("<<")

    def run(self):
        self.parent.parent.establish_menu(self.parent._parmen)

class WebAction(Action):
    """
    Action for opening urls in the system's  selected browser.
    """
    def __init__(self, *args, **kwargs):
        super(WebAction, self).__init__(*args, **kwargs)
        self._url = 'http://google.co.kr'
        self._icon = Icon.text('WebAction')

    def run(self):
        webbrowser.open(self._url, new=2)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if url.startswith("http"):
            self._url = url
        else:
            self._url = "https://www." + url

class Menu(Action):
    def __init__(self, *args, **kwargs):
        super(Menu, self).__init__(*args, **kwargs)
        self._primary = False
        self._items = dict((i, None) for i in BUTTON_RANGE)
        self._icon = Icon.text('Menu')
        self._parmen = None

    def __getitem__(self, item):
        return self._items[item]

    def set(self, button_number, action):
        self._items[button_number] = action
        if isinstance(action, SubMenu):
            self._items[button_number]._parmen = self

    def run(self):
        self.parent.establish_menu(self)



class SubMenu(Menu):
    def __init__(self, *args, **kwargs):
        super(SubMenu, self).__init__(*args, **kwargs)
        self.back_button = BackAction(self)
        self.set(1, self.back_button)

    def set(self, button_number, action):
        if button_number > 1 or isinstance( action, BackAction ):
            self._items[button_number] = action
            if isinstance(action, SubMenu):
                self._items[button_number]._parmen = self
        else:
            raise Exception("First button is reserved for going back.")

class Profile(object):
    def __init__(self):
        self.main_menu = Menu(self)
        self.current_menu = self.main_menu


        self.wa = WebAction(self)
        self.wa2 = WebAction(self)
        self.wa2.url = "facebook.com"

        self.menu2 = SubMenu(self)
        self.wa3 = WebAction(self)
        self.wa3.url = "nbc.com"
        self.wa3._icon = Icon.text('nbc!')

        self.menu3 = SubMenu(self)
        self.menu2.set(3, self.menu3 )

        self.gmail = WebAction(self)
        self.gmail.url = "gmail.com"
        self.gmail._icon = Icon.text('gmail!')

        self.menu3.set(2, self.gmail)

        self.menu2.set(2, self.wa3)

        self.main_menu.set( 1, self.wa )
        self.main_menu.set( 2, self.wa2)

        self.main_menu.set(3, self.menu2 )

        self.establish_menu( self.main_menu )

    def establish_menu(self, menu):
        self.current_menu = menu
        for button in BUTTON_RANGE:

            if self.current_menu._items.get(button):
                print("updating button %d" %button)
                eg.display_update(button, self.current_menu[button]._icon)
            else:
                eg.display_clear(button)


MP = Profile()



"""

cmds = {}
for i in range(1,16):
    cmds[i] = "eg.display_update(%d, Icon.text('%d', size=24))" %(i, i)


def word_card(st=None):
    for word in s.split(" "):
        eg.display_update(2, Icon.text(word, size=12))
        time.sleep(0.3)
        eg.display_clear(2)
"""

cw = profile_manager.ControlWindow()
cw.show()
while True:
    try:
        chosen = eg.button_listen_key(list(range(1,16)))[0]
        if MP.current_menu._items.get(chosen):
            MP.current_menu[chosen]._run()
    except:
        print('error state')


