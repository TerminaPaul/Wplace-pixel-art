import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from Background import Background


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Truc qui marche pas V1")
        self.root.resizable(False, False)

        self.bg = None          # objet Background (chargé après ouverture d'image)
        self.photo = None       # c'est important
        self.historique = []    # liste des sauvegardes pour le "retour" (pourquoi c'est si simple :'/)

        self._setup_ui()


    #  Construction de l'interface # ------------------------------------------------------------------ #

    def _setup_ui(self):
        # --- Barre de boutons ---
        toolbar = tk.Frame(self.root, bg="#2b2b2b", pady=6)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#444", "fg": "white", "relief": "flat",
                     "padx": 12, "pady": 4, "cursor": "hand2"}

        tk.Button(toolbar, text="Ouvrir",    command=self._ouvrir,      **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Sauvegarder", command=self._sauvegarder, **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="Retour",    command=self._retour,      **btn_style).pack(side=tk.LEFT, padx=4)

        # --- Canvas pour afficher l'image ---
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e",
                                width=1600, height=900,
                                cursor="crosshair")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_clic) # Clic gauche → fait l'action

    #  Affichage de l'image # ------------------------------------------------------------------ #

    def _afficher_image(self):
        if self.bg is None:
            return

        # Adapter la taille du canvas à l'image
        w, h = self.bg.img.size
        self.canvas.config(width=w, height=h)

        # Conversion PIL → Tkinter (y parait sa marche)
        self.photo = ImageTk.PhotoImage(self.bg.img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    #  Affichage de l'image # ------------------------------------------------------------------ #

    def _ouvrir(self):
        chemin = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images PNG", "*.png"), ("Toutes les images", "*.*")]
        )
        if not chemin:
            return

        self.bg = Background(chemin)
        self.historique.clear()
        self._afficher_image()

    def _on_clic(self, event):
        if self.bg is None:
            messagebox.showinfo("Info", "Oe non fait pas sa si ya rien d'ouvert.")
            return

        x, y = event.x, event.y

        self.historique.append(self.bg.img.copy()) #save avant modif

        # Appel Background
        self.bg.transparent(x, y) # t deja = 50
        self._afficher_image()

    def _sauvegarder(self):
        chemin = filedialog.asksaveasfilename(
            title="Ou sauvegarder ?",
            defaultextension=".png",
            filetypes=[("Images PNG", "*.png")]
        )
        if chemin:
            nom_sans_ext = chemin.removesuffix(".png")
            self.bg.save(nom_sans_ext)

    def _retour(self):
        self.bg.img = self.historique.pop()
        self._afficher_image()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()