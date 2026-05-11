from abc import ABC, abstractmethod
from datetime import datetime


# =====================================================
# LOGGER
# =====================================================

class Logger:

    @staticmethod
    def registrar(mensaje):

        with open("logs.txt", "a", encoding="utf-8") as archivo:

            archivo.write(
                f"{datetime.now()} -> {mensaje}\n"
            )


# =====================================================
# EXCEPCIONES
# =====================================================

class ClienteInvalidoError(Exception):
    pass


class ServicioError(Exception):
    pass


class ReservaError(Exception):
    pass


# =====================================================
# CLASE ABSTRACTA
# =====================================================

class Entidad(ABC):

    @abstractmethod
    def mostrar_info(self):
        pass


# =====================================================
# CLIENTE
# =====================================================

class Cliente(Entidad):

    def __init__(self, nombre, correo, telefono):

        self.__nombre = nombre
        self.__correo = correo
        self.__telefono = telefono

        self.validar()

    def validar(self):

        if not self.__nombre.strip():
            raise ClienteInvalidoError(
                "Nombre vacío"
            )

        if "@" not in self.__correo:
            raise ClienteInvalidoError(
                "Correo inválido"
            )

        if len(self.__telefono) < 7:
            raise ClienteInvalidoError(
                "Teléfono inválido"
            )

    def get_nombre(self):
        return self.__nombre

    def mostrar_info(self):

        return (
            f"{self.__nombre} | "
            f"{self.__correo} | "
            f"{self.__telefono}"
        )


# =====================================================
# SERVICIO ABSTRACTO
# =====================================================

class Servicio(ABC):

    def __init__(self, nombre, precio):

        self.nombre = nombre
        self.precio = precio

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# =====================================================
# SERVICIOS
# =====================================================

class ReservaSala(Servicio):

    def __init__(self, horas):

        super().__init__(
            "Reserva Sala",
            50
        )

        self.horas = horas

    def calcular_costo(self):

        return self.precio * self.horas

    def descripcion(self):

        return (
            f"Sala reservada "
            f"{self.horas} horas"
        )


class AlquilerEquipo(Servicio):

    def __init__(self, dias):

        super().__init__(
            "Alquiler Equipo",
            35
        )

        self.dias = dias

    def calcular_costo(self):

        return self.precio * self.dias

    def descripcion(self):

        return (
            f"Equipo alquilado "
            f"{self.dias} días"
        )


class AsesoriaEspecializada(Servicio):

    def __init__(self, sesiones):

        super().__init__(
            "Asesoría",
            120
        )

        self.sesiones = sesiones

    def calcular_costo(self):

        return self.precio * self.sesiones

    def descripcion(self):

        return (
            f"Asesoría de "
            f"{self.sesiones} sesiones"
        )


# =====================================================
# RESERVA
# =====================================================

class Reserva:

    def __init__(
        self,
        cliente,
        servicio
    ):

        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):

        try:

            costo = self.servicio.calcular_costo()

        except Exception as e:

            self.estado = "Fallida"

            Logger.registrar(str(e))

            raise ReservaError(
                "No se pudo confirmar"
            ) from e

        else:

            self.estado = "Confirmada"

            return costo

        finally:

            Logger.registrar(
                "Proceso finalizado"
            )

    def mostrar_info(self):

        return (
            f"Cliente: "
            f"{self.cliente.get_nombre()} | "
            f"Servicio: "
            f"{self.servicio.nombre} | "
            f"Estado: "
            f"{self.estado}"
        )


# =====================================================
# LISTAS
# =====================================================

clientes = []
reservas = []


# =====================================================
# MENÚ PRINCIPAL
# =====================================================

while True:

    print("\n========== SOFTWARE FJ ==========")
    print("1. Registrar cliente")
    print("2. Crear reserva")
    print("3. Ver clientes")
    print("4. Ver reservas")
    print("5. Salir")

    opcion = input("Seleccione una opción: ")

    # =================================================
    # REGISTRAR CLIENTE
    # =================================================

    if opcion == "1":

        try:

            nombre = input("Nombre: ")
            correo = input("Correo: ")
            telefono = input("Teléfono: ")

            cliente = Cliente(
                nombre,
                correo,
                telefono
            )

            clientes.append(cliente)

            print("Cliente registrado")

            Logger.registrar(
                f"Cliente agregado: {nombre}"
            )

        except Exception as e:

            print("ERROR:", e)

            Logger.registrar(str(e))

    # =================================================
    # CREAR RESERVA
    # =================================================

    elif opcion == "2":

        try:

            if len(clientes) == 0:

                raise ReservaError(
                    "No hay clientes registrados"
                )

            print("\nCLIENTES:")

            for i, c in enumerate(clientes):

                print(
                    i,
                    "-",
                    c.get_nombre()
                )

            indice = int(
                input("Seleccione cliente: ")
            )

            cliente = clientes[indice]

            print("\nSERVICIOS")
            print("1. Reserva Sala")
            print("2. Alquiler Equipo")
            print("3. Asesoría")

            tipo = input(
                "Seleccione servicio: "
            )

            # =========================================
            # SALA
            # =========================================

            if tipo == "1":

                horas = int(
                    input("Horas: ")
                )

                servicio = ReservaSala(horas)

            # =========================================
            # EQUIPO
            # =========================================

            elif tipo == "2":

                dias = int(
                    input("Días: ")
                )

                servicio = AlquilerEquipo(dias)

            # =========================================
            # ASESORÍA
            # =========================================

            elif tipo == "3":

                sesiones = int(
                    input("Sesiones: ")
                )

                servicio = AsesoriaEspecializada(
                    sesiones
                )

            else:

                raise ServicioError(
                    "Servicio inválido"
                )

            reserva = Reserva(
                cliente,
                servicio
            )

            costo = reserva.confirmar()

            reservas.append(reserva)

            print(
                f"Reserva creada. "
                f"Costo: ${costo}"
            )

            Logger.registrar(
                "Reserva creada correctamente"
            )

        except Exception as e:

            print("ERROR:", e)

            Logger.registrar(str(e))

    # =================================================
    # VER CLIENTES
    # =================================================

    elif opcion == "3":

        print("\nCLIENTES:\n")

        for cliente in clientes:

            print(cliente.mostrar_info())

    # =================================================
    # VER RESERVAS
    # =================================================

    elif opcion == "4":

        print("\nRESERVAS:\n")

        for reserva in reservas:

            print(reserva.mostrar_info())

    # =================================================
    # SALIR
    # =================================================

    elif opcion == "5":

        print("Saliendo del sistema...")

        break

    else:

        print("Opción inválida")