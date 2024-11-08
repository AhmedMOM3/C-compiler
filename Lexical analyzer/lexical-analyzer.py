import re
import enum
import os

class TokenType(enum.Enum):
    # Keywords
    KEYWORD = 'KEYWORD'
    # Data types
    INT = 'INT'
    FLOAT = 'FLOAT'
    CHAR = 'CHAR'
    # Identifiers
    IDENTIFIER = 'IDENTIFIER'
    # Literals
    STRING_LITERAL = 'STRING_LITERAL'
    INTEGER_LITERAL = 'INTEGER_LITERAL'
    FLOAT_LITERAL = 'FLOAT_LITERAL'
    # Operators
    ARITHMETIC_OP = 'ARITHMETIC_OP'
    RELATIONAL_OP = 'RELATIONAL_OP'
    LOGICAL_OP = 'LOGICAL_OP'
    BITWISE_OP = 'BITWISE_OP'
    # Punctuators
    PUNCTUATOR = 'PUNCTUATOR'
    # Preprocessor
    PREPROCESSOR = 'PREPROCESSOR'
    # Comments
    COMMENT = 'COMMENT'
    # Error
    ERROR = 'ERROR'

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, '{self.value}', Line: {self.line}, Column: {self.column})"

class Lexer:
    def __init__(self):
        # Keywords
        self.keywords = {
            'int', 'float','double', 'char', 'void', 'return', 'if', 'else', 
            'while', 'for', 'do', 'switch', 'case', 'break', 'continue', 
            'default', 'struct', 'enum', 'static', 'const','printf',
            'auto','extern','goto'
        }
        
        # Token patterns
        self.patterns = [
            # Preprocessor directives
            (r'#\s*include\s*(<[^>]+>|"[^"]+")' , TokenType.PREPROCESSOR),
            
            # Comments (single and multi-line)
            (r'//.*?$', TokenType.COMMENT),
            (r'/\*.*?\*/', TokenType.COMMENT, re.DOTALL),
            
            # String Literals
            (r'"[^"]*"', TokenType.STRING_LITERAL),
            
            # Float Literals (before Integer to catch decimal points)
            (r'\d+\.\d+([eE][+-]?\d+)?', TokenType.FLOAT_LITERAL),
            
            # Integer Literals (decimal, hex, octal)
            (r'0[xX][0-9a-fA-F]+|0[0-7]+|\d+', TokenType.INTEGER_LITERAL),
            
            # Identifiers (must come after literals to prevent false matches)
            (r'[a-zA-Z_][a-zA-Z0-9_]*', TokenType.IDENTIFIER),
            
            # Arithmetic Operators
            (r'\+|\-|\*|/|%|\+\+|--', TokenType.ARITHMETIC_OP),
            
            # Relational Operators
            (r'==|!=|<=|>=|<|>', TokenType.RELATIONAL_OP),
            
            # Logical Operators
            (r'&&|\|\||!', TokenType.LOGICAL_OP),
            
            # Bitwise Operators
            (r'&|\||\^|~|<<|>>', TokenType.BITWISE_OP),
            
            # Punctuators
            (r'[{}\[\]();,.]', TokenType.PUNCTUATOR),
            
            # Assignment Operators
            (r'=|\+=|-=|\*=|/=|%=|&=|\|=|\^=', TokenType.ARITHMETIC_OP),
        ]
        
    
    def tokenize(self, code):
        tokens = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            col = 0
            while col < len(line):
                # Skip whitespace
                match = re.match(r'\s+', line[col:])
                if match:
                    col += len(match.group())
                    continue
                
                # Try each pattern
                matched = False
                for pattern_info in self.patterns:
                    # Handle different pattern formats (with or without flags)
                    if len(pattern_info) == 2:
                        pattern, token_type = pattern_info
                        flags = 0
                    else:
                        pattern, token_type, flags = pattern_info
                    
                    match = re.match(pattern, line[col:], flags)
                    if match:
                        value = match.group()
                        
                        # Special handling for keywords and identifiers
                        if token_type == TokenType.IDENTIFIER:
                            if value in self.keywords:
                                token_type = TokenType.KEYWORD
                        
                        tokens.append(Token(
                            token_type, 
                            value, 
                            line_num, 
                            col + 1
                        ))
                        
                        col += len(value)
                        matched = True
                        break
                
                # If no match found, it's an error
                if not matched:
                    tokens.append(Token(
                        TokenType.ERROR, 
                        line[col], 
                        line_num, 
                        col + 1
                    ))
                    col += 1
        
        return tokens

def interactive_lexer(file_path):
    """
    Interactive lexical analyzer that allows users to input their C code
    and see the tokenization results.
    """
    print("C Lexical Analyzer")
    print("-------------------------------")
    
    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: ", file_path, " file not found.")
        return
    
    # Create lexer and tokenize
    lexer = Lexer()
    try:
        tokens = lexer.tokenize(code)
        
        # Print tokens with formatting
        print("\n--- Tokenization Results ---")
        print(f"Total Tokens: {len(tokens)}")
        print("------------------------------------------------------------------------")
        print("| Line | Column |           Type            |           Value          |")
        print("------------------------------------------------------------------------")
        
        for token in tokens:
            print(f"| {token.line:<4} | {token.column:<6} | {str(token.type).ljust(25):<18} | {token.value:<14} |")
        
        print("------------------------------------------------------------------------")
        
        # Count tokens by type
        token_counts = {}
        for token in tokens:
            token_counts[token.type] = token_counts.get(token.type, 0) + 1
        
        print("\n--- Token Type Summary ---")
        for token_type, count in token_counts.items():
            print(f"{str(token_type).ljust(25)}: {count}")
    
    except Exception as e:
        print(f"Error during tokenization: {e}")

def main():
    interactive_lexer(os.path.join(os.path.dirname(__file__),'input.c'))

if __name__ == "__main__":
    main()
