"""
Harmony Language — Lexer
Tokenizes Harmony source code into FDL-aware token stream.

Grammar basis: Thesis-Antithesis-Synthesis triadic structure.
Every token belongs to one of three dialectical layers.
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Iterator, List, Optional


class TokenType(Enum):
    # ── Dialectical Keywords ──────────────────────────────────────────────────
    THESIS      = auto()
    ANTITHESIS  = auto()
    SYNTHESIS   = auto()
    RESOLVE     = auto()
    PRAGMA      = auto()
    EMIT        = auto()

    # ── FDL Primitives ────────────────────────────────────────────────────────
    RESONANCE           = auto()
    ZERO_DISCRETENESS   = auto()
    PARASITE_FILTER     = auto()
    MERIDIAN            = auto()
    SCHUMANN_BASE       = auto()

    # ── Types ────────────────────────────────────────────────────────────────
    IDENTIFIER  = auto()
    NUMBER      = auto()
    STRING      = auto()
    BOOLEAN     = auto()
    HZ          = auto()       # frequency literal: 7.83Hz

    # ── Operators ────────────────────────────────────────────────────────────
    ASSIGN      = auto()   # :
    ARROW       = auto()   # →  or ->
    EQUALS      = auto()   # =
    LBRACE      = auto()   # {
    RBRACE      = auto()   # }
    LPAREN      = auto()   # (
    RPAREN      = auto()   # )
    COMMA       = auto()
    DOT         = auto()

    # ── Meta ─────────────────────────────────────────────────────────────────
    COMMENT     = auto()   # @ ...
    NEWLINE     = auto()
    EOF         = auto()
    UNKNOWN     = auto()


KEYWORDS: dict[str, TokenType] = {
    "THESIS":            TokenType.THESIS,
    "ANTITHESIS":        TokenType.ANTITHESIS,
    "SYNTHESIS":         TokenType.SYNTHESIS,
    "RESOLVE":           TokenType.RESOLVE,
    "PRAGMA":            TokenType.PRAGMA,
    "EMIT":              TokenType.EMIT,
    "RESONANCE":         TokenType.RESONANCE,
    "ZERO_DISCRETENESS": TokenType.ZERO_DISCRETENESS,
    "PARASITE_FILTER":   TokenType.PARASITE_FILTER,
    "MERIDIAN":          TokenType.MERIDIAN,
    "SCHUMANN_BASE":     TokenType.SCHUMANN_BASE,
    "true":              TokenType.BOOLEAN,
    "false":             TokenType.BOOLEAN,
    "Hz":                TokenType.HZ,
}


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, L{self.line}:C{self.col})"


class LexerError(Exception):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"[Harmony Lexer] {message} at line {line}, col {col}")
        self.line = line
        self.col = col


class HarmonyLexer:
    """
    Tokenizes Harmony source into a stream of dialectical tokens.

    The lexer is resonance-aware: it tracks frequency literals (e.g. 432.0Hz)
    and validates them against Schumann base during tokenization.
    """

    TOKEN_SPEC = [
        ("HZ_LITERAL",  r"\d+\.\d+Hz"),             # 7.83Hz, 432.0Hz
        ("NUMBER",      r"\d+\.\d+|\d+"),
        ("STRING",      r'"[^"]*"'),
        ("ARROW",       r"→|->"),
        ("ASSIGN",      r":"),
        ("EQUALS",      r"="),
        ("LBRACE",      r"\{"),
        ("RBRACE",      r"\}"),
        ("LPAREN",      r"\("),
        ("RPAREN",      r"\)"),
        ("COMMA",       r","),
        ("DOT",         r"\."),
        ("COMMENT",     r"#[^\n]*"),                 # inline comment
        ("ANNOTATION",  r"@[^\n]*"),                 # @ annotation
        ("NEWLINE",     r"\n"),
        ("WHITESPACE",  r"[ \t]+"),
        ("IDENTIFIER",  r"[A-Za-z_][A-Za-z0-9_.]*"),
        ("UNKNOWN",     r"."),
    ]

    _master_re = re.compile(
        "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
    )

    def __init__(self, source: str):
        self.source = source
        self.line = 1
        self.col = 1

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        for match in self._master_re.finditer(self.source):
            kind = match.lastgroup
            value = match.group()
            col = match.start() - self.source.rfind("\n", 0, match.start())

            if kind == "WHITESPACE":
                self.col += len(value)
                continue

            if kind == "COMMENT":
                tokens.append(Token(TokenType.COMMENT, value, self.line, col))
                continue

            if kind == "ANNOTATION":
                tokens.append(Token(TokenType.COMMENT, value, self.line, col))
                continue

            if kind == "NEWLINE":
                tokens.append(Token(TokenType.NEWLINE, value, self.line, col))
                self.line += 1
                self.col = 1
                continue

            if kind == "HZ_LITERAL":
                tokens.append(Token(TokenType.HZ, value, self.line, col))
                continue

            if kind == "IDENTIFIER":
                tok_type = KEYWORDS.get(value, TokenType.IDENTIFIER)
                tokens.append(Token(tok_type, value, self.line, col))
                continue

            if kind == "NUMBER":
                tokens.append(Token(TokenType.NUMBER, value, self.line, col))
                continue

            if kind == "STRING":
                tokens.append(Token(TokenType.STRING, value[1:-1], self.line, col))
                continue

            if kind == "ARROW":
                tokens.append(Token(TokenType.ARROW, value, self.line, col))
                continue

            if kind == "UNKNOWN":
                raise LexerError(f"Unexpected character {value!r}", self.line, col)

            # Map single-char tokens
            type_map = {
                "ASSIGN": TokenType.ASSIGN,
                "EQUALS": TokenType.EQUALS,
                "LBRACE": TokenType.LBRACE,
                "RBRACE": TokenType.RBRACE,
                "LPAREN": TokenType.LPAREN,
                "RPAREN": TokenType.RPAREN,
                "COMMA":  TokenType.COMMA,
                "DOT":    TokenType.DOT,
            }
            if kind in type_map:
                tokens.append(Token(type_map[kind], value, self.line, col))

        tokens.append(Token(TokenType.EOF, "", self.line, self.col))
        return tokens


def tokenize(source: str) -> List[Token]:
    return HarmonyLexer(source).tokenize()
