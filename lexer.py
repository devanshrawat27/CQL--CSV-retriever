"""
Lexer for CSV Query Language
Tokenizes SQL-like queries into tokens for parsing
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Keywords
    SELECT = auto()
    FROM = auto()
    WHERE = auto()
    GROUP = auto()
    BY = auto()
    ORDER = auto()
    HAVING = auto()
    LIMIT = auto()
    AS = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    DISTINCT = auto()
    ASC = auto()
    DESC = auto()
    
    # Aggregate functions
    COUNT = auto()
    SUM = auto()
    AVG = auto()
    MIN = auto()
    MAX = auto()
    
    # String functions
    UPPER = auto()
    LOWER = auto()
    
    # Operators
    EQUALS = auto()          # =
    NOT_EQUALS = auto()      # !=
    LESS_THAN = auto()       # <
    GREATER_THAN = auto()    # >
    LESS_EQUAL = auto()      # <=
    GREATER_EQUAL = auto()   # >=
    PLUS = auto()            # +
    MINUS = auto()           # -
    MULTIPLY = auto()        # *
    DIVIDE = auto()          # /
    
    # Delimiters
    COMMA = auto()
    LPAREN = auto()
    RPAREN = auto()
    DOT = auto()
    
    # Literals and identifiers
    IDENTIFIER = auto()
    NUMBER = auto()
    STRING = auto()
    
    # Special
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r})"


class Lexer:
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None
        
        # Keywords mapping
        self.keywords = {
            'SELECT': TokenType.SELECT,
            'FROM': TokenType.FROM,
            'WHERE': TokenType.WHERE,
            'GROUP': TokenType.GROUP,
            'BY': TokenType.BY,
            'ORDER': TokenType.ORDER,
            'HAVING': TokenType.HAVING,
            'LIMIT': TokenType.LIMIT,
            'AS': TokenType.AS,
            'AND': TokenType.AND,
            'OR': TokenType.OR,
            'NOT': TokenType.NOT,
            'DISTINCT': TokenType.DISTINCT,
            'ASC': TokenType.ASC,
            'DESC': TokenType.DESC,
            'COUNT': TokenType.COUNT,
            'SUM': TokenType.SUM,
            'AVG': TokenType.AVG,
            'MIN': TokenType.MIN,
            'MAX': TokenType.MAX,
            'UPPER': TokenType.UPPER,
            'LOWER': TokenType.LOWER,
        }
    
    def error(self, msg: str):
        raise Exception(f"Lexer error at line {self.line}, column {self.column}: {msg}")
    
    def advance(self):
        """Move to next character"""
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset=1):
        """Look ahead at next character without advancing"""
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        """Skip whitespace and comments"""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '-' and self.peek() == '-':
                # Skip SQL-style comments
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
            else:
                break
    
    def read_number(self):
        """Read numeric literal"""
        start_line = self.line
        start_col = self.column
        num_str = ''
        has_dot = False
        
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot:
                    self.error("Invalid number format")
                has_dot = True
            num_str += self.current_char
            self.advance()
        
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER, value, start_line, start_col)
    
    def read_string(self):
        """Read string literal (single or double quoted)"""
        start_line = self.line
        start_col = self.column
        quote_char = self.current_char
        self.advance()  # Skip opening quote
        
        string_value = ''
        while self.current_char is not None and self.current_char != quote_char:
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n':
                    string_value += '\n'
                elif self.current_char == 't':
                    string_value += '\t'
                elif self.current_char == '\\':
                    string_value += '\\'
                elif self.current_char == quote_char:
                    string_value += quote_char
                else:
                    string_value += self.current_char
                self.advance()
            else:
                string_value += self.current_char
                self.advance()
        
        if self.current_char != quote_char:
            self.error("Unterminated string")
        
        self.advance()  # Skip closing quote
        return Token(TokenType.STRING, string_value, start_line, start_col)
    
    def read_identifier(self):
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        identifier = ''
        
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            identifier += self.current_char
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(identifier.upper(), TokenType.IDENTIFIER)
        value = identifier if token_type == TokenType.IDENTIFIER else identifier.upper()
        
        return Token(token_type, value, start_line, start_col)
    
    def get_next_token(self) -> Token:
        """Get next token from input"""
        while self.current_char is not None:
            start_line = self.line
            start_col = self.column
            
            # Skip whitespace
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            # Skip comments
            if self.current_char == '-' and self.peek() == '-':
                self.skip_whitespace()
                continue
            
            # Numbers
            if self.current_char.isdigit():
                return self.read_number()
            
            # Strings
            if self.current_char in ('"', "'"):
                return self.read_string()
            
            # Identifiers and keywords
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_identifier()
            
            # Two-character operators
            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.NOT_EQUALS, '!=', start_line, start_col)
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.LESS_EQUAL, '<=', start_line, start_col)
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col)
            
            # Single-character tokens
            single_char_tokens = {
                '=': TokenType.EQUALS,
                '<': TokenType.LESS_THAN,
                '>': TokenType.GREATER_THAN,
                '+': TokenType.PLUS,
                '-': TokenType.MINUS,
                '*': TokenType.MULTIPLY,
                '/': TokenType.DIVIDE,
                ',': TokenType.COMMA,
                '(': TokenType.LPAREN,
                ')': TokenType.RPAREN,
                '.': TokenType.DOT,
            }
            
            if self.current_char in single_char_tokens:
                char = self.current_char
                token_type = single_char_tokens[char]
                self.advance()
                return Token(token_type, char, start_line, start_col)
            
            self.error(f"Unexpected character: {self.current_char}")
        
        return Token(TokenType.EOF, None, self.line, self.column)
    
    def tokenize(self) -> List[Token]:
        """Tokenize entire input and return list of tokens"""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break
        return tokens


if __name__ == "__main__":
    # Test the lexer
    test_query = """
    SELECT name, age, SUM(salary) as total
    FROM employees.csv
    WHERE age > 30 AND department = 'Engineering'
    GROUP BY name, age
    ORDER BY total DESC
    LIMIT 10
    """
    
    lexer = Lexer(test_query)
    tokens = lexer.tokenize()
    
    print("Tokens:")
    for token in tokens:
        print(f"  {token}")
