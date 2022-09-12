from functools import partial
from tkinter import *
import tkinter.font
import random
import pygame
import os


# Criando uma classe para aplicar o hover nos botões
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self['image'] = img_botoes[f'botao{self["text"]}']

    def on_enter(self, e):
        self['image'] = img_botoes[f'botao{self["text"]}hover']

    def on_leave(self, e):
        self['image'] = img_botoes[f'botao{self["text"]}']


def main():
    resetar_jogo()
    limpar_janela()

    # Label para exibir o layout do jogo
    label_bg['image'] = layout_img
    label_bg.place(x=0, y=0)

    # Posicionando todos os botões de órgãos
    criar_botoes()

    # Embaralhando a ordem dos órgãos que serão pedidos
    embaralhar_orgaos()

    # Label para exibir o órgão pedido
    orgao_pedido.place(x=150, y=575)

    # Botão de confirmar a posição escolhida do órgão
    botao_confirmar['command'] = confirmar_posicao
    botao_confirmar.place(x=420, y=562)

    # Botão de reset
    botao_reset['command'] = resetar_jogo
    botao_reset.place(x=100, y=15)

    # Botao de menu
    botao_menu['command'] = menu_principal
    botao_menu.place(x=20, y=15)


def menu_principal():
    resetar_jogo()
    limpar_janela()

    # Colocando a imagem de fundo do menu principal
    label_bg['image'] = menu_img
    label_bg.place(x=0, y=0)

    # Botão para começar o jogo
    botao_novo_jogo['command'] = main
    botao_novo_jogo.place(x=382, y=288)

    # Botão para ir ao tutorial
    botao_como_jogar['command'] = tutorial
    botao_como_jogar.place(x=384, y=417)

    # Botão de ligar e desligar a música
    interruptor_musica.place(x=38, y=560)


def tutorial():
    global passo_tutorial, tutorial_img

    limpar_janela()

    # Colocando a imagem correspondente ao passo do tutorial
    tutorial_img = PhotoImage(file=f'imagens/tutorial/tutorial{passo_tutorial}.png')
    label_bg['image'] = tutorial_img
    label_bg.place(x=0, y=0)

    botao_entendi_tutorial.place_forget()

    if passo_tutorial <= 5:
        # Posicionando o botão de entendi de acordo com o passo do tutorial
        botao_entendi_x = botao_entendi_posicoes[passo_tutorial][0]
        botao_entendi_y = botao_entendi_posicoes[passo_tutorial][1]
        botao_entendi_tutorial.place(x=botao_entendi_x, y=botao_entendi_y)
    else:
        # Posicionando os botões de menu e jogar no último passo do tutorial
        botao_menu_tutorial.place(x=172, y=501)
        botao_jogar_tutorial.place(x=364, y=501)

        # Resetando o passo do tutorial
        passo_tutorial = 0

    passo_tutorial += 1


def limpar_janela():
    # Limpando todos os elementos da janela, menos a janela em si
    for widget in janela.winfo_children():
        widget.place_forget()


def resetar_jogo():
    # Apagando todos os órgãos na lista
    for label in label_nomes:
        label_nomes[label]['text'] = ''
        label_correcoes[label]['text'] = ''
        label_nomes[label]['font'] = 'Arial 18 bold'
        label_nomes[label]['fg'] = 'white'

    # Resetando o contador e os órgãos acertados
    global contador_orgaos_confirmados, orgaos_acertados
    contador_orgaos_confirmados = 0
    orgaos_acertados = 0

    # Re-embaralhando a lista de órgãos
    random.shuffle(orgaos_embaralhados)
    orgao_pedido['text'] = orgaos_embaralhados[0]

    # Apagando mensagem final
    canvas_final.destroy()


def escrever_nome_orgao(num_orgao):
    # Apagando todos os nomes que já não foram confirmados para não escreve o mesmo nome em mais de uma posição
    for label in label_nomes:
        if label_nomes[label]['font'] == 'Arial 18 bold':
            label_nomes[label]['text'] = ''

    # Escrevendo o órgão pedido na posição escolhida, caso a posição já não esteja confirmada
    if label_nomes[num_orgao]['font'] == 'Arial 18 bold':
        label_nomes[num_orgao]['text'] = orgao_pedido['text']


