# Model : camada de armazenamento e manipulação de dados
import os
import datetime
START_TIME: int = 22
MAX_ATTEMPS: int = 3
# Dicionario com as informações do processo
# [0]*PID       = Id do processo
# [1]*COMMAND   =  O nome do arquivo do executável entre parênteses
# [2]*STATE     = Estado do processo
#       -> R : em execução
#       -> S : aguardando por interrupção
#       -> D : aguardando por não interrupção
#       -> Z : zumbi
#       -> T : paralisado ou rastreado
# [3]*PPID      = PID do processo pai
# [4]PGRP      = ID do grupo do processo
# [5]SESSION   = ID da sessão do processo
# [6]TTY       = tty que o processo usa
# [7]TPGID     = A ID do grupo do processo que atualmente detém o tty no qual o processo está conectado.
# [8]FLAGS     = indicadores do processo
# [9]MINFLT    = número de pequenos erros do processo
# [10]CMINFLT   = número de erros menores do processo e de seus processos filhos.
# [11]MAJFLT    = número de erros maiores do processo;
# [12]UTIME     = número de ciclos do processador que o processo tem previsto em modo usuário;
# [13]STIME     = número de ciclos do processador que o processo tem previsto em modo kernel;
# [14]CUTIME    = número de ciclos do processador que o processo e seus filhos têm previsto em modo usuário;
# [15]CSTIME    = número de ciclos do processador que o processo e seus filhos têm previstos em modo kernel;
# [16]COUNTER   = número máximo de ciclos do processador do próximo período de processamento destinado ao processo, ou o tempo restante no período atual, caso o processo esteja ocupando o processador.
# [17]PRIORITY  = valor padrão acrescido de 15. O valor nunca é negativo no kernel.
# [18]TIMEOUT   = tempo em ciclos do processador do próximo período de espera;
# [19]ITREALVALUE   = O tempo (em ciclos do processador) antes que o próximo SIGALRM seja enviado para o processo relativo a um intervalo de tempo.
# [20]*STARTTIME = tempo, em ciclos do processador, que o processo iniciou após o sistema ser iniciado.
# [21]*VSIZE     = tamanho da memória virtual;
# [22]RSS       = tamanho do conjunto residente;
# [23]RLIM      = Limite em bytes do rss do processo (normalmente 2,147,483,647).
# [24]STARTCODE = O endereço acima do qual o texto do  programa deve ser executado.
# [25]ENDCODE   = O endereço abaixo do qual o texto do programa deve ser executado.
# [26]STARTSTACK    = endereço de início da pilha;
# [27]KSTKESP   = O valor atual de esp (ponteiro da pilha com 32 bits), conforme encontrado na pilha de páginas do kernel para o processo.
# [28]KSTKEIP   = EIP atual (ponteiro da instrução com 32 bits).
# [29]SIGNAL    = mapa de bits dos sinais pendentes (normalmente zero).
# [30]BLOCKED   = mapa de bits dos sinais bloqueados
# [31]SIGIGNORE = mapa de bits dos sinais ignorados
# [32]SIGCATCH  = mapa de bits de sinais recebidos
# [33]WCHAN     = Este é o canal no qual o processo fica esperando. Este é o endereço da chamada ao sistema, e pode ser analisada em uma lista de nomes, caso se necessite de um nome textual (caso se tenha um /etc/psdatabase atualizado, então tente ps -l para ver o campo WCHAN em ação).
proc = '/proc'

# ID : int
# name : str
class VProcess:
    def __init__(self, id : int, command: str, state: str, PPID: int, start_time: str, vsize: int):
        self.id = id
        self.command = command
        if (state=='R'):
            self.state = "Execução"
        elif(state == 'S' or state == 'D'):
            self.state = "Aguardando"
        elif(state == 'Z'):
            self.state = "Zumbi"
        elif(state == 'T'):
            self.state = "Paralisado"
        elif(state == 'I'):
            self.state = "Inativo"
        else:
            self.state = "Desconhecido"
        self.PPID = PPID
        #date = datetime.datetime.fromtimestamp(int(start_time))
        #self.start_time = date.strftime("%Y-%m-%d %H:%M:%S")
        self.start_time = start_time
        self.vsize = vsize
    def getId(self) -> int:
        return self.id
    def getCommand(self) -> str:
        return self.command
    def getState(self) -> str:
        return self.state
    def getInfo(self) -> list:
        return [self.id, self.command, self.state, self.PPID, self.start_time, self.vsize]

def findPIDs() -> list:
    pid = []
    if os.path.exists(proc):
        dir_list = os.listdir(proc)
        for name_dir in dir_list:
            if name_dir.isdigit():
                pid.append(name_dir)
    return pid

def findName(pid : int) -> str | None:
    path = f"{proc}/{pid}"
    if os.path.exists(path):
        with open(f"{path}/comm", "r") as file:
            return file.readline().strip()
    return None

def getInfoProcess() -> list:
    list_process: list = []
    lpid = findPIDs()
    for pid in lpid:
        try:
            with open(f"/proc/{pid}/stat") as file:
                process_info = file.readline().strip().split()
                list_process.append(VProcess(int(process_info[0]), str(process_info[1]), str(process_info[2]), int(process_info[3]), str(process_info[START_TIME]), int(process_info[21])))
                ok = True
        except Exception as e:
            print(f"ERROR({pid}): {e}")
    return list_process
