class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme

    def __repr__(self):
        return f"Token({self.token_type}, {self.lexeme})"


class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add(self, token):
        self.symbols[token.lexeme] = token.token_type

    def __repr__(self):
        return "\n".join([f"{lexeme}: {token_type}" for lexeme, token_type in self.symbols.items()])


class Parser:
    def __init__(self, input_string):
        self.input_string = input_string
        self.current_index = 0
        self.symbol_table = SymbolTable()

    def parse(self):
        self.symbol_table = SymbolTable()
        success, tree = self.E()
        if success and self.current_index == len(self.input_string):
            print("Input string is accepted.")
            print("Symbol Table:")
            print(self.symbol_table)
            print("Parse Tree:")
            print(tree)
        else:
            print("Input string is not accepted.")

    def match(self, expected):
        if self.current_index < len(self.input_string) and self.input_string[self.current_index] == expected:
            self.current_index += 1
            return True
        return False

    def E(self):
        success, tree = self.T()
        if success:
            success2, tree2 = self.E_prime()
            if success2:
                return True, ["E", tree, tree2]
            else:
                return True, ["E", tree]
        return False, None

    def E_prime(self):
        if self.match('+'):
            success, tree = self.T()
            if success:
                success2, tree2 = self.E_prime()
                if success2:
                    return True, ["E'", "+", tree, tree2]
                else:
                    return True, ["E'", "+", tree]
            return False, None
        return True, []

    def T(self):
        success, tree = self.F()
        if success:
            success2, tree2 = self.T_prime()
            if success2:
                return True, ["T", tree, tree2]
            else:
                return True, ["T", tree]
        return False, None

    def T_prime(self):
        if self.match('*'):
            success, tree = self.F()
            if success:
                success2, tree2 = self.T_prime()
                if success2:
                    return True, ["T'", "*", tree, tree2]
                else:
                    return True, ["T'", "*", tree]
            return False, None
        return True, []

    def F(self):
        if self.match('('):
            success, tree = self.E()
            if success and self.match(')'):
                return True, ["F", "(", tree, ")"]
            return False, None
        elif self.match_id():
            return True, ["F", Token("id", self.input_string[self.current_index - 1])]
        return False, None

    def match_id(self):
        if self.current_index < len(self.input_string) and self.input_string[self.current_index].isalnum():
            self.symbol_table.add(Token("id", self.input_string[self.current_index]))
            self.current_index += 1
            return True
        return False


def main():
    while True:
        input_string = input("Enter an arithmetic expression (or 'exit' to quit): ")
        if input_string.lower() == "exit":
            break
        parser = Parser(input_string)
        parser.parse()


if __name__ == "__main__":
    main()
