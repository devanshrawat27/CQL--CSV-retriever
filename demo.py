#!/usr/bin/env python3
"""
CSV Query Compiler - Demo Script
Demonstrates the compiler's capabilities
"""

import subprocess
import sys

def run_demo(title, command):
    """Run a demo command and display results"""
    print("\n" + "="*70)
    print(f"DEMO: {title}")
    print("="*70)
    print(f"Command: {command}")
    print("-"*70)
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    print()

def main():
    print("""
╔══════════════════════════════════════════════════════════════════╗
║                   CSV QUERY COMPILER DEMO                         ║
║                                                                   ║
║  A compiler that translates SQL-like queries for CSV files       ║
║  into executable Python code                                     ║
╚══════════════════════════════════════════════════════════════════╝
    """)
    
    demos = [
        (
            "Simple SELECT with LIMIT",
            'python compiler.py -q "SELECT * FROM employees.csv LIMIT 3" --run'
        ),
        (
            "Filter with WHERE clause",
            'python compiler.py -q "SELECT name, age, salary FROM employees.csv WHERE age > 30 AND department = \'Engineering\' ORDER BY salary DESC" --run'
        ),
        (
            "GROUP BY with Aggregates",
            'python compiler.py -q "SELECT department, COUNT(*) as count, AVG(salary) as avg_salary FROM employees.csv GROUP BY department ORDER BY avg_salary DESC" --run'
        ),
        (
            "Complex Query with HAVING",
            'python compiler.py examples/query3.sql --run'
        ),
    ]
    
    print("Running demos...")
    print("(This may take a moment)")
    
    for title, command in demos:
        run_demo(title, command)
    
    print("="*70)
    print("✅ All demos completed successfully!")
    print("="*70)
    print("\nTo try your own queries:")
    print('  python compiler.py -q "YOUR QUERY HERE" --run')
    print("\nOr compile to a file:")
    print('  python compiler.py myquery.sql -o output.py')
    print("\nFor more examples, see the examples/ directory")
    print()

if __name__ == "__main__":
    main()
