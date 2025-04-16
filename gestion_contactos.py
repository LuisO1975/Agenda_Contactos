"""Clase GestionContactos que permite inicializar una lista de contactos y 
proporciona métodos para agregar, eliminar, buscar y mostrar contactos. La
clase Contacto representa un contacto individual. y la clase GestionContactos
permite gestionar una lista de contactos y actua sobre el Archivo de
contactos.

La clase GestionContactos tiene 3 grupos de métodos:
Metodos sobre la lista de contactos:
- Agregar un contacto a la lista.
- Buscar un contacto.
- Eliminar un contacto.
- Mostrar todos los contactos.
- Verificar si un contacto ya existe en la lista.
Metodos sobre el archivo de contactos:
- Inicializar la lista de contactos.
- limpiar contactos duplicados o erróneos.
- Actualizar el archivo de contactos.
- Agregar contacto a archivo.
Metodos para adaptar cadenas:
- contacto_cadena: Quita de una cadena generada con el metodo __str__
    las etiquetas de Nombre,apellidos, telefono y email.
- quitar_acentos: Elimina los acentos de una cadena para la busqueda.

Manejara la creacion, modificacion y eliminacion de contactos, ademas de 
permitir guardar y cargar contactos desde el archivo"""
import os
from mis_contactos import Contacto
from mis_excepciones import MisExcepciones
import re
import unicodedata

