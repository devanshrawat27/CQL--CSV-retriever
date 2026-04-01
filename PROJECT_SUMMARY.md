# CSV Query Compiler - Project Summary

## Overview

A complete compiler implementation that translates SQL-like queries for CSV files into executable Python code. This project demonstrates all major phases of compiler design: lexical analysis, parsing, semantic analysis, and code generation.

## Project Structure

```
csv_query_compiler/
├── Core Compiler Components
│   ├── lexer.py              # Lexical analyzer (tokenization)
│   ├── parser.py             # Parser (builds AST)
│   ├── ast_nodes.py          # AST node definitions
│   ├── semantic_analyzer.py  # Semantic validation
│   └── code_generator.py     # Python code generation
│
├── Main Program
│   └── compiler.py           # CLI entry point
│
├── Documentation
│   ├── README.md             # Full documentation
│   ├── QUICKSTART.md         # Quick start guide
│   └── PROJECT_SUMMARY.md    # This file
│
├── Examples & Data
│   ├── employees.csv         # Sample data file
│   ├── examples/
│   │   ├── query1.sql        # Simple SELECT with WHERE
│   │   ├── query2.sql        # GROUP BY with aggregates
│   │   └── query3.sql        # Complex with HAVING
│   └── demo.py               # Interactive demo
│
└── Generated Code
    └── (user's generated .py files)
```

## Compiler Architecture

### Phase 1: Lexical Analysis (lexer.py)
**Input:** Query string
**Output:** Token stream
**Features:**
- Recognizes 40+ token types
- Handles keywords, operators, literals, identifiers
- Supports SQL-style comments (--)
- Line and column tracking for error messages

**Example:**
```
"SELECT name FROM data.csv"
↓
[Token(SELECT), Token(IDENTIFIER, 'name'), Token(FROM), Token(IDENTIFIER, 'data'), ...]
```

### Phase 2: Parsing (parser.py)
**Input:** Token stream
**Output:** Abstract Syntax Tree (AST)
**Features:**
- Recursive descent parser
- Operator precedence handling
- Expression parsing with proper precedence
- Error recovery with meaningful messages

**Example:**
```
Tokens: [SELECT, name, FROM, ...]
↓
SelectQuery(
  columns=[ColumnRef(Identifier('name'))],
  from_table='data.csv',
  where=None,
  ...
)
```

### Phase 3: Semantic Analysis (semantic_analyzer.py)
**Input:** AST
**Output:** Validated AST + error list
**Features:**
- Column name validation (if CSV provided)
- GROUP BY constraint checking
- Aggregate function validation
- Type checking for operations
- HAVING clause validation

**Example:**
```
Query: SELECT age FROM data.csv GROUP BY name
        ↓
Error: Column 'age' must appear in GROUP BY or be used in aggregate
```

### Phase 4: Code Generation (code_generator.py)
**Input:** Validated AST
**Output:** Executable Python code
**Features:**
- Efficient Python code generation
- Streaming CSV processing
- Memory-efficient grouping
- Optimized sorting and filtering
- Clean, readable output

**Example:**
```
AST: SelectQuery(...)
↓
Generated Python code with:
- CSV reading logic
- WHERE filtering
- GROUP BY aggregation
- ORDER BY sorting
- Result formatting
```

## Language Features

### Supported SQL Syntax

```sql
SELECT [DISTINCT] column_list
FROM file.csv
[WHERE condition]
[GROUP BY column_list]
[HAVING condition]
[ORDER BY column [ASC|DESC], ...]
[LIMIT n]
```

### Operators & Functions

**Comparison:** =, !=, <, >, <=, >=
**Logical:** AND, OR, NOT
**Arithmetic:** +, -, *, /
**Aggregates:** COUNT, SUM, AVG, MIN, MAX
**String:** UPPER, LOWER

## Usage Examples

### Command Line Usage

```bash
# Inline query
python compiler.py -q "SELECT * FROM data.csv" --run

# From file
python compiler.py query.sql -o output.py

# With CSV validation
python compiler.py query.sql -c data.csv --run

# Show AST
python compiler.py query.sql --show-ast

# Show tokens
python compiler.py query.sql --show-tokens
```

### Programmatic Usage

```python
from lexer import Lexer
from parser import Parser
from code_generator import PythonCodeGenerator

# Parse query
lexer = Lexer("SELECT * FROM data.csv")
tokens = lexer.tokenize()
parser = Parser(tokens)
ast = parser.parse()

# Generate code
generator = PythonCodeGenerator(ast)
python_code = generator.generate()

# Execute
exec(python_code)
```

## Technical Highlights

### Design Patterns Used
- **Visitor Pattern** - For AST traversal
- **Strategy Pattern** - Different code generation strategies
- **Builder Pattern** - AST construction
- **Factory Pattern** - Token creation

### Key Algorithms
- **Recursive Descent Parsing** - Top-down parser
- **Operator Precedence Climbing** - Expression parsing
- **Hash-based Grouping** - Efficient GROUP BY
- **Multi-key Sorting** - ORDER BY implementation

### Performance Characteristics
- **Time Complexity:**
  - Lexing: O(n) where n = query length
  - Parsing: O(n) where n = number of tokens
  - Code generation: O(m) where m = AST size
  - Query execution: O(r) where r = number of CSV rows

