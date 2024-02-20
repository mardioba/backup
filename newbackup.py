# -*- coding: utf-8 -*-

import os
import threading
import tkinter as tk
import zipfile
from tkinter import *
from tkinter.ttk import Treeview, Scrollbar
from tkinter.filedialog import askdirectory
from tkinter.messagebox import *
from datetime import datetime
from mega import mega_login, mega_logout,mega_put
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
        ###### Configurando Atalhos
        self.janela.bind("<Control-O>", lambda event: self.carregar_DIR())
        self.janela.bind("<Control-D>", lambda event: self.diretorio_destino_FUNCAO())
        self.janela.bind("<Control-o>", lambda event: self.carregar_DIR())
        self.janela.bind("<Control-d>", lambda event: self.diretorio_destino_FUNCAO())
        menu = Menu(self.janela)
        self.janela.config(menu=menu)
        opcoes_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Opções", menu=opcoes_menu)
        opcoes_menu.add_separator()
        opcoes_menu.add_command(label="Carregar Diretorios Home", command=self.Carregar_Diretorios_Home, activebackground="#87CEFA")
        opcoes_menu.add_separator()
        opcoes_menu.add_command(label="Selecionar Diretório", command=self.carregar_DIR, activebackground="#87CEFA", accelerator="Ctrl+O")
        opcoes_menu.add_command(label="Remover Diretorio da Lista", command=self.remover_diretorio_tree, activebackground="#87CEFA")
        opcoes_menu.add_separator()
        opcoes_menu.add_command(label="Onde Salvar", command=self.diretorio_destino_FUNCAO, activebackground="#87CEFA", accelerator="Ctrl+D")
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
        btn_backup=tk.Button(self.janela,image=self.img_backup_redu, text="Backup", compound=TOP,command=self.aviso_e_backup)
        btn_backup.place(x=self.largura-80,y=0)
        self.tree = Treeview(self.janela, columns=("col1"))
        self.tree.heading("#0", text="Item")
        self.tree.heading("col1", text="Path")
        self.tree.column("#0", width=70, anchor='n')
        self.tree.column("col1", width=300, anchor='n')
        self.tree.tag_configure('zebrado', background='#f0f0ff')
        self.tree.place(relx=0.5, rely=0.6, anchor=tk.CENTER, relheight=0.4, relwidth=0.85)
        scrollbar = Scrollbar(self.janela, orient="vertical", command=self.tree.yview)
        scrollbar.place(relx=0.9248, rely=0.4, relheight=0.4)
        self.lblAviso=Label(self.janela,text="")
        self.lblAviso.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        self.lblDir_destino=Label(self.janela,text="", justify=LEFT)
        self.lblDir_destino.place(x=self.largura-290, y=self.altura-220, anchor=tk.CENTER)
        self.img_pastaNOVA=PhotoImage(file="img/pastas-64.png")
        self.img_pastaNOVA_redu=self.img_pastaNOVA.subsample(2,2)
        self.lblonde=Label(self.janela,text="onde \narquivo ZIP\nserá salvo", image=self.img_pastaNOVA_redu, compound=RIGHT, font=("Arial", 8, "bold"), cursor="hand2")
        self.lblonde.place(x=self.largura-400, y=self.altura-218, anchor=tk.CENTER)
        self.lblonde.bind("<Button-1>", lambda event: self.diretorio_destino_FUNCAO())
    def Carregar_Diretorios_Home(self):
        try:
            # Lista de diretórios com caracteres acentuados
            lista_bkp = ['Vídeos', 'Músicas', 'Documentos', 'script', 'Imagens', 'Área de trabalho']
            home = os.path.expanduser('~')
            indice = len(self.tree.get_children()) + 1
            for caminho in lista_bkp:
                # Monta o caminho completo
                FOLDER = os.path.join(home, caminho)
                print(FOLDER)
                # Verifica se o diretório existe antes de inserir na treeview
                if os.path.exists(FOLDER):
                    self.tree.insert('', 'end', text=str(indice), values=(FOLDER,))
                    indice += 1
                else:
                    print(f'O diretório "{FOLDER}" não existe.')
        except Exception as e:
            raise e
      # end try
    def carregar_DIR(self):
        home = os.path.expanduser('~')
        dir=askdirectory(initialdir=home)
        self.inserir_tree(path=dir)
    def aviso_e_backup(self):
        self.aviso()
        self.backup()

    def diretorio_destino_FUNCAO(self):
        home = os.path.expanduser('~')
        destino=askdirectory(initialdir=home)
        self.lblDir_destino.config(text=destino, font=("Arial", 10, "bold"), foreground="red")
        
    def backup(self):
        tamanho=self.tree.get_children()
        if (len(tamanho) == 0):
            showerror(title="Backup", message="Nenhum diretório foi inserido.")
            self.lblAviso.config(text="")
        else:
            if len(self.lblDir_destino["text"]) == 0:
                diretorio_destino = "BKP"
            else:
                diretorio_destino = self.lblDir_destino["text"]
            threads = []  # Lista para armazenar as threads
            for item in self.tree.get_children():
                diretorio = self.tree.item(item, 'values')
                diretorio = diretorio[0]
                self.janela.after(1000, self.aviso)
                self.janela.update_idletasks()
                thread = threading.Thread(target=self.executar_compactacao, args=(diretorio, diretorio_destino))
                thread.start()
                threads.append(thread)  # Adiciona a thread à lista
            # Espera todas as threads terminarem
            for thread in threads:
                thread.join()
            self.mostrar_mensagem_conclusao()

    def aviso(self):
        self.lblAviso.config(text=f"Compactando diretorios, favor aguardar a msg de conclusão...", foreground="black",background="white",font=("Arial", 11, "bold"))

    def inserir_tree(self, path):
        for item in self.tree.get_children():
            if self.tree.item(item, 'values')[0] == path:
                showinfo(title="Backup", message="O path já existe na Lista.")
                return
        proximo_item = len(self.tree.get_children()) + 1
        self.tree.insert('', 'end', text=f'{proximo_item}', values=(path,))
        self.aplicar_estilo_zebrado()

    def aplicar_estilo_zebrado(self):
        for i, item in enumerate(self.tree.get_children()):
            if i % 2 == 0:
                self.tree.item(item, tags=('zebrado',))
            else:
                self.tree.item(item, tags=())

    def executar_compactacao(self, diretorio_origem, diretorio_destino):
        try:
            agora = datetime.now()
            nome = diretorio_origem.split('/')[-1]
            nome_arquivo_zip = f"{nome}_{agora.strftime('%d%m%Y%H%M%S%f')}.zip"
            nome_arquivo_zip = os.path.join(diretorio_destino, nome_arquivo_zip)
            with zipfile.ZipFile(nome_arquivo_zip, "w") as zip:
                for raiz, diretorios, arquivos in os.walk(diretorio_origem):
                    for arquivo in arquivos:
                        caminho_completo_arquivo = os.path.join(raiz, arquivo)
                        zip.write(caminho_completo_arquivo, arcname=caminho_completo_arquivo.replace(diretorio_origem, ""))
        except Exception as e:
            raise e
    def Tela_MSG(self, message):
      self.top = tk.Toplevel(self.janela, background='#FFD700')
      self.top.title("Mensagem Personalizada")
      largura=450
      largura_tela=self.top.winfo_screenwidth()
      altura=100
      altura_tela=self.top.winfo_screenheight()
      x=largura_tela/2 - largura/2
      def fechar_limpar():
        self.top.destroy()
        self.tree.delete(*self.tree.get_children())
        self.lblAviso.config(background="#d9d9d9", text="")
        
      y=altura_tela/2 - altura/2
      self.top.overrideredirect(True)
      self.top.geometry("%dx%d+%d+%d" % (largura, altura, x, y))
      self.label = tk.Label(self.top, text=message, background='#FFD700',font=("Arial", 12, "bold"))
      self.label.pack(padx=20, pady=20)
      self.ok_button = tk.Button(self.top, text="OK", command=fechar_limpar)
      self.ok_button.pack(pady=1)
      self.btn_nuvem = tk.Button(self.top, text="Enviar p\ mega.nz", command=self.escolher_que_envia)
      self.btn_nuvem.place(x=280, y=65, anchor=tk.NW)
      # self.janela.withdraw()
    def remover_diretorio_tree(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
        else:
            showinfo("Nenhuma linha selecionada", "Por favor, selecione uma linha para excluir.")

    def mostrar_mensagem_conclusao(self):
      self.Tela_MSG(message="Todos os diretórios foram compactados com sucesso.")
      # self.lblAviso.config(text="Todos os diretórios foram compactados com sucesso.", foreground="green",background="white")
      # showinfo("Backup Concluído", "Todos os diretórios foram compactados com sucesso.")
    def escolher_que_envia(self):
        self.top.destroy()
        self.TLmega=Toplevel()
        self.TLmega.title("Mensagem Personalizada")
        largura=650
        largura_tela=self.TLmega.winfo_screenwidth()
        altura=300
        altura_tela=self.TLmega.winfo_screenheight()
        x=largura_tela/2 - largura/2
        y = altura_tela/2 - altura/2
        self.TLmega.geometry("%dx%d+%d+%d" % (largura, altura, x, y))
        lista, caminho_absoluto=self.listar_Backups()
        print("Caminho absoluto:",caminho_absoluto)
#################################### CheckList Começa Aqui

        def add_item():
            selected_item = checklist.curselection()
            for item_index in selected_item:
                item = checklist.get(item_index)
                if item not in selected_items:
                    selected_items.append(item)
            update_selected_items()

        def remove_item():
            selected_item = selected_checklist.curselection()
            for item_index in selected_item:
                item = selected_checklist.get(item_index)
                selected_items.remove(item)
            update_selected_items()

        def print_selected_items():
            print("Itens selecionados:")
            for item in selected_items:
                print(item)

        def update_selected_items():
            selected_checklist.delete(0, tk.END)
            for item in selected_items:
                selected_checklist.insert(tk.END, item)

        # Inicializa a lista de itens selecionados
        selected_items = []

        # Cria o frame para os itens da checklist
        checklist_frame = tk.Frame(self.TLmega, width=250)
        checklist_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Cria a lista de checklist
        checklist = tk.Listbox(checklist_frame, selectmode=tk.MULTIPLE)
        checklist.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Adiciona os itens à lista de checklist
        for item in lista:
            checklist.insert(tk.END, item)

        # Cria o frame para os botões
        button_frame = tk.Frame(self.TLmega, width=150)
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        add_button = tk.Button(button_frame, text="Adicionar", command=add_item)
        add_button.pack(fill=tk.X)

        remove_button = tk.Button(button_frame, text="Remover", command=remove_item)
        remove_button.pack(fill=tk.X)

        print_button = tk.Button(button_frame, text="Imprimir\nselecionados", command=print_selected_items)
        print_button.pack(fill=tk.X)

        # Cria o frame para os itens selecionados
        selected_frame = tk.Frame(self.TLmega, width=250, background="red")
        #cor = #d9d9d9
        selected_frame.pack(side=tk.LEFT)

        # Cria a lista de itens selecionados
        selected_checklist = tk.Listbox(selected_frame)
        selected_checklist.pack()
    def listar_Backups(self):
      dir = self.lblDir_destino["text"]
      backups=[]
      if len(dir) == 0:
        dir = "BKP"
      else:
        pass
      # end if
      for arquivos_zip in os.listdir(dir):
        zip_absoluto=os.path.join(dir, arquivos_zip)
        script_path = os.path.abspath(__file__)
        cortar = script_path.split("/")[-1]
        script_path=script_path.replace(cortar, "")
        # print("Caminho absoluto do script:", os.path.join(script_path, arquivos_zip))
        backups.append(arquivos_zip)
      return backups, script_path
if __name__ == "__main__":
    # script_path = os.path.abspath(__file__)
    # cortar = script_path.split("/")[-1]
    # script_path=script_path.replace(cortar, "")
    # print("Caminho absoluto do script:", script_path)
    APP()
