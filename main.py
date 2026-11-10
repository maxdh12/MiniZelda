
import pygame
import json
import os
import math

# Inicializando o pygame
pygame.init()

# Configurações da janela
LARGURA = 1080
ALTURA = 720

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Mini Zelda")

# Cores
VERDE = (50, 150, 50)
VERMELHO = (200, 40, 40)
AZUL = (55, 118, 171)
PELE = (255, 220, 177)

# Carregar sprites do jogador
sprite_parado = pygame.image.load(
    "imagens/parado.png"
).convert_alpha()

sprite_parado = pygame.transform.scale(
    sprite_parado,
    (64, 64)
)

sprite_cima = pygame.image.load(
    "imagens/cima.png"
).convert_alpha()

sprite_baixo = pygame.image.load(
    "imagens/baixo.png"
).convert_alpha()

sprite_esquerda = pygame.image.load(
    "imagens/esquerda.png"
).convert_alpha()

sprite_direita = pygame.image.load(
    "imagens/direita.png"
).convert_alpha()


# Carregar sprites do inimigo
imagem_inimigo = pygame.image.load(
    "imagens/inimigo.png"
).convert_alpha()

print("Tamanho da imagem:", imagem_inimigo.get_size())


# Função para carregar animações do inimigo
def carregar_animacao(caminho):

    folha = pygame.image.load(caminho).convert_alpha()

    largura_quadro = folha.get_width() // 3
    altura_quadro = folha.get_height()

    quadros = []

    for i in range(3):

        quadro = folha.subsurface((
            i * largura_quadro,
            0,
            largura_quadro,
            altura_quadro
        )).copy()

        quadro = pygame.transform.scale(
            quadro,
            (64, 84)
        )

        quadros.append(quadro)

    return quadros


# Carregar animações de movimento do inimigo
animacoes_inimigo = {
    "cima": carregar_animacao("imagens/inimigo_cima.png"),
    "baixo": carregar_animacao("imagens/inimigo_baixo.png"),
    "esquerda": carregar_animacao("imagens/inimigo_esquerda.png"),
    "direita": carregar_animacao("imagens/inimigo_direita.png")
}


# Carregar animação de morte do inimigo
animacao_morte = carregar_animacao(
    "imagens/inimigo_morte.png"
)


# Sprite do inimigo parado
sprite_inimigo_parado = pygame.transform.scale(
    imagem_inimigo,
    (64, 84)
)


# Carregar coração de vida
coracao_vida = pygame.image.load(
    "imagens/coracao_pixel.png"
).convert()

# Deixar o fundo preto transparente
coracao_vida.set_colorkey((0, 0, 0))

# Ajustar tamanho
coracao_vida = pygame.transform.scale(
    coracao_vida,
    (48, 42)
)


# Vida do jogador
vida_jogador = 3
game_over = False
game_over_transicao = False

# Proteção após receber dano
tempo_protecao = 0
duracao_protecao = 1000


# Carregar mapas
mapa_original = pygame.image.load(
    "imagens/mapa.png"
).convert()

mapa_vila_original = pygame.image.load(
    "imagens/vila.jpeg"
).convert()

mapa_acampamento_original = pygame.image.load(
    "imagens/acampamento.png"
).convert()


# Identificar o mapa atual
mapa_atual = "casa"


# Lista de mapas
mapas = {
    "casa": mapa_original,
    "vila": mapa_vila_original,
    "acampamento": mapa_acampamento_original
}


def atualizar_mapa():

    largura_tela = tela.get_width()
    altura_tela = tela.get_height()

    return pygame.transform.scale(
        mapas[mapa_atual],
        (largura_tela, altura_tela)
    )


mapa = atualizar_mapa()


# Separar os quadros das animações do jogador
quadros = {
    "cima": [],
    "baixo": [],
    "esquerda": [],
    "direita": []
}

sprites = {
    "cima": sprite_cima,
    "baixo": sprite_baixo,
    "esquerda": sprite_esquerda,
    "direita": sprite_direita
}