- **Space Complexity:**
  - Compilation: O(n + m) for tokens and AST
  - Execution: O(r) for result storage

## Example Compilation Process

### Input Query
```sql
SELECT department, AVG(salary) as avg_sal
FROM employees.csv
WHERE age > 30
GROUP BY department
ORDER BY avg_sal DESC
```

### Step 1: Tokens
```
SELECT, department, COMMA, AVG, LPAREN, salary, RPAREN, AS, avg_sal,
FROM, employees, DOT, csv, WHERE, age, GREATER_THAN, 30,
GROUP, BY, department, ORDER, BY, avg_sal, DESC, EOF
```

### Step 2: AST
```
SelectQuery
  columns: [
    ColumnRef(Identifier('department')),
    ColumnRef(FunctionCall('AVG', [Identifier('salary')]), alias='avg_sal')
  ]
  from_table: 'employees.csv'
  where: BinaryOperation(Identifier('age'), >, Number(30))
  group_by: [Identifier('department')]
  order_by: [OrderBy(Identifier('avg_sal'), DESC)]
```

### Step 3: Semantic Analysis
```
✓ Column 'department' exists
✓ Column 'salary' exists
✓ Column 'age' exists
✓ GROUP BY columns match SELECT non-aggregates
✓ All aggregate functions used correctly
```

### Step 4: Generated Code
```python
import csv
from collections import defaultdict

def execute_query():
    groups = defaultdict(list)
    
    with open('employees.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if float(row['age']) > 30:
                key = (row['department'],)
                groups[key].append(row)
    
    results = []
    for key, group_rows in groups.items():
        dept = key[0]
        avg_sal = sum(float(r['salary']) for r in group_rows) / len(group_rows)
        results.append({'department': dept, 'avg_sal': avg_sal})
    
    results.sort(key=lambda x: x['avg_sal'], reverse=True)
    
    # Output...
```

## Testing

### Run All Tests
```bash
# Run demos
python demo.py

# Test individual queries
python compiler.py examples/query1.sql --run
python compiler.py examples/query2.sql --run
python compiler.py examples/query3.sql --run
```

### Test Coverage
- ✅ Simple SELECT
- ✅ WHERE with multiple conditions
- ✅ GROUP BY with aggregates
- ✅ HAVING clause
- ✅ ORDER BY (ASC/DESC)
- ✅ LIMIT
- ✅ DISTINCT
- ✅ String functions
- ✅ Arithmetic operations
- ✅ Complex nested expressions

## Educational Value

This project teaches:

1. **Compiler Design**
   - Lexical analysis techniques
   - Grammar design and parsing
   - AST construction
   - Code generation strategies

2. **Language Design**
   - Syntax design decisions
   - Operator precedence
   - Type systems
   - Semantic rules

3. **Software Engineering**
   - Modular architecture
   - Error handling
   - Testing strategies
   - Documentation

4. **Algorithms & Data Structures**
   - Tokenization algorithms
   - Tree structures (AST)
   - Hash-based grouping
   - Sorting algorithms

## Potential Extensions

### Easy Additions
- More string functions (SUBSTRING, CONCAT, TRIM)
- Date/time functions
- CASE expressions
- Column aliases in WHERE clause
- Multiple file support (UNION)

### Medium Complexity
- JOIN operations (INNER, LEFT, RIGHT)
- Subqueries
- Window functions (ROW_NUMBER, RANK)
- CTEs (WITH clause)
- Type inference system

### Advanced Features
- Query optimization passes
- C code generation for performance
- Parallel execution
- Index creation and usage
- Query plan visualization
- JIT compilation

## Performance Notes

### Strengths
- Streaming CSV processing (low memory)
- Efficient grouping with hash tables
- Single-pass reading
- Minimal overhead

### Optimization Opportunities
- Could parallelize GROUP BY
- Could use indexes for WHERE
- Could optimize multi-column GROUP BY
- Could cache compiled queries

## Use Cases

1. **Data Analysis** - Quick analysis without database setup
2. **Log Processing** - Analyze application logs
3. **ETL** - Transform data before loading
4. **Education** - Learn compiler design
5. **Prototyping** - Rapid query development
6. **Automation** - Generate report scripts

## Limitations

### Current Limitations
- Single CSV file per query (no JOINs)
- No subqueries
- Limited function library
- Python-only code generation
- No query optimization passes
- No prepared statements

### By Design
- No runtime dependencies (uses standard library)
- Text-based output only
- No GUI
- Command-line interface only

## Dependencies

**None!** Uses only Python standard library:
- `csv` - CSV reading
- `re` - Regular expressions (in lexer)
- `enum` - Enumerations
- `dataclasses` - Data classes
- `argparse` - Command-line parsing
- `collections` - defaultdict
- `pathlib` - File paths

## Credits

Built as an educational project demonstrating:
- Compiler construction techniques
- Programming language implementation
- Software engineering best practices
- Clean code principles

## License

Free for educational use.

## Getting Started

1. Read `QUICKSTART.md` for immediate usage
2. Try `python demo.py` for examples
3. Read `README.md` for full documentation
4. Explore `examples/` for query samples
5. Study the code to learn compiler design!

## Questions?

Check the documentation:
- `README.md` - Full reference
- `QUICKSTART.md` - Quick start
- Code comments - Implementation details
- `examples/` - Real usage examples

Happy compiling! 🚀
