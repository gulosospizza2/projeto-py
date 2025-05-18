import os

USUARIOS = "usuarios.txt"
HISTORICO = "historico.txt"
PLAYLISTS = "playlists.txt"

MUSICAS = [
    {"id": "1", "nome": "dunkelheit", "artista": "Burzum", "genero": "Rock"},
    {"id": "2", "nome": "beautiful remains", "artista": "Black Veil Brides", "genero": "Rock"},
    {"id": "3", "nome": "love story", "artista": "Taylor Swift", "genero": "Pop"},
    {"id": "4", "nome": "video games", "artista": "Lana Del Rey", "genero": "Pop"},
    {"id": "5", "nome": "dark harvest", "artista": "Ghost Mountain", "genero": "Trap"},
    {"id": "6", "nome": "wendigo", "artista": "Sematary", "genero": "Trap"},
]

def cadastrar():
    user = input("Usuário: ")
    senha = input("Senha: ")
    with open(USUARIOS, "a", encoding="utf-8") as f:
        f.write(user + ";" + senha + "\n")

def login():
    user = input("Usuário: ")
    senha = input("Senha: ")
    if os.path.exists(USUARIOS):
        with open(USUARIOS, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 2:
                    u, s = partes
                    if u == user and s == senha:
                        print("Bem-vindo!")
                        menu_usuario(user)
                        return
    print("Login incorreto")

def buscar():
    termo = input("Buscar por nome: ").lower()
    for m in MUSICAS:
        if termo in m["nome"]:
            print(f"{m['id']}: {m['nome']} - {m['artista']} - {m['genero']}")

def curtir(usuario):
    for m in MUSICAS:
        print(f"{m['id']}: {m['nome']} - {m['artista']} - {m['genero']}")
    idm = input("ID da música: ")
    print("[1] Curtir  [2] Descurtir")
    op = input("Escolha: ")
    if op == "1":
        acao = "curtida"
    elif op == "2":
        acao = "descurtida"
    else:
        print("Opção inválida.")
        return
    with open(HISTORICO, "a", encoding="utf-8") as f:
        f.write(usuario + ";" + idm + ";" + acao + "\n")
    print(f"Música {acao} !")

def historico(usuario):
    if os.path.exists(HISTORICO):
        with open(HISTORICO, "r", encoding="utf-8") as f:
            linhas = f.readlines()
        for acao in ["curtida", "descurtida"]:
            print("\n== " + acao.title() + " ==")
            for l in linhas:
                partes = l.strip().split(";")
                if len(partes) == 3:
                    u, idm, a = partes
                    if u == usuario and a == acao:
                        for m in MUSICAS:
                            if m["id"] == idm:
                                print(f"- {m['nome']} - {m['artista']} - {m['genero']}")

def carregar_playlists():
    playlists = {}
    if os.path.exists(PLAYLISTS):
        with open(PLAYLISTS, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) == 3:
                    user, nome, ids = partes
                    playlists[(user, nome)] = ids.split(",") if ids else []
    return playlists

def salvar_playlists(playlists):
    with open(PLAYLISTS, "w", encoding="utf-8") as f:
        for (user, nome), ids in playlists.items():
            linha = user + ";" + nome + ";" + ",".join(ids)
            f.write(linha + "\n")

def playlist_menu(user):
    pl = carregar_playlists()
    p = input("Nome da playlist: ")
    chave = (user, p)
    if chave not in pl:
        pl[chave] = []
    while True:
        op = input("[1] Adicionar Música  [2] Remover Música  [3] Ver Playlist  [4] Excluir Playlist  [0] Sair: ")
        if op == "1":
            for m in MUSICAS:
                print(f"{m['id']}: {m['nome']} - {m['artista']} - {m['genero']}")
            idm = input("ID da música: ")
            pl[chave].append(idm)
        elif op == "2":
            idm = input("ID da música que quer remover: ")
            if idm in pl[chave]:
                pl[chave].remove(idm)
        elif op == "3":
            print(f"\nPlaylist: {p}")
            for idm in pl[chave]:
                for m in MUSICAS:
                    if m["id"] == idm:
                        print(f"- {m['nome']} - {m['artista']} - {m['genero']}")
        elif op == "4":
            confirmar = input(f"Tem certeza que deseja excluir a playlist '{p}'? (s/n): ").lower()
            if confirmar == "s":
                if chave in pl:
                    del pl[chave]
                    print("Playlist excluída!")
                    break
                else:
                    print("Playlist não encontrada.")
        elif op == "0":
            break
    salvar_playlists(pl)

def menu_usuario(user):
    while True:
        print("\n[1] Buscar [2] Curtir [3] Histórico [4] Playlist [0] Sair")
        op = input("Escolha: ")
        if op == "1":
            buscar()
        elif op == "2":
            curtir(user)
        elif op == "3":
            historico(user)
        elif op == "4":
            playlist_menu(user)
        elif op == "0":
            break

def main():
    while True:
        print("\n== Spotifei ==")
        print("1 - Cadastrar\n2 - Login\n0 - Sair")
        op = input("Escolha: ")
        if op == "1":
            cadastrar()
        elif op == "2":
            login()
        elif op == "0":
            print("Saindo...")
            break

if __name__ == "__main__":
    main()
