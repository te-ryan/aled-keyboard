#!/usr/bin/python3
#
#    Copyright (C) 2021 Ryan Richarlison <ryanricharlison@protonmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import pyxhook
import time
import os
import random
import sys

# Função que será executada ao pressionar uma tecla
def OnKeyPress(event):

    global stop
    global hotkey
    global atalho
    global led
    global anim

    # Verificando se o modo de selecionar atalho está ativado
    if atalho:
        hotkey = event.Key
        print_message(f'\nAtalho definido: {hotkey}')
        atalho = False
        print_message(f"""
            Pronto! Basta apertar "{hotkey}" para parar o programa.
            ------------------------- ALED KEYBOARD 2.0 --------------------
        """)
        return

    # Verificando se o usuário pressionou a tecla de atalho para sair
    if event.Key == hotkey:
        stop = True
        # Gerando um erro de KeyboardInterrupt
        raise KeyboardInterrupt()

    # Verificando se o usuário selecionou a animação 1
    if anim == 1:
        if led:
            os.system(xset_off)
            led = False
        else:
            os.system(xset_on)
            led = True

    # Exibindo o log da tecla pressionada
    if log:
        print_message(f'Tecla pressionada: {event.Key}')

# Função que será chamada para criar um atalho
def a_set():

    global atalho

    hm = pyxhook.HookManager()

    if _onkeydown:
        hm.KeyDown = OnKeyPress

    elif _onkeyup:
        hm.KeyUp = OnKeyPress

    elif _onkeypress:
        hm.KeyDown = OnKeyPress
        hm.KeyUp = OnKeyPress

    hm.HookKeyboard()
    hm.start()

    print_message('Digite a tecla de atalho para parar o programa: ')

    atalho = True

# Função para rodar um arquivo de animação
def run_animation(animation_content):

    # Criando um FOR que percorre linha por linha
    for action in animation_content:
        if stop: return
        # Retirando espaços e verificando se a linha começa com #
        if action.replace(' ', '').startswith('#'): continue
        # Retirando quebra de linhas
        action = action.lower().replace('\n', '').split(' ')
        # Verificando se a ação é um SLEEP
        if action[0] == 'sleep':
            if log: print_message(f'SLEEP {action[1]}')
            # Esperando determinado tempo
            time.sleep(float(action[1]))
        # Verificando se a ação é um LED
        elif action[0] == 'led':
            if log: print_message(f'LED {action[1]}')
            # Caso o segundo parâmetro for "ON", ligar as led
            if action[1] == 'on': os.system(xset_on)
            # Caso for "OFF", desligar
            elif action[1] == 'off': os.system(xset_off)
        # Repetindo a script, caso a função seja !loop
        elif action[0] == '!loop':
            run_animation(animation_content)

# Função para imprimir uma mensagem na tela
def print_message(message):

    print(f'\033[1;35m', end='')

    for l in message:
        print(l, end='')

    print('\033[0;0m')

