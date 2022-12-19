from pandas import DataFrame
import psutil

class Processos():
    def __init__(self) -> None:
        self.proc_info = []
        self.qtd_processos = 10
        self.atributos_processos = [
            'pid',
            'name',
            'status',
            'username',
            #'cpu_percent',
            'memory_percent',
            'nice',
        ]
        self.__inicializa_info_processos()

    
    def __inicializa_info_processos(self):
        processos = psutil.process_iter(self.atributos_processos)

        lista_aux = []

        for i in processos:
            lista_aux.append(i.info)
        
        df = DataFrame(lista_aux)

        self.proc_info = df.sort_values('memory_percent', axis=0, ascending=True).to_dict(orient='records')[:self.qtd_processos+1]

        
    def atualiza_info_processos(self):
        processos = psutil.process_iter(self.atributos_processos)

        lista_aux = []

        for i in processos:
            lista_aux.append(i.info)
        
        df = DataFrame(lista_aux)

        self.proc_info = df.sort_values('memory_percent', axis=0, ascending=False).to_dict(orient='records')[:self.qtd_processos+1]

        #print(self.proc_info)

    def get_infos_processo(self, index):
        pid = self.proc_info[index]['pid']
        nome = self.proc_info[index]['name']
        usuario = self.proc_info[index]['username']
        nice = self.proc_info[index]['nice']
        #cpu_percent = self.proc_info[index]['cpu_percent']
        uso_memoria = round(self.proc_info[index]['memory_percent'], 2)
        status = self.proc_info[index]['status']
        return pid, nome, usuario, nice, uso_memoria, status