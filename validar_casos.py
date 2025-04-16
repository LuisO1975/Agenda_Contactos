"""Clase Verificar para poder validar expresiones regulares, tendra 5 
atributos constantes de clase que corresponden a las expresiones regulares
y 1 metodo de clase: 

Metodo:
- validar_expresion: Se usara una llave (key) para escoger que opcion sera
validada.


Accederemos a esta clase para verificar las entradas que provea un usuario"""
import re

class Verificar:
    """Clase para hacer la verificación de las expresiones regulares"""
    NOMBRE_R = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'
    APELLIDO_R = r'^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$'
    TELEFONO_R = r'^(?:\+34|0034|34)?[6-9]\d{8}$'
    MAIL_R = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    S_N = r'^[sSnN]$'
    
    @classmethod
    def validar_expresion(cls, key: str, n_intentos: int =3, \
                          n_opcion: int =0) -> tuple:
        """Valida una expresión regular.

        Argumentos:
            key (str): 'nombre', 'apellido', 'telefono', 'email'
                        'elimina' , 's_n' o 'opcion'.
            n_intentos: Numero de intentos  (opcional) 3 por defecto.
            n_opcion: Numero de opciones a escoger (solo key='elimina' lo usa)

        Salida: tupla de valores (resultado: bool, valor: str)
            resultado: True si la expresión es válida, False en caso contrario.
            valor: cadena ingresada ya verficada, None si es invalida.
        """
        def generar_patron(x: int) -> str:
            """Genera una expresión regular para validar números entre 1 y x."""
            if x < 10:
                # Si x es menor que 10, solo permitir números de un dígito.
                return rf'^[1-{x}]$'
            else:
                # Si 10 <= x < 99, incluir números de uno y dos dígitos.
                return rf'^[1-9]$|^[1-9][0-9]$|^{x}$'
        
        intentos = n_intentos  # Número máximo de intentos.
        while intentos > 0:
            if key == 'nombre':
                # Evalua que el Nombre este correcto.
                entrada = input("Introduce el Nombre (solo letras y espacios): ")
                if re.fullmatch(cls.NOMBRE_R, entrada):
                    return (True, entrada.title())
                else:
                    print(f"Error: Solo se permiten letras y espacios, "\
                          f"Inténtalo de nuevo.")
            elif key == 'apellido':
                # Evalua que los apellidos esten correctos.
                entrada = input("Introduce el Apellido (solo letras y espacios): ")
                if re.fullmatch(cls.APELLIDO_R, entrada):
                    return (True, entrada.title())
                else:
                    print(f"Error: Solo se permiten letras y espacios, "\
                          f"Inténtalo de nuevo.")
            elif key == 'telefono':
                # Evalua que el telefono tenga formato de España.
                entrada = input("Introduce el Teléfono (Ejm: +34XXXXXXXXX): ")
                if re.fullmatch(cls.TELEFONO_R, entrada):
                    entrada = '+34'+ entrada[-9:]
                    return (True, entrada)
                else:
                    print("Error: Ingresa un número de teléfono válido.")
            elif key == 'email':
                # Evalua que el email cumpla con las condiciones de email.
                entrada = input("Introduce el Email (Ejm: micorreo@micorreo.com): ")
                if re.fullmatch(cls.MAIL_R, entrada.lower()):
                    return (True, entrada)
                else:
                    print("Error: Ingresa un email válido.")
            elif key == 'elimina':
                #print(n_opcion)
                patron = generar_patron(n_opcion)
                # print(patron)
                entrada = input(f"Introduce el Indice a Eliminar (1-{n_opcion}): ")
                if re.fullmatch(patron, entrada.lower()):
                    return (True, entrada)
                else:
                    print("Error: Ingresa un Numero válido.")
            elif key == 'opcion':
                #print(n_opcion)
                patron = generar_patron(5)
                # print(patron)
                entrada = input(f"Escoge una Opcion (1-5): ")
                if re.fullmatch(patron, entrada.lower()):
                    return (True, entrada)
                else:
                    print("Error: Ingresa un Numero válido.")
            elif key == 's_n':
                entrada = input("Quiere realizar esta accion (S/N): ")
                if re.fullmatch(cls.S_N, entrada.lower()):
                    return (True, entrada)
            else:
                print("Error: Llave no válida.")
                return (False, None)

            intentos -= 1  # Reducir el número de intentos
            if intentos > 0:
                print(f"Te quedan {intentos} intentos.")
            else:
                print("Has excedido el número máximo de intentos.")
                return (False, None)

"""Este codigo que sigue es solo con motivo de hacer pruebas al modulo"""
if __name__ == '__main__':
    entrada = None
    ver_1 = Verificar()
    while entrada != 6:
        resultado = False
        print("""*** Evaluar expresiones ***
              1.- Evaluar Nombre
              2.- Evaluar Apellido
              3.- Evaluar Número de Teléfono
              4.- Evaluar Email
              5.- Evaluar Numero de indice
              6.- Salir""")
        entrada = int(input('Ingresa una Opción (1-5): '))
        if entrada == 1:
            resultado, valor = ver_1.validar_expresion('nombre',3)
            if resultado:
                print(f'El Nombre es: {valor}')
        elif entrada == 2:
            resultado, valor = ver_1.validar_expresion('apellido',2)
            if resultado:
                print(f'El Apellido es: {valor}')
        elif entrada == 3:
            resultado, valor = ver_1.validar_expresion('telefono')
            if resultado:
                print(f'El Telefono es: {valor}')
        elif entrada == 4:
            resultado, valor = ver_1.validar_expresion('email')
            if resultado:
                print(f'El email es: {valor}')
        elif entrada == 5:
            resultado, valor = ver_1.validar_expresion('elimina', n_opcion = 6)
            if resultado:
                print(f'El indice a eliminar es: {valor}')
        elif entrada == 6:
            print('Salir del programa')

    