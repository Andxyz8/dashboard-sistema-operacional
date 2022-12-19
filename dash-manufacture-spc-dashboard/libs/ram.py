import psutil

class RAM():
    def __init__(self) -> None:
        self.ram_info = {}
        self.total = 0
        self.__inicializa_info_ram()


    def __inicializa_info_ram(self):
        memoria = psutil.virtual_memory()
        self.total = memoria.total
        self.ram_info['Disponivel'] = memoria.available


    def atualiza_info_ram(self):
        memoria = psutil.virtual_memory()
        self.ram_info['Disponivel'] = memoria.available

    
    def get_ram_em_uso(self):
        return (self.total-self.ram_info['Disponivel'])

    