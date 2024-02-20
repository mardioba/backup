import subprocess, datetime, re, os
def ver_mega_instalado():
    try:
        output = subprocess.check_output(["mega-version"], stderr=subprocess.STDOUT, text=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando 'mega-version': {e}")
        return False

def mega_login(username, password):
    try:
        subprocess.run(f"mega-login {username} {password}", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def mega_mkdir(folder_name):
    try:
        subprocess.run(f"mega-mkdir {folder_name}", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def mega_logout():
    try:
        subprocess.run("mega-logout", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False
def is_dir_nuvem(diretorio_nuvem):
    result = subprocess.run(f"mega-attr {diretorio_nuvem}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = result.stdout
    v = re.findall(r'API:err', output.decode("utf-8"))
    if len(v) == 0:
        return True
    else:
        return False
def mega_ls(diretorio):
    try:
        ex=subprocess.run(f"mega-ls {diretorio}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print('Retorno:',ex.stdout.decode("utf-8"))
        ver=re.findall(r'Couldn\'t find',ex.stdout.decode("utf-8"))
        # print("Retorno Ver ls: ",len(ver))
        if (len(ver)==0):
          return True
        else:
          return False
        # end if
    except subprocess.CalledProcessError:
        return False
def ver_login():
    try:
        ex=subprocess.run("mega-login", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print('Retorno:',ex.stdout.decode("utf-8"))
        ver=re.findall(r'Already logged in',ex.stdout.decode("utf-8"))
        # print("Retorno Ver login: ",len(ver))
        if len(ver)>0:
          return True
    except subprocess.CalledProcessError:
        return False
def tamanho_arquivo_nuvem(arq_local):
    arq_nuvem=arq_local.split('/')[-1]
    print(arq_nuvem)
    try:
        # Executa o comando mega-du e redireciona a saída para o comando awk
        result = subprocess.run(["mega-du", arq_nuvem, "-h"], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        
        # Executa o comando awk para obter a segunda coluna
        result = subprocess.run(["awk", "{print $2}"], input=output, stdout=subprocess.PIPE, text=True)
        size_str = result.stdout.strip()
        
        # Converte para float, se possível
        # size = float(size_str)
        size_formatado=size_str.replace('SIZE', '').replace('storage', '').replace('\n', '').strip()
        size = round(float(size_formatado), 2)
        return "{:.2f}".format(size)  # Formata a saída com duas casas decimais
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando 'mega-du': {e}")
        return None
def mega_put(arq_local, arquivo_nuvem):
    data = datetime.datetime.now().strftime("%d_%m_%Y")
    diretorio_nuvem=os.path.join("BKP",data)
    nuvem=os.path.join(diretorio_nuvem,arquivo_nuvem)
    if is_dir_nuvem(diretorio_nuvem):
        pass
    else:
        mega_mkdir(diretorio_nuvem)
    try:
        result=subprocess.run(f"mega-put {arq_local} {nuvem}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout
        output = output.decode("utf-8")
        output = output.replace('Upload finished','Carregamento concluído')
        return output, diretorio_nuvem
    except subprocess.CalledProcessError:
        return False
# print(ver_login())
# if ver_login():
#   print("Logado")
# else:
#   print("Nao logado")
#   logar=mega_login("graca-moreira@hotmail.com", "G@L120486##")
# arq_folder="06_12_2023"
# r=tamanho_arquivo(arq_folder)
# print(f'{r} MB')
# end if
# r=ver_mega_instalado()
# if (r):
#   print("Instalado")
#   # comment: 
# else:
#   print("Nao instalado")
# mega_login("graca-moreira@hotmail.com", "G@L120486##")
if __name__ == "__main__":
    total=len(os.listdir("/home/mardio/BKP"))
    print('Enviando',total)
    contador = 1
    for arquivo in os.listdir("/home/mardio/BKP"):
        print(f'Enviando - {contador} de {total}')
        arquivo_absoluto = os.path.join("/home/mardio/BKP",arquivo)
        print(arquivo_absoluto,arquivo)
        r=mega_put(arq_local=arquivo_absoluto, arquivo_nuvem=arquivo)
        print(r)
        contador += 1
    print('Finalizado')
