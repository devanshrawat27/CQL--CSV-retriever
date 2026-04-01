#!/usr/bin/env python3
"""
CSV Query Compiler - Main Entry Point
Compiles SQL-like queries for CSV files into executable Python code
"""

import argparse
import sys
from pathlib import Path

from lexer import Lexer
from parser import Parser
from semantic_analyzer import SemanticAnalyzer
from code_generator import PythonCodeGenerator
from ast_nodes import ast_to_string


def compile_query(query_string: str, csv_file: str = None, output_file: str = None, 
                  show_ast: bool = False, show_tokens: bool = False, 
                  run_immediately: bool = False):
    """
    Compile a CSV query to Python code
    
    Args:
        query_string: The SQL-like query to compile
        csv_file: Path to CSV file (for validation)
        output_file: Path to save generated Python code
        show_ast: Print the Abstract Syntax Tree
        show_tokens: Print the token list
        run_immediately: Execute the generated code immediately
    """
    
    try:
        # Step 1: Lexical Analysis
        print("🔍 Step 1: Lexical Analysis...")
        lexer = Lexer(query_string)
        tokens = lexer.tokenize()
        
        if show_tokens:
            print("\nTokens:")
            for token in tokens:
                print(f"  {token}")
            print()
        
        print(f"✓ Generated {len(tokens)} tokens")
        
        # Step 2: Parsing
        print("\n🔍 Step 2: Parsing...")
        parser = Parser(tokens)
        ast = parser.parse()
        
        if show_ast:
            print("\nAbstract Syntax Tree:")
            print(ast_to_string(ast))
            print()
        
        print("✓ Built Abstract Syntax Tree")
        
        # Step 3: Semantic Analysis
        print("\n🔍 Step 3: Semantic Analysis...")
        analyzer = SemanticAnalyzer(ast, csv_file)
        
        if not analyzer.analyze():
            print("\n❌ Semantic errors found:")
            for error in analyzer.get_errors():
                print(f"  • {error}")
            return False
        
        print("✓ Query is semantically valid")
        
        # Step 4: Code Generation
        print("\n🔍 Step 4: Code Generation...")
        generator = PythonCodeGenerator(ast)
        python_code = generator.generate()
        
        print("✓ Generated Python code")
        
        # Save or display code
        if output_file:
            with open(output_file, 'w') as f:
                f.write(python_code)
            print(f"\n💾 Saved generated code to: {output_file}")
        else:
            print("\n" + "=" * 70)
            print("Generated Python Code:")
            print("=" * 70)
            print(python_code)
            print("=" * 70)
        
        # Run immediately if requested
        if run_immediately:
            print("\n▶️  Executing generated code...\n")
            print("-" * 70)
            # Create a namespace with necessary imports
            import csv
            from collections import defaultdict
            namespace = {
                'csv': csv, 
                'defaultdict': defaultdict, 
                'sys': sys,
                '__name__': '__main__'  # Make the if __name__ block execute
            }
            exec(python_code, namespace)
            print("-" * 70)
        
        return True
    
    except Exception as e:
        print(f"\n❌ Compilation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    parser = argparse.ArgumentParser(
        description="CSV Query Compiler - Compile SQL-like queries for CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compile a query from a file
  python compiler.py query.sql -c data.csv -o output.py
  
  # Compile and run immediately
  python compiler.py query.sql -c data.csv --run
  
  # Compile a query directly from command line
  python compiler.py -q "SELECT * FROM data.csv WHERE age > 30" --run
  
  # Show AST and tokens
  python compiler.py query.sql --show-ast --show-tokens
        """
    )
    
    parser.add_argument(
        'query_file',
        nargs='?',
        help='File containing the query (or use -q for inline query)'
    )
    
    parser.add_argument(
        '-q', '--query',
        help='Query string (alternative to query_file)'
    )
    
    parser.add_argument(
        '-c', '--csv',
        help='CSV file path (for validation)'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file for generated Python code'
    )
    
    parser.add_argument(
        '--run',
        action='store_true',
        help='Execute the generated code immediately'
    )
    
    parser.add_argument(
        '--show-ast',
        action='store_true',
        help='Display the Abstract Syntax Tree'
    )
    
    parser.add_argument(
        '--show-tokens',
        action='store_true',
        help='Display the token list'
    )
    
    args = parser.parse_args()
    
    # Get query string
    if args.query:
        query_string = args.query
    elif args.query_file:
        try:
            with open(args.query_file, 'r') as f:
                query_string = f.read()
        except FileNotFoundError:
            print(f"❌ Error: Query file not found: {args.query_file}")
            return 1
    else:
        parser.print_help()
        return 1
    
    # Compile the query
    print("🚀 CSV Query Compiler")
    print("=" * 70)
    print(f"Query: {query_string.strip()[:100]}...")
    print("=" * 70)
    
    success = compile_query(
        query_string=query_string,
        csv_file=args.csv,
        output_file=args.output,
        show_ast=args.show_ast,
        show_tokens=args.show_tokens,
        run_immediately=args.run
    )
    
    if success:
        print("\n✅ Compilation successful!")
        return 0
    else:
        print("\n❌ Compilation failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
