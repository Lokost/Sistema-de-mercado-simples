# coding: UTF-8
# Arquivo: janelas

from n_gui import *
from bd import *

bd = BD()

def entrar() -> bool | None:
    janela=login()

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break

        elif evt == 'login':
            if bd.conectar(val['hosts'], val['usuario'], val['senha']):
                janela.close()
                return True
            
            else:
                janela['erro'].update( visible=True )

def inicio():
    janela = principal()
    janela.TKroot.minsize(840, 630)

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break
            
        elif evt == 'Clientes':
            clientes()
        
        elif evt == 'Produtos':
            produtos()

def clientes():
    janela = table_editor('clientes', bd, ['Nome', 'CPF', 'Telefone'])

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break

def produtos():
    janela = table_editor('produtos', bd, ['ID','Produto', 'Quantidade', 'Código', 'Preço'])

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break

        if evt == 'Adicionar':
            prod = add_product()
            if prod:
                bd.registrar_produto(*prod)
                janela['itens'].update(bd.get_table('produtos'))

def warning(msg:str, sn:bool, lista:list = [], table:list[list] = [[]]):
    janela = aviso(msg, sn, lista, table)

    while True:
        evt, val = janela.read()

        if evt in ['ok', 'n', WIN_CLOSED]:
            janela.close()
            return False
        
        elif evt == 's':
            janela.close()
            return True

def add_product():
    itens = ['Produto', 'Quantidade', 'Código', 'Preço']
    janela = add_itens(itens)
    valid = False

    while True:
        evt, val = janela.read()

        if evt in ['cancel', WIN_CLOSED]:
            janela.close()
            break
        
        if evt == 'add':
            keys = [i.lower() for i in itens]
            info = [val[i] for i in keys]
            if None in info or '' in info:
                valid = False
                warning('Falta informações!', False)
            else:
                valid = True
                janela.close()
                return info

# Fim