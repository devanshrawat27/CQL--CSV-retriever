"""
Abstract Syntax Tree (AST) node definitions
Represents the structure of parsed queries
"""

from dataclasses import dataclass
from typing import List, Optional, Union
from enum import Enum


class BinaryOp(Enum):
    """Binary operators"""
    ADD = '+'
    SUBTRACT = '-'
    MULTIPLY = '*'
    DIVIDE = '/'
    EQUALS = '='
    NOT_EQUALS = '!='
    LESS_THAN = '<'
    GREATER_THAN = '>'
    LESS_EQUAL = '<='
    GREATER_EQUAL = '>='
    AND = 'AND'
    OR = 'OR'


class UnaryOp(Enum):
    """Unary operators"""
    NOT = 'NOT'
    NEGATE = '-'


class AggregateFunc(Enum):
    """Aggregate functions"""
    COUNT = 'COUNT'
    SUM = 'SUM'
    AVG = 'AVG'
    MIN = 'MIN'
    MAX = 'MAX'


class StringFunc(Enum):
    """String functions"""
    UPPER = 'UPPER'
    LOWER = 'LOWER'


# Base AST Node
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass


# Expression nodes
@dataclass
class Number(ASTNode):
    """Numeric literal"""
    value: Union[int, float]


@dataclass
class String(ASTNode):
    """String literal"""
    value: str


@dataclass
class Identifier(ASTNode):
    """Column name or table reference"""
    name: str


@dataclass
class BinaryOperation(ASTNode):
    """Binary operation (e.g., a + b, x > 5)"""
    left: ASTNode
    op: BinaryOp
    right: ASTNode


@dataclass
class UnaryOperation(ASTNode):
    """Unary operation (e.g., NOT condition, -value)"""
    op: UnaryOp
    operand: ASTNode


@dataclass
class FunctionCall(ASTNode):
    """Function call (aggregate or string functions)"""
    name: str  # Function name (COUNT, SUM, UPPER, etc.)
    args: List[ASTNode]
    is_aggregate: bool = False


@dataclass
class ColumnRef(ASTNode):
    """Column reference with optional alias"""
    expr: ASTNode  # Expression (can be Identifier, FunctionCall, etc.)
    alias: Optional[str] = None


@dataclass
class OrderByClause(ASTNode):
    """ORDER BY specification"""
    expr: ASTNode
    ascending: bool = True


# Main query node
@dataclass
class SelectQuery(ASTNode):
    """Complete SELECT query"""
    columns: List[ColumnRef]  # SELECT columns
    from_table: str  # FROM table (CSV filename)
    where: Optional[ASTNode] = None  # WHERE clause
    group_by: Optional[List[ASTNode]] = None  # GROUP BY columns
    having: Optional[ASTNode] = None  # HAVING clause
    order_by: Optional[List[OrderByClause]] = None  # ORDER BY
    limit: Optional[int] = None  # LIMIT
    distinct: bool = False  # DISTINCT flag


def ast_to_string(node: ASTNode, indent: int = 0) -> str:
    """Convert AST to readable string representation"""
    prefix = "  " * indent
    
    if isinstance(node, Number):
        return f"{prefix}Number({node.value})"
    
    elif isinstance(node, String):
        return f"{prefix}String({node.value!r})"
    
    elif isinstance(node, Identifier):
        return f"{prefix}Identifier({node.name})"
    
    elif isinstance(node, BinaryOperation):
        result = f"{prefix}BinaryOp({node.op.value})\n"
        result += ast_to_string(node.left, indent + 1) + "\n"
        result += ast_to_string(node.right, indent + 1)
        return result
    
    elif isinstance(node, UnaryOperation):
        result = f"{prefix}UnaryOp({node.op.value})\n"
        result += ast_to_string(node.operand, indent + 1)
        return result
    
    elif isinstance(node, FunctionCall):
        result = f"{prefix}FunctionCall({node.name})\n"
        for arg in node.args:
            result += ast_to_string(arg, indent + 1) + "\n"
        return result.rstrip()
    
    elif isinstance(node, ColumnRef):
        result = f"{prefix}ColumnRef"
        if node.alias:
            result += f" (as {node.alias})"
        result += "\n"
        result += ast_to_string(node.expr, indent + 1)
        return result
    
    elif isinstance(node, OrderByClause):
        result = f"{prefix}OrderBy ({'ASC' if node.ascending else 'DESC'})\n"
        result += ast_to_string(node.expr, indent + 1)
        return result
    
    elif isinstance(node, SelectQuery):
        result = f"{prefix}SelectQuery\n"
        result += f"{prefix}  FROM: {node.from_table}\n"
        result += f"{prefix}  DISTINCT: {node.distinct}\n"
        result += f"{prefix}  SELECT:\n"
        for col in node.columns:
            result += ast_to_string(col, indent + 2) + "\n"
        
        if node.where:
            result += f"{prefix}  WHERE:\n"
            result += ast_to_string(node.where, indent + 2) + "\n"
        
        if node.group_by:
            result += f"{prefix}  GROUP BY:\n"
            for expr in node.group_by:
                result += ast_to_string(expr, indent + 2) + "\n"
        
        if node.having:
            result += f"{prefix}  HAVING:\n"
            result += ast_to_string(node.having, indent + 2) + "\n"
        
        if node.order_by:
            result += f"{prefix}  ORDER BY:\n"
            for order in node.order_by:
                result += ast_to_string(order, indent + 2) + "\n"
        
        if node.limit:
            result += f"{prefix}  LIMIT: {node.limit}\n"
        
        return result.rstrip()
    
    return f"{prefix}Unknown({type(node).__name__})"
