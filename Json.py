from PIL import Image

WPLACE_PALETTE = {
    (0,   0,   0  ): "Noir",
    (60,  60,  60 ): "Gris foncé",
    (120, 120, 120): "Gris",
    (170, 170, 170): "Gris moyen",
    (210, 210, 210): "Gris clair",
    (255, 255, 255): "Blanc",
    (96,  0,   24 ): "Rouge profond",
    (165, 14,  30 ): "Rouge foncé",
    (237, 28,  36 ): "Rouge",
    (250, 128, 114): "Rouge clair",
    (228, 92,  26 ): "Orange foncé",
    (255, 127, 39 ): "Orange",
    (246, 170, 9  ): "Or",
    (249, 221, 59 ): "Jaune",
    (255, 250, 188): "Jaune clair",
    (156, 132, 49 ): "Verge d'or foncée",
    (197, 173, 49 ): "Verge d'or",
    (232, 212, 95 ): "Jaune verge d'or clair",
    (74,  107, 58 ): "Olive foncée",
    (90,  148, 74 ): "Olive",
    (132, 197, 115): "Olive claire",
    (14,  185, 104): "Vert foncé",
    (19,  230, 123): "Vert",
    (135, 255, 94 ): "Vert clair",
    (12,  129, 110): "Sarcelle foncée",
    (16,  174, 166): "Sarcelle",
    (19,  225, 190): "Bleu-vert clair",
    (15,  121, 159): "Cyan foncé",
    (96,  247, 242): "Cyan",
    (187, 250, 242): "Cyan clair",
    (40,  80,  158): "Bleu foncé",
    (64,  147, 228): "Bleu",
    (125, 199, 255): "Bleu clair",
    (77,  49,  184): "Indigo foncé",
    (107, 80,  246): "Indigo",
    (153, 177, 251): "Indigo clair",
    (74,  66,  132): "Bleu Ardoise Foncé",
    (122, 113, 196): "Bleu ardoise",
    (181, 174, 241): "Bleu ardoise clair",
    (120, 12,  153): "Violet foncé",
    (170, 56,  185): "Violet",
    (224, 159, 249): "Violet clair",
    (203, 0,   122): "Rose foncé",
    (236, 31,  128): "Rose",
    (243, 141, 169): "Rose clair",
    (155, 82,  73 ): "Pêche Foncé",
    (209, 128, 120): "Pêche",
    (250, 182, 164): "Pêche Claire",
    (104, 70,  52 ): "Brun foncé",
    (149, 104, 42 ): "Marron",
    (219, 164, 99 ): "Marron clair",
    (123, 99,  82 ): "Bronzage Foncé",
    (156, 132, 107): "Bronzé",
    (214, 181, 148): "Beige clair",
    (209, 128, 81 ): "Beige foncé",
    (248, 178, 119): "Beige",
    (255, 197, 165): "Beige très clair",
    (109, 100, 63 ): "Pierre sombre",
    (148, 140, 107): "Pierre",
    (205, 197, 158): "Pierre légère",
    (51,  57,  65 ): "Ardoise foncée",
    (109, 117, 141): "Ardoise",
    (179, 185, 209): "Ardoise claire",
}

def trier_pixels_proche(pixels):
    if not pixels:
        return []
    restants = pixels.copy()
    ordonnes = [restants.pop(0)]
    while restants:
        dernier = ordonnes[-1]
        plus_proche = min(restants, key=lambda p: (p["x"] - dernier["x"])**2 + (p["y"] - dernier["y"])**2)
        ordonnes.append(plus_proche)
        restants.remove(plus_proche)
    return ordonnes

class Json:
    def __init__(self, img):
        self.img = Image.open(img).convert("RGBA")
        self.nom = img

    def save_pixels(self):
        import os
        width, height = self.img.size

        couleurs = {}
        for y in range(height):
            for x in range(width):
                r, g, b, a = self.img.getpixel((x, y))
                if a == 255:
                    nom = WPLACE_PALETTE.get((r, g, b), "Inconnu")
                    if nom not in couleurs:
                        couleurs[nom] = []
                    couleurs[nom].append({"x": x, "y": y})

        for nom in couleurs:
            couleurs[nom] = trier_pixels_proche(couleurs[nom])

        nom_sortie = os.path.basename(self.nom) + ".json"
        with open(nom_sortie, "w", encoding="utf-8") as f:
            f.write('{\n')
            items = list(couleurs.items())
            for i, (nom, pixels) in enumerate(items):
                virgule = "," if i < len(items) - 1 else ""
                f.write(f'  "{nom}": [\n')
                for j, pixel in enumerate(pixels):
                    virgule2 = "," if j < len(pixels) - 1 else ""
                    f.write(f'    {{"x": {pixel["x"]}, "y": {pixel["y"]}}}{virgule2}\n')
                f.write(f'  ]{virgule}\n')
            f.write('}')

if __name__ == "__main__":
    perso = Json("test.png")
    perso.save_pixels()