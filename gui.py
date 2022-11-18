# coding: utf-8
# Usuario: gabri

from PySimpleGUI import *
from defs import *
from bd import *

nome_mercado = 'Loko mercado'
bd = BD()
f_geral = (None, 10)
theme('SystemDefault1')

def login():
    """Janela de login para o Banco de dados"""
    layout = [
        [
            Text(
                text='host'
            ),
            Combo(
                values=hosts(),
                k='host',
                default_value=hosts()[0],
                readonly=True
            )
        ],
        [
            Text(
                text='Usuário'
            ),
            Input(
                k='usuario',
                justification='center',
                focus=True
            ),
        ],
        [
            Text(
                text='Senha'
            ),
            Input(
                key='senha',
                password_char='*',
                justification='center',
                expand_x=True
            )
        ],
        [
            Text(
                text='Erro no login!',
                text_color='red',
                tooltip='Mais informações no terminal',
                visible=False,
                k='erro'
            )
        ],
        [
            Button(
                button_text='Entrar',
                k='login',
                bind_return_key=True
            )
        ]
    ]

    janela = Window(
        title='Login',
        layout=layout,
        font=f_geral,
        resizable=False,
        element_justification='right',
        modal=True
    )
    a.alerta('Bem vindo ao sistema de mercado LokoMercado!')

    while True:
        evt, val = janela.read()
        if evt == WIN_CLOSED:
            break

        elif evt == 'login':
            if bd.conectar(val['host'], val['usuario'], val['senha']):
                janela.close()
                return True

            else:
                janela['erro'].update(
                    visible=True
                )


def aviso(msg, sn=True, lista=None, tabela=str()):
    """Janela de aviso - SN (Sim e Não)"""
    if tabela == 'produtos':
        tabela = bd.obter_produtos()

    if lista and tabela != '':
        for i in lista:
            msg += '\n' + tabela[i][1]

    else:
        msg += '\n'.join(lista)

    if sn:
        layout = [
            [
                Text(
                    text=msg
                )
            ],
            [
                Button(
                    button_text='Sim',
                    k='sim',
                    bind_return_key=True
                ),
                Button(
                    button_text='Não',
                    k='nao'
                )
            ]
        ]

    else:
        layout = [
            [
                Text(
                    text=msg
                )
            ],
            [
                Button(
                    button_text='ok',
                    k='ok',
                    bind_return_key=True
                )
            ]
        ]

    janela = Window(
        title='Aviso',
        layout=layout,
        element_justification='center',
        font=f_geral,
        modal=True
    )

    while True:
        evt, val = janela.read()

        if evt in ['nao', 'ok', WIN_CLOSED]:
            janela.close()
            return False

        elif evt == 'sim':
            janela.close()
            return True


def principal():
    menu = [
        ['Tabelas', [
            'Clientes',
            'Produtos'
        ]]
    ]

    layout = [
        [
            Menu(
                menu_definition=menu
            )
        ],
        [
            Listbox(
                values=[],
                k='saida',
                size=(130, 24),
                font=(None, 15),
                expand_x=True,
                expand_y=True
            )
        ],
        [
            Text(
                text='Valor:',
                font=(None, 20)
            ),
            Text(
                text='0.0',
                font=(None, 20),
                background_color='gray',
                text_color='white',
                size=(30, 1),
                k='valor',
                justification='right'
            )
        ],
        [
            Text(
                text='SubTotal:',
                font=(None, 20)
            ),
            Text(
                text='0.0',
                font=(None, 20),
                background_color='gray',
                text_color='white',
                size=(30, 1),
                k='sub',
                justification='right'
            )
        ]
    ]

    janelas = {
        "Clientes": lambda: clientes(),
        "Produtos": lambda: produtos()
    }

    janela = Window(
        title=nome_mercado,
        layout=layout,
        font=f_geral,
        element_justification='right',
        modal=True
    )

    while True:
        evt, val = janela.read()
        if evt == WIN_CLOSED:
            return 3

        elif evt in janelas:
            janelas[evt]()


def clientes():
    bd.detectar_tabelas()

    menu = [
        [
            'Gerenciar', [
                'Adicionar',
                'Remover',
                '---',
                'Limpar Tabela'
            ]
        ]
    ]

    heads = [
        'ID',
        'Nome'
    ]

    resultado = bd.obter_clientes()

    layout = [
        # Linha 1
        [
            Menu(
                menu_definition=menu
            )
        ],
        # Linha 2
        [
            Text(
                text='Pesquisa:'
            ),
            Input(
                k='pesquisa',
                enable_events=True,
                justification='center',
                expand_x=True
            ),
            OptionMenu(
                values=heads,
                k='filtro',
                default_value=heads[0]
            )
        ],
        # Linha 3
        [
            Table(
                values=resultado,
                headings=heads,
                k='clientes',
                justification='center',
                expand_x=True,
                expand_y=True
            )
        ],
        # Linha 4
        [
            Text(
                text=f'{len(resultado)} resultados encontrados',
                k='quant'
            )
        ],
        # Linha 5
        [
            Button(
                button_text='Info do cliente',
                k='info',
                tooltip='Visualisar informações do cliente selecionado',
                expand_x=True
            )
        ]
    ]

    janela = Window(
        title='Clientes',
        layout=layout,
        font=f_geral,
        element_justification='center',
        modal=True
    )

    def atualizar():
        janela['clientes'].update(resultado)
        janela['quant'].update()

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break

        elif evt == 'Adicionar':
            adicionar_cliente()
            resultado = bd.obter_clientes()
            atualizar()

        elif evt == 'pesquisa':
            resultado = bd.pesquisar_clientes(val['pesquisa'], val['filtro'])

        elif evt == 'Limpar tabela':
            bd.resetar_tabela_clientes()
            resultado = bd.obter_clientes()
            atualizar()


