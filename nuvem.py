import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter as tk
from os import path, listdir
from datetime import datetime
import re
from mega import mega_login, mega_logout


path_bkp = "/home/mardio/BKP"
lista=listdir(path_bkp)
for nome in lista:
  data = re.findall(r'_[0-9]*', nome)
  data = data[0].replace('_', '')
  print(data)
  dia= data[0:2]
  mes= data[2:4]
  ano = data[4:8]
  data_string=f"{dia}/{mes}/{ano}"
  data_completa=datetime.strptime(data_string, "%d/%m/%Y")
  data_c_formatada=data_completa.strftime("%d/%m/%Y")
  arquivo=path.join(path_bkp, nome)
  data_criacao = path.getctime(arquivo)
  data_formatada = datetime.fromtimestamp(data_criacao).strftime("%d/%m/%Y")
  print(data_c_formatada,data_formatada)
  if data_c_formatada == data_formatada:
    print("igual")
  else:
    print("diferente")
  # data = re.findall(r'_[0-9]*', nome[0])
  nome=re.findall(r'^.*_',nome)
  # nome=nome[0].replace('_', '')
  
  # print(nome, data)

janela = tk.Tk()
janela.title("Exemplo de Combobox")
janela.geometry("300x200")

# Defina as opções para o Combobox
opcoes = lista
opcoes.insert(0, "")
# Variável para armazenar a opção selecionada
opcao_selecionada = tk.StringVar()

# Crie o Combobox e associe-o à variável de opção selecionada
largura_maxima = max(len(opcao) for opcao in opcoes)
combobox = ttk.Combobox(janela, textvariable=opcao_selecionada, values=opcoes, width=largura_maxima + 2, justify="center")
combobox.pack(pady=10, padx=10)  # Adicione um pouco de espaço ao redor do Combobox
combobox.bind("<<ComboboxSelected>>", lambda event: print("Opção selecionada:", opcao_selecionada.get()))
# Defina uma opção padrão selecionada
opcao_selecionada.set(opcoes[0])

# Função para imprimir a opção selecionada
def imprimir_opcao():
    print("Opção selecionada:", opcao_selecionada.get())

# Botão para imprimir a opção selecionada
botao = ttk.Button(janela, text="Imprimir Opção", command=imprimir_opcao)
botao.pack(pady=10)

# Execute o loop principal da janela
janela.mainloop()
