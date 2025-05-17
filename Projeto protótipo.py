import os

# Arquivos
USUARIOS = "usuarios.txt"
MUSICAS = "musicas.txt"
HISTORICO = "historico.txt"
PLAYLISTS = "playlists.txt"

# Menus
MENU_PRINCIPAL = {
    1: "Cadastrar usuário",
    2: "Login",
    0: "Sair"
}

MENU_DO_USUARIO = {
    1: "Buscar músicas",
    2: "Curtir/descurtir música",
    3: "Visualizar histórico",
    4: "Gerenciar playlists",
    0: "Sair"
}

MENU_PLAYLISTS = {
    1: "Criar playlist",
    2: "Adicionar música",
    3: "Remover música",
    4: "Excluir playlist",
    5: "Listar playlists",
    0: "Voltar"
}
ESCOLHA_DE_MUSICAS = [
    {"id": "1", "nome": "dunkelheit", "artista": "Burzum", "genero": "Rock"},
    {"id": "2", "nome": "beautiful demains", "artista": "Black Veil Brides", "genero": "Rock"},
    {"id": "3", "nome": "love story", "artista": "Taylor Swift", "genero": "Pop"},
    {"id": "4", "nome": "video games", "artista": "Lana Del Rey", "genero": "Pop"},
    {"id": "5", "nome": "dark harvest", "artista": "Ghost Mountain", "genero": "Trap"},
    {"id": "6", "nome": "wendigo", "artista": "Sematary", "genero": "Trap"},

]
def limpar():
    os.system("cls" if os.name == "nt" else "clear")

def exibir_menu(menu):
    for op, desc in menu.items():
        print(f"{op} - {desc}")

# Usuário
def cadastrar_usuario():
    nome = input("Cadastre seu nome de usuário: ")
    senha = input("Cadastre sua senha: ")
    with open(USUARIOS, "a", encoding="utf-8") as f:
        f.write(f"{nome};{senha}\n")
    print("Usuário cadastrado!")

def login():
    nome = input("Usuário: ")
    senha = input("Senha: ")
    with open(USUARIOS, "r", encoding="utf-8") as f:
        for linha in f:
            user, passw = linha.strip().split(";")
            if nome == user and senha == passw:
                print("Login bem-sucedido!")
                menu_usuario(nome)
            elif nome == user and senha != passw:
                print("Usuário não encontrado.")
            elif nome != user and senha == passw:
                print("Usuário não encontrado.")
                return
    print("Usuário ou senha incorretos.")

# Músicas
def buscar_musicas():
    termo = input("Nome da música: ").lower()
    musicas = ESCOLHA_DE_MUSICAS
    achadas = [m for m in musicas if termo in m["nome"].lower()]
    if achadas:
        for m in achadas:
            print(f"{m['id']}: {m['nome']} - {m['artista']} ({m['genero']})")
    else:
        print("Música não encontrada.")

# Curtir e descurtir
def curtir_ou_descurtir(usuario):
    musicas = ESCOLHA_DE_MUSICAS
    for m in musicas:
        print(f"{m['id']}: {m['nome']} - {m['artista']}")
    id_musica = input("Digite o ID da música que quer curtir: ")
    acao = input("curtir ou descurtir? ").lower()
    if acao in ["curtir", "descurtir"]:
        with open(HISTORICO, "a", encoding="utf-8") as f:
            f.write(f"{usuario};{id_musica};{acao}\n")
        print(f"Música {acao} registrada!")
    else:
        print("Error")
# Histórico
def visualizar_historico(usuario):
    musicas = ESCOLHA_DE_MUSICAS
    curtidas = []
    descurtidas = []
    if os.path.exists(HISTORICO):
        with open(HISTORICO, "r", encoding="utf-8") as f:
            for linha in f:
                user, id_musica, acao = linha.strip().split(";")
                if user == usuario:
                    musica = next((m for m in musicas if m["id"] == id_musica), None)
                    if musica:
                        if acao == "curtir":
                            curtidas.append(musica)
                        elif acao == "descurtir":
                            descurtidas.append(musica)
    print("\n== Curtidas ==")
    for m in curtidas:
        print(f"- {m['nome']} - {m['artista']}")
    print("\n== Descurtidas ==")
    for m in descurtidas:
        print(f"- {m['nome']} - {m['artista']}")

