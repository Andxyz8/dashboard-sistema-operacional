import subprocess
import platform

class InfoSistema():
    def executa_comando_terminal(self, comando):
        comando_executado = subprocess.run(
            args=comando,
            shell=True,
            capture_output=True,
            universal_newlines=True
        )

        return comando_executado.stdout


    def get_info_system(self):
        variaveis_Sistema = platform.uname()
        return variaveis_Sistema.system


    def get_info_node(self):
        variaveis_Sistema = platform.uname()
        return variaveis_Sistema.node


    def get_info_release(self):
        variaveis_Sistema = platform.uname()
        return variaveis_Sistema.release


    def get_info_version(self):
        variaveis_Sistema = platform.uname()
        return variaveis_Sistema.version


    def get_info_processador(self):
        comando = self.executa_comando_terminal("lshw -class CPU")
        comando = comando.split("cpu")
        comando = comando[1]
        comando = comando.split("fabricante")
        comando = comando[0]
        comando = comando.split(":")
        comando = comando[1]
        return comando


    def get_info_ram(self):
        comando = self.executa_comando_terminal("grep MemTotal /proc/meminfo")
        comando = comando.split(":")
        return str(round((float(comando[1][:-4])/(1024*1024)), 2)) + 'GB'
