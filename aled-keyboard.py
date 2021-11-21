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

atalho = False
tecla_de_atalho = None
log = False
stop = False
led = False
_onkeydown = False
_onkeyup = False
_onkeypress = False

def OnKeyPress(event):
    global stop
    global tecla_de_atalho
    global atalho
    global led
    global anim
    if atalho:
        tecla_de_atalho = event.Key
        print(f'\nAtalho definido: {tecla_de_atalho}')
        atalho = False
        print(f'\n\n\nPronto! Basta apertar "{tecla_de_atalho}" para parar o programa.')
        return
    if event.Key == tecla_de_atalho:
        stop = True
        raise KeyboardInterrupt()
    if anim == 1:
        if led:
            os.system(xset_off)
            led = False
        else:
            os.system(xset_on)
            led = True
    if log:
        print(f'Tecla pressionada: {event.Key}')

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
    print('Digite a tecla de atalho para parar o programa: ')
    atalho = True

def run_animation(animation_content):
    for action in animation_content:
        if stop: return
        if action.replace(' ', '').startswith('#'): continue
        action = action.lower().replace('\n', '').split(' ')
        if action[0] == 'sleep':
            if log: print(f'SLEEP {action[1]}')
            time.sleep(float(action[1]))
        elif action[0] == 'led':
            if log: print(f'LED {action[1]}')
            if action[1] == 'on': os.system(xset_on)
            elif action[1] == 'off': os.system(xset_off)
        elif action[0] == '!loop':
            run_animation(animation_content)

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
    try:
        CONFIG = open('config', 'r')
    except FileNotFoundError:
        print('O arquivo de configurações não foi encontrado.')
        return
    for line in CONFIG.readlines():
        if line.replace(' ', '').startswith('#'): continue
        line = line.replace('\n', '')
        if line.split('=')[0].lower() == 'on':
            xset_on = line.split('=')[1].lower()
        elif line.split('=')[0].lower() == 'off':
            xset_off = line.split('=')[1].lower()
        elif line.split('=')[0].lower() == 'log':
            if line.split('=')[1].lower() == 'true': log = True
            else: log = False
    try:
        xset_on
        xset_off
    except NameError:
        print('Ocorreu um erro de configuração. Certifique-se de que o arquivo "config" esteja correto.')
        return
    print("""
    ***************************************************************
    Tipos de animações:
        1) Quando um tecla for pressionada.
        2) A um determinado intervalo de tempo.
        3) A um intervalo de tempo aleatorio.
        4) Abrir uma animação personalizada.
    ***************************************************************
    """)
    anim = input(' => ')
    try:
        int(anim)
    except ValueError:
        print('Opção invalida. Escolha entre uma das opções acima.')
        return
    anim = int(anim)
    if anim > 5 or anim < 1:
        print('Opção invalida. Escolha entre uma das opções acima.')
        return
    led = True
    os.system(xset_on)
    print('AVISO: Caso as led do seu teclado acederam, isso significa que está funcionando corretamente. Não nos responsabilizamos por qualquer dano causado no seu hardware.')
    print('Aperte Enter para continuar ou CTRL + C para sair.')
    input()
    print(f'Animação selecionada: {str(anim)}')
    if anim == 1:
        print("""
        **********************************
        Deseja executar essa ação quando?
            1) OnKeyDown
            2) OnKeyUp
            3) OnKeyPress
        **********************************
        """)
        qe = input(' => ')
        try:
            int(qe)
        except ValueError:
            print('Opção invalida. Escolha entre uma das opções acima.')
            return
        qe = int(qe)
        if qe > 3 or qe < 1:
            print('Opção invalida. Escolha entre uma das opções acima.')
            return
        if qe == 1: _onkeydown = True
        elif qe == 2: _onkeyup = True
        elif qe == 3: _onkeypress = True
        a_set()
    elif anim == 2:
        _onkeydown = True
        print('Selecione o invervalo ( segundos )')
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
        print('Tempo min (segundos)')
        min = float(input(' => '))
        print('Tempo max (segundos)')
        max = float(input(' => '))
        a_set()
        while not stop:
            if led:
                os.system(xset_off)
                led = False
            elif not led:
                os.system(xset_on)
                led = True
            time.sleep(random.uniform(min, max))
    elif anim == 4:
        animations = os.listdir('animations')
        print('    ***************************************************************')
        print('    Selecione uma animação: ')
        count = 1
        if len(animations) == 0:
            print('Nenhuma animação encontrada.')
            return
        for animation in animations:
            print(f'        {count}) {animation}')
        print('    ***************************************************************')
        a = input(' => ')
        try:
            int(a)
        except ValueError:
            print('Opção invalida. Escolha entre uma das opções acima.')
            return
        a = int(a)
        if a > len(animations) or a < len(animations):
            print('Opção invalida. Escolha entre uma das opções acima.')
            return
        animation_content = open('animations/' + animations[a-1]).readlines()
        run_animation(animation_content)

main()
