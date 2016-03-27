from plasta.logic.manager import BaseManager
from cuenta import Cuenta


class CuentasManager(BaseManager):
    """
    Clase manejadora de las cuentas.
    """
    
    def __init__(self,almacen,reset = False):
        ''''''
        BaseManager.__init__(self,almacen,reset)
        self.CLASS = Cuenta
        self.searchname = self.CLASS.nombre
        
        self._start_operations()
    
    def cuentasDeIngreso(self):        
        cuentas = filter(lambda obj : True if obj.tipo == "Ingreso" else False, self.getall())
        cuentas.sort()
        return cuentas 
    
    def cuentasDeEgreso(self):        
        cuentas = filter(lambda obj : True if obj.tipo == "Egreso" else False, self.getall())
        cuentas.sort()
        return cuentas
    
    def existeNombreCuenta(self, nombreCuenta):
        existe = False
        cuentas = self.getall()
        for cuenta in cuentas:
            if cuenta.nombre == nombreCuenta: 
                existe = True
        return existe
    
    def actualizarBalance(self, cuenta):
        """
        Si una cuenta se modifica de ingreso -> egreso o viceversa, 
        se actualizara el monto del balance recalculando el monto 
        de cada cuenta.
        """
        pass
    
    def actualizarMontoCuenta(self, cuenta, monto):
        cuenta.monto += monto
        self.almacen.commit()
        
       
