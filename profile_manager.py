import sys
sys.path.append( "Z:/software/scripts/pyMod" )

from PySide2.QtGui import *
from PySide2.QtCore import *
from functools import partial
import uuid







class ButtonMenu(QMenu):
    def __init__(self, parent=None):
        super(ButtonMenu, self).__init__()
        self.parent = parent

        cmds = { "Make Folder"  :"",
                 "Rename"       : "",
                 "Print parent" : "",
                 "Web Link" : "",
                 "Run Script" : ""
        }

        for name, cmd in cmds.iteritems():
            act = QAction(self)
            act.setText(name)
            self.addAction(act)
            act.triggered.connect( partial( self.action_relay, name ) )

    def action_relay(self, info):
        self.parent.parent.parent.action_relay(self.parent, cmd=info)







class ControlWindow(QWidget):
    def __init__(self):
        super(ControlWindow, self).__init__()

        self._menus = {}
        self._menu_lib = {}

        self.switch = QComboBox()
        self.stack = QStackedWidget()

        self.current_menu = ""


        self.master_layout = QVBoxLayout()

        self.add_menu( "main" )
        self.add_menu( "secondary")
        #self.build_menus()

        self.master_layout.addWidget( self.switch )
        self.master_layout.addWidget( self.stack)

        self.switch.addItems(["1", "2"])

        self.setLayout(self.master_layout)

        self.switch.currentIndexChanged.connect(  self.stack.setCurrentIndex  )


    def show_menu(self, id):
        self.stack.setCurrentIndex( self._menus[id]['stackind'] )
        self.current_menu = id

    def add_menu(self, name="", description="", parent=None):
        count = len(self._menus.keys())
        menu = {}
        if count==0:
            menu["menu_array"] = MenuArray(parent=self, primary=True, parent_menu=parent)
        else:
            menu["menu_array"] = MenuArray(parent=self, parent_menu=parent)
        id = menu["menu_array"].id

        self._menus[id] = menu
        self._menus[id]['name'] = name
        self._menus[id]['description'] = ""
        self._menus[id]['root'] = False
        self._menus[id]['parent'] = parent

        self.stack.addWidget(self._menus[id]['menu_array'])
        c = self.stack.count()
        print("stack is %d big" %c)
        self._menus[id]['stackind'] = c-1

        return self._menus[id]['menu_array']



    def build_menus(self):
        for c, menu in enumerate(self._menus.keys()):
            pass




    def action_relay(self, button, cmd=None):

        button.setText('clicked')
        if cmd=="Make Folder":
            button.setText('Folder!')
            button.type = "Folder"
            print("does this work?")
            m = self.add_menu(name="Folder1", parent=button.parent.id)
            button.folder_menu = m.id
        elif cmd=="Web Link":
            button.set_profile('web')
        elif cmd=="Run Script":
            button.set_profile('script')



    def button_relay(self, button):
        print( "Menu: %s, Button %d, Type: %s" %( button.parent.id, button.id, button.type ) )

        if button.type == "Folder":
            self.stack.setCurrentIndex( self._menus[button.folder_menu]['stackind'] )
            print("attempted to go to folder %s, at index %d" %(button.parent.id , self._menus[button.parent.id]['stackind'] ))


class ActionButton(QToolButton):
    def __init__(self, text=None, parent=None, id=0):
        super(ActionButton, self).__init__()
        self.parent = parent
        self.id = id
        self.type = None
        self.folder_menu = None

        if text:
            self.setText( str(text) )
        self.setMinimumWidth(100)
        self.setMinimumHeight(100)
        #self.setPopupMode( QToolButton.InstantPopup )
        self.button_menu = ButtonMenu(self)
        self.setMenu( self.button_menu )


        self.clicked.connect( partial(self.parent.parent.button_relay, self ))

    def set_profile(self, profile):
        if profile=="back":
            self.setText( "<<" )
            self.setMenu(None)
            self.type = "Folder"
        elif profile=="web":
            self.setText("WebLink")
            self.type = "WebLink"
        elif profile=="script":
            self.setText("</?+>")
            self.type = "Script"


class MenuArray(QWidget):

    button_clicked = Signal(())

    def __init__(self, prefix="Button", parent=None, primary=False, parent_menu=None):
        super(MenuArray, self).__init__()
        self.parent = parent
        self.prefix = prefix
        self.id = str(uuid.uuid4())
        self.master_layout = QGridLayout()
        self.setLayout( self.master_layout )

        self.button_positions = [(i,j) for i in range(3) for j in range(5)]
        self.buttons = {}
        for c, pos in enumerate(self.button_positions):

            self.buttons[c+1] = ActionButton( str(c+1), parent=self, id=c+1)
            if c==0:
                if primary==False:
                    self.buttons[c + 1].set_profile("back")
                    self.buttons[c + 1].folder_menu = parent_menu
            self.master_layout.addWidget( self.buttons[c+1], *pos )
            self.buttons[c+1].setMinimumHeight(50)


    def __getitem__(self, item):
        return self.buttons[item]