for direcao_sprite in quadros:

    largura = sprites[direcao_sprite].get_width()
    altura = sprites[direcao_sprite].get_height()

    for i in range(10):

        inicio = round(i * largura / 10)
        fim = round((i + 1) * largura / 10)

        quadro = sprites[direcao_sprite].subsurface(
            (inicio, 0, fim - inicio, altura)
        )

        quadro = pygame.transform.scale(
            quadro,
            (64, 64)
        )

        quadros[direcao_sprite].append(quadro)


# Posição inicial do jogador
jogador_x = 660
jogador_y = 410


# Posição inicial do inimigo
inimigo_x = 900
inimigo_y = 450

inimigo_largura = 48
inimigo_altura = 48
inimigo_velocidade = 1.5


# Vida do inimigo
inimigo_vida = 3
inimigo_morto = False

# Animação de morte
inimigo_morrendo = False
quadro_morte = 0
tempo_animacao_morte = 0
velocidade_animacao_morte = 150

# Controle para não receber vários golpes de uma vez
golpe_acertou = False


# Criar área de colisão do inimigo
def criar_colisao_inimigo():

    return pygame.Rect(
        inimigo_x + 15,
        inimigo_y + 45,
        34,
        30
    )


# Animação do inimigo
inimigo_direcao = "parado"
inimigo_quadro = 0
inimigo_tempo_animacao = 0
inimigo_velocidade_animacao = 180


# Configurações do ataque
atacando = False
tempo_ataque = 0
duracao_ataque = 250
progresso_ataque = 0


# Configurações do jogador
velocidade = 3
direcao = "parado"


# Área de saída dos mapas
saida_casa = pygame.Rect(618, 690, 95, 30)
saida_vila = pygame.Rect(580, 270, 110, 50)
saida_vila_sul = pygame.Rect(545, 750, 100, 40)
saida_acampamento_norte = pygame.Rect(580, 0, 100, 60)


# Transição de mapas
transicao_ativa = False
fase_transicao = ""
alpha_transicao = 0

mapa_destino = ""
destino_x = 0
destino_y = 0


# Configuração da colisão do jogador
COLISAO_X = 18
COLISAO_Y = 30
COLISAO_LARGURA = 30
COLISAO_ALTURA = 30


# Criar área de colisão do jogador
def criar_colisao():

    return pygame.Rect(
        jogador_x + COLISAO_X,
        jogador_y + COLISAO_Y,
        COLISAO_LARGURA,
        COLISAO_ALTURA
    )


# Configurações da animação do jogador
quadro_atual = 0
tempo_animacao = 0
velocidade_animacao = 150


# Relógio
relogio = pygame.time.Clock()


# Obstáculos iniciais da casa
obstaculos_iniciais = [
    pygame.Rect(40, 28, 22, 220),
    pygame.Rect(350, 250, 64, 64),
    pygame.Rect(500, 180, 64, 64)
]


# Carregar colisões de cada mapa
def carregar_colisoes(nome_mapa):

    arquivo_colisoes = f"colisoes_{nome_mapa}.json"

    if os.path.exists(arquivo_colisoes):

        try:

            with open(arquivo_colisoes, "r") as arquivo:
                dados = json.load(arquivo)

            return [
                pygame.Rect(x, y, largura, altura)
                for x, y, largura, altura in dados
            ]

        except (json.JSONDecodeError, ValueError):

            print("Arquivo de colisões inválido.")

    if nome_mapa == "casa":
        return obstaculos_iniciais.copy()

    return []


# Carregar colisões do mapa inicial
obstaculos = carregar_colisoes(mapa_atual)


# Configurações da tela
rodando = True
tela_cheia = False


# Editor de colisões
editando = False
inicio_colisao = None


