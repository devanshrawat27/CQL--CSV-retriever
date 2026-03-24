<div align="center">

# 🗄️ CQL — CSV Query Language Retriever

### *Query Your CSV Files Like a Database — No Engine Required*

[![Language](https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Type](https://img.shields.io/badge/Type-Compiler%20Project-FF6B6B?style=for-the-badge)](.)
[![Course](https://img.shields.io/badge/Course-Compiler%20Design-6C63FF?style=for-the-badge)](.)
[![Team](https://img.shields.io/badge/Team-Syntax%20Syndicate-00C896?style=for-the-badge)](.)
[![PBL](https://img.shields.io/badge/PBL-2024--25-F7B731?style=for-the-badge)](.)

---

> **"Why import your data into a database when your compiler can do the querying?"**  
> CQL is a lightweight SQL-like query compiler that lets you run queries directly on CSV/TSV files — fast, clean, and dependency-free.

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [System Architecture](#-system-architecture)
- [Compiler Pipeline](#-compiler-pipeline)
- [Technologies Used](#-technologies-used)
- [Project Goals & Milestones](#-project-goals--milestones)
- [Deliverables](#-deliverables)
- [Assumptions](#-assumptions)
- [Team Information](#-team-information)
- [Academic Details](#-academic-details)
- [References](#-references)

---

## 🔍 About the Project

**CQL (CSV Query Language)** is a full-stack compiler project that implements a custom SQL-like language designed specifically for querying CSV and TSV files. Instead of loading data into a database or writing pandas scripts, users can write clean, readable queries that get compiled and executed directly.

This project demonstrates the complete **compiler design pipeline** — from tokenization all the way to executable code generation — applied to a real-world, practical use case.

### ✨ What Makes CQL Different?

| Feature | Traditional Tools | CQL |
|--------|------------------|-----|
| Requires database setup | ✅ Yes | ❌ No |
| Needs programming knowledge | ✅ Yes (pandas) | ❌ No |
| SQL-like syntax | ⚠️ Partial | ✅ Full |
| Works directly on CSV | ⚠️ Limited | ✅ Native |
| Lightweight | ❌ No | ✅ Yes |
| Demonstrates compiler concepts | ❌ No | ✅ Yes |

---

## 🚩 Problem Statement

CSV files are one of the most widely used formats for storing structured data — yet querying them efficiently is surprisingly painful. Current solutions all have drawbacks:

- **Python/pandas** → Requires scripting knowledge, verbose for simple queries
- **Excel** → GUI-only, not scriptable, struggles with large files
- **MySQL / SQLite** → Overkill; requires a full database import/export cycle
- **`awk` / shell tools** → Low-level, non-intuitive, not SQL-friendly

**CQL solves this** by compiling SQL-like queries into optimized, streaming Python code that processes CSV files directly — no database, no heavy dependencies, no overhead.

---

## 🏗️ System Architecture

The CQL system follows a classic **multi-stage compiler architecture**:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CQL COMPILER PIPELINE                       │
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────────────┐  │
│  │          │   │          │   │ Semantic  │   │                │  │
│  │  LEXER   │──▶│  PARSER  │──▶│ Analyzer  │──▶│   OPTIMIZER   │  │
│  │          │   │          │   │           │   │                │  │
│  └──────────┘   └──────────┘   └──────────┘   └────────────────┘  │
│   Tokens ▶▶      AST ▶▶       Validated AST ▶▶  Optimized AST      │
│                                                        │            │
│                                               ┌────────▼────────┐  │
│                                               │ CODE GENERATOR  │  │
│                                               │  (Python Code)  │  │
│                                               └─────────────────┘  │
│                                                        │            │
│                                               ┌────────▼────────┐  │
│                                               │  CSV EXECUTOR   │  │
│                                               │   (Output)      │  │
│                                               └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Compiler Pipeline

### 1. 🔤 Lexer (Lexical Analyzer)
Scans the raw SQL-like query string and converts it into a stream of **tokens** (keywords, identifiers, operators, literals). This is the entry point of the compiler.

```
Input:  SELECT name, age FROM data.csv WHERE age > 21
Output: [SELECT] [IDENTIFIER:name] [COMMA] [IDENTIFIER:age] [FROM] ...
```

### 2. 🌳 Parser (Syntax Analysis)
Uses a **Recursive Descent Parser** to consume the token stream and build an **Abstract Syntax Tree (AST)** — a structured, hierarchical representation of the query.

### 3. ✅ Semantic Analyzer
Validates the AST against the actual CSV schema:
- Are the referenced **column names valid**?
- Are **data types compatible** in comparisons?
- Are **JOIN conditions** properly formed?

### 4. ⚡ Optimizer
Applies query optimization strategies to make execution faster:
- **Predicate Pushdown** — Apply WHERE filters as early as possible
- **Projection Pruning** — Drop unused columns early in the pipeline

### 5. 💻 Code Generator
Translates the optimized AST into **clean, executable Python code** using the built-in `csv` module with streaming processing — enabling memory-efficient handling of large files.

---

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| **Primary Language** | Python 3.x |
| **Parser Type** | Recursive Descent Parser (hand-written) |
| **CSV Processing** | Python `csv` module (streaming) |
| **Data Structures** | Python `dataclasses`, `collections` |
| **Testing** | Custom test datasets |

---

## 🎯 Project Goals & Milestones

### Goals
- [x] Design a clean SQL-like query language tailored for CSV files
- [x] Implement a Lexer and recursive-descent Parser
- [x] Build a Semantic Analyzer for schema validation
- [x] Apply query optimization techniques (predicate pushdown, projection pruning)
- [x] Generate optimized, streaming Python code as output

### Milestones

| # | Milestone | Description |
|---|-----------|-------------|
| 1 | **Lexer & Parser** | Tokenization + AST generation |
| 2 | **Semantic Analyzer** | Column & type validation |
| 3 | **Query Optimizer** | Push filters, prune projections |
| 4 | **Code Generation & Testing** | Python codegen + full test suite |

---

## 📦 Deliverables

1. ✅ **Working CSV Query Compiler** — End-to-end CQL → Python pipeline
2. ✅ **SQL-like Query Language** — Custom language specification & grammar
3. ✅ **Optimized Python Code Generator** — Streaming, memory-efficient output
4. ✅ **Sample Datasets & Test Results** — Validation against real CSV files
5. ✅ **Project Documentation** — Full design and implementation report

---

## 📌 Assumptions

The following assumptions are made about the input CSV files:

- 📄 CSV files **contain a header row** (first row = column names)
- 🔍 **Data types can be inferred** from values (integer, float, string)
- 🏗️ Files are **well-structured** (no corrupted rows or malformed escaping)
- 🔗 **JOIN operations** are limited to equality conditions (`col1 = col2`)

---

## 👨‍💻 Team Information

<div align="center">

### 🏷️ Team Name: **Syntax Syndicate**

</div>

| Role | Name | University Roll No. | Student ID | Email |
|------|------|-------------------|------------|-------|
| 👑 **Team Lead** | Lakshya Dhiman | 2319033 | 2302111412 | ld815652@gmail.com |
| 🧑‍💻 **Member** | Devansh Rawat | 2318717 | 230112620 | devanshdevr@gmail.com |
| 🧑‍💻 **Member** | Vedant Devrani | 2319842 | 230112049 | vedantdevrani177@gmail.com |

---

## 🎓 Academic Details

| Detail | Information |
|--------|-------------|
| **Course** | Compiler Design |
| **Project Type** | Project Based Learning (PBL) |
| **Project Title** | CQL — CSV Query Language Retriever |
| **Mentor / Guide** | **Ms. Preeti Badhani** |
| **Evaluator** | **Mr. Mukesh Kumar** |

---

## 📚 References

1. **Python Software Foundation. (2024).** Python Documentation — CSV Module.  
   🔗 https://docs.python.org/3/library/csv.html

2. **Python Software Foundation. (2024).** Python Documentation — Collections Module.  
   🔗 https://docs.python.org/3/library/collections.html

3. **Python Software Foundation. (2024).** Python Documentation — Dataclasses Module.  
   🔗 https://docs.python.org/3/library/dataclasses.html

---

<div align="center">

**Made with 💻 & ☕ by Team Syntax Syndicate**  
*Compiler Design PBL | 2024–25*

</div>
