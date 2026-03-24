<div align="center">

# 🗄️ CQL — CSV Query Language

**A compiler that translates SQL-like queries into executable Python code — directly on CSV files.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen?style=flat-square)
![Course](https://img.shields.io/badge/Course-Compiler%20Design-6C63FF?style=flat-square)
![Team](https://img.shields.io/badge/Team-Syntax%20Syndicate-FF6B6B?style=flat-square)

</div>

---

## What is this?

CQL lets you write SQL-like queries and run them directly on CSV files — no database, no imports, no setup. You write a query, point it at a file, and the compiler handles the rest: tokenizing, parsing, validating, optimizing, and generating clean streaming Python code.

```bash
python compiler.py -q "SELECT name, salary FROM employees.csv WHERE age > 30 ORDER BY salary DESC" --run
```

---

## Features

- `SELECT` with column selection and aliases
- `WHERE` with comparison and logical operators (`AND`, `OR`, `NOT`)
- `GROUP BY` with aggregate functions
- `HAVING` clause for filtering grouped results
- `ORDER BY` with `ASC` / `DESC`
- `LIMIT` and `DISTINCT`
- Aggregate functions — `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- String functions — `UPPER`, `LOWER`
- Arithmetic operations — `+`, `-`, `*`, `/`
- Semantic validation with detailed error messages
- Code generation to efficient Python

---

## Installation

No external dependencies. Uses Python standard library only.

```bash
git clone https://github.com/your-username/cql.git
cd cql
```

---

## Usage

### Compile a query file
```bash
python compiler.py examples/query1.sql -c employees.csv -o output.py
python output.py
```

### Inline query
```bash
python compiler.py -q "SELECT * FROM employees.csv WHERE age > 30" -c employees.csv --run
```

### Debug options
```bash
# View the Abstract Syntax Tree
python compiler.py examples/query1.sql --show-ast

# View token stream
python compiler.py examples/query1.sql --show-tokens
```

---

## Query Examples

**Simple filter with sorting:**
```sql
SELECT name, age, salary
FROM employees.csv
WHERE age > 30 AND department = 'Engineering'
ORDER BY salary DESC
LIMIT 5
```

**Aggregation:**
```sql
SELECT department, COUNT(*) as count, AVG(salary) as avg_sal
FROM employees.csv
GROUP BY department
ORDER BY avg_sal DESC
```

**HAVING clause:**
```sql
SELECT department, SUM(salary) as total
FROM employees.csv
WHERE age < 40
GROUP BY department
HAVING COUNT(*) >= 2
ORDER BY total DESC
```

**String functions:**
```sql
SELECT UPPER(name) as name_upper, LOWER(department) as dept_lower
FROM employees.csv
WHERE age > 25
```

**Arithmetic:**
```sql
SELECT name, salary, salary * 1.1 as raised_salary
FROM employees.csv
ORDER BY salary DESC
```

---

## Compiler Architecture

The compiler runs through four phases:

```
Query String
     │
     ▼
┌─────────────────┐
│     LEXER       │  Breaks query into tokens
│   lexer.py      │  keywords · identifiers · operators · literals
└────────┬────────┘
         │ token stream
         ▼
┌─────────────────┐
│     PARSER      │  Recursive descent parser
│   parser.py     │  Builds an Abstract Syntax Tree (AST)
└────────┬────────┘
         │ AST
         ▼
┌─────────────────┐
│    SEMANTIC     │  Validates column names against CSV schema
│    ANALYZER     │  Checks GROUP BY constraints & aggregate usage
└────────┬────────┘
         │ validated AST
         ▼
┌─────────────────┐
│     CODE        │  Emits clean Python code
│   GENERATOR     │  Streaming row-by-row via csv module
└────────┬────────┘
         │
         ▼
    output.py
```

### Phase Details

<details>
<summary><b>Phase 1 — Lexer</b></summary>
<br>

Scans the raw query string and produces a flat token stream:

```
SELECT name, age FROM employees.csv WHERE age > 30
  ↓
[SELECT] [IDENT:name] [,] [IDENT:age] [FROM] [IDENT:employees.csv] [WHERE] [IDENT:age] [>] [INT:30]
```

</details>

<details>
<summary><b>Phase 2 — Parser</b></summary>
<br>

Hand-written recursive descent parser. Builds a structured AST:

```
SelectQuery
├── columns: [ColumnRef(name), ColumnRef(age)]
├── from: employees.csv
├── where: BinaryOp(>)
│   ├── Identifier(age)
│   └── Number(30)
└── order_by: [OrderBy(salary, DESC)]
```

</details>

<details>
<summary><b>Phase 3 — Semantic Analyzer</b></summary>
<br>

- Validates column names exist in the CSV
- Checks `GROUP BY` constraints
- Ensures aggregate functions are used correctly
- Validates that `HAVING` is only used with `GROUP BY`

</details>

<details>
<summary><b>Phase 4 — Code Generator</b></summary>
<br>

Translates the AST into streaming Python code:

```python
import csv

def execute_query():
    with open('employees.csv', 'r') as f:
        reader = csv.DictReader(f)
        results = []
        for row in reader:
            if int(row.get('age', 0)) > 30:
                results.append({'name': row['name'], 'age': row['age']})
        # sort, limit, output...
```

</details>

---

## File Structure

```
cql/
├── compiler.py             # Main entry point
├── lexer.py                # Lexical analyzer
├── parser.py               # Parser — builds AST
├── ast_nodes.py            # AST node definitions
├── semantic_analyzer.py    # Semantic validator
├── code_generator.py       # Python code generator
├── employees.csv           # Sample dataset
├── examples/
│   ├── query1.sql
│   ├── query2.sql
│   └── query3.sql
└── README.md
```

---

## Error Handling

The compiler gives clear errors at every phase:

```
# Lexer error
❌ Lexer error at line 1, column 5: Unexpected character '@'

# Parser error
❌ Parser error at line 2, column 1: Expected FROM but got WHERE

# Semantic error
❌ Semantic errors:
   • Unknown column: invalid_col
   • 'age' must appear in GROUP BY or be used in an aggregate function
```

---

## Supported Operators

| Type | Operators |
|------|-----------|
| Comparison | `=` `!=` `<` `>` `<=` `>=` |
| Logical | `AND` `OR` `NOT` |
| Arithmetic | `+` `-` `*` `/` |
| Aggregate | `COUNT` `SUM` `AVG` `MIN` `MAX` |
| String | `UPPER` `LOWER` |

---

## Team

**Syntax Syndicate**

| Role | Name |
|------|------|
| Team Lead | Lakshya Dhiman |
| Member | Devansh Rawat |
| Member | Vedant Devrani |

**Mentor** — Ms. Preeti Badhani  
**Evaluator** — Mr. Mukesh Kumar

---

*Compiler Design · PBL 2026*
