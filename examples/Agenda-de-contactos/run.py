import sys
from PyQt4 import QtGui
from contacto.manager import ContactosManager
from contacto.gui import ContactosGUI
from storm.locals import *

# object Store de Storm
DATABASE = create_database('sqlite: contactos.db')
almacen = Store(DATABASE)

# manager instance
# reset: if TRUE, delete all rows of contacts in database
cm = ContactosManager(almacen, reset = False)

# displaying the window
app = QtGui.QApplication(sys.argv)
window = ContactosGUI( manager = cm, managers = [] )
window.show()
sys.exit(app.exec_())
