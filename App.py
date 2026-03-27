import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from Background import Background


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Wplace Pixel Art")
        self.root.resizable(False, False)

        self.bg = None          # objet Background (chargé après ouverture d'image)
        self.photo = None       # référence ImageTk (obligatoire pour éviter le garbage collector)
        self.historique = []    # liste des sauvegardes pour le "retour"

        self._setup_ui()

    # ------------------------------------------------------------------ #
    #  Construction de l'interface                                         #
    # ------------------------------------------------------------------ #

    def _setup_ui(self):
        # --- Barre de boutons ---
        toolbar = tk.Frame(self.root, bg="#2b2b2b", pady=6)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_style = {"bg": "#444", "fg": "white", "relief": "flat",
                     "padx": 12, "pady": 4, "cursor": "hand2"}

        tk.Button(toolbar, text="📂 Ouvrir",    command=self._ouvrir,      **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="💾 Sauvegarder", command=self._sauvegarder, **btn_style).pack(side=tk.LEFT, padx=4)
        tk.Button(toolbar, text="↩ Retour",    command=self._retour,      **btn_style).pack(side=tk.LEFT, padx=4)

        # --- Label tolérance + slider ---
        tk.Label(toolbar, text="Tolérance :", bg="#2b2b2b", fg="white").pack(side=tk.LEFT, padx=(16, 4))
        self.tolerance = tk.IntVar(value=50)
        tk.Scale(toolbar, from_=0, to=150, orient=tk.HORIZONTAL,
                 variable=self.tolerance, bg="#2b2b2b", fg="white",
                 highlightthickness=0, length=120).pack(side=tk.LEFT)

        # --- Label d'info (coordonnées du dernier clic) ---
        self.info_var = tk.StringVar(value="Ouvre une image pour commencer")
        tk.Label(toolbar, textvariable=self.info_var,
                 bg="#2b2b2b", fg="#aaa").pack(side=tk.RIGHT, padx=8)

        # --- Canvas pour afficher l'image ---
        self.canvas = tk.Canvas(self.root, bg="#1e1e1e",
                                width=600, height=500,
                                cursor="crosshair")
        self.canvas.pack()

        # Clic gauche → rendre transparent
        self.canvas.bind("<Button-1>", self._on_clic)

    # ------------------------------------------------------------------ #
    #  Affichage de l'image                                                #
    # ------------------------------------------------------------------ #

    def _afficher_image(self):
        if self.bg is None:
            return

        # Adapter la taille du canvas à l'image
        w, h = self.bg.img.size
        self.canvas.config(width=w, height=h)

        # Conversion PIL → Tkinter (garder la référence dans self.photo !)
        self.photo = ImageTk.PhotoImage(self.bg.img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)

    # ------------------------------------------------------------------ #
    #  Actions                                                             #
    # ------------------------------------------------------------------ #

    def _ouvrir(self):
        chemin = filedialog.askopenfilename(
            title="Choisir une image",
            filetypes=[("Images PNG", "*.png"), ("Toutes les images", "*.*")]
        )
        if not chemin:
            return

        # On retire l'extension .png car Background l'ajoute lui-même
        nom_sans_ext = chemin.removesuffix(".png")

        self.bg = Background(nom_sans_ext)
        self.historique.clear()
        self._afficher_image()
        self.info_var.set(f"Image chargée — clic pour supprimer le fond")

    def _on_clic(self, event):
        if self.bg is None:
            messagebox.showinfo("Info", "Ouvre d'abord une image !")
            return

        x, y = event.x, event.y

        # Sauvegarde de l'état actuel avant modification (pour le retour)
        self.historique.append(self.bg.img.copy())

        # Appel à la méthode de ta classe Background
        self.bg.transparent(x, y, t=self.tolerance.get())

        self._afficher_image()
        self.info_var.set(f"Clic en ({x}, {y})  —  tolérance {self.tolerance.get()}")

    def _sauvegarder(self):
        if self.bg is None:
            messagebox.showinfo("Info", "Aucune image à sauvegarder.")
            return

        chemin = filedialog.asksaveasfilename(
            title="Sauvegarder sous",
            defaultextension=".png",
            filetypes=[("Images PNG", "*.png")]
        )
        if chemin:
            nom_sans_ext = chemin.removesuffix(".png")
            self.bg.save(nom_sans_ext)
            messagebox.showinfo("Succès", f"Image sauvegardée !\n{chemin}")

    def _retour(self):
        if not self.historique:
            messagebox.showinfo("Info", "Aucune action à annuler.")
            return

        # Restaure le dernier état sauvegardé
        self.bg.img = self.historique.pop()
        self._afficher_image()
        self.info_var.set("Retour à l'étape précédente")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()