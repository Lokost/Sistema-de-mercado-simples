# coding: utf-8
# Usuario: gabri

"""Funções estáticas do aplicativo"""

def hosts():
    h = open('hosts.txt').read()
    lista = h.split('\n')
    return lista


# Fim