# Loop principal
while rodando:

    dt = relogio.tick(60)


    # Diminuir tempo de proteção
    if tempo_protecao > 0:
        tempo_protecao -= dt


    # Eventos
    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False


        if evento.type == pygame.KEYDOWN:

            # Reiniciar jogo
            if game_over and evento.key == pygame.K_r:

                vida_jogador = 3
                game_over = False
                game_over_transicao = False
                alpha_transicao = 0

                mapa_atual = "casa"
                mapa = atualizar_mapa()
                obstaculos = carregar_colisoes(mapa_atual)

                jogador_x = 660
                jogador_y = 410

                inimigo_x = 900
                inimigo_y = 450

                inimigo_vida = 3
                inimigo_morto = False
                inimigo_morrendo = False

                quadro_morte = 0
                tempo_animacao_morte = 0

                golpe_acertou = False

                tempo_protecao = 0


            # Atacar com a espada
            if evento.key == pygame.K_SPACE and not atacando and not game_over and not game_over_transicao:

                atacando = True
                tempo_ataque = duracao_ataque
                progresso_ataque = 0
                golpe_acertou = False


            # Ativar ou desativar editor
            if evento.key == pygame.K_F2:

                editando = not editando
                inicio_colisao = None


            # Salvar colisões com F5
            if evento.key == pygame.K_F5 and editando:

                arquivo_colisoes = f"colisoes_{mapa_atual}.json"

                dados = [
                    list(obstaculo)
                    for obstaculo in obstaculos
                ]

                with open(arquivo_colisoes, "w") as arquivo:
                    json.dump(dados, arquivo)

                print("Colisões salvas!")


            # Alternar tela cheia
            if evento.key == pygame.K_F11:

                tela_cheia = not tela_cheia

                if tela_cheia:

                    tela = pygame.display.set_mode(
                        (0, 0),
                        pygame.FULLSCREEN
                    )

                else:

                    tela = pygame.display.set_mode(
                        (LARGURA, ALTURA)
                    )

                mapa = atualizar_mapa()


        # Ações do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN:

            # Botão esquerdo: começar a desenhar
            if editando and evento.button == 1:

                inicio_colisao = evento.pos


            # Botão direito: apagar colisão
            elif editando and evento.button == 3:

                for obstaculo in reversed(obstaculos):

                    if obstaculo.collidepoint(evento.pos):

                        obstaculos.remove(obstaculo)
                        break


        # Finalizar colisão
        if evento.type == pygame.MOUSEBUTTONUP:

            if editando and evento.button == 1 and inicio_colisao is not None:

                fim_colisao = evento.pos

                x = min(inicio_colisao[0], fim_colisao[0])
                y = min(inicio_colisao[1], fim_colisao[1])

                largura = abs(fim_colisao[0] - inicio_colisao[0])
                altura = abs(fim_colisao[1] - inicio_colisao[1])

                if largura > 0 and altura > 0:

                    obstaculos.append(
                        pygame.Rect(x, y, largura, altura)
                    )

                inicio_colisao = None


    # Capturar teclas pressionadas
    teclas = pygame.key.get_pressed()

    movimento_x = 0
    movimento_y = 0
    andando = False


    # Movimentação horizontal
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:

        movimento_x -= velocidade
        direcao = "esquerda"
        andando = True


    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:

        movimento_x += velocidade
        direcao = "direita"
        andando = True


    # Movimentação vertical
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:

        movimento_y -= velocidade
        direcao = "cima"
        andando = True


    if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:

        movimento_y += velocidade
        direcao = "baixo"
        andando = True


    # Desativar movimento durante edição e transições
    if editando or transicao_ativa or game_over or game_over_transicao:

        movimento_x = 0
        movimento_y = 0
        andando = False


    # Criar retângulo de colisão atualizado
    jogador_rect = criar_colisao()


    # Colisão horizontal
    novo_rect = jogador_rect.move(movimento_x, 0)

    colidiu = False

    for obstaculo in obstaculos:

        if novo_rect.colliderect(obstaculo):

            colidiu = True
            break


    if not colidiu:
        jogador_x += movimento_x


    # Atualizar colisão após movimento horizontal
    jogador_rect = criar_colisao()


    # Colisão vertical
    novo_rect = jogador_rect.move(0, movimento_y)

    colidiu = False

    for obstaculo in obstaculos:

        if novo_rect.colliderect(obstaculo):

            colidiu = True
            break


    if not colidiu:
        jogador_y += movimento_y


    # Controlar animação do jogador
    if andando:

        tempo_animacao += dt

        if tempo_animacao >= velocidade_animacao:

            quadro_atual += 1

            if quadro_atual >= 10:
                quadro_atual = 0

            tempo_animacao = 0

    else:

        quadro_atual = 0
        tempo_animacao = 0


    # Impedir que o jogador saia da tela
    jogador_x = max(
        0,
        min(jogador_x, tela.get_width() - 64)
    )

    jogador_y = max(
        0,
        min(jogador_y, tela.get_height() - 64)
    )


    # Verificar saída dos mapas
    jogador_rect = criar_colisao()


    # Iniciar transição
    if not transicao_ativa and not game_over and not game_over_transicao:

        if mapa_atual == "casa" and jogador_rect.colliderect(saida_casa):

            transicao_ativa = True
            fase_transicao = "escurecer"

            mapa_destino = "vila"
            destino_x = 600
            destino_y = 300


        elif mapa_atual == "vila" and jogador_rect.colliderect(saida_vila):

            transicao_ativa = True
            fase_transicao = "escurecer"

            mapa_destino = "casa"
            destino_x = 630
            destino_y = 610


        elif mapa_atual == "vila" and jogador_rect.colliderect(saida_vila_sul):

            transicao_ativa = True
            fase_transicao = "escurecer"

            mapa_destino = "acampamento"
            destino_x = 580
            destino_y = 30


        elif mapa_atual == "acampamento" and jogador_rect.colliderect(saida_acampamento_norte):

            transicao_ativa = True
            fase_transicao = "escurecer"

            mapa_destino = "vila"
            destino_x = 580
            destino_y = 620


    # Controlar transição da tela
    if transicao_ativa:

        # Escurecer a tela
        if fase_transicao == "escurecer":

            alpha_transicao += 255 * dt / 500

            if alpha_transicao >= 255:

                alpha_transicao = 255

                mapa_atual = mapa_destino
                mapa = atualizar_mapa()
                obstaculos = carregar_colisoes(mapa_atual)

                jogador_x = destino_x
                jogador_y = destino_y

                fase_transicao = "clarear"


        # Clarear a tela
        elif fase_transicao == "clarear":

            alpha_transicao -= 255 * dt / 500

            if alpha_transicao <= 0:

                alpha_transicao = 0
                transicao_ativa = False
                fase_transicao = ""


    # Transição do Game Over
    if game_over_transicao:

        alpha_transicao += 255 * dt / 1000

        if alpha_transicao >= 255:

            alpha_transicao = 255
            game_over = True
            game_over_transicao = False


    # Controlar duração do ataque
    if atacando:

        tempo_ataque -= dt

        progresso_ataque = 1 - (tempo_ataque / duracao_ataque)

        if tempo_ataque <= 0:

            atacando = False
            progresso_ataque = 0


    # Desenhar mapa
    tela.blit(mapa, (0, 0))


    # Movimentação do inimigo
    distancia = 0

    if mapa_atual == "acampamento" and not transicao_ativa and not game_over and not game_over_transicao and not inimigo_morto and not inimigo_morrendo:

        diferenca_x = jogador_x - inimigo_x
        diferenca_y = jogador_y - inimigo_y

        distancia = math.hypot(diferenca_x, diferenca_y)

        if distancia > 1:

            # Identificar a direção do inimigo
            if abs(diferenca_x) > abs(diferenca_y):

                if diferenca_x > 0:
                    inimigo_direcao = "direita"

                else:
                    inimigo_direcao = "esquerda"

            else:

                if diferenca_y > 0:
                    inimigo_direcao = "baixo"

                else:
                    inimigo_direcao = "cima"


            # Movimentar inimigo
            inimigo_x += (diferenca_x / distancia) * inimigo_velocidade
            inimigo_y += (diferenca_y / distancia) * inimigo_velocidade


            # Controlar animação do inimigo
            inimigo_tempo_animacao += dt

            if inimigo_tempo_animacao >= inimigo_velocidade_animacao:

                inimigo_quadro += 1

                if inimigo_quadro >= 3:
                    inimigo_quadro = 0

                inimigo_tempo_animacao = 0


    # Escolher sprite do jogador
    if andando:

        imagem_atual = quadros[direcao][quadro_atual]

    else:

        if direcao == "parado":

            imagem_atual = sprite_parado

        else:

            imagem_atual = quadros[direcao][0]


    # Mostrar obstáculos
    # for obstaculo in obstaculos:

    #     pygame.draw.rect(
    #         tela,
    #         VERMELHO,
    #         obstaculo,
    #         2
    #     )


    # Mostrar saída para o acampamento
    if mapa_atual == "vila":

        pygame.draw.rect(
            tela,
            AZUL,
            saida_vila_sul,
            3
        )


    if mapa_atual == "acampamento":

        pygame.draw.rect(
            tela,
            AZUL,
            saida_acampamento_norte,
            3
        )


    # Mostrar colisão que está sendo desenhada
    if editando and inicio_colisao is not None:

        mouse_x, mouse_y = pygame.mouse.get_pos()

        x = min(inicio_colisao[0], mouse_x)
        y = min(inicio_colisao[1], mouse_y)

        largura = abs(mouse_x - inicio_colisao[0])
        altura = abs(mouse_y - inicio_colisao[1])

        preview = pygame.Rect(x, y, largura, altura)

        pygame.draw.rect(
            tela,
            AZUL,
            preview,
            2
        )


    # Desenhar personagem com efeito de piscar
    if tempo_protecao <= 0 or (tempo_protecao // 100) % 2 == 0:

        tela.blit(
            imagem_atual,
            (jogador_x, jogador_y)
        )


    # Desenhar corações de vida
    for i in range(vida_jogador):

        posicao_x = 20 + (i * 55)
        posicao_y = 20

        tela.blit(
            coracao_vida,
            (posicao_x, posicao_y)
        )


    # Desenhar espada durante o ataque
    if atacando:

        centro_x = jogador_x + 32
        centro_y = jogador_y + 32

        if direcao == "direita":
            angulo_base = 0

        elif direcao == "esquerda":
            angulo_base = math.pi

        elif direcao == "cima":
            angulo_base = -math.pi / 2

        else:
            angulo_base = math.pi / 2


        angulo_golpe = -0.8 + (progresso_ataque * 1.6)
        angulo = angulo_base + angulo_golpe

        inicio_x = centro_x + math.cos(angulo) * 20
        inicio_y = centro_y + math.sin(angulo) * 20

        ponta_x = centro_x + math.cos(angulo) * 70
        ponta_y = centro_y + math.sin(angulo) * 70

        px = -math.sin(angulo) * 5
        py = math.cos(angulo) * 5

        pontos_lamina = [
            (int(inicio_x + px), int(inicio_y + py)),
            (int(ponta_x), int(ponta_y)),
            (int(inicio_x - px), int(inicio_y - py))
        ]

        pygame.draw.polygon(
            tela,
            (100, 180, 255),
            pontos_lamina
        )

        pygame.draw.line(
            tela,
            (255, 255, 255),
            (int(inicio_x), int(inicio_y)),
            (int(ponta_x), int(ponta_y)),
            2
        )

        guarda_inicio = (
            int(inicio_x - math.sin(angulo) * 10),
            int(inicio_y + math.cos(angulo) * 10)
        )

        guarda_fim = (
            int(inicio_x + math.sin(angulo) * 10),
            int(inicio_y - math.cos(angulo) * 10)
        )

        pygame.draw.line(
            tela,
            (220, 160, 50),
            guarda_inicio,
            guarda_fim,
            5
        )

        cabo_x = inicio_x - math.cos(angulo) * 12
        cabo_y = inicio_y - math.sin(angulo) * 12

        pygame.draw.line(
            tela,
            (110, 65, 30),
            (int(inicio_x), int(inicio_y)),
            (int(cabo_x), int(cabo_y)),
            7
        )


    # Verificar ataque contra o inimigo
    if atacando and not golpe_acertou and not inimigo_morto and not inimigo_morrendo:

        centro_x = jogador_x + 32
        centro_y = jogador_y + 32

        if direcao == "direita":

            ataque_rect = pygame.Rect(
                centro_x + 10,
                centro_y - 10,
                65,
                70
            )

        elif direcao == "esquerda":

            ataque_rect = pygame.Rect(
                centro_x - 75,
                centro_y - 10,
                65,
                70
            )

        elif direcao == "cima":

            ataque_rect = pygame.Rect(
                centro_x - 30,
                centro_y - 75,
                60,
                75
            )

        else:

            ataque_rect = pygame.Rect(
                centro_x - 30,
                centro_y + 10,
                60,
                75
            )


        inimigo_rect = criar_colisao_inimigo()

        if mapa_atual == "acampamento" and ataque_rect.colliderect(inimigo_rect):

            inimigo_vida -= 1
            golpe_acertou = True

            print("Inimigo recebeu dano!")
            print("Vida do inimigo:", inimigo_vida)

            if inimigo_vida <= 0:

                inimigo_morrendo = True
                quadro_morte = 0
                tempo_animacao_morte = 0

                print("Inimigo derrotado!")


    # Verificar colisão entre jogador e inimigo
    if mapa_atual == "acampamento" and not transicao_ativa and not game_over and not game_over_transicao and not inimigo_morto and not inimigo_morrendo:

        jogador_rect = criar_colisao()
        inimigo_rect = criar_colisao_inimigo()

        if jogador_rect.colliderect(inimigo_rect):

            if tempo_protecao <= 0 and vida_jogador > 0:

                vida_jogador -= 1
                tempo_protecao = duracao_protecao

                if vida_jogador <= 0:
                    game_over_transicao = True

                print("Jogador recebeu dano!")
                print("Vida restante:", vida_jogador)


    # Atualizar animação de morte
    if inimigo_morrendo:

        tempo_animacao_morte += dt

        if tempo_animacao_morte >= velocidade_animacao_morte:

            tempo_animacao_morte = 0

            if quadro_morte < len(animacao_morte) - 1:

                quadro_morte += 1

            else:

                inimigo_morto = True
                inimigo_morrendo = False


    # Desenhar inimigo no acampamento
    if mapa_atual == "acampamento" and not inimigo_morto:

        if inimigo_morrendo:

            imagem_inimigo_atual = animacao_morte[quadro_morte]

        elif distancia > 1 and not transicao_ativa and not game_over and not game_over_transicao:

            imagem_inimigo_atual = animacoes_inimigo[inimigo_direcao][inimigo_quadro]

        else:

            imagem_inimigo_atual = sprite_inimigo_parado


        tela.blit(
            imagem_inimigo_atual,
            (int(inimigo_x), int(inimigo_y))
        )


        # Barra de vida do inimigo
        if not inimigo_morrendo:

            barra_largura = 50
            barra_altura = 6

            proporcao_vida = inimigo_vida / 3

            largura_vida = int(barra_largura * proporcao_vida)


            # Fundo da barra
            pygame.draw.rect(
                tela,
                (80, 0, 0),
                (inimigo_x + 7, inimigo_y - 12, barra_largura, barra_altura)
            )


            # Vida restante
            pygame.draw.rect(
                tela,
                (0, 220, 0),
                (inimigo_x + 7, inimigo_y - 12, largura_vida, barra_altura)
            )


    # Atualizar colisão para desenhar
    jogador_rect = criar_colisao()


    # Criar efeito de tela preta
    if alpha_transicao > 0:

        camada_preta = pygame.Surface(
            tela.get_size(),
            pygame.SRCALPHA
        )

        camada_preta.fill(
            (0, 0, 0, int(alpha_transicao))
        )

        tela.blit(camada_preta, (0, 0))


    # Tela de Game Over
    if game_over:

        fonte_game_over = pygame.font.Font(None, 90)

        texto_game_over = fonte_game_over.render(
            "GAME OVER",
            True,
            VERMELHO
        )

        fonte_reiniciar = pygame.font.Font(None, 36)

        texto_reiniciar = fonte_reiniciar.render(
            "Pressione R para reiniciar",
            True,
            (255, 255, 255)
        )

        tela.blit(
            texto_game_over,
            texto_game_over.get_rect(
                center=(tela.get_width() // 2, 300)
            )
        )

        tela.blit(
            texto_reiniciar,
            texto_reiniciar.get_rect(
                center=(tela.get_width() // 2, 380)
            )
        )


    # Atualizar tela
    pygame.display.flip()


# Encerrar pygame
pygame.quit()
