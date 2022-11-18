# coding: utf-8
# Usuario: gabri

from datetime import datetime as dt
from os import mkdir, name
from os.path import expanduser, exists


class util:
    caminho = str()

    def __init__(self):
        self.gerar_arquivo_log()

    def alerta(self, mensagem):
        hora = dt.now().strftime('%H:%M:%S')
        msg = f'[{hora}] {mensagem}'
        print(msg)
        with open(f'{self.caminho}/{dt.now().strftime("log %d-%m-%y")}.txt', 'a') as arq:
            arq.write(f'\n{msg}')

    def gerar_arquivo_log(self):
        if name == 'nt':
            self.caminho = f'{expanduser("~")}/appdata/Roaming/lokoMercado'
        else:
            self.caminho = f'{expanduser("~")}/.lokoMercado'

        if not exists(self.caminho):
            mkdir(self.caminho)

        if not exists(f'{self.caminho}/{dt.now().strftime("log %d-%m-%y")}.txt'):
            with open(f'{self.caminho}/{dt.now().strftime("log %d-%m-%y")}.txt', 'w') as arq:
                arq.write(dt.now().strftime("log %d-%m-%y\n"))

        print(self.caminho)

# Fim
