"""
Semantic Analyzer for CSV Query Language
Validates queries and performs type checking
"""

import csv
from typing import Set, Dict, List, Optional
from ast_nodes import *
from pathlib import Path


class SemanticAnalyzer:
    def __init__(self, query: SelectQuery, csv_path: Optional[str] = None):
        self.query = query
        self.csv_path = csv_path
        self.available_columns: Set[str] = set()
        self.has_aggregates = False
        self.non_aggregate_columns: Set[str] = set()
        self.errors: List[str] = []
        
        # Load CSV headers if path provided
        if csv_path:
            self.load_csv_headers(csv_path)
    
    def load_csv_headers(self, csv_path: str):
        """Load column names from CSV file"""
        try:
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                if headers:
                    self.available_columns = set(headers)
        except FileNotFoundError:
            self.errors.append(f"CSV file not found: {csv_path}")
        except Exception as e:
            self.errors.append(f"Error reading CSV file: {e}")
    
    def analyze(self) -> bool:
        """Run semantic analysis on the query"""
        self.errors = []
        
        # Check if we have column information
        if not self.available_columns and self.csv_path:
            # Already tried to load, but failed
            return False
        
        # Analyze SELECT columns
        self.analyze_select_columns()
        
        # Analyze WHERE clause
        if self.query.where:
            self.analyze_expression(self.query.where, allow_aggregates=False)
        
        # Analyze GROUP BY
        if self.query.group_by:
            self.analyze_group_by()
        
        # Analyze HAVING clause
        if self.query.having:
            if not self.query.group_by:
                self.errors.append("HAVING clause requires GROUP BY")
            self.analyze_expression(self.query.having, allow_aggregates=True)
        
        # Analyze ORDER BY
        if self.query.order_by:
            for order_clause in self.query.order_by:
                self.analyze_expression(order_clause.expr, allow_aggregates=self.has_aggregates)
        
        # Check GROUP BY constraints
        if self.query.group_by:
            self.validate_group_by_constraints()
        
        return len(self.errors) == 0
    
    def analyze_select_columns(self):
        """Analyze SELECT column list"""
        for col_ref in self.query.columns:
            # Check for SELECT *
            if isinstance(col_ref.expr, Identifier) and col_ref.expr.name == '*':
                if len(self.query.columns) > 1:
                    self.errors.append("Cannot mix * with other columns in SELECT")
                if self.query.group_by:
                    self.errors.append("Cannot use SELECT * with GROUP BY")
                continue
            
            self.analyze_expression(col_ref.expr, allow_aggregates=True)
    
    def analyze_group_by(self):
        """Analyze GROUP BY clause"""
        for expr in self.query.group_by:
            if self.contains_aggregate(expr):
                self.errors.append("GROUP BY cannot contain aggregate functions")
            self.analyze_expression(expr, allow_aggregates=False)
    
    def validate_group_by_constraints(self):
        """Validate that non-aggregate columns in SELECT are in GROUP BY"""
        if not self.query.group_by:
            return
        
        # Get columns referenced in GROUP BY
        group_by_columns = set()
        for expr in self.query.group_by:
            group_by_columns.update(self.get_column_references(expr))
        
        # Check each SELECT column
        for col_ref in self.query.columns:
            if isinstance(col_ref.expr, Identifier) and col_ref.expr.name == '*':
                continue
            
            # If it's not an aggregate, it must be in GROUP BY
            if not self.contains_aggregate(col_ref.expr):
                col_refs = self.get_column_references(col_ref.expr)
                for col in col_refs:
                    if col not in group_by_columns:
                        self.errors.append(
                            f"Column '{col}' must appear in GROUP BY clause or be used in aggregate function"
                        )
    
    def analyze_expression(self, expr: ASTNode, allow_aggregates: bool):
        """Analyze an expression"""
        if isinstance(expr, Number) or isinstance(expr, String):
            pass  # Literals are always valid
        
        elif isinstance(expr, Identifier):
            # Check if column exists (if we have column info)
            if self.available_columns and expr.name != '*':
                if expr.name not in self.available_columns:
                    self.errors.append(f"Unknown column: {expr.name}")
        
        elif isinstance(expr, BinaryOperation):
            self.analyze_expression(expr.left, allow_aggregates)
            self.analyze_expression(expr.right, allow_aggregates)
        
        elif isinstance(expr, UnaryOperation):
            self.analyze_expression(expr.operand, allow_aggregates)
        
        elif isinstance(expr, FunctionCall):
            if expr.is_aggregate:
                self.has_aggregates = True
                if not allow_aggregates:
                    self.errors.append(
                        f"Aggregate function {expr.name} not allowed in this context"
                    )
            
            # Analyze function arguments
            for arg in expr.args:
                # Aggregates can't contain aggregates
                self.analyze_expression(arg, allow_aggregates=False)
    
    def contains_aggregate(self, expr: ASTNode) -> bool:
        """Check if expression contains aggregate functions"""
        if isinstance(expr, FunctionCall):
            return expr.is_aggregate
        
        elif isinstance(expr, BinaryOperation):
            return self.contains_aggregate(expr.left) or self.contains_aggregate(expr.right)
        
        elif isinstance(expr, UnaryOperation):
            return self.contains_aggregate(expr.operand)
        
        return False
    
    def get_column_references(self, expr: ASTNode) -> Set[str]:
        """Get all column references in an expression"""
        columns = set()
        
        if isinstance(expr, Identifier):
            if expr.name != '*':
                columns.add(expr.name)
        
        elif isinstance(expr, BinaryOperation):
            columns.update(self.get_column_references(expr.left))
            columns.update(self.get_column_references(expr.right))
        
        elif isinstance(expr, UnaryOperation):
            columns.update(self.get_column_references(expr.operand))
        
        elif isinstance(expr, FunctionCall):
            for arg in expr.args:
                columns.update(self.get_column_references(arg))
        
        return columns
    
    def get_errors(self) -> List[str]:
        """Get list of semantic errors"""
        return self.errors
    
    def print_errors(self):
        """Print all semantic errors"""
        if self.errors:
            print("Semantic Errors:")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        else:
            print("No semantic errors found.")


if __name__ == "__main__":
    from parser import parse_query
    
    # Test semantic analyzer
    test_query = """
    SELECT name, SUM(salary) as total
    FROM employees.csv
    WHERE age > 30
    GROUP BY name
    ORDER BY total DESC
    """
    
    ast = parse_query(test_query)
    
    # Analyze without CSV file
    analyzer = SemanticAnalyzer(ast)
    if analyzer.analyze():
        print("✓ Query is semantically valid")
    else:
        analyzer.print_errors()
