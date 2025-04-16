"""Crearemos una clase Contacto que contenga los siguientes atributos:
Atributos:
- Nombres (nombres)-> str
- Apellidos (apellidos)-> str
- Telefono (numero_de_telefono)-> int
- Correo (correo)-> str

Metodos:
- __str__() -> str
- datos_completos() -> str
- linea_a_contacto(linea: str) ->object

El metodos __str__() debera devolver una cadena de texto con la siguiente
estructura:
    "Nombre: {nombres} Apellidos: {apellidos}, Telefono: {numero_de_telefono},
     Correo: {correo}"
El metodo datos_completos debera devolver una cadena de texto con la siguiente
estructura:
    "{nombres},{apellidos},{numero_de_telefono},{correo}
El metodo linea_a_contacto devuelve un objeto Contacto a partir de un str,
funciona como un segundo constructor"""
from mis_excepciones import MisExcepciones

class Contacto:
    """Clase Contacto para crear la información de un contacto."""
    def __init__(self, nombres=None, apellidos=None, \
                 numero_de_telefono=None, correo=None):
        # Inicializamos en None para poder crear objetos vacios
        self.nombres = nombres
        self.apellidos = apellidos
        self.numero_de_telefono = numero_de_telefono
        self.correo = correo

    def __str__(self):
        # Redefino el metodo para adaptarlo a la visualizacion por consola
        return f"Nombres:   {self.nombres}\nApellidos: {self.apellidos}\n" \
               f"Telefono:  {self.numero_de_telefono}\nCorreo:    {self.correo}"

    def linea_a_contacto(self, linea: str) -> object:
        """Convierte una linea a un objeto de la clase Cliente
            es como un constructor adicional"""
        try:
            datos = linea.strip().split(',')
            if len(datos) != 4:
                raise MisExcepciones(f"La linea '{linea}' no tiene el formato "\
                                      f"correcto.", codigo_error = 1046)
            contacto = Contacto(datos[0].strip(), datos[1].strip(),\
                                datos[2].strip(), datos[3].strip())
            return contacto
        except MisExcepciones as e:
            print(f"{e}")
        
    def datos_completos(self) -> str:
        """Devuelve una cadena de texto con todos los datos del contacto.
           Formato: nombres,apellidos,numero_de_telefono,correo"""
        try:
            datos = f"{self.nombres.strip()},{self.apellidos.strip()},"\
                    f"{self.numero_de_telefono},{self.correo.strip()}"
            if datos == None:
                raise MisExcepciones(error_original="El Contacto esta vacio", codigo_error=1060)
            return datos
        except Exception as e:
            print(f'{e}')
    
"""Codigo con el motivo de probar el modulo"""
if __name__ == "__main__":
    try:
        contacto1 = Contacto('Luis Miguel', 'Ortiz Lopez', 34641193239, \
                             'luismortizl1975@gmail.com')
        print(contacto1)
        print(contacto1.datos_completos())
        print(contacto1.linea_a_contacto(",,,"))
    except MisExcepciones as e:
        print(f"Error capturado: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

   
