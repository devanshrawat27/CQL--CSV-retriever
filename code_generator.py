"""
Code Generator for CSV Query Language
Generates executable Python code from AST
"""

from ast_nodes import *
from typing import List, Set


class PythonCodeGenerator:
    def __init__(self, query: SelectQuery):
        self.query = query
        self.indent_level = 0
        self.code_lines: List[str] = []
        self.used_variables: Set[str] = set()
    
    def indent(self) -> str:
        """Get current indentation"""
        return "    " * self.indent_level
    
    def add_line(self, line: str = ""):
        """Add a line of code"""
        if line:
            self.code_lines.append(self.indent() + line)
        else:
            self.code_lines.append("")
    
    def generate(self) -> str:
        """Generate complete Python code"""
        self.code_lines = []
        
        # Add imports
        self.add_line("import csv")
        self.add_line("import sys")
        self.add_line("from collections import defaultdict")
        self.add_line()
        
        # Generate main function
        self.add_line("def execute_query():")
        self.indent_level += 1
        
        # Generate query execution code
        if self.query.group_by:
            self.generate_grouped_query()
        else:
            self.generate_simple_query()
        
        self.indent_level -= 1
        self.add_line()
        
        # Add main execution
        self.add_line("if __name__ == '__main__':")
        self.indent_level += 1
        self.add_line("execute_query()")
        self.indent_level -= 1
        
        return "\n".join(self.code_lines)
    
    def generate_simple_query(self):
        """Generate code for queries without GROUP BY"""
        
        # Open CSV file
        self.add_line(f"with open('{self.query.from_table}', 'r', encoding='utf-8') as f:")
        self.indent_level += 1
        self.add_line("reader = csv.DictReader(f)")
        self.add_line("results = []")
        self.add_line()
        
        # Process each row
        self.add_line("for row in reader:")
        self.indent_level += 1
        
        # Generate WHERE clause
        if self.query.where:
            where_code = self.generate_expression(self.query.where)
            self.add_line(f"if {where_code}:")
            self.indent_level += 1
        
        # Handle SELECT *
        if len(self.query.columns) == 1 and isinstance(self.query.columns[0].expr, Identifier):
            if self.query.columns[0].expr.name == '*':
                self.add_line("results.append(dict(row))")
                self.indent_level -= 1
                if self.query.where:
                    self.indent_level -= 1
                self.indent_level -= 1
                self.generate_output_code()
                return
        
        # Generate SELECT columns
        self.add_line("result_row = {")
        self.indent_level += 1
        
        for i, col_ref in enumerate(self.query.columns):
            col_name = col_ref.alias if col_ref.alias else self.get_column_name(col_ref.expr)
            col_expr = self.generate_expression(col_ref.expr)
            comma = "," if i < len(self.query.columns) - 1 else ""
            self.add_line(f"'{col_name}': {col_expr}{comma}")
        
        self.indent_level -= 1
        self.add_line("}")
        self.add_line("results.append(result_row)")
        
        # Close WHERE if block
        if self.query.where:
            self.indent_level -= 1
        
        # Close for loop
        self.indent_level -= 1
        
        # Close file
        self.indent_level -= 1
        self.add_line()
        
        # Generate output code
        self.generate_output_code()
    
    def generate_grouped_query(self):
        """Generate code for queries with GROUP BY"""
        
        # Open CSV file
        self.add_line(f"with open('{self.query.from_table}', 'r', encoding='utf-8') as f:")
        self.indent_level += 1
        self.add_line("reader = csv.DictReader(f)")
        self.add_line()
        
        # Create group storage
        self.add_line("# Group data")
        self.add_line("groups = defaultdict(list)")
        self.add_line()
        
        # Process each row and group
        self.add_line("for row in reader:")
        self.indent_level += 1
        
        # Generate WHERE clause
        if self.query.where:
            where_code = self.generate_expression(self.query.where)
            self.add_line(f"if {where_code}:")
            self.indent_level += 1
        
        # Generate group key
        group_key_parts = []
        for expr in self.query.group_by:
            group_key_parts.append(self.generate_expression(expr))
        
        group_key = ", ".join(group_key_parts)
        if len(group_key_parts) == 1:
            self.add_line(f"key = ({group_key},)")
        else:
            self.add_line(f"key = ({group_key})")
        self.add_line("groups[key].append(row)")
        
        # Close WHERE if block
        if self.query.where:
            self.indent_level -= 1
        
        # Close for loop
        self.indent_level -= 1
        
        # Close file
        self.indent_level -= 1
        self.add_line()
        
        # Process groups and compute aggregates
        self.add_line("# Compute aggregates for each group")
        self.add_line("results = []")
        self.add_line()
        self.add_line("for key, group_rows in groups.items():")
        self.indent_level += 1
        
        # Unpack group key
        group_vars = [f"group_val_{i}" for i in range(len(self.query.group_by))]
        if len(group_vars) == 1:
            self.add_line(f"{group_vars[0]} = key[0]")
        else:
            self.add_line(f"{', '.join(group_vars)} = key")
        self.add_line()
        
        # Generate aggregate computations
        self.generate_aggregate_computations()
        self.add_line()
        
        # Generate HAVING clause
        if self.query.having:
            having_code = self.generate_aggregate_expression(self.query.having)
            self.add_line(f"if {having_code}:")
            self.indent_level += 1
        
        # Build result row
        self.add_line("result_row = {")
        self.indent_level += 1
        
        for i, col_ref in enumerate(self.query.columns):
            col_name = col_ref.alias if col_ref.alias else self.get_column_name(col_ref.expr)
            col_expr = self.generate_aggregate_expression(col_ref.expr)
            comma = "," if i < len(self.query.columns) - 1 else ""
            self.add_line(f"'{col_name}': {col_expr}{comma}")
        
        self.indent_level -= 1
        self.add_line("}")
        self.add_line("results.append(result_row)")
        
        # Close HAVING if block
        if self.query.having:
            self.indent_level -= 1
        
        # Close for loop
        self.indent_level -= 1
        self.add_line()
        
        # Generate output code
        self.generate_output_code()
    
    def generate_aggregate_computations(self):
        """Generate code to compute aggregate values"""
        aggregates = self.collect_aggregates(self.query)
        
        for i, agg in enumerate(aggregates):
            func_name = agg.name
            var_name = f"agg_{i}"
            
            if func_name == 'COUNT':
                if agg.args and isinstance(agg.args[0], Identifier) and agg.args[0].name == '*':
                    self.add_line(f"{var_name} = len(group_rows)")
                else:
                    arg_expr = self.generate_expression(agg.args[0])
                    self.add_line(f"{var_name} = sum(1 for row in group_rows if {arg_expr} is not None)")
            
            elif func_name == 'SUM':
                arg_expr = self.generate_expression(agg.args[0])
                self.add_line(f"{var_name} = sum(float({arg_expr}) for row in group_rows)")
            
            elif func_name == 'AVG':
                arg_expr = self.generate_expression(agg.args[0])
                self.add_line(f"_values = [float({arg_expr}) for row in group_rows]")
                self.add_line(f"{var_name} = sum(_values) / len(_values) if _values else 0")
            
            elif func_name == 'MIN':
                arg_expr = self.generate_expression(agg.args[0])
                self.add_line(f"_values = [float({arg_expr}) for row in group_rows]")
                self.add_line(f"{var_name} = min(_values) if _values else None")
            
            elif func_name == 'MAX':
                arg_expr = self.generate_expression(agg.args[0])
                self.add_line(f"_values = [float({arg_expr}) for row in group_rows]")
                self.add_line(f"{var_name} = max(_values) if _values else None")
    
    def collect_aggregates(self, query: SelectQuery) -> List[FunctionCall]:
        """Collect all aggregate function calls in the query"""
        aggregates = []
        
        for col_ref in query.columns:
            aggregates.extend(self.find_aggregates(col_ref.expr))
        
        if query.having:
            aggregates.extend(self.find_aggregates(query.having))
        
        if query.order_by:
            for order in query.order_by:
                aggregates.extend(self.find_aggregates(order.expr))
        
        # Remove duplicates while preserving order
        seen = set()
        unique_aggs = []
        for agg in aggregates:
            agg_str = f"{agg.name}({','.join(str(a) for a in agg.args)})"
            if agg_str not in seen:
                seen.add(agg_str)
                unique_aggs.append(agg)
        
        return unique_aggs
    
    def find_aggregates(self, expr: ASTNode) -> List[FunctionCall]:
        """Find all aggregate functions in an expression"""
        aggregates = []
        
        if isinstance(expr, FunctionCall) and expr.is_aggregate:
            aggregates.append(expr)
        elif isinstance(expr, BinaryOperation):
            aggregates.extend(self.find_aggregates(expr.left))
            aggregates.extend(self.find_aggregates(expr.right))
        elif isinstance(expr, UnaryOperation):
            aggregates.extend(self.find_aggregates(expr.operand))
        
        return aggregates
    
    def generate_aggregate_expression(self, expr: ASTNode) -> str:
        """Generate code for expressions in GROUP BY context (with aggregates)"""
        if isinstance(expr, FunctionCall) and expr.is_aggregate:
            # Find the aggregate index
            aggregates = self.collect_aggregates(self.query)
            for i, agg in enumerate(aggregates):
                if (agg.name == expr.name and 
                    len(agg.args) == len(expr.args)):
                    # Simple comparison - could be more sophisticated
                    return f"agg_{i}"
            return "None"
        
        elif isinstance(expr, Identifier):
            # Check if it's a GROUP BY column
            for i, group_expr in enumerate(self.query.group_by):
                if isinstance(group_expr, Identifier) and group_expr.name == expr.name:
                    return f"group_val_{i}"
            return self.generate_expression(expr)
        
        elif isinstance(expr, BinaryOperation):
            left = self.generate_aggregate_expression(expr.left)
            right = self.generate_aggregate_expression(expr.right)
            return f"({left} {expr.op.value} {right})"
        
        elif isinstance(expr, UnaryOperation):
            operand = self.generate_aggregate_expression(expr.operand)
            if expr.op == UnaryOp.NOT:
                return f"not ({operand})"
            else:
                return f"-({operand})"
        
        return self.generate_expression(expr)
    
    def generate_output_code(self):
        """Generate code for sorting, limiting, and outputting results"""
        
        # Apply DISTINCT
        if self.query.distinct:
            self.add_line("# Remove duplicates")
            self.add_line("seen = set()")
            self.add_line("unique_results = []")
            self.add_line("for row in results:")
            self.indent_level += 1
            self.add_line("row_tuple = tuple(sorted(row.items()))")
            self.add_line("if row_tuple not in seen:")
            self.indent_level += 1
            self.add_line("seen.add(row_tuple)")
            self.add_line("unique_results.append(row)")
            self.indent_level -= 1
            self.indent_level -= 1
            self.add_line("results = unique_results")
            self.add_line()
        
        # Apply ORDER BY
        if self.query.order_by:
            self.add_line("# Sort results")
            
            # Build sort key function
            sort_keys = []
            for order in self.query.order_by:
                col_name = self.get_column_name(order.expr)
                reverse = not order.ascending
                sort_keys.append((col_name, reverse))
            
            # Multi-column sort
            for col_name, reverse in reversed(sort_keys):
                self.add_line(f"results.sort(key=lambda x: float(x.get('{col_name}', 0) or 0), reverse={reverse})")
            self.add_line()
        
        # Apply LIMIT
        if self.query.limit is not None:
            self.add_line(f"# Apply LIMIT")
            self.add_line(f"results = results[:{self.query.limit}]")
            self.add_line()
        
        # Output results
        self.add_line("# Output results")
        self.add_line("if results:")
        self.indent_level += 1
        self.add_line("# Print header")
        self.add_line("headers = list(results[0].keys())")
        self.add_line("print(','.join(headers))")
        self.add_line()
        self.add_line("# Print rows")
        self.add_line("for row in results:")
        self.indent_level += 1
        self.add_line("values = [str(row.get(h, '')) for h in headers]")
        self.add_line("print(','.join(values))")
        self.indent_level -= 1
        self.indent_level -= 1
        self.add_line("else:")
        self.indent_level += 1
        self.add_line("print('No results found')")
        self.indent_level -= 1
    
    def generate_expression(self, expr: ASTNode) -> str:
        """Generate Python code for an expression"""
        
        if isinstance(expr, Number):
            return str(expr.value)
        
        elif isinstance(expr, String):
            return f"'{expr.value}'"
        
        elif isinstance(expr, Identifier):
            return f"row.get('{expr.name}', '')"
        
        elif isinstance(expr, BinaryOperation):
            left = self.generate_expression(expr.left)
            right = self.generate_expression(expr.right)
            
            if expr.op == BinaryOp.AND:
                return f"({left} and {right})"
            elif expr.op == BinaryOp.OR:
                return f"({left} or {right})"
            elif expr.op == BinaryOp.EQUALS:
                return f"(str({left}) == str({right}))"
            elif expr.op == BinaryOp.NOT_EQUALS:
                return f"(str({left}) != str({right}))"
            elif expr.op in (BinaryOp.LESS_THAN, BinaryOp.GREATER_THAN, 
                           BinaryOp.LESS_EQUAL, BinaryOp.GREATER_EQUAL):
                # Try numeric comparison
                return f"(float({left} or 0) {expr.op.value} float({right} or 0))"
            else:
                return f"(float({left} or 0) {expr.op.value} float({right} or 0))"
        
        elif isinstance(expr, UnaryOperation):
            operand = self.generate_expression(expr.operand)
            if expr.op == UnaryOp.NOT:
                return f"not ({operand})"
            else:  # NEGATE
                return f"-({operand})"
        
        elif isinstance(expr, FunctionCall):
            if expr.name == 'UPPER':
                arg = self.generate_expression(expr.args[0])
                return f"str({arg}).upper()"
            elif expr.name == 'LOWER':
                arg = self.generate_expression(expr.args[0])
                return f"str({arg}).lower()"
            else:
                # This shouldn't happen in non-grouped queries
                return "None"
        
        return "None"
    
    def get_column_name(self, expr: ASTNode) -> str:
        """Get a display name for a column expression"""
        if isinstance(expr, Identifier):
            return expr.name
        elif isinstance(expr, FunctionCall):
            return expr.name.lower()
        else:
            return "expr"


if __name__ == "__main__":
    from parser import parse_query
    
    # Test code generator
    test_query = """
    SELECT name, age, salary
    FROM employees.csv
    WHERE age > 30 AND department = 'Engineering'
    ORDER BY salary DESC
    LIMIT 5
    """
    
    ast = parse_query(test_query)
    generator = PythonCodeGenerator(ast)
    code = generator.generate()
    
    print("Generated Python Code:")
    print("=" * 60)
    print(code)
