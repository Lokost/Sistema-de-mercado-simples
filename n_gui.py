# coding: UTF-8
# Arquivo: n_gui

from PySimpleGUI import *
from defs import *
from bd import BD

nome_mercado = 'Loko mercado'
f_geral = (None, 10)
theme('reddit')


menus = {
    'principal' : [['Tabelas',[
        'Clientes', 
        'Produtos'
    ]]],

    'tabela': [['Gerenciar',[
        'Adicionar',
        'Remover',
        '---',
        'Limpar Tabela'
    ]]]
}


def login() -> Window:
    """Janela de login para o Banco de dados"""
    host = hosts()

    layout = [
        [
            Text('host'),
            Combo(
                values=host,
                k='hosts',
                default_value=host[0],
                readonly=True
            )
        ],
        [
            Text('Usuário'),
            Input(
                k='usuario',
                justification='c',
                focus=True,
                expand_x=True
            )
        ],
        [
            Text('Senha'),
            Input(
                k='senha',
                password_char='*',
                justification='c',
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
                bind_return_key=True,
                expand_x=True
            )
        ]
    ]

    return Window(
        title='Login',
        layout=layout,
        font=f_geral,
        resizable=False,
        element_justification='r',
        element_padding=10,
        modal=True
    )

def aviso(msg, sn=True, lista=None, tabela=None) -> Window:
    '''Janela de aviso - SN (Sim ou Não)'''

    if lista and tabela:
        for i in lista:
            msg += f'\n{tabela[i][1]}'
    
    else:
        msg += '\n'.join(lista)

    layout = [
        [
            Text(msg)
        ]
    ]

    layout += [
        [
            Button(
                button_text='Sim',
                k='s',
                bind_return_key=True,
                expand_x=True
            ),
            Button(
                button_text='Não',
                k='n',
                expand_x=True
            )
        ]
    ] if sn else [
        [
            Button(
                button_text='OK',
                k='ok',
                expand_x=True
            )
        ]
    ]

    return Window(
        title='Aviso',
        layout=layout,
        element_justification='c',
        font=f_geral,
        element_padding=10,
        modal=True
    )

def principal() -> Window:
    layout = [
        [
            Menu(menus['principal'])
        ],
        [
            Table(
                values=[[]],
                headings=['Produto', 'quantidade', 'Valor'],
                k='saida',
                size=(130,24),
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
                size=(30,1),
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
                k='sub',
                justification='right',
                size=(30, 1)
            )
        ]
    ]

    return Window(
        title=nome_mercado,
        layout=layout,
        font=f_geral,
        element_justification='right',
        element_padding=10,
        resizable=True,
        modal=True,
        finalize=True
    )
    
def table_editor(table: str, bd, heads = []) -> Window:
    tabela = bd.get_table(table)

    layout = [
        [
            Menu(
                menu_definition=menus['tabela']
            )
        ],
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
                k='filter',
                default_value=heads[0]
            )
        ],
        [
            Table(
                values=tabela,
                headings=heads,
                max_col_width=100,
                k='itens',
                justification='center',
                expand_x=True,
                expand_y=True
            )
        ],
        [
            Text(
                f'{len(tabela)} restultado(s) encontrado(s)',
                k='quant'
            )
        ]
    ]

    return Window(
        title='Table editor',
        layout=layout,
        font=f_geral,
        element_justification='c',
        element_padding=10,
        modal=True
    )

def add_itens(values: list[str]) -> Window:
    layout = [[]]
    for i in values:
        layout += [
            [
                Text(f'{i}: '),
                Input(
                    k=i.lower(),
                    expand_x=True
                )
            ]
        ]
    
    layout += [
        [
            Button(
                button_text='Adicionar',
                k='add',
                expand_x=True
            ),
            Button(
                button_text='Cancelar',
                k='cancel',
                expand_x=True
            )
        ]
    ]

    return Window(
        title='Adicionar',
        layout=layout,
        resizable=False,
        font=f_geral,
        element_padding=10,
        modal=True
    )

# Fim