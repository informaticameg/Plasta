import sys
from PyQt4 import QtGui
from contacto.manager import ContactosManager
from contacto.gui import ContactosGUI
from storm.locals import *

# objeto Store de Storm
DATABASE = create_database('sqlite: contactos.db')
almacen = Store(DATABASE)

# instancia del manager
# reset: si esta en TRUE, borra todo lo correspondiente a ese objeto en la bd
cm = ContactosManager(almacen, reset = False)

# mostramos la ventana
app = QtGui.QApplication(sys.argv)
window = ContactosGUI( manager = cm, managers = [] )
window.show()
sys.exit(app.exec_())
