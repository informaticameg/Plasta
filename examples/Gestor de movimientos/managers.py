from tools.config import Configurations
from storm.locals import * #@UnusedWildImport
from movimiento.manager import MovimientosManager
from cuenta.manager import CuentasManager
from seccion.manager import SeccionesManager

class Managers :
    
    def __init__(self):
        
        config = Configurations()
        DATABASE = create_database('sqlite:' + config.getPathBD())
        almacen = Store(DATABASE)
        
        #RESET: True para borrar los datos correspondientes a un objeto
        reset_cm = False
        reset_movimientos = False

        self.cuentas = CuentasManager(almacen, reset = reset_cm)
        self.movimientos = MovimientosManager(almacen, reset = reset_movimientos)
        self.secciones = SeccionesManager(almacen, reset = False, managers = [self.cuentas])
        
        if reset_movimientos:
            balance = open("movimiento/data.db",'w')
            balance.write(str(0))
            balance.close()
