<div align="center">

```
 ██████╗ ██████╗ ██╗     
██╔════╝██╔═══██╗██║     
██║     ██║   ██║██║     
██║     ██║▄▄ ██║██║     
╚██████╗╚██████╔╝███████╗
 ╚═════╝ ╚══▀▀═╝ ╚══════╝
```

### CSV Query Language — *Query your files. No database required.*

<br/>

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Type](https://img.shields.io/badge/Type-Compiler-FF6B6B?style=for-the-badge)
![Course](https://img.shields.io/badge/Course-Compiler%20Design-6C63FF?style=for-the-badge)
![Team](https://img.shields.io/badge/Team-Syntax%20Syndicate-00C896?style=for-the-badge)
![PBL](https://img.shields.io/badge/PBL-2024--25-F7B731?style=for-the-badge)

<br/>

> **Write SQL. Point at a CSV. Get results.**  
> No imports. No database setup. No boilerplate.

</div>

---

## 📌 What is CQL?

CQL is a full compiler pipeline that takes SQL-like queries and runs them **directly on CSV files**. It tokenizes, parses, validates, optimizes, and generates streaming Python code — all from a single query string.

It's built to be lightweight, dependency-free, and to demonstrate every major stage of compiler design on a problem that's actually useful.

---

## 🔍 The Problem

| Tool | What's wrong |
|------|-------------|
| **pandas** | Verbose for simple queries; needs programming knowledge |
| **Excel** | Not scriptable; struggles with large files |
| **SQLite / MySQL** | Full database setup just to query a flat file |
| **`awk`** | Powerful but cryptic; nothing like SQL |
| **CQL ✦** | ✅ SQL syntax · ✅ No setup · ✅ Works on CSV · ✅ Memory efficient |

---

## ⚙️ Compiler Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Query String                                              │
│       │                                                     │
│       ▼                                                     │
│  ┌──────────┐                                               │
│  │  LEXER   │  →  Breaks query into tokens                  │
│  │          │     keywords · identifiers · operators        │
│  └────┬─────┘                                               │
│       │ token stream                                        │
│       ▼                                                     │
│  ┌──────────┐                                               │
│  │  PARSER  │  →  Recursive descent parser                  │
│  │          │     Builds an Abstract Syntax Tree (AST)      │
│  └────┬─────┘                                               │
│       │ AST                                                 │
│       ▼                                                     │
│  ┌──────────┐                                               │
│  │ SEMANTIC │  →  Validates column names vs CSV schema      │
│  │ ANALYZER │     Type-checks comparisons & expressions     │
│  └────┬─────┘                                               │
│       │ validated AST                                       │
│       ▼                                                     │
│  ┌──────────┐                                               │
│  │OPTIMIZER │  →  Predicate pushdown (filters early)        │
│  │          │     Projection pruning (drops unused cols)    │
│  └────┬─────┘                                               │
│       │ optimized AST                                       │
│       ▼                                                     │
│  ┌──────────┐                                               │
│  │  CODE    │  →  Emits clean Python code                   │
│  │   GEN    │     Streaming row-by-row via csv module       │
│  └────┬─────┘                                               │
│       │                                                     │
│       ▼                                                     │
│    Output                                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Stage Breakdown

<details>
<summary><b>01 · Lexer</b> — Tokenization</summary>
<br/>

Scans the raw query string character by character and produces a flat stream of tokens — `SELECT`, `FROM`, `WHERE`, identifiers, operators, and literals. This is the entry point of the compiler.

```
Input  → SELECT name, age FROM data.csv WHERE age > 21
Output → [SELECT] [IDENT:name] [,] [IDENT:age] [FROM] [IDENT:data.csv] [WHERE] [IDENT:age] [>] [INT:21]
```

</details>

<details>
<summary><b>02 · Parser</b> — AST Construction</summary>
<br/>

A hand-written **recursive descent parser** consumes the token stream and builds a hierarchical Abstract Syntax Tree. No parser-generator libraries — built from scratch.

</details>

<details>
<summary><b>03 · Semantic Analyzer</b> — Validation</summary>
<br/>

Walks the AST and validates it against the actual CSV schema:
- Are the referenced column names real?
- Are types compatible in comparisons?
- Are JOIN conditions well-formed?

Errors are caught here before any code runs.

</details>

<details>
<summary><b>04 · Optimizer</b> — Query Optimization</summary>
<br/>

Applies two core optimizations:

- **Predicate Pushdown** — moves `WHERE` filters as early in the pipeline as possible, so rows are eliminated before expensive operations
- **Projection Pruning** — drops columns that aren't referenced downstream, reducing memory and processing overhead

</details>

<details>
<summary><b>05 · Code Generator</b> — Output</summary>
<br/>

Translates the optimized AST into clean, executable Python code that uses the built-in `csv` module. Processing is row-by-row (streaming), so memory usage stays flat no matter how large the input file is.

</details>

---

## 🛠️ Technical Approach

```
Language     →  Python 3.x  
Parser       →  Hand-written recursive descent (no libraries)  
CSV Engine   →  Python built-in csv module (streaming)  
Dependencies →  Zero (standard library only)  
```

**Supported query features:**
- `SELECT` with column projection
- `FROM` targeting a `.csv` or `.tsv` file
- `WHERE` with comparison and logical operators
- `JOIN` on equality conditions across multiple files
- Automatic type inference (int · float · string)

---

## 🎯 Goals & Milestones

**Project Goals**
- [ ] Design a SQL-like grammar tailored for CSV querying
- [ ] Build a Lexer and hand-written recursive-descent Parser
- [ ] Implement Semantic Analyzer for schema validation
- [ ] Apply predicate pushdown and projection pruning
- [ ] Generate executable, streaming Python output

**Milestones**

| Phase | Milestone | Description |
|:-----:|-----------|-------------|
| `01` | **Lexer + Parser** | Tokenization, grammar definition, AST generation |
| `02` | **Semantic Analyzer** | Column & type validation against CSV schema |
| `03` | **Query Optimizer** | Predicate pushdown, projection pruning |
| `04` | **Code Gen + Testing** | Python codegen, streaming execution, test suite |

---

## 📌 Assumptions

- CSV files have a **header row** (first row = column names)
- Data types are **inferred** from values — no schema declaration needed
- Input files are **well-structured** with consistent formatting
- **JOIN** operations are limited to equality conditions only

---

## 👥 Team

<div align="center">

### `// SYNTAX SYNDICATE`

| Role | Name |
|------|------|
| 👑 Team Lead | Lakshya Dhiman |
| 🧑‍💻 Member | Devansh Rawat |
| 🧑‍💻 Member | Vedant Devrani |

<br/>

| | |
|---|---|
| **Mentor** | Ms. Preeti Badhani |
| **Evaluator** | Mr. Mukesh Kumar |

</div>

---

## 📚 References

- [Python CSV Module](https://docs.python.org/3/library/csv.html) — Python Software Foundation, 2024
- [Python Collections Module](https://docs.python.org/3/library/collections.html) — Python Software Foundation, 2024
- [Python Dataclasses Module](https://docs.python.org/3/library/dataclasses.html) — Python Software Foundation, 2024

---

<div align="center">

*Compiler Design · PBL 2024–25 · Syntax Syndicate*

</div>
