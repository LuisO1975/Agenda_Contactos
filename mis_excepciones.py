"""Crearemos una clase MisExcepciones clase hija de Exception, para 
controlar las excepciones que se produzcan de manera efectiva"""
class MisExcepciones(Exception):
    """Clase personalizada para manejar excepciones específicas y traducir errores al español."""

    # Diccionario de traducción de errores estándar al español
    ERRORES_TRADUCIDOS = {
        "ValueError": "Valor no válido.",
        "TypeError": "Tipo de dato no válido.",
        "KeyError": "Clave no encontrada en el diccionario.",
        "IndexError": "Índice fuera de rango.",
        "ZeroDivisionError": "No se puede dividir entre cero.",
        "FileNotFoundError": "Archivo no encontrado.",
        "IOError": "Error de entrada/salida.",
    }

    def __init__(self, mensaje=None, codigo_error=None, error_original=None):
        """
        Inicializa la excepción personalizada.

        Args:
            mensaje (str): Mensaje descriptivo del error.
            codigo_error (int, opcional): Código de error asociado.
            error_original (Exception, opcional): Excepción original capturada.
        """
        if error_original:
            # Traduce el error original si está en el diccionario
            tipo_error = type(error_original).__name__
            mensaje = self.ERRORES_TRADUCIDOS.get(tipo_error, str(error_original))
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        self.error_original = error_original

    def __str__(self):
        """Devuelve una representación en cadena de la excepción."""
        if self.codigo_error:
            return f"[Error {self.codigo_error}]: {self.mensaje}"
        return self.mensaje