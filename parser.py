"""
Parser for CSV Query Language
Converts tokens into an Abstract Syntax Tree (AST)
"""

from typing import List, Optional
from lexer import Token, TokenType, Lexer
from ast_nodes import *


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0] if tokens else None
    
    def error(self, msg: str):
        if self.current_token:
            raise Exception(
                f"Parser error at line {self.current_token.line}, "
                f"column {self.current_token.column}: {msg}"
            )
        raise Exception(f"Parser error: {msg}")
    
    def advance(self):
        """Move to next token"""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
    
    def peek(self, offset=1):
        """Look ahead at token without advancing"""
        peek_pos = self.pos + offset
        if peek_pos < len(self.tokens):
            return self.tokens[peek_pos]
        return None
    
    def expect(self, token_type: TokenType) -> Token:
        """Consume token of expected type or error"""
        if self.current_token is None:
            self.error(f"Expected {token_type.name} but reached end of input")
        if self.current_token.type != token_type:
            self.error(
                f"Expected {token_type.name} but got {self.current_token.type.name}"
            )
        token = self.current_token
        self.advance()
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any of the given types"""
        if self.current_token is None:
            return False
        return self.current_token.type in token_types
    
    def parse(self) -> SelectQuery:
        """Parse a SELECT query"""
        return self.parse_select_query()
    
    def parse_select_query(self) -> SelectQuery:
        """Parse: SELECT ... FROM ... [WHERE ...] [GROUP BY ...] [ORDER BY ...] [LIMIT ...]"""
        
        # SELECT keyword
        self.expect(TokenType.SELECT)
        
        # Check for DISTINCT
        distinct = False
        if self.match(TokenType.DISTINCT):
            distinct = True
            self.advance()
        
        # Parse column list
        columns = self.parse_column_list()
        
        # FROM clause
        self.expect(TokenType.FROM)
        from_table = self.expect(TokenType.IDENTIFIER).value
        
        # Handle file extensions (e.g., .csv, .tsv)
        if self.match(TokenType.DOT):
            self.advance()
            extension = self.expect(TokenType.IDENTIFIER).value
            from_table = f"{from_table}.{extension}"
        
        # Optional WHERE clause
        where = None
        if self.match(TokenType.WHERE):
            self.advance()
            where = self.parse_expression()
        
        # Optional GROUP BY clause
        group_by = None
        if self.match(TokenType.GROUP):
            self.advance()
            self.expect(TokenType.BY)
            group_by = self.parse_expression_list()
        
        # Optional HAVING clause
        having = None
        if self.match(TokenType.HAVING):
            self.advance()
            having = self.parse_expression()
        
        # Optional ORDER BY clause
        order_by = None
        if self.match(TokenType.ORDER):
            self.advance()
            self.expect(TokenType.BY)
            order_by = self.parse_order_by_list()
        
        # Optional LIMIT clause
        limit = None
        if self.match(TokenType.LIMIT):
            self.advance()
            limit = self.expect(TokenType.NUMBER).value
            if not isinstance(limit, int):
                self.error("LIMIT must be an integer")
        
        # Expect EOF
        self.expect(TokenType.EOF)
        
        return SelectQuery(
            columns=columns,
            from_table=from_table,
            where=where,
            group_by=group_by,
            having=having,
            order_by=order_by,
            limit=limit,
            distinct=distinct
        )
    
    def parse_column_list(self) -> List[ColumnRef]:
        """Parse: column1 [AS alias], column2, ..."""
        columns = []
        
        while True:
            # Check for SELECT *
            if self.match(TokenType.MULTIPLY):
                self.advance()
                columns.append(ColumnRef(expr=Identifier('*'), alias=None))
                break
            
            # Parse expression
            expr = self.parse_expression()
            
            # Check for AS alias
            alias = None
            if self.match(TokenType.AS):
                self.advance()
                alias = self.expect(TokenType.IDENTIFIER).value
            
            columns.append(ColumnRef(expr=expr, alias=alias))
            
            # Check for comma (more columns)
            if not self.match(TokenType.COMMA):
                break
            self.advance()
        
        return columns
    
    def parse_expression_list(self) -> List[ASTNode]:
        """Parse: expr1, expr2, ..."""
        expressions = []
        
        while True:
            expressions.append(self.parse_expression())
            
            if not self.match(TokenType.COMMA):
                break
            self.advance()
        
        return expressions
    
    def parse_order_by_list(self) -> List[OrderByClause]:
        """Parse: expr1 [ASC|DESC], expr2 [ASC|DESC], ..."""
        order_clauses = []
        
        while True:
            expr = self.parse_expression()
            
            # Check for ASC/DESC
            ascending = True
            if self.match(TokenType.DESC):
                ascending = False
                self.advance()
            elif self.match(TokenType.ASC):
                self.advance()
            
            order_clauses.append(OrderByClause(expr=expr, ascending=ascending))
            
            if not self.match(TokenType.COMMA):
                break
            self.advance()
        
        return order_clauses
    
    def parse_expression(self) -> ASTNode:
        """Parse expression with operator precedence"""
        return self.parse_or_expression()
    
    def parse_or_expression(self) -> ASTNode:
        """Parse: expr OR expr OR ..."""
        left = self.parse_and_expression()
        
        while self.match(TokenType.OR):
            self.advance()
            right = self.parse_and_expression()
            left = BinaryOperation(left=left, op=BinaryOp.OR, right=right)
        
        return left
    
    def parse_and_expression(self) -> ASTNode:
        """Parse: expr AND expr AND ..."""
        left = self.parse_comparison_expression()
        
        while self.match(TokenType.AND):
            self.advance()
            right = self.parse_comparison_expression()
            left = BinaryOperation(left=left, op=BinaryOp.AND, right=right)
        
        return left
    
    def parse_comparison_expression(self) -> ASTNode:
        """Parse: expr = expr, expr > expr, etc."""
        left = self.parse_additive_expression()
        
        comparison_ops = {
            TokenType.EQUALS: BinaryOp.EQUALS,
            TokenType.NOT_EQUALS: BinaryOp.NOT_EQUALS,
            TokenType.LESS_THAN: BinaryOp.LESS_THAN,
            TokenType.GREATER_THAN: BinaryOp.GREATER_THAN,
            TokenType.LESS_EQUAL: BinaryOp.LESS_EQUAL,
            TokenType.GREATER_EQUAL: BinaryOp.GREATER_EQUAL,
        }
        
        if self.match(*comparison_ops.keys()):
            op_token = self.current_token
            self.advance()
            right = self.parse_additive_expression()
            left = BinaryOperation(
                left=left,
                op=comparison_ops[op_token.type],
                right=right
            )
        
        return left
    
    def parse_additive_expression(self) -> ASTNode:
        """Parse: expr + expr, expr - expr"""
        left = self.parse_multiplicative_expression()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op_token = self.current_token
            self.advance()
            right = self.parse_multiplicative_expression()
            op = BinaryOp.ADD if op_token.type == TokenType.PLUS else BinaryOp.SUBTRACT
            left = BinaryOperation(left=left, op=op, right=right)
        
        return left
    
    def parse_multiplicative_expression(self) -> ASTNode:
        """Parse: expr * expr, expr / expr"""
        left = self.parse_unary_expression()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE):
            op_token = self.current_token
            self.advance()
            right = self.parse_unary_expression()
            op = BinaryOp.MULTIPLY if op_token.type == TokenType.MULTIPLY else BinaryOp.DIVIDE
            left = BinaryOperation(left=left, op=op, right=right)
        
        return left
    
    def parse_unary_expression(self) -> ASTNode:
        """Parse: NOT expr, -expr"""
        if self.match(TokenType.NOT):
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOperation(op=UnaryOp.NOT, operand=operand)
        
        if self.match(TokenType.MINUS):
            self.advance()
            operand = self.parse_unary_expression()
            return UnaryOperation(op=UnaryOp.NEGATE, operand=operand)
        
        return self.parse_primary_expression()
    
    def parse_primary_expression(self) -> ASTNode:
        """Parse: literals, identifiers, function calls, parenthesized expressions"""
        
        # Number literal
        if self.match(TokenType.NUMBER):
            value = self.current_token.value
            self.advance()
            return Number(value)
        
        # String literal
        if self.match(TokenType.STRING):
            value = self.current_token.value
            self.advance()
            return String(value)
        
        # Parenthesized expression
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        # Function calls and identifiers
        if self.match(TokenType.IDENTIFIER, TokenType.COUNT, TokenType.SUM, 
                      TokenType.AVG, TokenType.MIN, TokenType.MAX,
                      TokenType.UPPER, TokenType.LOWER):
            
            name_token = self.current_token
            name = name_token.value if name_token.type == TokenType.IDENTIFIER else name_token.type.name
            self.advance()
            
            # Check if it's a function call
            if self.match(TokenType.LPAREN):
                self.advance()
                
                # Parse arguments
                args = []
                if not self.match(TokenType.RPAREN):
                    # Special case: COUNT(*)
                    if name.upper() == 'COUNT' and self.match(TokenType.MULTIPLY):
                        self.advance()
                        args.append(Identifier('*'))
                    else:
                        args = self.parse_expression_list()
                
                self.expect(TokenType.RPAREN)
                
                # Determine if it's an aggregate function
                is_aggregate = name.upper() in ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX']
                
                return FunctionCall(name=name.upper(), args=args, is_aggregate=is_aggregate)
            
            # Just an identifier
            return Identifier(name)
        
        self.error(f"Unexpected token: {self.current_token.type.name}")


def parse_query(query_string: str) -> SelectQuery:
    """Convenience function to parse a query string"""
    lexer = Lexer(query_string)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    return parser.parse()


if __name__ == "__main__":
    # Test the parser
    test_query = """
    SELECT name, age, SUM(salary) as total_salary
    FROM employees.csv
    WHERE age > 30 AND department = 'Engineering'
    GROUP BY name, age
    HAVING SUM(salary) > 100000
    ORDER BY total_salary DESC
    LIMIT 10
    """
    
    ast = parse_query(test_query)
    print("Abstract Syntax Tree:")
    print(ast_to_string(ast))
