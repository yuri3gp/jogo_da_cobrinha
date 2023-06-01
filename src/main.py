import pygame
import time
import random
import sys

# Inicialização do Pygame
pygame.init()

# Definição das cores
cor_fundo = pygame.Color(0, 0, 0)  # Preto
cor_cobra = pygame.Color(0, 255, 0)  # Verde
cor_comida = pygame.Color(255, 0, 0)  # Vermelho
cor_gameover = pygame.Color(255, 255, 255)  # Branco

# Configurações da janela do jogo
largura = 640
altura = 480
tamanho_bloco = 20
placar_tamanho = 40

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake')

# Função para exibir o placar na tela
def mostrar_placar(pontos):
    fonte = pygame.font.SysFont('Arial', 20)
    texto = fonte.render('Pontos: ' + str(pontos), True, cor_cobra)
    janela.blit(texto, (0, 0))

# Função para exibir a tela de "Game Over"
def mostrar_gameover(pontos):
    fonte = pygame.font.SysFont('Arial', 50)
    texto1 = fonte.render('Game Over', True, cor_gameover)
    texto2 = fonte.render('Pontuação: ' + str(pontos), True, cor_gameover)
    texto3 = fonte.render('Pressione R para jogar novamente', True, cor_gameover)
    janela.blit(texto1, (largura / 2 - texto1.get_width() / 2, altura / 2 - texto1.get_height() - 30))
    janela.blit(texto2, (largura / 2 - texto2.get_width() / 2, altura / 2 - 15))
    janela.blit(texto3, (largura / 2 - texto3.get_width() / 2, altura / 2 + 30))

# Função para exibir a tela de "Records"
def mostrar_records(records):
    fonte = pygame.font.SysFont('Arial', 30)
    texto1 = fonte.render('Records', True, cor_gameover)
    janela.blit(texto1, (largura / 2 - texto1.get_width() / 2, 50))
    
    fonte2 = pygame.font.SysFont('Arial', 20)
    pos_y = 100
    for i, rec in enumerate(records):
        texto = fonte2.render(str(i+1) + '. ' + str(rec), True, cor_gameover)
        janela.blit(texto, (largura / 2 - texto.get_width() / 2, pos_y))
        pos_y += 30

# Função principal do jogo
def jogo_snake():
    # Configurações iniciais
    pos_x = largura / 2
    pos_y = altura / 2
    delta_x = 0
    delta_y = 0
    cobra = [[pos_x, pos_y]]
    comida = [random.randrange(1, largura/tamanho_bloco) * tamanho_bloco,
              random.randrange(1, altura/tamanho_bloco) * tamanho_bloco]
    pontos = 0
    game_over = False
    records = []

    try:
        with open('records.txt', 'r') as arquivo:
            for linha in arquivo:
                records.append(int(linha.strip()))
    except FileNotFoundError:
        pass

    # Loop principal
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if not game_over:
                    if evento.key == pygame.K_LEFT and delta_x != tamanho_bloco:
                        delta_x = -tamanho_bloco
                        delta_y = 0
                    elif evento.key == pygame.K_RIGHT and delta_x != -tamanho_bloco:
                        delta_x = tamanho_bloco
                        delta_y = 0
                    elif evento.key == pygame.K_UP and delta_y != tamanho_bloco:
                        delta_x = 0
                        delta_y = -tamanho_bloco
                    elif evento.key == pygame.K_DOWN and delta_y != -tamanho_bloco:
                        delta_x = 0
                        delta_y = tamanho_bloco
                else:
                    if evento.key == pygame.K_r:
                        jogo_snake()

        if not game_over:
            pos_x = (pos_x + delta_x) % largura
            pos_y = (pos_y + delta_y) % altura

            janela.fill(cor_fundo)
            pygame.draw.rect(janela, cor_comida, pygame.Rect(comida[0], comida[1], tamanho_bloco, tamanho_bloco))

            cobra.append([pos_x, pos_y])
            if len(cobra) > pontos + 1:
                del cobra[0]

            for segmento in cobra[:-1]:
                if segmento == [pos_x, pos_y]:
                    game_over = True

            for segmento in cobra:
                pygame.draw.rect(janela, cor_cobra, pygame.Rect(segmento[0], segmento[1], tamanho_bloco, tamanho_bloco))

            if pos_x == comida[0] and pos_y == comida[1]:
                comida = [random.randrange(1, largura/tamanho_bloco) * tamanho_bloco,
                          random.randrange(1, altura/tamanho_bloco) * tamanho_bloco]
                pontos += 1

            mostrar_placar(pontos)
        else:
            if pontos > 0:
                records.append(pontos)
                records.sort(reverse=True)
                records = records[:5]  # Manter apenas os 5 melhores recordes

                with open('records.txt', 'w') as arquivo:
                    for rec in records:
                        arquivo.write(str(rec) + '\n')

            mostrar_gameover(pontos)
            mostrar_records(records)

        pygame.display.update()
        time.sleep(0.1)

# Iniciar o jogo
jogo_snake()
