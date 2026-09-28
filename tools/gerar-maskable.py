#!/usr/bin/env python3
"""
Gera logos/logo-maskable.png a partir de logos/logo-512.png.

Um icone maskable e cortado pelo sistema em circulo (Android) ou por um
mascote (iOS). O conteudo tem de caber na "safe zone": o circulo util ocupa
80% do lado, ou seja ~10% de margem em cada lado. Colar o logo cheio no
canvas faria o leao ser cortado pelas bordas.

Este script reduz o logo a 60% (307x307) e centra-o num canvas 512x512
com o fundo escuro da app, deixando ~20% de margem em cada lado.

Uso:
    python tools/gerar-maskable.py

Requer Pillow:
    pip install Pillow
"""

import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit(
        "Falta a Pillow. Instala com:\n"
        "    pip install Pillow"
    )

# --- Parametros -----------------------------------------------------------

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "logos", "logo-512.png")
DESTINO = os.path.join(RAIZ, "logos", "logo-maskable.png")

CANVAS = 512          # lado do canvas final (obrigatorio para maskable)
ESCALA = 0.60         # o logo ocupa 60% do canvas
FUNDO = (11, 18, 12, 255)   # #0b120c em RGBA, o mesmo do manifest


def main():
    if not os.path.exists(ORIGEM):
        sys.exit("Nao encontro o ficheiro de origem: %s" % ORIGEM)

    alvo = int(round(CANVAS * ESCALA))          # 307 px
    margem = (CANVAS - alvo) // 2               # 102 px de cada lado

    with Image.open(ORIGEM) as img:
        # Converte para RGBA para poder colar sobre o fundo sem artefactos.
        logo = img.convert("RGBA")

        # Reduz mantendo a qualidade: LANCZOS e o melhor filtro para reduzir.
        logo = logo.resize((alvo, alvo), Image.LANCZOS)

    canvas = Image.new("RGBA", (CANVAS, CANVAS), FUNDO)
    canvas.paste(logo, (margem, margem), logo)   # a mascara usa o canal alpha

    canvas.save(DESTINO, "PNG", optimize=True)

    print("Gerado: %s" % DESTINO)
    print("  canvas: %dx%d" % (CANVAS, CANVAS))
    print("  logo:   %dx%d" % (alvo, alvo))
    print("  margem: %d px em cada lado (%.0f%%)" % (margem, margem / CANVAS * 100))


if __name__ == "__main__":
    main()