def confirmar_posicao():
    # Verificando o estado do botão para voltá-lo ao normal
    if botao_confirmar['text'] == '11':
        resetar_jogo()
        botao_confirmar['text'] = '0'
        botao_confirmar['image'] = img_botoes['botao0']

    # Deixando o órgão confirmado com underline
    orgao_confirmado = False
    for label in label_nomes.values():
        if label['text'] == orgao_pedido['text']:
            # Criando uma fonte com underline ativo
            arial_underline = tkinter.font.Font(label, label.cget('font'))
            arial_underline.configure(underline=True)
            label.configure(font=arial_underline)
            orgao_confirmado = True

    # Retornando a função caso o jogador não tenha escolhido uma posição para o órgão pedido
    if not orgao_confirmado:
        return 1

    # Pedindo o próximo órgão
    global contador_orgaos_confirmados
    contador_orgaos_confirmados += 1

    if contador_orgaos_confirmados < 8:
        orgao_pedido['text'] = orgaos_embaralhados[contador_orgaos_confirmados]
    # Finalizando o jogo e corrigindo respostas depois da confirmação da posição de todos os órgãos
    else:
        finalizar_jogo()


def finalizar_jogo():
    global orgaos_acertados

    # Verificando as respostas
    for label in label_correcoes:
        orgao_correto = orgaos[int(label) - 1]

        if label_nomes[label]['text'] == orgao_correto:
            label_nomes[label]['fg'] = verde

            orgaos_acertados += 1
        else:
            label_nomes[label]['fg'] = vermelho
            label_correcoes[label]['text'] = f'({orgao_correto})'

    # Mudando função do botão de confirmar para jogar novamente
    botao_confirmar['text'] = '11'
    botao_confirmar['image'] = img_botoes['botao11']

    # Mostrando mensagem final
    mensagem_final()


def mensagem_final():
    global msg_final, canvas_final

    # Definindo dimensões do canvas para mensagem final
    canvas_final = Canvas(janela, width=437, height=531, highlightthickness=0)

    # Mostrando canvas para conter a mensagem final
    canvas_final.place(x=100, y=15)

    # Verificando quantos órgãos foram acertados para escolher a mensagem correspondente
    if orgaos_acertados == 0:
        msg_final = PhotoImage(file='imagens/errou_todos.png')
    elif orgaos_acertados == 8:
        msg_final = PhotoImage(file='imagens/acertou_todos.png')
    else:
        msg_final = PhotoImage(file='imagens/acertou_alguns.png')
        
    # Mostrando mensagem selecionada
    canvas_final.create_image(0, 0, anchor=NW, image=msg_final)

    # Mostrando quantos órgãos foram acertados
    if 0 < orgaos_acertados < 8:
        canvas_final.create_text(95, 470, text=orgaos_acertados, font='Impact 56', fill='white')


def criar_botoes():
    global botoes, label_nomes, label_correcoes

    # Dicionário contendo as posições de todos os botões
    posicao_botoes = {'botao1': [88, 171.5], 'botao2': [522, 187], 'botao3': [62.5, 268.5],
                      'botao4': [512, 284.5], 'botao5': [49, 372], 'botao6': [521, 382],
                      'botao7': [72, 479], 'botao8': [482, 460]}

    # Criando os botões de órgãos e labels da lista
    y_nome = 37
    y_correcao = 70
    for i in range(1, 9):
        # Guardando função com seus parâmetros necessários
        escrever_nome_orgao_args = partial(escrever_nome_orgao, str(i))

        # Criando os 8 botões relativos aos órgãos
        botoes[str(i)] = HoverButton(janela, text=str(i), borderwidth=0,
                                     width=70, height=70, activebackground='#ffe603',
                                     command=escrever_nome_orgao_args)
        coordenadas = posicao_botoes[f'botao{i}']
        botoes[str(i)].place(x=coordenadas[0], y=coordenadas[1])

        # Criando os labels para conter os nomes de todos os órgãos
        label_nomes[str(i)] = Label(janela, text='', font='Arial 18 bold', anchor=W,
                                    bg=bg_menu, fg='white')
        label_nomes[str(i)].place(x=676, y=y_nome)

        # Criando os label para exibir as correções se necessário
        label_correcoes[str(i)] = Label(janela, text='', font='Arial 18 bold', anchor=W,
                                        bg=bg_menu, fg=verde)
        label_correcoes[str(i)].place(x=650, y=y_correcao)

        # Aumentando o eixo y para encaixar todos os labels na posição correta
        y_nome += 72
        y_correcao += 72


