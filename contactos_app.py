"""Consola principal del Sistema de Gestion de contactos"""
from validar_casos import Verificar
from gestion_contactos import GestionContactos
from mis_excepciones import MisExcepciones

try:
    entrada = None
    ver = Verificar()
    ges = GestionContactos()
    if not ges.inicializar_contactos():
        raise MisExcepciones(f"No se puede inicializar, fallo "\
                             f"de lectura o escritura en directorio."\
                            , codigo_error=3013)
    while entrada != '5':
        try:
            print("""\n\n*** ---Sistema de Gestion de Contactos--- ***
                1- Agregar Nuevo Contacto 
                2- Buscar Contactos
                3- Mostrar Todos los Contactos
                4- Eliminar Contacto
                5- Salir del Sistema\n""")
            res_ent, entrada = ver.validar_expresion('opcion')
            if not res_ent:
                raise MisExcepciones("Opcion Invalida. Volviendo al menu...")
            if entrada == '1':
                # Agregar Nuevo Contacto
                res_nom, nombre = ver.validar_expresion('nombre', 3)
                if not res_nom:
                    raise MisExcepciones(f"Nombre invalido. Operacion "\
                                         f"Cancelada", codigo_error=3030)
                res_ape, apellido = ver.validar_expresion('apellido', 3)
                if not res_ape:
                    raise MisExcepciones(f"Apellido invalido. Operacion "\
                                         f"Cancelada", codigo_error=3034)
                res_tel, telefono = ver.validar_expresion('telefono' , 3)
                if not res_tel:
                    raise MisExcepciones(f"Telefono invalido. Operacion "\
                                         f"Cancelada", codigo_error=3038)
                res_ema, email = ver.validar_expresion('email',3)
                if not res_ema:
                    raise MisExcepciones(f"Email invalido. Operacion "\
                                         f"Cancelada", codigo_error=3042)
                if not ges.agregar_contacto(f'{nombre}, {apellido},{telefono}\
                                            ,{email}'):
                    raise MisExcepciones("Fallo al Agregar Contacto", \
                                         codigo_error=3046)
                print('Operacion Agregar finalizada con exito.')
                        
            elif entrada == '2':
                    
                    # Buscar Contacto por frase
                res_nom, nombre = ver.validar_expresion('nombre', 3)
                if not res_nom:
                    raise MisExcepciones(f"Busqueda invalida. Operacion "\
                                         f"Cancelada", codigo_error=3055)
                busqueda = ges.buscar_contacto(nombre)
                if len(busqueda) <= 0:
                    raise MisExcepciones(f"No hay Coincidencias para "\
                                         f"{nombre}")
                print('\n***    Lista de coincidencias    ***')
                print('\n------------------------------------')
                print(f'\nHay {len(busqueda)} Coincidencias.\n')
                for i in range(len(busqueda)):
                    print(f'[{i+1}]:{busqueda[i]}')
                print('------------------------------------')
            elif entrada == '3':  
                # Mostrar todos los contactos
                print('\n*** Lista de todos los contactos ***')
                print('\n------------------------------------')
                print(ges.mostrar_todos_contactos())
                print('\n------------------------------------')
                        
            elif entrada == '4': 
                # Eliminar un contacto
                res_nom, nombre = ver.validar_expresion('nombre', 3)
                if not res_nom:
                    raise MisExcepciones(f"Busqueda invalida. Operacion "\
                                         f"Cancelada")
                busqueda = ges.buscar_contacto(nombre)
                if len(busqueda) <= 0:
                    raise MisExcepciones(f"No hay coincidencias para: "\
                                           f"{nombre}")
                print('\n***    Lista de coincidencias    ***')
                print('\n------------------------------------')
                print(f'\nHay {len(busqueda)} Coincidencias.\n')
                for i in range(len(busqueda)):
                    print(f'[{i+1}]:{busqueda[i]}')
                print('------------------------------------')
                res_eli, indice = ver.validar_expresion('elimina', \
                                        n_opcion = len(busqueda))
                if not res_eli:
                    raise MisExcepciones('Indice invalido. Operacion Cancelada')
                i = int(indice)-1
                print(f'Se eliminara el {i+1}\n {busqueda[i]}')
                res_conf, s_n =ver.validar_expresion('s_n')
                if not res_conf: 
                    raise MisExcepciones('Opcion Invalida. Operacion Cancelada')
                if s_n == 'n':
                    raise MisExcepciones('Operacion Cancelada')
                contacto_eliminar = busqueda[i]
                print('Eliminando registro...')
                contacto_eliminar = ges.contacto_cadena(contacto_eliminar)
                if not ges.eliminar_contacto(contacto_eliminar):
                    raise MisExcepciones('No se pudo Eliminar el contacto.', \
                                         codigo_error=3105)
                print('Operacion Eliminar realizada con exito')
                    
            elif entrada == '5':
                # Salir del programa
                print('Saliendo del programa...')
        except MisExcepciones as e:
            print(f'{e}')
        except Exception as e:
            print(f"Error inesperado: {e}")
    print('Fin del programa')
except Exception as e:
     error_traducido = MisExcepciones(error_original=e)
     print(f'{error_traducido}')
