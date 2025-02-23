from App import *
from ButtonView import *
from Controller import *
from Event import *
from Gate import *
from GateView import *
from Model import *
from Port import *
from PortView import *
from View import *
from WireView import *


def setUp():
    global eb, m, v, c

    eb = EventBus()
    m = Model(eb)
    v = View(eb, 1280, 720)
    c = Controller(eb, m, v)

def tearDown():
    m.clear()
    v.clear()


