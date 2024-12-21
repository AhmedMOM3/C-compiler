import string

non_terminals=set(string.ascii_uppercase[0:26])
terminals =set(string.ascii_lowercase[0:26])


def parse_string(rules, sequence, sel_set):
    stack = ['S']
    lenght= len(sequence)
    i=0
    while (i<lenght):
        if (len(stack)==0):
            return False, stack, i
        if (stack[-1] not in non_terminals and sequence[i] not in non_terminals):
            stack.pop()
            i+=1
            continue
        elif (stack[-1] in non_terminals and sequence[i] not in non_terminals):
            if (stack[-1] == "S" and sequence[i]== sel_set[0][0]):
                stack.pop()
                alph_dach_a = rules[0][::-1]
                stack.extend(alph_dach_a)
            elif (stack[-1] == "S" and sequence[i]== sel_set[1][0]):
                stack.pop()
                alph_dach_a = rules[1][::-1]
                stack.extend(alph_dach_a)
            elif (stack[-1] == "B" and sequence[i]== sel_set[2][0]):
                stack.pop()
                alph_dach_a = rules[2][::-1]
                stack.extend(alph_dach_a)
            elif (stack[-1] == "B" and sequence[i]== sel_set[3][0]):
                stack.pop()
                alph_dach_a = rules[3][::-1]
                stack.extend(alph_dach_a)
            else:
                return False, stack, i
    if (len(stack)==0):
        return True, stack, i
    else:
        return False, stack, i
        

def is_simple_grammar(rules):
    try:
        sel_set=[]
        for rule in rules:
            if (rule[0] not in non_terminals):
               sel_set.append(rule[0])
            else:
                return False, sel_set
        if (sel_set[0]!=sel_set[1] and sel_set[2]!=sel_set[3] ):
            return True, sel_set
        else:
            return False, sel_set
    except:
        return False,0


def main():
    while True:
        print("Recursive Descent Parsing For The Following Grammar\nEnter the grammar rules for the non-terminals.\nWe will start with 'S', make sure the other one is 'B' ")
        print( "👉grammers👈".center(40))
        rules = []
        print("Enter rule number one for non-terminal 'S': ",end="")
        rule1 = input().strip()
        rules.append(rule1)
        
        print("Enter rule number two for non-terminal 'S': ", end="")
        rule2 = input().strip()
        rules.append(rule2)
        
        print(f"Enter rule number one for non-terminal 'B': ", end="")
        rule3 = input().strip()
        rules.append(rule3)
        
        print(f"Enter rule number two for non-terminal 'B': ", end="")
        rule4 = input().strip()
        rules.append(rule4)
        
        
        is_simple, sel_set = is_simple_grammar(rules)
        
        if not is_simple:
            print("The grammar is not simple. Please enter a simple grammar.")
            print("===========================================================")
            continue
     
        
        while True:
            choice=4
            print("\nthis grammar is simple, Enter the string to be checked: ", end="")
            string = input().strip()
            print("-> The input string: " ,list(string))
            accepted, stack, i =parse_string(rules, string,sel_set)
            if accepted:
                print("-> Your input string is Accepted.")
                print("-> The Stack at the end: ", stack)
                print("-> The rest of unchecked string: ", string[i:])
            else:
                print("-> Your input string is Rejected.")
                print("-> The Stack at the end: ", stack)
                print("-> The rest of unchecked string: ", list(string[i:]))
            
            print("\n1-Another Grammar.")
            print("2-Another String.")
            print("3-Exit")
            choice = input("Enter your choice: ").strip()
            while(True):
                if (choice not in ['1','2','3']):
                    print("please enter a valid choice.")
                    choice = input("Enter your choice: ").strip()
                else:
                    break
            
            print("----------------------------")
            if choice == '1':
                break
            elif choice == '3':
                return
           
            

if __name__ == "__main__":
    main()
