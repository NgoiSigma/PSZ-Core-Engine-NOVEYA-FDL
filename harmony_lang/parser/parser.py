"""
Harmony Language — Parser
Builds a dialectical AST from the token stream.

Structure: every synthesis cycle produces a SynthesisNode that carries
the resolved state. PRAGMA nodes are collected as side-effect declarations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from harmony_lang.lexer.lexer import Token, TokenType, tokenize


# ─── AST NODES ────────────────────────────────────────────────────────────────

@dataclass
class FieldNode:
    key: str
    value: Any

@dataclass
class ThesisNode:
    name: str
    fields: List[FieldNode]

@dataclass
class AntithesisNode:
    name: str
    fields: List[FieldNode]

@dataclass
class NormalizationOpts:
    strategy: str           # ZERO_DISCRETENESS | SCHUMANN_BASE | PARASITE_FILTER
    resonance_check: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SynthesisNode:
    name: str
    thesis_ref: str
    antithesis_ref: str
    normalization: NormalizationOpts

@dataclass
class PragmaNode:
    emit_target: str        # synthesized variable name
    destination: str        # e.g. "metatron.kpi_metric"

@dataclass
class AnnotationNode:
    text: str

@dataclass
class ProgramNode:
    body: List[Any]         # ThesisNode | AntithesisNode | SynthesisNode | PragmaNode


# ─── PARSER ───────────────────────────────────────────────────────────────────

class ParseError(Exception):
    def __init__(self, message: str, token: Token):
        super().__init__(f"[Harmony Parser] {message} — got {token!r}")
        self.token = token


class HarmonyParser:
    """
    Recursive-descent parser for the Harmony language.
    Each parse_* method corresponds to one grammar rule.
    """

    def __init__(self, tokens: List[Token]):
        self.tokens = [t for t in tokens if t.type not in (TokenType.NEWLINE, TokenType.COMMENT)]
        self.pos = 0

    @property
    def current(self) -> Token:
        return self.tokens[self.pos]

    def peek(self, offset: int = 1) -> Token:
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else self.tokens[-1]

    def consume(self, expected: Optional[TokenType] = None) -> Token:
        tok = self.current
        if expected and tok.type != expected:
            raise ParseError(f"Expected {expected.name}", tok)
        self.pos += 1
        return tok

    def parse(self) -> ProgramNode:
        body = []
        while self.current.type != TokenType.EOF:
            node = self._parse_statement()
            if node is not None:
                body.append(node)
        return ProgramNode(body=body)

    def _parse_statement(self):
        tok = self.current
        if tok.type == TokenType.THESIS:
            return self._parse_thesis()
        if tok.type == TokenType.ANTITHESIS:
            return self._parse_antithesis()
        if tok.type == TokenType.SYNTHESIS:
            return self._parse_synthesis()
        if tok.type == TokenType.PRAGMA:
            return self._parse_pragma()
        # skip unknown
        self.pos += 1
        return None

    def _parse_thesis(self) -> ThesisNode:
        self.consume(TokenType.THESIS)
        name = self.consume(TokenType.IDENTIFIER).value
        fields = self._parse_field_block()
        return ThesisNode(name=name, fields=fields)

    def _parse_antithesis(self) -> AntithesisNode:
        self.consume(TokenType.ANTITHESIS)
        name = self.consume(TokenType.IDENTIFIER).value
        fields = self._parse_field_block()
        return AntithesisNode(name=name, fields=fields)

    def _parse_synthesis(self) -> SynthesisNode:
        self.consume(TokenType.SYNTHESIS)
        name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.EQUALS)
        self.consume(TokenType.RESOLVE)
        self.consume(TokenType.LPAREN)
        thesis_ref = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.COMMA)
        antithesis_ref = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.RPAREN)
        opts = self._parse_normalization_block()
        return SynthesisNode(
            name=name,
            thesis_ref=thesis_ref,
            antithesis_ref=antithesis_ref,
            normalization=opts,
        )

    def _parse_pragma(self) -> PragmaNode:
        self.consume(TokenType.PRAGMA)
        self.consume(TokenType.EMIT)
        self.consume(TokenType.LPAREN)
        target = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.ARROW)
        dest = self._parse_path()
        return PragmaNode(emit_target=target, destination=dest)

    def _parse_field_block(self) -> List[FieldNode]:
        self.consume(TokenType.LBRACE)
        fields = []
        while self.current.type != TokenType.RBRACE:
            key = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            value = self._parse_value()
            fields.append(FieldNode(key=key, value=value))
            if self.current.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RBRACE)
        return fields

    def _parse_normalization_block(self) -> NormalizationOpts:
        self.consume(TokenType.LBRACE)
        opts = NormalizationOpts(strategy="ZERO_DISCRETENESS")
        while self.current.type != TokenType.RBRACE:
            key = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.ASSIGN)
            value = self._parse_value()
            if key == "normalization":
                opts.strategy = str(value)
            elif key == "resonance_check":
                opts.resonance_check = str(value)
            else:
                opts.extra[key] = value
            if self.current.type == TokenType.COMMA:
                self.consume(TokenType.COMMA)
        self.consume(TokenType.RBRACE)
        return opts

    def _parse_value(self) -> Any:
        tok = self.current
        if tok.type == TokenType.NUMBER:
            self.pos += 1
            return float(tok.value) if "." in tok.value else int(tok.value)
        if tok.type == TokenType.HZ:
            self.pos += 1
            return float(tok.value.replace("Hz", ""))
        if tok.type == TokenType.STRING:
            self.pos += 1
            return tok.value
        if tok.type == TokenType.BOOLEAN:
            self.pos += 1
            return tok.value == "true"
        if tok.type in (TokenType.IDENTIFIER, TokenType.ZERO_DISCRETENESS,
                        TokenType.SCHUMANN_BASE, TokenType.PARASITE_FILTER):
            self.pos += 1
            return tok.value
        raise ParseError(f"Unexpected value token", tok)

    def _parse_path(self) -> str:
        parts = [self.consume(TokenType.IDENTIFIER).value]
        while self.current.type == TokenType.DOT:
            self.consume(TokenType.DOT)
            parts.append(self.consume(TokenType.IDENTIFIER).value)
        return ".".join(parts)


def parse(source: str) -> ProgramNode:
    tokens = tokenize(source)
    return HarmonyParser(tokens).parse()