class GestionContactos:
    """Clase GestionContactos para gestionar una lista de contactos."""

    LISTA_CONTACTOS = 'lista_contactos.txt'
    """Nombre del archivo donde se guardan los contactos."""

    def __init__(self):
        """Inicializa la lista de contactos vacia."""
        self.contactos = []

    def __str__(self):
        """Devuelve una cadena de texto con todos los contactos."""
        return '\n'.join(str(contacto)+'\n' for contacto in self.contactos)
    
    """Gestion de Contactos en lista de contactos"""
    def agregar_contacto(self, contacto) -> bool:
        """Agrega un contacto a la lista y al archivo.

        Atributos:
            -Contacto: 
            nombres= str, apellidos= str, numero_de_telefono= str, correo= str"""
        try:
            contacto_vacio = Contacto()
            contacto_nuevo = contacto_vacio.linea_a_contacto(contacto)
            if contacto_nuevo == None:
                raise MisExcepciones(f"El contacto '{contacto}' no tiene el "\
                                     f"formato correcto.", codigo_error=2058)
            # Verificar si el contacto ya existe
            if self.verificar_contacto(contacto):
                raise MisExcepciones(f'El contacto {contacto_nuevo.nombres} '\
                        f'{contacto_nuevo.apellidos} ya existe.', codigo_error=2062)
            agrega_contacto = self.agregar_contacto_a_archivo(contacto)
            if not agrega_contacto:
                raise MisExcepciones(f'Error al archivar a: {contacto_nuevo.nombres} '\
                        f'{contacto_nuevo.apellidos}.',codigo_error=2066)
            self.contactos.append(contacto_nuevo)
            print(f'Contacto: {contacto_nuevo.nombres} '\
                 f'{contacto_nuevo.apellidos} agregado correctamente.')
            return True
        except MisExcepciones as e:
            print(f"{e}")
            return False
  
    def buscar_contacto(self, contacto_a_buscar) -> list:
        """Busca uno o mas coincidencias del contacto en la lista.

        Atributos:
            -Contacto a buscar: str"""
        contactos_encontrados=[]
        bus = str(contacto_a_buscar).lower()
        bus = self.quitar_acentos(bus)
        for con in self.contactos:
            coincidencia = bus in self.quitar_acentos(con.datos_completos().lower())
            if coincidencia>0:
                contactos_encontrados.append(f'\n{con}\n')
        return contactos_encontrados

    def eliminar_contacto(self, contacto_eliminar: str) ->bool:
        """Elimina un contacto de la lista y del archivo.

        Atributos:
            -contacto_eliminar: 
            nombres= str, apellidos= str, 
            numero_de_telefono= int, correo= str"""
        try:
            contacto_vacio = Contacto()
            contacto_a_eliminar = contacto_vacio.linea_a_contacto(contacto_eliminar)
            if contacto_a_eliminar == None:
                raise MisExcepciones(f"El contacto '{contacto_eliminar}' no tiene "\
                                     f"el formato correcto.", codigo_error=2101)
            for con in self.contactos:
                if con.datos_completos() == contacto_a_eliminar.datos_completos():
                    self.contactos.remove(con)
                    if self.actualizar_archivo_contactos():
                        print(f"Contacto:\n{con} eliminado.")
                    return True   
            raise MisExcepciones(f"No se encontró el contacto "\
                                f"{contacto_eliminar}", codigo_error=2109)
        except MisExcepciones as e:
            print(f"{e}")
            return False

    def mostrar_todos_contactos(self) -> str:
        """Muestra todos los contactos."""
        try:
            if len(self.contactos) == 0:
                raise MisExcepciones("No hay contactos disponibles.", codigo_error=2118)
            return "\n".join('['+str(i+1)+']:\n'+str(self.contactos[i])+"\n"\
                                for i in range(len(self.contactos)))
        except MisExcepciones as e:
            print(f"{e}")
   
    def verificar_contacto(self, contacto_verificar) -> bool:
        """Verifica si un contacto ya existe en la lista."""
        contacto_vacio = Contacto()
        contacto_a_verificar = contacto_vacio.linea_a_contacto(contacto_verificar)
        for con in self.contactos:
                if con.datos_completos() == contacto_a_verificar.datos_completos():
                    return True
        return False
    
    """Gestion de contactos en archivo de contactos"""  
    def inicializar_contactos(self) -> bool:
        """Inicializa la lista de contactos desde un archivo."""
        try:
            if not os.path.exists(self.LISTA_CONTACTOS):
                raise MisExcepciones("El archivo de contactos no existe, "\
                                     f"se intentara crear uno nuevo", codigo_error=2139)
            contacto_vacio = Contacto()
            with open(self.LISTA_CONTACTOS, 'r', encoding='utf-8') as archivo:
                for lin in archivo:
                    contacto = contacto_vacio.linea_a_contacto(lin)
                    if contacto != None:
                        self.contactos.append(contacto)
                    else:
                        print(f'Error en formato del contacto: {lin.strip()}')
                if not self.contactos:
                    print("No se encontraron contactos en el archivo.")
                else:
                    self.limpiar_contactos() # Limpiar contactos duplicados o erróneos 
            self.actualizar_archivo_contactos()
            return True
        except MisExcepciones as e:
            print(f"{e}")
            with open(self.LISTA_CONTACTOS, 'w', encoding='utf-8') as archivo:
                    archivo.write("")  # Crear el archivo si no existe
            return True
         
    def limpiar_contactos(self) -> bool:
        """Elimina los contactos duplicados, y las lineas con errores."""
        # Convertir la lista de objetos Contacto a una lista de cadenas
        # usando el método datos_completos() de la clase Contacto
        lista_contactos = [contacto.datos_completos() for contacto in self.contactos]
        # Usar un conjunto para eliminar duplicados
        lista_contactos_sin_duplicados = list(set(lista_contactos))
        if len(lista_contactos) == len(lista_contactos_sin_duplicados):
            print("No hay contactos duplicados.")
            return False
        else:
            # Convertir la lista de cadenas de nuevo a objetos Contacto
            self.contactos = []
            contacto_vacio = Contacto()
            for contacto in lista_contactos_sin_duplicados:
                nuevo_contacto = contacto_vacio.linea_a_contacto(contacto)
                if nuevo_contacto != None:
                   self.contactos.append(nuevo_contacto)
                else:
                    print(f"Error al convertir el contacto: {contacto}. No se pudo agregar.")
            print("Se eliminaron los contactos duplicados y datos con errores.")
            return True

    def actualizar_archivo_contactos(self) -> bool:
        """Actualiza el archivo de contactos."""
        try: 
            if not os.path.exists(self.LISTA_CONTACTOS):
                raise MisExcepciones("El archivo de contactos no existe o es "\
                                     f"inaccesible", codigo_error=2188)
            with open(self.LISTA_CONTACTOS, 'w', encoding='utf-8') as archivo:
                for contacto in self.contactos:
                    archivo.write(contacto.datos_completos() + '\n')
                print("Archivo de contactos actualizado.")
                return True
        except MisExcepciones as e:
            print(f"{e}")
            return False

    def agregar_contacto_a_archivo(self, contacto_a_agregar) ->bool:
        """Agregar un contacto al archivo de contactos"""
        contacto_vacio = Contacto()
        contacto_nuevo = contacto_vacio.linea_a_contacto(contacto_a_agregar)
        if contacto_nuevo != None:
            with open(self.LISTA_CONTACTOS, 'a', encoding='utf-8') as archivo:
                archivo.write(contacto_nuevo.datos_completos() + '\n')
            return True
        else:
            return False

    """Gestion de adaptacion de cadenas de texto"""
    def contacto_cadena(self, contacto: str) ->str:
        """Retorna una cadena sin las etiquetas de la funcion __str__ del 
            contacto"""
        cadena_salida = contacto.strip()
        cadena_salida = re.sub(r'(\n|Nombres:   )', '', cadena_salida)
        cadena_salida = re.sub(r'(Apellidos: |Telefono:  |Correo:    )', ',', cadena_salida)
        return cadena_salida

    def quitar_acentos(self, cadena: str) ->str:
        """Elimina los acentos de una cadena de texto."""
        # Normaliza la cadena a la forma NFD (descompone caracteres acentuados)
        cadena_normalizada = unicodedata.normalize('NFD', cadena)
        # Usa una expresión regular para eliminar los caracteres de acento
        cadena_sin_acentos = re.sub(r'[\u0300-\u036f]', '', cadena_normalizada)
        return cadena_sin_acentos

