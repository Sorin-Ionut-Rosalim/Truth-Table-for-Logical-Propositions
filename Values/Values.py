
def negation(val):
    return not val

def conjunction(val1, val2):
    return val1 and val2

def disjunction(val1,val2):
    return val1 or val2

def implication(val1, val2):
    return not(val1 and not val2)

def equivalence(val1, val2):
    return val1 == val2

def is_two_param_operator(op):
    return op in ['&' ,'|' ,'>' ,'=']

def is_atom(element):
    if type(element) != type(""):
        return False
    return element.isupper()

def is_atom_or_prop(elem):
    if type(elem) == type([]):
        return True
    else:
        return is_atom(elem)

def op_to_str(op):
    if op == '!':
        return '¬'
    if op == '&':
        return '/\\'
    if op == '|':
        return 'V'
    if op == '>':
        return '->'
    if op == '=':
        return '<=>'

def logic_prop_to_str(prop):
    if is_atom(prop):
        return prop
    if len(prop) == 2:
        return '(' + op_to_str(prop[0]) + '' + logic_prop_to_str(prop[1]) + ')'
    if len(prop) == 3:
        return '(' + logic_prop_to_str(prop[0]) + '' + op_to_str(prop[1]) + '' + logic_prop_to_str(prop[2]) + ')'

class LogicProposition:
    def __str__(self):
        return logic_prop_to_str(self.prop)


    def __init__(self, proposition ):
        if type(proposition) == type(''):
            proposition = proposition.strip()
            #Remove white character form beginning and end of the string
            if len(proposition) == 1:
                self.prop = proposition
                self.atoms = set([proposition])
                #set() returns:
                #an empty set if no parameters are passed
                #a set constructed from the given iterable parameter
                return

            self.prop = None
            self.atoms = set()

            def create_prop(iter):
                    element = []
                    try:
                        while True:
                            el = next(iter)
                            if el == '(':
                                element.append(create_prop(iter))
                            elif el == '!' or el == '¬':
                                element.append('!')
                            elif el == '&' or el == '/\\' or el == '^':
                                element.append('&')
                            elif el == '|' or el == 'V' or el == 'v':
                                element.append('|')
                            elif el == '>' or el == '->' or el == '→':
                                element.append('>')
                            elif el == '=' or el == '<=>' or el == '≡':
                                element.append('=')
                            elif el == ')':
                                if len(element) == 2:
                                    #The assert keyword lets you test if a condition in your code returns True, 
                                    #if not, the program will raise an AssertionError.
                                    assert(element[0] == '!')
                                    assert(is_atom_or_prop(element[1]))
                                elif len(element) == 3:
                                    assert(is_two_param_operator(element[1]))
                                    assert(is_atom_or_prop(element[0]))
                                    assert(is_atom_or_prop(element[2]))

                                return element 
                                #Finished element
                            elif el == ' ':
                                pass
                            elif el.isupper() and el.isalpha():
                                element.append(el)
                                #Atomic prop
                                self.atoms.add(el)
                            else:
                                raise ValueError(f"Unexpected value: {el}")
                    except StopIteration:
                        raise StopIteration
                        #Retrun Element/Final of iteration

            i = iter(proposition)
            #The iter() function creates an object which can be iterated one element at a time.
            assert(next(i) == '(')
            self.prop = create_prop(iter(i))

        else:
            self.prop = proposition
            self.atoms = set()
            
            def gen_atoms(prop):
                if is_atom(prop):
                    self.atoms.add(prop)
                elif len(prop) == 2:
                    gen_atoms(prop[1])
                elif len(prop) == 3:
                    gen_atoms(prop[0])
                    gen_atoms(prop[2])
            gen_atoms(self.prop)

        self.atoms = list(sorted(list(self.atoms)))
        #We sort alphabetically the list with atomic propositions


    def combinations(self):
        limit = len(self.atoms)

        def generator(val = 0, l = []):
            if val == limit:
                yield l
                #yield is used to return from a function without destroying the states of its local variable and when the function is called,
                # the execution starts from the last yield statement. Any function that contains a yield keyword is termed as generator.
                #e.g. for 2 atomic prop A B we will have all the combinations [F,F] [F,T], [T,F], [T,T]
                #we will have 2^n rows in our truth tabel where n is the number of atomic prop
            else:
                yield from generator(val + 1, l + [False])
                yield from generator(val + 1, l + [True])

        return generator()


    def evaluator(self, values):
        
        def evaluation(element):
            if is_atom(element):
                return values[element]
            if len(element) == 2:
                return negation(evaluation(element[1]))
            elif len(element) == 3:
                if element[1] == '&':
                    return conjunction(evaluation(element[0]),evaluation(element[2]))
                if element[1] == '|':
                    return disjunction(evaluation(element[0]),evaluation(element[2]))
                if element[1] == '>':
                    return implication(evaluation(element[0]),evaluation(element[2]))
                if element[1] == '=':
                    return equivalence(evaluation(element[0]),evaluation(element[2]))

        return evaluation(self.prop)


    def subpropositions(self):
        
        def generator(prop):
            if is_atom(prop):
                return
            if len(prop) == 2:
                yield from generator(prop[1])
            elif len(prop) == 3:
                yield from generator(prop[0])
                yield from generator(prop[2])

            yield LogicProposition(prop)

        return generator(self.prop)

def print_table(table, max_width):
    
    if max_width is None:
        max_width = [10] * len(table[0])
    for line in table:
        for i, item in zip(range(100000), line):
            if item == 'T':
                print(str(item).rjust(max_width[i]), end=" | ")
            elif item == 'F':
                print(str(item).rjust(max_width[i]), end=" | ")
            else:
                print(str(item).rjust(max_width[i]), end=" | ")
        
        print()

def gen_table(prop):
	table = []

	def first_line():
		line = []
		line.append('#')
		line += list(prop.atoms)
		# line.append(l)
		line += list(prop.subpropositions())

		return line

	table.append(first_line())

	for no, i in zip(range(99999), prop.combinations()):
		line = []
		line.append(no + 1)
		line += ["T" if elem else "F" for elem in i]

		for prop in prop.subpropositions():
			value = prop.evaluator({j[0]: j[1] for j in zip(prop.atoms, i)})
			line.append("T" if value else "F")
		table.append(line)

	return table

def get_max_width(table):
	width = [0] * len(table[0])
	for line in table:
		for i in range(len(line)):
			new_width = len(str(line[i]))
			if width[i] < new_width:
				width[i] = new_width
	return width

p = None
print(" !, ¬ are the symbol for not\n",\
    "|, /\\ are the symbol for or\n",\
    "&,  V are the symbol for and\n",\
    ">, -> are the symbol for implies\n",\
    "=, <=> are the symbol for equivalence\n",\
    "Any upper case letter is an atomic proposition")
p = input(" Please input a string of symbols:\n")
prop = LogicProposition(p)
table = gen_table(prop)
print_table(table, get_max_width(table))