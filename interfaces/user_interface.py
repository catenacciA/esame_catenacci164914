from managers.space_manager import SpaceManager


def add_space(manager, user):
    space_name = input("Inserisci il nome dello spazio: ").strip()
    if not space_name:
        print("Il nome dello spazio non può essere vuoto.")
        return
    is_private = input("Spazio privato? (s/n): ").strip().lower() == 's'
    try:
        manager.add_space(user, space_name, is_private)
        print(f"Spazio '{space_name}' aggiunto.")
    except Exception as e:
        print(f"Errore durante l'aggiunta dello spazio: {e}")


def remove_space(manager, user):
    space_name = input("Inserisci il nome dello spazio da rimuovere: ").strip()
    if not space_name:
        print("Il nome dello spazio non può essere vuoto.")
        return
    try:
        manager.remove_space(user, space_name)
        print(f"Spazio '{space_name}' rimosso.")
    except SpaceManager.SpaceNotFoundException as e:
        print(e)
    except SpaceManager.SpaceHasBookingsException as e:
        print(e)
    except Exception as e:
        print(f"Errore durante la rimozione dello spazio: {e}")


def book_space(manager, user):
    space_name = input("Inserisci il nome dello spazio da prenotare: ").strip()
    date = input("Inserisci la data di prenotazione (GG-MM-AAAA): ").strip()
    if not space_name or not date:
        print("Nome dello spazio e data non possono essere vuoti.")
        return
    try:
        manager.book_space(user, space_name, date)
    except Exception as e:
        print(f"Errore durante la prenotazione dello spazio: {e}")


def view_bookings(manager, user):
    try:
        manager.view_user_bookings(user)
    except Exception as e:
        print(f"Errore durante la visualizzazione delle prenotazioni: {e}")


def export_bookings(manager, user):
    filename = input("Inserisci il nome del file per l'esportazione (es. 'prenotazioni.txt'): ").strip()
    if not filename:
        print("Il nome del file non può essere vuoto.")
        return
    try:
        manager.export_user_bookings(user, filename)
    except Exception as e:
        print(f"Errore durante l'esportazione delle prenotazioni: {e}")


def user_menu():
    print("\n--- Menu Utente ---")
    print("1. Aggiungi Spazio")
    print("2. Rimuovi Spazio")
    print("3. Prenota Spazio")
    print("4. Visualizza Prenotazioni")
    print("5. Esporta Prenotazioni")
    print("0. Torna al Menu Principale")
    return input("Seleziona un'opzione: ").strip()


def user_interface(manager, user):
    while True:
        choice = user_menu()

        if choice == '1':
            add_space(manager, user)
        elif choice == '2':
            remove_space(manager, user)
        elif choice == '3':
            book_space(manager, user)
        elif choice == '4':
            view_bookings(manager, user)
        elif choice == '5':
            export_bookings(manager, user)
        elif choice == '0':
            break
        else:
            print("Opzione non valida. Riprova.")

