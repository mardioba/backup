import zipfile, os

# Definindo o caminho do diretório a ser compactado
diretorio_origem = "/home/mardio/script/"

# Definindo o nome do arquivo ZIP
nome_arquivo_zip = "script.zip"

# Definindo o caminho do arquivo ZIP
caminho_arquivo_zip = "/home/mardio/BKP/" + nome_arquivo_zip

# Criando um objeto ZipFile
with zipfile.ZipFile(caminho_arquivo_zip, "w") as zip:
    
    # Percorrendo o diretório de origem
    for raiz, diretorios, arquivos in os.walk(diretorio_origem):
        for arquivo in arquivos:
            
            # Adicionando cada arquivo ao arquivo ZIP
            caminho_completo_arquivo = os.path.join(raiz, arquivo)
            zip.write(caminho_completo_arquivo, arcname=caminho_completo_arquivo.replace(diretorio_origem, ""))

print("Diretório compactado com sucesso!")