"""Codigo con el proposito de probar el modulo"""
if __name__ == '__main__':
    gestion1 = GestionContactos()
    contactos1 = [
        'Luis Miguel,Ortiz Lopez,34641193239,luismortizl1975@gmail.com',
        'Claudia del Valle, Santiago Montilla, 34642153258,claudiasantiago@gmail.com',
        'Victor Manuel, Ortiz Lopez, 346544789636,victor@hotmail.com',
        'Luis Miguel,Ortiz Santiago,34641651239,luismos@gmail.com',
        'Hilda del Carmen, Moreno Luna, 34654445588, hmore1@gmail.com',
        'Juan,Perez,45455454,loco@hhh.com']
    
    gestion1.inicializar_contactos()
    #[gestion1.agregar_contacto(contacto) for contacto in contactos1]
    #contacto2 = Contacto('','Ortiz Lopez',0,'')

    #print(gestion1.quitar_acentos('Holá comó éstas tu'))
    #print(gestion1.verificar_contacto('Luis Miguel,Ortiz Santiago,34641651239,luismos@gmail.com'))
    #print(f"\n{gestion1.mostrar_todos_contactos()}")
    
    #print(f"\n{gestion1.mostrar_todos_contactos()}")
    #print(gestion1.agregar_contacto(',,,'))
    #print(gestion1.agregar_contacto('Lucia del Valle,Ortiz Santiago,34641457896,lucia2020@gmail.com'))
    #print(gestion1.buscar_contacto('Luis'))
    print(gestion1.eliminar_contacto('Lucia del Valle,Ortiz Santiago,34641457896,lucia2020@gmail.com'))
   