# Playlists
def carregar_playlists():
    playlists = {}
    if os.path.exists(PLAYLISTS):
        with open(PLAYLISTS, "r", encoding="utf-8") as f:
            for linha in f:
                user, nome, ids = linha.strip().split(";")
                playlists[(user, nome)] = ids.split(",") if ids else []
    return playlists

def salvar_playlists(playlists):
    with open(PLAYLISTS, "w", encoding="utf-8") as f:
        for (user, nome), ids in playlists.items():
            f.write(f"{user};{nome};{','.join(ids)}\n")

def criar_playlist(user):
    nome = input("Nome da nova playlist: ")
    playlists = carregar_playlists()
    if (user, nome) in playlists:
        print("Já existe.")
    else:
        playlists[(user, nome)] = []
        salvar_playlists(playlists)
        print("Playlist criada.")

def adicionar_musica_playlist(user):
    nome = input("Nome da playlist: ")
    playlists = carregar_playlists()
    chave = (user, nome)
    if chave not in playlists:
        print("Playlist não existe.")
        return
    musicas = ESCOLHA_DE_MUSICAS
    for m in musicas:
        print(f"{m['id']}: {m['nome']}")
    id_musica = input("ID da música: ")
    playlists[chave].append(id_musica)
    salvar_playlists(playlists)
    print("Música adicionada.")

def remover_musica_playlist(user):
    nome = input("Nome da playlist: ")
    playlists = carregar_playlists()
    chave = (user, nome)
    if chave not in playlists:
        print("Playlist não existe.")
        return
    print("IDs atuais:", ", ".join(playlists[chave]))
    id_musica = input("ID da música para remover: ")
    if id_musica in playlists[chave]:
        playlists[chave].remove(id_musica)
        salvar_playlists(playlists)
        print("Removida.")
    else:
        print("Música não encontrada.")

def excluir_playlist(user):
    nome = input("Nome da playlist: ")
    playlists = carregar_playlists()
    chave = (user, nome)
    if chave in playlists:
        del playlists[chave]
        salvar_playlists(playlists)
        print("Excluída.")
    else:
        print("Não existe.")

def listar_playlists(user):
    playlists = carregar_playlists()
    musicas = ESCOLHA_DE_MUSICAS
    for (u, nome), ids in playlists.items():
        if u == user:
            print(f"\nPlaylist: {nome}")
            for idm in ids:
                m = next((m for m in musicas if m["id"] == idm), None)
                if m:
                    print(f" - {m['nome']} - {m['artista']}")

# Menus
def menu_playlists(usuario):
    while True:
        print("\n== PLAYLISTS ==")
        exibir_menu(MENU_PLAYLISTS)
        op = int(input("Opção: "))
        if op == 1:
            criar_playlist(usuario)
        elif op == 2:
            adicionar_musica_playlist(usuario)
        elif op == 3:
            remover_musica_playlist(usuario)
        elif op == 4:
            excluir_playlist(usuario)
        elif op == 5:
            listar_playlists(usuario)
        elif op == 0:
            break
        else:
            print("Opção inválida.")

def menu_usuario(usuario):
    while True:
        print(f"\n== SPOTIFEI - Usuário: {usuario} ==")
        exibir_menu(MENU_DO_USUARIO)
        op = int(input("Opção: "))
        if op == 1:
            buscar_musicas()
        elif op == 2:
            curtir_ou_descurtir(usuario)
        elif op == 3:
            visualizar_historico(usuario)
        elif op == 4:
            menu_playlists(usuario)
        elif op == 0:
            break
        else:
            print("Opção inválida.")

def main():
    while True:
        print("\n== SPOTIFEI ==")
        exibir_menu(MENU_PRINCIPAL)
        op = int(input("Opção: "))
        if op == 1:
            cadastrar_usuario()
        elif op == 2:
            login()
        elif op == 0:
            print("Até logo!")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()
