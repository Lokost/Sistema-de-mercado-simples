# coding: utf-8
# Usuario: gabri

"""Arquivo de gerenciamento do banco de dados"""

from mysql.connector import connect
from util import util

a = util()


class BD:
    __mydb = None
    __db_cursor = None

    # Tabelas (O undeline duplo "__" é para deixá-las no modo privado!

    __clientes = '''
                create table clientes(
                    ID int auto_increment primary key not null,
                    Nome varchar(70) not null,
                    CPF varchar(11) not null,
                    Telefone varchar(11),
                    Divida float
                )
                '''

    __produtos = '''
                create table produtos(
                    ID int auto_increment primary key not null,
                    Produto varchar(70) not null,
                    Quantidade int not null,
                    Codigo varchar(30),
                    Preco float not null
                )
                '''

    # Gerenciamento geral do DB
    def conectar(self, host, user, senha) -> bool:
        try:
            self.__mydb = connect(
                host=host,
                user=user,
                password=senha,
                database='teste'
            )  # alterar database para a existente para o serviço!

        except Exception as e:
            a.alerta(str(e))
            a.alerta('host, usuario ou senha estão incorretos!')
            return False

        else:
            a.alerta(f'Login realizado com o usuário: {user}')
            self.__db_cursor = self.__mydb.cursor()
            return True

    def desconectar(self) -> None:
        self.__mydb.disconnect()

    def detectar_tabelas(self) -> None:
        self.__db_cursor.execute('show tables')
        tabelas = self.__db_cursor.fetchall()
        produtos = False
        clientes = False
        for i in tabelas:
            if 'produtos' in i:
                produtos = True

            elif 'clientes' in i:
                clientes = True

        if not produtos:
            self.__db_cursor.execute(self.__produtos)

        if not clientes:
            self.__db_cursor.execute(self.__clientes)

    def get_table(self, table: str) -> list:
        self.__db_cursor.execute(f'select * from {table}')
        return self.__db_cursor.fetchall()

    # Gerenciamento da tabela de produtos
    def obter_produtos(self) -> list:
        self.__db_cursor.execute('select * from produtos')
        return self.__db_cursor.fetchall()

    def registrar_produto(self, prod, quant, cod, preco) -> int:
        try:
            self.__db_cursor.execute('select * from produtos')
            tabela = self.__db_cursor.fetchall()

            for i in tabela:
                if prod in i or cod in i and cod != '':
                    return 2

            sql = 'insert into produtos(Produto, Quantidade, Codigo, Preco) values (%s,%s,%s,%s)'
            val = [prod, quant, cod, preco]
            self.__db_cursor.execute(sql, val)
            self.__mydb.commit()
            return 1

        except Exception as e:
            a.alerta(str(e))
            return 0

    def remover_produtos(self, produtos):
        tabela = self.obter_produtos()
        for i in produtos:
            print(f'Deletando produto: {tabela[i][1]}')
            self.__db_cursor.execute(f'delete from produtos where ID={tabela[i][0]}')
        self.__mydb.commit()

    def resetar_tabela_produtos(self) -> None | list:
        try:
            print('Deletando tabela... aguarde')
            self.__db_cursor.execute('drop table produtos')
            self.__mydb.commit()
            a.alerta('Recarregando tabela... aguarde')
            self.__db_cursor.execute(self.__produtos)
            a.alerta('Pronto!')
            return self.__db_cursor.execute('select * from produtos')

        except Exception as e:
            a.alerta(str(e))

    def pesquisa_produto(self, filtro, pesquisa) -> list:
        self.__db_cursor.execute(f'select * from produtos where {filtro} like "%{pesquisa}%')
        return self.__db_cursor.fetchall()

    # Gerenciamento da tabela clientes
    def obter_clientes(self) -> list:
        self.__db_cursor.execute('select * from clientes')
        return self.__db_cursor.fetchall()

    def resetar_tabela_clientes(self) -> list:
        a.alerta('Deletando tabela clientes... aguarde')
        self.__db_cursor.execute('drop table clientes')
        self.__mydb.commit()
        a.alerta('Recriando tabela clientes... aguarde')
        self.__db_cursor.execute(self.__clientes)
        self.__db_cursor.execute('select * from clientes')
        a.alerta('pronto!')
        return self.__db_cursor.fetchall()
    
    def registrar_cliente(self, nome, cpf, telefone):
        sql = 'insert into clientes(Nome, CPF, Telefone) values (%s, %s, %s)'
        val = (nome, cpf, telefone)
        tabela = self.obter_clientes()
        existente = False

        try:
            for i in tabela:
                if nome in i or cpf in i:
                    existente = True

                if not existente:
                    self.__db_cursor.execute(sql, val)
                    self.__mydb.commit()
                    return 0

                else:
                    return 2

        except Exception as e:
            a.alerta(e)
            return 1

    def pesquisar_clientes(self, pesquisa, filtro):
        self.__db_cursor.execute(f'select * from clientes where {filtro} like "%{pesquisa}%"')
        return self.__db_cursor.fetchall()
# Fim