# Função principal
def main():

    global atalho
    global stop
    global xset_on
    global xset_off
    global log
    global _onkeydown
    global _onkeyup
    global _onkeypress
    global led
    global intervalo
    global anim

    # Abrindo arquivo de configurações
    try:
        CONFIG = open('config', 'r')
    except FileNotFoundError:
        print_message('O arquivo de configurações não foi encontrado.')
        return

    # Lendo linha por linha do arquivo
    for line in CONFIG.readlines():
        # Retirando espaços e verificando se a linha começa com #
        if line.replace(' ', '').startswith('#'): continue
        # Retiando quebra de linhas
        line = line.replace('\n', '')
        # Verificando se o primeiro argumento passado é "ON"
        if line.split('=')[0].lower() == 'on':
            # Defininido o segundo argumento como valor da váriavel XSET_ON
            xset_on = line.split('=')[1].lower()
        # Verificando se o primeiro argumento passado é "OFF"
        elif line.split('=')[0].lower() == 'off':
            # Defininido o segundo argumento como valor da váriavel XSET_OFF
            xset_off = line.split('=')[1].lower()
        # Verificando se o primeiro argumento passado é "LOG"
        elif line.split('=')[0].lower() == 'log':
            if line.split('=')[1].lower() == 'true': log = True
            else: log = False

    try:
        xset_on
        xset_off
    except NameError:
        print_message('Ocorreu um erro de configuração. Certifique-se de que o arquivo "config" esteja correto.')
        return

    print_message("""
                        ALED KEYBOARD 2.0
    ***************************************************************
    Tipos de animações:
        1) Quando um tecla for pressionada.
        2) A um determinado intervalo de tempo.
        3) A um intervalo de tempo aleatorio.
        4) Abrir uma animação personalizada.
    ***************************************************************
    """)

    anim = input(' => ')

    # Verificando se a váriavel ANIM pode ser um inteiro
    try:
        int(anim)
    except ValueError:
        print_message('Opção invalida. Escolha entre uma das opções acima.')
        return

    # Transformando a váriavel ANIM em um inteiro
    anim = int(anim)

    # Validando a opção escolhida
    if anim > 5 or anim < 1:
        print_message('Opção invalida. Escolha entre uma das opções acima.')
        return

    led = True

    # Ligando as led do teclado
    os.system(xset_on)

    print_message('AVISO: Caso as led do seu teclado acederam, isso significa que está funcionando corretamente. Não nos responsabilizamos por qualquer dano causado no seu hardware.')
    print_message('Aperte Enter para continuar ou CTRL + C para sair.')

    input()

    print_message(f'Animação selecionada: {str(anim)}')

    if anim == 1:
        print_message("""
        **********************************
        Deseja executar essa ação quando?
            1) OnKeyDown
            2) OnKeyUp
            3) OnKeyPress
        **********************************
        """)

        qe = input(' => ')

        # Verificando se a váriavel QE pode ser um inteiro
        try:
            int(qe)
        except ValueError:
            print_message('Opção invalida. Escolha entre uma das opções acima.')
            return

        # Transformando a váriavel QE em um inteiro
        qe = int(qe)

        # Validando a opção escolhida
        if qe > 3 or qe < 1:
            print_message('Opção invalida. Escolha entre uma das opções acima.')
            return

        if qe == 1: _onkeydown = True
        elif qe == 2: _onkeyup = True
        elif qe == 3: _onkeypress = True

        a_set()

    elif anim == 2:
        _onkeydown = True

        print_message('Selecione o invervalo ( segundos )')
        i = float(input(' => '))

        a_set()

        while not stop:

            if led:
                os.system(xset_off)
                led = False

            elif not led:
                os.system(xset_on)
                led = True

            time.sleep(i)

    elif anim == 3:

        _onkeydown = True

        print_message('Tempo min (segundos)')
        min = float(input(' => '))

        print_message('Tempo max (segundos)')
        max = float(input(' => '))

        a_set()

        while not stop:

            # Verificando se a LED está ligada
            if led:
                # Desligando a LED
                os.system(xset_off)
                led = False

            # Verificando se a LED está desligada
            elif not led:
                # Ligando a led
                os.system(xset_on)
                led = True

            # Esperando um tempo aleatório entre MIN e MAX
            time.sleep(random.uniform(min, max))

    elif anim == 4:
        animations = os.listdir('animations')
        print_message('    ***************************************************************')
        print_message('    Selecione uma animação: ')

        count = 1

        # Verificando se o número das animações encontradas é igual a 0
        if len(animations) == 0:
            print_message('Nenhuma animação encontrada.')
            return

        # Percorrendo cada animação
        for animation in animations:
            # Exibindo na tela
            print_message(f'        {count}) {animation}')

        print_message('    ***************************************************************')
        a = input(' => ')

        # Verificando se a váriavel A pode ser um inteiro
        try:
            int(a)
        except ValueError:
            print_message('Opção invalida. Escolha entre uma das opções acima.')
            return

        # Transformando a váriavel QE em um inteiro
        a = int(a)

        # Validando a opção escolhida
        if a > len(animations) or a < len(animations):
            print_message('Opção invalida. Escolha entre uma das opções acima.')
            return

        animation_content = open('animations/' + animations[a-1]).readlines()
        run_animation(animation_content)

atalho = False
hotkey = None
log = False
stop = False
led = False
_onkeydown = False
_onkeyup = False
_onkeypress = False

main()
