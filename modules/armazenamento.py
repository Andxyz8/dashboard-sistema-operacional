from random import random
import psutil

class Armazenamento():
    def __init__(self) -> None:
        self.total = 0
        self.ocupado = 0
        self.device_info = []
        self.__inicializa_infos_armazenamento()


    def __inicializa_infos_armazenamento(self):
        for i in psutil.disk_partitions():
            dict_particao = {}
            if 'snap' in i.mountpoint:
                continue
            
            try:
                dict_particao['device'] = i.device
                dict_particao['mountpoint'] = i.mountpoint
            except:
                continue
            
            dict_particao['cor'] = self.random_hex_color()
            self.device_info.append(dict_particao)

            espaco = psutil.disk_usage(dict_particao['mountpoint'])
            dict_particao['ocupado'] = round(espaco.used/(1024**3),2)
            self.ocupado += dict_particao['ocupado']
            self.total += round(espaco.total/(1024**3), 2)

        for i in self.device_info:
            i['percentual'] = round((i['ocupado']*100)/self.total, 2)

        # for i in self.device_info:
        #     print(i)

    
    def random_hex_color(self, end=0xff0000):
        return str('#%06X' % round(random() * end))