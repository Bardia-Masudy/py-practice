### Contact Book

#with open('', 'w') as book

class Contact(object):
    def __init__(self) -> None:
        response = []
        # Prompts user for input upon creation.
        for i in ['deal','profession','email address','phone number']: 
            response.append(input(f"What is their {i}?:\n"))
            print('')
        self.notes, self.role, self.email, self.phone = response

contactBook = {}



def addContact(name):
    info = Contact()
    contactBook.setdefault(name, info)

def showBook():
    for name, info in contactBook.values():
        print(f'{name}:\n{info.notes}\n{info.role}\n{info.email} - {info.phone}')

addContact('Jim')

showBook()