from PIL import Image, ImageDraw

# Tamanho da imagem (por exemplo, 32x32 pixels)
img_size = (50, 50)
img = Image.new("RGBA", img_size, (0, 0, 0, 0))  # Fundo transparente

draw = ImageDraw.Draw(img)

# Desenha um círculo vermelho para representar a maçã
center = (img_size[0] // 2, img_size[1] // 2)
radius = 10
draw.ellipse(
    [center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius],
    fill=(255, 0, 0, 255)
)

# Desenha uma pequena folha verde no topo
leaf_coords = [
    (center[0], center[1] - radius),       # ponto de ancoragem na borda superior
    (center[0] - 5, center[1] - radius - 10),
    (center[0] + 5, center[1] - radius - 10)
]
draw.polygon(leaf_coords, fill=(0, 255, 0, 255))

# Salva a imagem como PNG
img.save("apple.png")
print("Imagem da maçã gerada com sucesso!")