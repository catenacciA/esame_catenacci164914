import pickle
import argparse
import os
from datetime import datetime
from models.users import User
from models.space import Space
from models.bookings import Booking


class SpaceManager:
    class SpaceNotFoundException(Exception):
        pass

    class SpaceHasBookingsException(Exception):
        pass

    class SpaceAlreadyExistsException(Exception):
        pass

    class InvalidSpaceNameException(Exception):
        pass

    class InvalidBookingDateException(Exception):
        pass

    class UserNotFoundException(Exception):
        pass

    def __init__(self):
        self.users = []
        self.spaces = []

    def create_user(self, username):
        if self.find_user(username):
            raise ValueError(f"L'utente '{username}' esiste già.")
        if not username:
            raise ValueError("Il nome utente non può essere vuoto.")
        user = User(username)
        self.users.append(user)
        return user

    def find_user(self, username):
        return next((user for user in self.users if user.username == username), None)

    def find_space(self, name):
        return next((space for space in self.spaces if space.name == name), None)

    def add_space(self, user, name, is_private):
        if not isinstance(user, User):
            raise TypeError("Oggetto utente non valido.")
        if not name:
            raise self.InvalidSpaceNameException("Il nome dello spazio non può essere vuoto.")
        if self.find_space(name):
            raise self.SpaceAlreadyExistsException(f"Lo spazio '{name}' esiste già.")
        space = Space(name, is_private)
        self.spaces.append(space)
        user.spaces.append(space)

    def remove_space(self, user, space_name):
        if not isinstance(user, User):
            raise TypeError("Oggetto utente non valido.")
        space_to_remove = next((space for space in user.spaces if space.name == space_name), None)
        if space_to_remove:
            if any(space_to_remove.bookings):
                raise self.SpaceHasBookingsException(
                    f"Lo spazio '{space_name}' ha prenotazioni esistenti e non può essere eliminato.")
            user.spaces.remove(space_to_remove)
            self.spaces.remove(space_to_remove)
        else:
            raise self.SpaceNotFoundException(
                f"Lo spazio '{space_name}' non è stato trovato per l'utente '{user.username}'.")

    def book_space(self, user, space_name, date):
        if not isinstance(user, User):
            raise TypeError("Oggetto utente non valido.")
        if not date:
            raise ValueError("La data di prenotazione non può essere vuota.")
        try:
            booking_date = datetime.strptime(date, "%d-%m-%Y")
            if booking_date < datetime.now():
                raise self.InvalidBookingDateException("La data di prenotazione non può essere nel passato.")
        except ValueError:
            raise self.InvalidBookingDateException("Formato della data di prenotazione non valido. Utilizzare "
                                                   "GG-MM-AAAA.")

        space = next((s for s in self.spaces if s.name == space_name), None)
        if space:
            if space.is_private and space not in user.spaces:
                raise PermissionError(f"Lo spazio '{space_name}' è privato e non può essere prenotato.")
            if any(booking.date == date for booking in space.bookings):
                raise ValueError(f"Lo spazio '{space_name}' è stato già prenotato per la data {date}.")
            booking = Booking(user, space, date)
            space.bookings.append(booking)
            user.bookings.append(booking)
            print(f"Lo spazio '{space_name}' è stato prenotato per la data {date}.")
        else:
            raise self.SpaceNotFoundException(f"Spazio '{space_name}' non trovato.")

    def view_user_bookings(self, user):
        if not isinstance(user, User):
            raise TypeError("Oggetto utente non valido.")
        print(f"Prenotazioni per l'utente '{user.username}':")
        for booking in user.bookings:
            print(f"Spazio: {booking.space.name}, Data: {booking.date}")

    def save_data(self, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump({'users': self.users, 'spaces': self.spaces}, file)
            print(f"Dati salvati in {filename}.")
        except (IOError, pickle.PicklingError) as e:
            print(f"Errore nel salvataggio dei dati: {e}")

    def load_data(self, filename):
        if not os.path.exists(filename):
            print(f"File {filename} non trovato.")
            return
        try:
            with open(filename, 'rb') as file:
                data = pickle.load(file)
                self.users = data.get('users', [])
                self.spaces = data.get('spaces', [])
            print(f"Dati caricati da {filename}.")
        except (IOError, pickle.UnpicklingError) as e:
            print(f"Errore nel caricamento dei dati: {e}")

    def export_user_bookings(self, user, filename):
        if not isinstance(user, User):
            raise TypeError("Oggetto utente non valido.")
        try:
            with open(filename, 'w') as file:
                file.write(f"Prenotazioni per l'utente '{user.username}':\n")
                for booking in user.bookings:
                    file.write(f"Spazio: {booking.space.name}, Data: {booking.date}\n")
            print(f"Prenotazioni esportate in: {filename}.")
        except IOError as e:
            print(f"Errore nell'esportazione delle prenotazioni: {e}")


def main():
    parser = argparse.ArgumentParser(description='Gestione degli spazi.')
    parser.add_argument('-b', '--backup-file', type=str, required=True,
                        help='File di backup da cui caricare i dati.')
    parser.add_argument('-e', '--export-file', type=str, required=True,
                        help='File in cui esportare le prenotazioni.')
    parser.add_argument('-u', '--username', type=str, required=True,
                        help='Nome utente le cui prenotazioni devono essere esportate.')
    args = parser.parse_args()

    manager = SpaceManager()
    manager.load_data(args.backup_file)

    user = manager.find_user(args.username)
    if not user:
        print(f"Utente '{args.username}' non trovato.")
        return

    manager.export_user_bookings(user, args.export_file)


if __name__ == "__main__":
    main()
