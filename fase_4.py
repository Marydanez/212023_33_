# ============================================
# PROYECTO: SOFTWARE FJ
# Sistema de Gestión de Clientes, Servicios y Reservas
# Programación Orientada a Objetos + Manejo Avanzado de Excepciones
# ============================================

from abc import ABC, abstractmethod
from datetime import datetime


# =========================================================
# LOGGER
# =========================================================

class Logger:

    ARCHIVO_LOG = "logs.txt"

    @staticmethod
    def registrar(mensaje):

        with open(Logger.ARCHIVO_LOG, "a", encoding="utf-8") as archivo:

            archivo.write(
                f"{datetime.now()} -> {mensaje}\n"
            )


# =========================================================
# EXCEPCIONES PERSONALIZADAS
# =========================================================

class ClienteInvalidoError(Exception):
    pass


class ServicioNoDisponibleError(Exception):
    pass


class ReservaError(Exception):
    pass


# =========================================================
# CLASE ABSTRACTA GENERAL
# =========================================================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# =========================================================
# CLASE CLIENTE
# Encapsulación + Validaciones
# =========================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        self.validar_datos()

    # ==========================
    # VALIDACIONES
    # ==========================

    def validar_datos(self):

        if not self.__nombre.strip():
            raise ClienteInvalidoError(
                "El nombre del cliente está vacío"
            )

        if "@" not in self.__correo:
            raise ClienteInvalidoError(
                "Correo electrónico inválido"
            )

        if len(self.__telefono) < 7:
            raise ClienteInvalidoError(
                "Número telefónico inválido"
            )

    # ==========================
    # GETTERS
    # ==========================

    def get_nombre(self):
        return self.__nombre

    def get_correo(self):
        return self.__correo

    def get_telefono(self):
        return self.__telefono

    # ==========================
    # SETTERS
    # ==========================

    def set_telefono(self, nuevo_telefono):

        if len(nuevo_telefono) < 7:
            raise ClienteInvalidoError(
                "El nuevo teléfono es inválido"
            )

        self.__telefono = nuevo_telefono

    # ==========================
    # MÉTODO ABSTRACTO
    # ==========================

    def mostrar_info(self):

        return (
            f"Cliente: {self.__nombre} | "
            f"Correo: {self.__correo} | "
            f"Teléfono: {self.__telefono}"
        )


# =========================================================
# CLASE ABSTRACTA SERVICIO
# Abstracción + Polimorfismo
# =========================================================

class Servicio(Entidad, ABC):

    def __init__(self, nombre, precio_base):

        self.nombre = nombre
        self.precio_base = precio_base

    # ==========================
    # MÉTODOS ABSTRACTOS
    # ==========================

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    # ==========================
    # SOBRECARGA SIMULADA
    # ==========================

    def calcular_costo_con_extra(
        self,
        impuesto=0,
        descuento=0
    ):

        total = self.calcular_costo()

        total += total * impuesto

        total -= descuento

        return total


# =========================================================
# SERVICIO 1: RESERVA DE SALAS
# =========================================================

class ReservaSala(Servicio):

    def __init__(self, horas):

        super().__init__(
            "Reserva de Sala",
            50
        )

        self.horas = horas

        self.validar_parametros()

    def validar_parametros(self):

        if self.horas <= 0:
            raise ServicioNoDisponibleError(
                "Las horas deben ser mayores a 0"
            )

    def calcular_costo(self):

        return self.precio_base * self.horas

    def descripcion(self):

        return (
            f"Reserva de sala por "
            f"{self.horas} horas"
        )

    def mostrar_info(self):

        return self.descripcion()


# =========================================================
# SERVICIO 2: ALQUILER DE EQUIPOS
# =========================================================

class AlquilerEquipo(Servicio):

    def __init__(self, dias):

        super().__init__(
            "Alquiler de Equipos",
            35
        )

        self.dias = dias

        self.validar_parametros()

    def validar_parametros(self):

        if self.dias <= 0:
            raise ServicioNoDisponibleError(
                "Los días deben ser mayores a 0"
            )

    def calcular_costo(self):

        return self.precio_base * self.dias

    def descripcion(self):

        return (
            f"Alquiler de equipo por "
            f"{self.dias} días"
        )

    def mostrar_info(self):

        return self.descripcion()


# =========================================================
# SERVICIO 3: ASESORÍAS ESPECIALIZADAS
# =========================================================

class AsesoriaEspecializada(Servicio):

    def __init__(self, sesiones):

        super().__init__(
            "Asesoría Especializada",
            120
        )

        self.sesiones = sesiones

        self.validar_parametros()

    def validar_parametros(self):

        if self.sesiones <= 0:
            raise ServicioNoDisponibleError(
                "Las sesiones deben ser mayores a 0"
            )

    def calcular_costo(self):

        return self.precio_base * self.sesiones

    def descripcion(self):

        return (
            f"Asesoría especializada de "
            f"{self.sesiones} sesiones"
        )

    def mostrar_info(self):

        return self.descripcion()