def embaralhar_orgaos():
    # Embaralha a lista de órgãos para depois serem pedidos um a um
    random.shuffle(orgaos_embaralhados)
    orgao_pedido['text'] = orgaos_embaralhados[0]


def liga_desliga_musica():
    global musica_ligada

    if musica_ligada:
        interruptor_musica['image'] = img_botoes['botao18']
        interruptor_musica['text'] = '18'
        pygame.mixer.music.set_volume(0)
        musica_ligada = False
    else:
        interruptor_musica['image'] = img_botoes['botao14']
        interruptor_musica['text'] = '14'
        pygame.mixer.music.set_volume(0.5)
        musica_ligada = True


def manter_plano(event):
    for botao in botoes:
        if event.widget is botoes[botao]:
            event.widget.config(relief=FLAT)


# Iniciando a janela
janela = Tk()

# Definindo variáveis globais
contador_orgaos_confirmados = 0
orgaos_acertados = 0
passo_tutorial = 1
musica_ligada = True
verde = '#72ff00'
vermelho = '#ff0000'
bg_menu = '#00aea7'
orgaos = ['Boca', 'Esôfago', 'Fígado', 'Estômago', 'Vesícula Biliar', 'Intestino Grosso',
          'Intestino Delgado', 'Ânus']
orgaos_embaralhados = ['Boca', 'Esôfago', 'Fígado', 'Estômago', 'Vesícula Biliar', 'Intestino Grosso',
                       'Intestino Delgado', 'Ânus']
botao_entendi_posicoes = {1: [154, 492], 2: [696, 250], 3: [265, 390],
                          4: [270, 386], 5: [276, 449]}
layout_img = PhotoImage(file='imagens/layout.png')
menu_img = PhotoImage(file='imagens/menu.png')
icone_janela = PhotoImage(file='imagens/minion_icone.png')
tutorial_img = PhotoImage()
img_botoes = {}
botoes = {}
label_nomes = {}
label_correcoes = {}

# Guardando as imagens de todos os botões
for imgbotao in os.listdir(path='imagens/botoes/'):
    img_botoes[imgbotao[:-4]] = PhotoImage(file=f'imagens/botoes/{imgbotao}')

# Criando botões para serem posicionados
label_bg = Label(janela, image=layout_img)
orgao_pedido = Label(janela, text='', font='Universal-Serif 19 bold', fg='white', bg=bg_menu)
botao_confirmar = HoverButton(janela, width=184, height=58, bd=0, text='0')
botao_reset = HoverButton(janela, width=63, height=58, bd=0, text='9')
botao_menu = HoverButton(janela, width=63, height=58, bd=0, text='10')
botao_novo_jogo = HoverButton(janela, width=238, height=88, bd=0, text='12')
botao_como_jogar = HoverButton(janela, width=238, height=88, bd=0, text='13')
interruptor_musica = HoverButton(janela, width=73, height=67, bd=0, text='14', command=liga_desliga_musica)
botao_entendi_tutorial = HoverButton(janela, width=144, height=46, bd=0, text='15', command=tutorial)
botao_menu_tutorial = HoverButton(janela, width=144, height=46, bd=0, text='16', command=menu_principal)
botao_jogar_tutorial = HoverButton(janela, width=144, height=46, bd=0, text='17', command=main)

# Canvas para mostrar mensagem final
canvas_final = Canvas(janela)
msg_final = None

if __name__ == '__main__':
    # Abrindo o menu principal
    menu_principal()

    # Inicia o sistema de som
    pygame.mixer.init()
    pygame.mixer.music.load('trilha_sonora/Minions Bounce.mp3')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    # Definindo o tamanho da janela
    janela.geometry('1000x650')

    # Não deixa que o tamanho da janela seja redefinido
    janela.resizable(width=False, height=False)

    # Muda o nome do título da janela
    janela.title('Monte o Minion')

    # Muda o ícone da janela
    janela.iconphoto(True, icone_janela)

    # Impede que os botões de órgão afundem quando pressionados
    janela.bind('<Button 1>', manter_plano)

    # Mantém a janela aberta
    janela.mainloop()
