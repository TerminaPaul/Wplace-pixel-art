from Background import Background

if __name__ == '__main__':
    x = int(input('Donner la coordonnée du point "x" : '))
    y = int(input('Donner la coordonnée du point "y" : '))
    img = (Background("test1"))
    img.transparent(x, y)

    while True:
        answer = input("Continuer les modifications ? \noui/non/retour")

        if answer == "oui":
            img.save("test1_result")
            x = int(input('Donner la coordonnée du point "x" : '))
            y = int(input('Donner la coordonnée du point "y" : '))
            img = Background("test1_result")
            img.transparent(x, y)

        elif answer == "non":
            img.save("test1_result")
            print("Ok image sauvegardée")
            break

        elif answer == "retour":
            print("Retour a l'étape precedent")
            x = int(input('Donner la coordonnée du point "x" : '))
            y = int(input('Donner la coordonnée du point "y" : '))
            img = Background("test1_result")
            img.transparent(x, y)