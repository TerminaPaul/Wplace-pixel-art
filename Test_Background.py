from Background import Background

if __name__ == '__main__':
    x = int(input('Donner la coordonnée du point "x" : '))
    y = int(input('Donner la coordonnée du point "y" : '))
    img = (Background("test"))
    img.save("test_result_backup")
    img.transparent(x, y)

    while True:
        img.save("test_result")
        img.show()
        answer = input("Continuer les modifications ? \noui/non/retour")

        if answer == "oui":
            img.save("test_result_backup")
            x = int(input('Donner la coordonnée du point "x" : '))
            y = int(input('Donner la coordonnée du point "y" : '))
            img = Background("test_result")
            img.transparent(x, y)

        elif answer == "non":
            print("Ok image sauvegardée")
            break

        elif answer == "retour":
            print("Retour a l'étape precedent")
            x = int(input('Donner la coordonnée du point "x" : '))
            y = int(input('Donner la coordonnée du point "y" : '))
            img = Background("test_result_backup")
            img.transparent(x, y)