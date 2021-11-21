#!/usr/bin/bash

# Verificando se a plataforma é um Linux
if [ $(uname) = "Linux" ]

then

  # Verificando se o PIP está instalado
  if [ -f "/usr/bin/pip3" ]

  then

      # Instalando a biblioteca Xlib para Python3 com PIP
      pip3 install python-xlib

  else

      echo "PIP3 não encontrado."
      echo "Aperte CTRL + C para cancelar"
      echo "ou pressione Enter para tentar fazer a instalação automática."
      read

      # Instalando PIP para Python3

      # Verificando se o sistema operacional possui o gerenciador de pacotes pacman
      if [ -f "/usr/bin/pacman" ]
      then
        # Instalando PIP com Pacman
        sudo pacman -S python-pip
        echo "PIP3 instalado. Tente rodar o script novamente."
        exit
      fi

      # Verificando se o sistema operacional possui o gerenciador de pacotes apt-get
      if [ -f "/usr/bin/apt-get" ]
      then
        # Instalando PIP com APT
        sudo apt-get install python-pip
        echo "PIP3 instalado. Tente rodar o script novamente."
        exit
      fi

      # Exibindo uma mensagem de erro
      echo "Não foi possivel instalar PIP3."
      echo "Tente fazer a instalação manualmente."
      exit

  fi

else

  # Exibindo uma mensagem de erro
  echo "Não foi possivel instalar XLIB."
  echo "Tente fazer a instalação manualmente."
  exit

fi
