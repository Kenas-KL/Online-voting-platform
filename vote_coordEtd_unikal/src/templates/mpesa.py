
def mpesa_menu()
    print("\n-- M-Pesa Menu --")
    print("1. Envoyer de l'argent")

def envoyer_argent(solde):
    numéro = input("Entrez le numéro du destinateur:")
    try:
        montant = float(input("Entrez le montant à envoyer:"))
            if montant <= 0:
                print ("Montant invalide.")
            elif montant > solde:
                print("solde insuffisant.")
            else: 
                solde = montant
                print(f"Transaction réussie.
        vous avez envoyer {montant}KES à {numero}.")
            except ValueError:
                print("Entrée non valide.")
            return solde 
            