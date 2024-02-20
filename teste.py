from tkinter import *
from ttkwidgets import CheckboxTreeview
import tkinter as tk
import os

root = tk.Tk()
root.title("Arquivos e Tamanho")
root.geometry("600x400")

fr_tree=Frame(root,borderwidth=2, relief="groove", background="white")
fr_tree.place(x=10, y=10, width=590, height=300)
# Criando as barras de rolagem
vsb = Scrollbar(fr_tree, orient="vertical")
hsb = Scrollbar(fr_tree, orient="horizontal")

# Adicionando as barras de rolagem à janela
vsb.pack(side="right", fill="y")
hsb.pack(side="bottom", fill="x")

tree = CheckboxTreeview(fr_tree, columns=("col1"), yscrollcommand=vsb.set, xscrollcommand=hsb.set)
tree.heading("#0", text="Arquivo")
tree.column("#0", minwidth=0, anchor="n",width=200)
tree.heading("col1", text="Tamanho (MB)")
tree.column("col1", minwidth=0, anchor="n", width=80)

tree.place(x=0, y=0, width=570, height=280)

vsb.config(command=tree.yview)
hsb.config(command=tree.xview)

def get_selected_items():
    selected_items = []
    for item in tree.get_children():
        if tree.tag_has("checked", item):
            value = tree.item(item, "text")
            selected_items.append(value)
    print("Itens selecionados:", selected_items)

def toggle_checkbox(item):
    tags = tree.item(item, "tags")
    if tags and "checked" in tags:
        tree.item(item, tags=())
    else:
        tree.item(item, tags=("checked",))

def insert_files_and_sizes(directory):
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        if os.path.isfile(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)  # convertendo para MB
            tree.insert("", "end", text=file, values=(f"{size_mb:.2f}"))

# Diretório onde os arquivos estão
directory = "BKP"
insert_files_and_sizes(directory)

btn = tk.Button(root, text="Imprimir", command=get_selected_items)
btn.place(relx=0.5, rely=0.85, anchor="center")
root.mainloop()
