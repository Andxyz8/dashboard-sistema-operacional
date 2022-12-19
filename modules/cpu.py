import psutil

class CPU():
    def __init__(self) -> None:
        self.core_info = []
        self.qtd_cores = psutil.cpu_count()
        self.__inicializa_cpu_info()


    def __get_uso_atual_cpu(self, index):
        return psutil.cpu_percent(interval=0.5, percpu=True)[index]


    def __inicializa_cpu_info(self):
        for index in range(self.qtd_cores):
            dict_cpu_info = {}

            dict_cpu_info[index] = 'CORE_'+str(index)

            dict_cpu_info['uso_anterior'] = []
            
            aux_uso_atual = self.__get_uso_atual_cpu(index)

            dict_cpu_info['uso_anterior'].append(aux_uso_atual)

            dict_cpu_info['uso_atual'] = aux_uso_atual


            self.core_info.append(dict_cpu_info)

    
    def atualiza_info_cores(self):
        for index in range(self.qtd_cores):

            aux_uso_atual = self.__get_uso_atual_cpu(index)

            self.core_info[index]['uso_atual'] = aux_uso_atual

            #if(len(self.core_info[index]['uso_anterior']) > 30):
            #    self.core_info[index]['uso_anterior'] = self.core_info[index]['uso_anterior'][1:]

            self.core_info[index]['uso_anterior'].append(aux_uso_atual)

        #print(self.core_info)


