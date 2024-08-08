from customtkinter import CTk, CTkButton, CTkLabel, CTkToplevel
from PIL import Image, ImageTk
import random

# Configurações do jogo
NUM_LINHAS = 4
NUM_COLUNAS = 4
CARTAO_SIZE_W = 150
CARTAO_SIZE_H = 150
IMAGENS_CARTAO = ["imagens/uva.png", "imagens/abacaxi.png", "imagens/banana.png", "imagens/kiwi.png",
                  "imagens/laranja.png", "imagens/maça.png", "imagens/melancia.png", "imagens/pera.png"]
COR_BACKGROUND = "#343a40"
COR_LETRA = "white"
FONT_STYLE = ('Arial', 12, "bold")
FONT_STYLE_DERROTA = ('Arial', 20, "bold")
TENTATIVAS_MAX = 20

# Função para criar o grid de cartas com imagens
def create_card_grid():
    imagens = IMAGENS_CARTAO * 2
    random.shuffle(imagens)
    return [imagens[i * NUM_COLUNAS:(i + 1) * NUM_COLUNAS] for i in range(NUM_LINHAS)]

# Função para fechar o jogo
def fechar_jogo():
    janela.destroy()

# Função para inicializar o jogo
def inicializar_jogo():
    global cartoes, cartao_revelar, cartao_correspondentes, numero_tentativas, grid

    grid = create_card_grid()
    cartoes = [[None for _ in range(NUM_COLUNAS)] for _ in range(NUM_LINHAS)]
    cartao_revelar = []
    cartao_correspondentes = []
    numero_tentativas = 0

    # Atualizar a label de tentativas
    label_tentativas.configure(text=f'Tentativas: {numero_tentativas}/{TENTATIVAS_MAX}')

    # Remover todos os widgets antigos da janela
    for widget in janela.grid_slaves():
        widget.grid_forget()

    # Recriar os botões dos cartões
    for linha in range(NUM_LINHAS):
        for col in range(NUM_COLUNAS):
            cartao = CTkButton(janela, width=CARTAO_SIZE_W, height=CARTAO_SIZE_H, text="", fg_color="black",
                               corner_radius=5, command=lambda l=linha, c=col: revelar_cartao(l, c))
            cartao.grid(row=linha, column=col, padx=5, pady=5)
            cartoes[linha][col] = cartao

    # Botão para sair do jogo
    botao_sair = CTkButton(janela, text="Sair", command=fechar_jogo)
    botao_sair.grid(row=NUM_LINHAS, column=NUM_COLUNAS - 1, padx=10, pady=10, sticky='se')

    # Recriar a label de tentativas
    label_tentativas.grid(row=NUM_LINHAS, columnspan=NUM_COLUNAS, padx=10, pady=10)

# Função para revelar o cartão
def revelar_cartao(linha, col):
    cartao = cartoes[linha][col]
    if len(cartao_revelar) < 2 and cartao not in cartao_revelar and (linha, col) not in cartao_correspondentes:
        imagem = Image.open(grid[linha][col])
        imagem = imagem.resize((CARTAO_SIZE_W, CARTAO_SIZE_H))
        imagem_tk = ImageTk.PhotoImage(imagem)
        cartao.configure(image=imagem_tk, text="")
        cartao.image = imagem_tk  # Manter uma referência da imagem para evitar que ela seja coletada pelo garbage collector
        cartao_revelar.append((linha, col))
        if len(cartao_revelar) == 2:
            janela.after(1000, verificar_cartoes)

# Função para verificar se os cartões correspondem
def verificar_cartoes():
    global numero_tentativas
    linha1, col1 = cartao_revelar[0]
    linha2, col2 = cartao_revelar[1]

    if grid[linha1][col1] == grid[linha2][col2]:
        cartao_correspondentes.append((linha1, col1))
        cartao_correspondentes.append((linha2, col2))
        
    else:
        cartoes[linha1][col1].configure(image="", text="")
        cartoes[linha2][col2].configure(image="", text="")
        
    numero_tentativas += 1

    cartao_revelar.clear()
    label_tentativas.configure(text=f'Tentativas: {numero_tentativas}/{TENTATIVAS_MAX}')

    if len(cartao_correspondentes) == NUM_LINHAS * NUM_COLUNAS:
        label_tentativas.configure(text=f'Parabéns! Você ganhou em {numero_tentativas} tentativas.')
    elif numero_tentativas >= TENTATIVAS_MAX:
        label_tentativas.configure(text=f'Você perdeu! Tentativas: {numero_tentativas}/{TENTATIVAS_MAX}')
        exibir_mensagem_derrota()

# Função para abrir a janela principal (uso exclusivo para reiniciar)
def abrir_janela():
    janela.deiconify()
    inicializar_jogo()

# Função para exibir a mensagem de derrota e reiniciar o jogo
def exibir_mensagem_derrota():
    janela.withdraw()
    nova_janela = CTkToplevel(janela)
    nova_janela.title("DERROTA")
    nova_janela.geometry("300x300")
    nova_janela.resizable(False, False)

    largura_janela, altura_janela = 300, 300
    largura_botao, altura_botao = 100, 50
    x, y = (largura_janela - largura_botao) / 2, (altura_janela - altura_botao) / 2

    btn = CTkButton(nova_janela, text="REINICIAR", command=lambda: [abrir_janela(), nova_janela.destroy()],
                    width=largura_botao, height=altura_botao)
    btn.place(x=x, y=y)

    label_mensagem = CTkLabel(nova_janela, text='Tente Novamente!!', font=FONT_STYLE_DERROTA)
    label_mensagem.place(x=65, y=90)

# Criando a interface
janela = CTk()
janela.title("Jogo de Memória")
janela.configure(bg_color=COR_BACKGROUND)

# Label para número de tentativas
label_tentativas = CTkLabel(janela, text=f'Tentativas: 0/{TENTATIVAS_MAX}', text_color=COR_LETRA, bg_color=COR_BACKGROUND, font=FONT_STYLE)
label_tentativas.grid(row=NUM_LINHAS, columnspan=NUM_COLUNAS, padx=10, pady=10)

# Icon (favicon)
janela.iconbitmap('favicon/favicon.ico')

# Inicializar o jogo pela primeira vez
inicializar_jogo()

# Iniciar a interface gráfica
janela.mainloop()
