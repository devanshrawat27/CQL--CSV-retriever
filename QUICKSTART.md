# CSV Query Compiler - Quick Start Guide

## Installation

No installation needed! Just Python 3.7+

## Try It Now

### 1. Run a Simple Query

```bash
python compiler.py -q "SELECT * FROM employees.csv LIMIT 3" --run
```

**Output:**
```
name,age,department,salary,hire_date
Alice Johnson,28,Engineering,85000,2020-03-15
Bob Smith,35,Engineering,95000,2018-07-22
Carol Williams,42,Sales,75000,2015-11-10
```

### 2. Filter Data

```bash
python compiler.py -q "SELECT name, salary FROM employees.csv WHERE department = 'Engineering' ORDER BY salary DESC" --run
```

**Output:**
```
name,salary
Bob Smith,95000
Grace Wilson,92000
David Brown,88000
Alice Johnson,85000
Ivy Taylor,78000
```

### 3. Aggregate Data

```bash
python compiler.py -q "SELECT department, COUNT(*) as count, AVG(salary) as avg_sal FROM employees.csv GROUP BY department ORDER BY avg_sal DESC" --run
```

**Output:**
```
department,count,avg_sal
Engineering,5,87600.0
Sales,3,78666.67
Marketing,2,67500.0
```

### 4. Use Example Queries

```bash
# Query 1: Filter and sort
python compiler.py examples/query1.sql --run

# Query 2: Group by with aggregates
python compiler.py examples/query2.sql --run

# Query 3: Complex with HAVING clause
python compiler.py examples/query3.sql --run
```

### 5. Generate Standalone Python Script

```bash
# Compile query to a Python file
python compiler.py examples/query2.sql -o analyze_departments.py

# Run the generated script anytime
python analyze_departments.py
```

## Quick Command Reference

| Command | Description |
|---------|-------------|
| `python compiler.py query.sql --run` | Compile and execute |
| `python compiler.py -q "SELECT..."` | Inline query |
| `python compiler.py query.sql -o out.py` | Save to file |
| `python compiler.py query.sql --show-ast` | Show syntax tree |
| `python compiler.py query.sql --show-tokens` | Show tokens |

## Supported SQL Features

✅ SELECT with column selection
✅ WHERE with AND, OR, NOT
✅ GROUP BY with aggregates
✅ HAVING clause
✅ ORDER BY ASC/DESC
✅ LIMIT
✅ DISTINCT
✅ Aggregate functions: COUNT, SUM, AVG, MIN, MAX
✅ String functions: UPPER, LOWER
✅ Comparison: =, !=, <, >, <=, >=
✅ Arithmetic: +, -, *, /

## Example Queries

### Find high earners
```sql
SELECT name, salary
FROM employees.csv
WHERE salary > 80000
ORDER BY salary DESC
```

### Department statistics
```sql
SELECT 
    department,
    COUNT(*) as employees,
    AVG(salary) as avg_salary,
    MAX(salary) as max_salary
FROM employees.csv
GROUP BY department
HAVING COUNT(*) > 1
ORDER BY avg_salary DESC
```

### Filter and transform
```sql
SELECT 
    UPPER(name) as name_upper,
    age,
    salary * 1.1 as raised_salary
FROM employees.csv
WHERE age BETWEEN 25 AND 35
ORDER BY age
```

## Need Help?

See `README.md` for full documentation.

## What Makes This Special?

- ✨ **No Database Setup** - Works directly with CSV files
- ✨ **Generates Real Code** - Creates standalone Python scripts
- ✨ **Educational** - See exactly how compilers work
- ✨ **Fast** - Optimized code generation
- ✨ **Portable** - Just Python standard library

Happy querying! 🚀
