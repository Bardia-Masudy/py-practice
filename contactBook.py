### Contact Book

#with open('', 'w') as book

class Item(object):
    def __init__(self, objType) -> None:
        responses = []
        match objType:
            case 'edge':
                questions = []
            case 'hindrance':
                questions = []
            case 'power':
                questions = []
            case 'rule':
                questions = []
            case 'equipment':
                questions = []
        # Prompts user for input upon creation.
        for i in questions: 
            responses.append(input(i))
        self.info = responses
        self.type = objType
class InfoBook(object):
    def __init__(self) -> None:
        self.edges = []
        self.hindrances = []
        self.powers = []
        self.rules = []
        self.equipment = []
    
    def addItem(self, objType):
        match objType:
            case 'edge':
                self.edges.append(Item(objType))
            case 'hindrance':
                self.hindrances.append(Item(objType))
            case 'power':
                self.powers.append(Item(objType))
            case 'rule':
                self.rules.append(Item(objType))
            case 'equipment':
                self.equipment.append(Item(objType))
                
book = InfoBook()

book.addItem('edge')

print(book.edges[0])

# Edge, Hindrance, Power, (Rules?), (Equipment?)
# Edge: Name, Requirements, Rules Text, Origin Book + Page Number
# Hindrance: Name, (Minor/Major), Rules Text, Origin Book + Page Number
# Power: Name, Cost, Range, Duration, Rank, Rules Text, Modifiers, (Spell Lists?), Origin Book + Page Number
# Item: Name, Rules Text (could be split into different items, weapon, armour, etc.), Origin Book + Page Number