# Aled Keyboard

**Essa versão é compativél apenas com sistemas GNU/Linux**

Aled Keyboard é um software criado com Python 3. O objetivo dessa script é produzir animações com as leds do teclado.
Dependendo do hardware do seu teclado, pode causar danos, como por exemplo, queimar as leds. Não nós responsabilizamos, caso isso aconteça.

# Requisitos:

  - Python 3 instalado.
  - Biblioteca Libx para Python3.
  - Xorg

# Ambiente de teste
  *Linux endeavour 5.10.80-1-lts x86_64 GNU/Linux*

# Como instalar? ( GNU/Linux )

## Instalação da biblioteca [Xlib](https://pypi.org/project/xlib/)

```sh
chmod +x xlib-install.sh
./xlib-install.sh
```

## Instalação da biblioteca [Xlib](https://pypi.org/project/xlib/) ( manualmente )

### Com PIP3:
```sh
pip3 install python3-xlib
```

### No Ubuntu, Debian, Linux Mint
```sh
sudo apt-get install python-pip
```

### No Arch Linux
```sh
sudo pacman -S python-pip
```

## Iniciando o script
```sh
python3 aled-keyboard.py 
```

# Criando animações personalizadas
Para criar uma animação personalizada, primeiro crie um arquivo com o nome da animação em [**animations/**](animations).

## Função LED
A função LED pode desligar e ligar a LED

Para desligar a led do teclado, use `LED OFF` e para desligar a led do teclado, use `LED ON`.

## Função SLEEP
A função SLEEP é responsavél por esperar um determinado tempo em segundos, antes de executar a próxima função.
Exemplo `SLEEP 2` espera 2s, `SLEEP 0.3` espera 300ms ( 0.3 segundos ).

## Função !LOOP
A função !loop é usada para repetir a animação novamente.

Obs: para selecionar uma animação personalizada, use a opção **4**.

# License

[License MIT](LICENSE)
