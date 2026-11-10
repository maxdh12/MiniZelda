
from PIL import Image

# Matriz do coração em pixel art
# P = vermelho principal
# E = vermelho escuro
# B = branco
# . = fundo preto

coracao = [
    "................",
    "..PPPP....PPPP..",
    ".PPPPPP..PPPPPP.",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPPPP",
    "PPPPPPPPPPPPPEEP",
    ".PPPPPPPPPPPPEE.",
    "..PPPPPPPPPPEE..",
    "...PPPPPPPPEE...",
    "....PPPPPPPEE...",
    ".....PPPPPEE....",
    "......PPPEE.....",
    ".......PPE......",
    "........E.......",
]

# Definir as cores
cores = {
    ".": (0, 0, 0),
    "P": (255, 0, 0),
    "E": (139, 0, 0),
    "B": (255, 255, 255)
}

# Criar imagem
largura = len(coracao[0])
altura = len(coracao)

imagem = Image.new("RGB", (largura, altura), (0, 0, 0))

# Desenhar cada pixel
for y, linha in enumerate(coracao):
    for x, pixel in enumerate(linha):
        imagem.putpixel((x, y), cores[pixel])

# Adicionar brilho branco
imagem.putpixel((3, 2), cores["B"])
imagem.putpixel((4, 2), cores["B"])
imagem.putpixel((2, 3), cores["B"])

# Ampliar sem perder a aparência pixelada
escala = 4

imagem = imagem.resize(
    (largura * escala, altura * escala),
    Image.Resampling.NEAREST
)

# Salvar imagem
imagem.save("coracao_pixel.png")

print("Coração criado com sucesso!")
