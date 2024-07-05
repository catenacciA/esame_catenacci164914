from managers.space_manager import SpaceManager
from interfaces.user_interface import user_interface


def select_user(manager):
    username = input("Inserisci il nome utente: ").strip()
    user = manager.find_user(username)
    if user:
        print(f"Utente '{username}' selezionato.")
        return user
    else:
        print(f"Utente '{username}' non trovato.")
        return None


def create_new_user(manager):
    while True:
        username = input("Inserisci il nome utente: ").strip()
        if not username:
            print("Il nome utente non può essere vuoto. Riprova.")
            continue
        try:
            user = manager.create_user(username)
            print(f"Utente '{username}' creato e selezionato.")
            return user
        except ValueError as e:
            print(e)
        except Exception as e:
            print(f"Errore nella creazione dell'utente: {e}")


def save_data(manager):
    filename = input("Inserisci il nome del file di backup (es. 'backup.pkl'): ").strip()
    if filename:
        try:
            manager.save_data(filename)
        except Exception as e:
            print(f"Errore nel salvataggio dei dati: {e}")
    else:
        print("Nome del file non valido.")


def load_data(manager):
    filename = input("Inserisci il nome del file di backup da caricare (es. 'backup.pkl'): ").strip()
    if filename:
        try:
            manager.load_data(filename)
        except Exception as e:
            print(f"Errore nel caricamento dei dati: {e}")
    else:
        print("Nome del file non valido.")


def main_menu():
    print("\n--- Menu Principale ---")
    print("1. Seleziona Utente")
    print("2. Crea Nuovo Utente")
    print("3. Carica Dati")
    print("4. Salva Dati")
    print("0. Esci")
    return input("Seleziona un'opzione: ").strip()


def general_interface():
    manager = SpaceManager()

    while True:
        choice = main_menu()

        if choice == '1':
            user = select_user(manager)
            if user:
                user_interface(manager, user)
        elif choice == '2':
            user = create_new_user(manager)
            user_interface(manager, user)
        elif choice == '3':
            load_data(manager)
        elif choice == '4':
            save_data(manager)
        elif choice == '0':
            if input("Vuoi salvare i dati prima di uscire? (s/n): ").strip().lower() == 's':
                save_data(manager)
            print("Uscita dal programma.")
            break
        else:
            print("Opzione non valida. Riprova.")


if __name__ == "__main__":
    general_interface()