# =========================================================
# CLASE RESERVA
# =========================================================

class Reserva:

    def __init__(
        self,
        cliente,
        servicio,
        duracion
    ):

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"

    # =====================================================
    # CONFIRMAR RESERVA
    # try / except / else / finally
    # =====================================================

    def confirmar(self):

        try:

            if self.duracion <= 0:

                raise ReservaError(
                    "La duración debe ser mayor a 0"
                )

            costo = self.servicio.calcular_costo()

        except Exception as error:

            self.estado = "Fallida"

            Logger.registrar(
                f"ERROR EN RESERVA: {error}"
            )

            # Encadenamiento de excepciones
            raise ReservaError(
                "No fue posible confirmar la reserva"
            ) from error

        else:

            self.estado = "Confirmada"

            Logger.registrar(
                f"Reserva confirmada para "
                f"{self.cliente.get_nombre()}"
            )

            return costo

        finally:

            Logger.registrar(
                "Proceso de reserva finalizado"
            )

    # =====================================================
    # CANCELAR RESERVA
    # =====================================================

    def cancelar(self):

        self.estado = "Cancelada"

        Logger.registrar(
            f"Reserva cancelada para "
            f"{self.cliente.get_nombre()}"
        )

    # =====================================================
    # MOSTRAR INFORMACIÓN
    # =====================================================

    def mostrar_info(self):

        return (
            f"Cliente: {self.cliente.get_nombre()} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Estado: {self.estado}"
        )


# =========================================================
# SISTEMA PRINCIPAL
# =========================================================

clientes = []
reservas = []

print("\n===================================")
print("SISTEMA SOFTWARE FJ")
print("===================================\n")


# =========================================================
# OPERACIONES DEL SISTEMA
# =========================================================

operaciones = [

    # CLIENTES VÁLIDOS
    ("cliente", "Juan Pérez", "juan@gmail.com", "1234567"),
    ("cliente", "María López", "maria@gmail.com", "7654321"),

    # CLIENTES INVÁLIDOS
    ("cliente", "", "correo_malo", "111"),
    ("cliente", "Carlos", "carlosgmail.com", "999"),

    # SERVICIOS CORRECTOS
    ("sala", 4),
    ("equipo", 3),
    ("asesoria", 2),

    # SERVICIOS INCORRECTOS
    ("sala", -5),
    ("equipo", 0),
    ("asesoria", -1)
]


# =========================================================
# EJECUCIÓN DE OPERACIONES
# =========================================================

for operacion in operaciones:

    try:

        # =================================================
        # REGISTRO DE CLIENTES
        # =================================================

        if operacion[0] == "cliente":

            cliente = Cliente(
                operacion[1],
                operacion[2],
                operacion[3]
            )

            clientes.append(cliente)

            print(
                "CLIENTE REGISTRADO:",
                cliente.mostrar_info()
            )

            Logger.registrar(
                f"Cliente registrado: "
                f"{cliente.get_nombre()}"
            )

        # =================================================
        # RESERVA DE SALAS
        # =================================================

        elif operacion[0] == "sala":

            servicio = ReservaSala(
                operacion[1]
            )

            reserva = Reserva(
                clientes[0],
                servicio,
                operacion[1]
            )

            costo = reserva.confirmar()

            reservas.append(reserva)

            print(
                f"RESERVA DE SALA EXITOSA | "
                f"Costo: ${costo}"
            )

        # =================================================
        # ALQUILER DE EQUIPOS
        # =================================================

        elif operacion[0] == "equipo":

            servicio = AlquilerEquipo(
                operacion[1]
            )

            reserva = Reserva(
                clientes[0],
                servicio,
                operacion[1]
            )

            costo = reserva.confirmar()

            reservas.append(reserva)

            print(
                f"ALQUILER EXITOSO | "
                f"Costo: ${costo}"
            )

        # =================================================
        # ASESORÍAS
        # =================================================

        elif operacion[0] == "asesoria":

            servicio = AsesoriaEspecializada(
                operacion[1]
            )

            reserva = Reserva(
                clientes[0],
                servicio,
                operacion[1]
            )

            costo = reserva.confirmar()

            reservas.append(reserva)

            print(
                f"ASESORÍA EXITOSA | "
                f"Costo: ${costo}"
            )

    # =====================================================
    # MANEJO GENERAL DE ERRORES
    # =====================================================

    except Exception as error:

        print(
            "ERROR CONTROLADO:",
            error
        )

        Logger.registrar(
            f"ERROR GENERAL: {error}"
        )


# =========================================================
# MOSTRAR RESULTADOS FINALES
# =========================================================

print("\n===================================")
print("RESUMEN FINAL")
print("===================================\n")

print("CLIENTES REGISTRADOS:\n")

for cliente in clientes:

    print(cliente.mostrar_info())

print("\nRESERVAS REALIZADAS:\n")

for reserva in reservas:

    print(reserva.mostrar_info())


print("\n===================================")
print("SISTEMA FINALIZADO CORRECTAMENTE")
print("===================================\n")