import os
import tkinter as tk
import zipfile
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *
from datetime import datetime

class APP():

  def __init__(self):
    self.Tela()
    self.Imagens()
    self.Componentes()
    self.janela.mainloop()
  def Tela(self):
    self.janela = Tk()
    self.janela.title("Backup")
    self.largura = 500
    self.altura = 300
    largura_tela = self.janela.winfo_screenwidth()
    altura_tela = self.janela.winfo_screenheight()
    x = (largura_tela - self.largura) / 2
    y = (altura_tela - self.altura) / 2
    self.janela.geometry("%dx%d+%d+%d" % (self.largura, self.altura, x, y))
    menu = Menu(self.janela)
    self.janela.config(menu=menu)
    opcoes_menu = Menu(menu, tearoff=0)
    menu.add_cascade(label="Opções", menu=opcoes_menu)
    opcoes_menu.add_separator()
    opcoes_menu.add_command(label="Carregar Diretorios Home", command=self.backup)
    opcoes_menu.add_separator()
    opcoes_menu.add_command(label="Selecionar Diretório", command=self.carregar_DIR)
    # opcoes_menu.add_command(label="Fazer Backup", command=self.backup)
    opcoes_menu.add_command(label="Remover Diretorio da Lista", command=self.remover_diretorio_tree)
    opcoes_menu.add_separator()
    opcoes_menu.add_command(label="Onde Salvar", command=self.diretorio_destino_FUNCAO)
    opcoes_menu.add_separator()
    opcoes_menu.add_command(label="Sair", command=self.janela.destroy)
  def Imagens(self):
    self.img_backup=PhotoImage(file="img/backup-64.png")
    self.img_backup_redu=self.img_backup.subsample(4,4)
    self.img_salvar=PhotoImage(file="img/salvar-64.png")
    self.img_salvar_redu=self.img_salvar.subsample(4,4)
    self.img_pasta=PhotoImage(file="img/pastas-64.png")
    self.img_pasta_redu=self.img_pasta.subsample(4,4)
  def Componentes(self):
    # btn_Salvar=tk.Button(self.janela,image=self.img_salvar_redu, text="Salvar", compound=TOP,command=self.backup)
    # btn_Salvar.grid(row=0,column=0)
    btn_backup=tk.Button(self.janela,image=self.img_backup_redu, text="Backup", compound=TOP,command=self.backup)
    btn_backup.place(x=self.largura-80,y=0)
    # btn_pastas=tk.Button(self.janela,image=self.img_pasta_redu, text="Pastas", compound=TOP,command=self.carregar_DIR)
    # btn_pastas.grid(row=0,column=2)
    
    ############ TREEVIEW ############
    self.tree = Treeview(self.janela, columns=("col1"))
    self.tree.heading("#0", text="Item")
    self.tree.heading("col1", text="Path")
    self.tree.column("#0", width=70, anchor='n')
    self.tree.column("col1", width=300, anchor='n')
    # Cor de fundo para linhas zebradas
    self.tree.tag_configure('zebrado', background='#f0f0ff')
    # Adicione aqui os dados da treeview
    # for i in range(2):
    #   self.tree.insert('', 'end', text=f'{i}', values=(f'Path {i}'))
    self.tree.place(relx=0.5, rely=0.6, anchor=tk.CENTER, relheight=0.4, relwidth=0.85)
    self.aplicar_estilo_zebrado()  # Aplicar estilo zebrado
    scrollbar = Scrollbar(self.janela, orient="vertical", command=self.tree.yview)
    scrollbar.place(relx=0.9248, rely=0.4, relheight=0.4)
    self.lblAviso=Label(self.janela,text="aqui")
    self.lblAviso.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
    self.img_pastaNOVA=PhotoImage(file="img/pastas-64.png")
    self.img_pastaNOVA_redu=self.img_pastaNOVA.subsample(2,2)
    self.lblonde=Label(self.janela,text="onde \narquivo ZIP\nserá salvo", image=self.img_pastaNOVA_redu, compound=RIGHT, font=("Arial", 8, "bold"), cursor="hand2")
    self.lblonde.place(x=self.largura-400, y=self.altura-218, anchor=tk.CENTER)
    self.lblonde.bind("<Button-1>", lambda event: self.diretorio_destino_FUNCAO())
    
    self.lblDir_destino=Label(self.janela,text="", justify=LEFT)
    self.lblDir_destino.place(x=self.largura-290, y=self.altura-220, anchor=tk.CENTER)
    #Menu

  def carregar_DIR(self):
    home = os.path.expanduser('~')
    dir=askdirectory(initialdir=home)
    self.inserir_tree(path=dir)
  def diretorio_destino_FUNCAO(self):
    home = os.path.expanduser('~')
    destino=askdirectory(initialdir=home)
    self.lblDir_destino.config(text=destino, font=("Arial", 10, "bold"), foreground="red")
    
  def backup(self):
    tamanho=self.tree.get_children()
    if (len(tamanho) == 0):
      showerror(title="Backup", message="Nenhum diretório foi inserido.")
    else:
      # comment: 
    # end if
      for item in self.tree.get_children():
        diretorio = self.tree.item(item, 'values')
        diretorio = diretorio[0]  # Índice 1 corresponde à coluna "Diretório"
        self.compactar_arquivos(diretorio_destino=diretorio, diretorio_origem=diretorio)
  def inserir_tree(self, path):
      # Verificar se o path já existe na treeview
      for item in self.tree.get_children():
          if self.tree.item(item, 'values')[0] == path:
              # Se o path já existir, exibir uma mensagem e retornar sem inserir nova linha
              showinfo(title="Backup", message="O path já existe na Lista.")
              return

      # Calcular o próximo número na sequência
      proximo_item = len(self.tree.get_children()) + 1
      # Adicionar nova linha com o próximo número na sequência
      self.tree.insert('', 'end', text=f'{proximo_item}', values=(path,))
      self.aplicar_estilo_zebrado()  # Atualizar estilo zebrado

  def aplicar_estilo_zebrado(self):
      for i, item in enumerate(self.tree.get_children()):
          if i % 2 == 0:
              self.tree.item(item, tags=('zebrado',))
          else:
              self.tree.item(item, tags=())
  def compactar_arquivos(self, diretorio_origem, diretorio_destino):
      # Obter a data e hora atual
      agora = datetime.now()
      diretorio_origem = diretorio_origem
      diretorio_destino = diretorio_destino
      nome = diretorio_origem.split('/')[-1]
      
      # Definindo o nome do arquivo ZIP
      nome_arquivo_zip = f"{nome}_{agora.strftime('%d%m%Y%H%M%S%f')}.zip"
      print(nome_arquivo_zip)

      # # Definindo o caminho do arquivo ZIP
      # caminho_arquivo_zip = "/home/mardio/BKP/" + nome_arquivo_zip

      # # Criando um objeto ZipFile
      # with zipfile.ZipFile(caminho_arquivo_zip, "w") as zip:
          
      #     # Percorrendo o diretório de origem
      #     for raiz, diretorios, arquivos in os.walk(diretorio_origem):
      #         for arquivo in arquivos:
                  
      #             # Adicionando cada arquivo ao arquivo ZIP
      #             caminho_completo_arquivo = os.path.join(raiz, arquivo)
      #             zip.write(caminho_completo_arquivo, arcname=caminho_completo_arquivo.replace(diretorio_origem, ""))

      # print("Diretório compactado com sucesso!")    
  def remover_diretorio_tree(self):
    selected_item = self.tree.selection()
    if selected_item:
        self.tree.delete(selected_item)
    else:
        showinfo("Nenhuma linha selecionada", "Por favor, selecione uma linha para excluir.")
      
      
if __name__ == "__main__":
  APP()