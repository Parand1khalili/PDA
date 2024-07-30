class PDA:
    def __init__(self):
        self.states = set()  
        self.sigma = set()  
        self.transitions = {}  
        self.start_state = None  
        self.final_state = None  

    def new_state(self, state):
        self.states.add(state)

    def add_transition(self, current_state, input_symbol, stack_top, next_state, stack_push):
        if (current_state, input_symbol, stack_top) not in self.transitions: #if there is not a key as current,input,top add it
            self.transitions[(current_state, input_symbol, stack_top)] = []
        self.transitions[(current_state, input_symbol, stack_top)].append((next_state, stack_push))

def output(pda):
    print(' '.join(pda.sigma))  
    print(' '.join(pda.states))  
    print(pda.start_state)  
    print(pda.final_state)

    for i, j in pda.transitions.items():
        for k in j:
            if i[2] == 'λ':  # Check if the current stack top is epsilon (λ)
                if k[1] == 'λ':  # Check if the stack replacement is epsilon (λ)
                    print(f"{i[0][1:]}, {i[1]}, None, {k[0][1:]}, None")
                else:
                    print(f"{i[0][1:]}, {i[1]}, None, {k[0][1:]}, PUSH({k[1]})")
            else:
                print(f"{i[0][1:]}, {i[1]}, {i[2]}, {k[0][1:]}, POP")

#get input
CFG = dict()
n = int(input("Number of rules: "))
print("Enter CFG:")
for i in range(n):
    s = input()
    if s[0] not in CFG:
        CFG[s[0]] = []
    CFG[s[0]].append(''.join(s[2:-1].split(',')))  # Parse and store the grammar rules

pda = PDA() 
#this transactions are neede in any type of cfg:
pda.new_state("q0")
pda.new_state("q1")
pda.add_transition("q0", "λ", "λ", "q1", "Z")  # Transition to push stack symbol Z
pda.new_state("q2")
state_num = 3
pda.add_transition("q1", "λ", "λ", "q2", "a")  # Transition to push stack symbol a

# Extract input alphabet from the grammar
for st, to in CFG.items():
    for k in to:
        for char in k:
            if char.isalpha() and char.lower() == char:
                pda.sigma.add(char)

# Add transitions for input symbols
for i in pda.sigma:
    pda.add_transition("q2", i, i, "q2", "λ")  # Consume the input symbol 

# Add transitions based on grammar productions
for variable in CFG.keys():
    for production in CFG[variable]:
        last = ""
        reversed_production = reversed(production) #you should add them in reversed in stack bc stack is FILO
        pda.new_state(f"q{state_num}")
        pda.add_transition("q2", "λ", variable, f"q{state_num}", "λ") #add transition if we see variable to reach their rules
        last = f"q{state_num}"
        state_num += 1
        for symbol in reversed_production:
            pda.new_state(f"q{state_num}")
            pda.add_transition(last, "λ", "λ", f"q{state_num}", symbol) #add a cycle for each rule
            last = f"q{state_num}"
            state_num += 1

        pda.new_state(f"q{state_num}")
        pda.add_transition(last, "λ", "λ", "q2", "λ") #transition to reach q2 from each last node of each cycle
        state_num += 1

# Create the final state and the transition to it
pda.new_state(f"q{state_num}")
pda.add_transition("q2", "λ", "Z", f"q{state_num}", "λ")
pda.final_state = f"q{state_num}"
pda.start_state = "q0"

output(pda)