def adicionar_cliente():
    layout = [
        [
            Text(
                text='Nome*'
            ),
            Input(
                k='nome'
            )
        ],
        [
            Text(
                text='CPF*'
            ),
            Input(
                k='cpf'
            )
        ],
        [
            Text(
                text='Telefone'
            ),
            Input(
                k='tel'
            )
        ],
        [
            Text(
                text='Verifique os dados registrados!',
                visible=False,
                key='aviso'
            )
        ],
        [
            Button(
                button_text='Cadastrar',
                k='cad',
                expand_x=True,
                bind_return_key=True
            ),
            Button(
                button_text='Cancelar',
                k='cancel',
                expand_x=True
            )
        ]
    ]

    janela = Window(
        title='Adicionar cliente',
        layout=layout,
        font=f_geral,
        resizable=False,
        element_justification='right',
        modal=True
    )

    while True:
        evt, val = janela.read()

        if evt in [WIN_CLOSED, 'cancel']:
            janela.close()
            break

        if evt == 'cad':
            reg = bd.registrar_cliente(val['nome'], val['cpf'], val['tel'])

            match reg:
                case 1:
                    janela['aviso'].update(
                        text='Não foi possível realizar o cadastro!',
                        visible=True
                    )

                case 2:
                    janela['aviso'].update(
                        text='Cliente já cadastrado!',
                        visible=True
                    )

                case 0:
                    janela.close()
                    break


def produtos():
    menu = [
        ['Gerenciar', [
            'Adicionar',
            'Remover',
            '---',
            'Limpar Tabela'
        ]]
    ]
    heads = [
        'ID',
        'Produto',
        'Quantidade',
        'Código',
        'Preço'
    ]

    filtros = [
        'ID',
        'Produto',
        'Codigo'
    ]

    lista_prod = bd.obter_produtos()

    layout = [
        # Linha 1
        [
            Menu(
                menu_definition=menu
            )
        ],
        # Linha 2
        [
            Text(
                text="Pesquisa"
            ),
            Input(
                k='Pesquisa',
                enable_events=True,
                expand_x=True
            ),
            OptionMenu(
                values=filtros,
                default_value=filtros[0],
                k='filtro'
            )
        ],
        # Lista 3
        [
            Table(
                values=lista_prod,
                headings=heads,
                max_col_width=100,
                k='produtos',
                justification='center',
                expand_y=True,
                expand_x=True
            )
        ],
        # Lista 4
        [
            Text(
                text=f'{len(lista_prod)} resultado(s) encontrado(s)',
                k='quant_prod'
            )
        ]
    ]

    janela = Window(
        title='Produtos',
        layout=layout,
        font=f_geral,
        element_justification='center',
        modal=True
    )

    while True:
        evt, val = janela.read()

        if evt == WIN_CLOSED:
            break

        elif evt == 'Adicionar':
            janela.close()
            adicionar_produto()
            break

        elif evt == 'Remover':
            if aviso('Deseja deletar os seguintes itens?', sn=True, lista=val['produtos']) and val['produtos']:
                bd.remover_produtos(val['produtos'])
                lista_prod = bd.obter_produtos()

            else:
                aviso('Selecione ao menos um item para remover', False)

        elif evt == 'Limpar tabela':
            if aviso('Deseja limpar a tabela produtos?'):
                janela['produtos'].update(bd.resetar_tabela_produtos())

        elif evt == 'pesquisa':
            lista_prod = bd.pesquisa_produto(val['filtro'], val['pesquisa'])

        janela['produtos'].update(lista_prod)
        janela['quant_prod'].update(f'{len(lista_prod)} resultado(s) encontrado(s)')


def adicionar_produto():
    layout = [
        # Linha 1
        [
            Text(
                text='Produto*'
            ),
            Input(
                k='produto',
                expand_x=True
            )
        ],
        # Linha 2
        [
            Text(
                text='Quantidade*'
            ),
            Input(
                k='quant',
                expand_x=True
            )
        ],
        # Linha 3
        [
            Text(
                text='Código'
            ),
            Input(
                k='cod',
                expand_x=True
            )
        ],
        # Linha 4
        [
            Text(
                text='Preço'
            ),
            Input(
                k='preco',
                expand_x=True
            )
        ],
        # Linha 5
        [
            Text(
                text='Verifique as informações inseridas',
                text_color='red',
                visible=False,
                k='erro'
            )
        ],
        # Linha 6
        [
            Button(
                button_text='Registrar',
                k='regis',
                expand_x=True,
                bind_return_key=True
            ),
            Button(
                button_text='Cancelar',
                k='cancel',
                expand_x=True
            )
        ]
    ]

    janela = Window(
        title='Adicionar Produto',
        layout=layout,
        font=f_geral,
        element_justification='right',
        modal=True
    )

    while True:
        evt, val = janela.read()

        if evt in [WIN_CLOSED, 'cancel']:
            janela.close()
            break

        elif evt == 'regis':
            registro = bd.registrar_produto(val['produto'], val['quant'], val['cod'], val['preco'])
            match registro:
                case 0:
                    janela['erro'].update('Verifique as informações digitadas', visible=True)

                case 1:
                    janela['erro'].update('Produto já registrado', visible=True)

                case _:
                    janela.close()

# Fim
