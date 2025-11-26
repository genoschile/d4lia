import asyncio
from typing import AsyncGenerator

class SillonEventManager:
    def __init__(self):
        self.listeners: set[asyncio.Queue] = set()

    async def subscribe(self) -> AsyncGenerator:
        """
        Cada suscriptor obtiene una cola asyncio.Queue donde recibirá eventos.
        """
        queue = asyncio.Queue()
        self.listeners.add(queue)
        try:
            while True:
                # Espera a que llegue un evento y lo emite al cliente
                yield await queue.get()
        finally:
            self.listeners.remove(queue)

    async def emit(self, sillon):
        """
        Envía un sillón actualizado a todos los suscriptores activos.
        """
        for queue in self.listeners:
            await queue.put(sillon)


# Instancia global (singleton)
sillon_event_manager = SillonEventManager()
