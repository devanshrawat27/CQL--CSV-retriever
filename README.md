# CQL — CSV Query Language

> A SQL-like query compiler that runs directly on CSV files. No database. No setup. Just queries.

---

## What is this?

Most tools for querying CSV data either need a full database import, or require writing Python scripts from scratch. CQL sits in between — you write a simple SQL-like query, and the compiler handles the rest.

Under the hood, it's a complete compiler implementation: lexer, parser, semantic analyzer, optimizer, and code generator. The output is streaming Python code that processes your CSV without ever loading it fully into memory.

---

## Compiler Pipeline

```
  Query String
       │
       ▼
┌─────────────────┐
│     LEXER       │  Breaks the query into tokens
│                 │  SELECT, FROM, WHERE, identifiers, operators...
└────────┬────────┘
         │  token stream
         ▼
┌─────────────────┐
│     PARSER      │  Recursive descent parser
│                 │  Builds an Abstract Syntax Tree (AST)
└────────┬────────┘
         │  AST
         ▼
┌─────────────────┐
│    SEMANTIC     │  Validates column names against CSV schema
│    ANALYZER     │  Type-checks comparisons and expressions
└────────┬────────┘
         │  validated AST
         ▼
┌─────────────────┐
│   OPTIMIZER     │  Predicate pushdown — filters applied early
│                 │  Projection pruning — drops unused columns
└────────┬────────┘
         │  optimized AST
         ▼
┌─────────────────┐
│     CODE        │  Generates clean Python code
│   GENERATOR     │  Streaming CSV processing via csv module
└────────┬────────┘
         │
         ▼
     Output
```

---

## Why build this?

CSV files are everywhere. But the moment you want to do anything non-trivial with them — filter, join, aggregate — you're either writing pandas boilerplate or spinning up a database.

CQL treats the query as a first-class program to be compiled, not just evaluated. This makes it a natural fit for demonstrating compiler design concepts on a problem people actually run into.

---

## Current Tools & Their Gaps

| Tool | Problem |
|------|---------|
| pandas | Requires Python knowledge; verbose for simple queries |
| Excel | Not scriptable; chokes on large files |
| SQLite / MySQL | Full DB setup needed just to query a flat file |
| `awk` | Powerful but not SQL-friendly or readable |

---

## Technical Approach

The system is written entirely in Python. The parser is hand-written using recursive descent — no parser generator libraries. CSV processing in the generated code uses Python's built-in `csv` module with row-by-row streaming, so memory usage stays flat regardless of file size.

**Supported in queries:**
- `SELECT` with column projection
- `FROM` targeting a CSV file
- `WHERE` with comparison and logical operators
- `JOIN` on equality conditions
- Basic type inference (int, float, string)

---

## Assumptions

- CSV files have a header row
- Data types are inferred from values
- Files are well-formed
- JOINs are limited to equality conditions

---

## Goals & Milestones

**Goals**
- Design a SQL-like grammar for CSV querying
- Implement lexer and recursive-descent parser
- Validate queries against actual CSV schema
- Apply predicate pushdown and projection pruning
- Generate executable, streaming Python output

**Milestones**

| Phase | What |
|-------|------|
| 1 | Lexer + Parser |
| 2 | Semantic Analyzer |
| 3 | Query Optimizer |
| 4 | Code Generation + Testing |

---

## References

- Python CSV Module — https://docs.python.org/3/library/csv.html
- Python Collections Module — https://docs.python.org/3/library/collections.html
- Python Dataclasses — https://docs.python.org/3/library/dataclasses.html

---

## Team

**Syntax Syndicate**

- Lakshya Dhiman
- Devansh Rawat
- Vedant Devrani

**Mentor** — Ms. Preeti Badhani  
**Evaluator** — Mr. Mukesh Kumar
