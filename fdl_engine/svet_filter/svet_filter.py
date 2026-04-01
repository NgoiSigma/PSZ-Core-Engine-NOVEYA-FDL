"""
Оболочка СВЕТ — SVET Filter
"Да будет Свет" (Бут. 1:3)

The SVET (Light Shell) is the absolute transparency layer.
Every action in the NOVEYA system passes through this filter.
If it cannot be shown to every citizen — it does not happen.

This module implements the PragmaLayer gateway for Harmony programs:
synthesized values are validated here before being emitted to targets.
"""

from __future__ import annotations
import logging
import math
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

SCHUMANN_HZ    = 7.83
FREQ_432_HZ    = 432.0       # Creative resonance (Amazon Nova integration)
TOLERANCE_HZ   = 0.5


@dataclass
class SVETResult:
    valid: bool
    synthesis: str           # "CLEAR" | "VIOLATION" | "ANOMALY"
    violations: List[Dict]
    coherence: float         # 0.0 → 1.0
    frequency_status: str

    def to_dict(self) -> Dict:
        return {
            "valid": self.valid,
            "synthesis": self.synthesis,
            "violations": self.violations,
            "coherence": round(self.coherence, 4),
            "frequency_status": self.frequency_status,
        }


class SVETFilter:
    """
    Stateless filter — validates any action dict against FDL theses.

    Usage:
        result = SVETFilter.validate({
            "middleman_cut": 0.0,
            "public_trace": True,
            "contribution": 1.0,
            "resonance_hz": 7.83,
        })
        assert result.synthesis == "CLEAR"
    """

    @staticmethod
    def validate(action: Dict[str, Any]) -> SVETResult:
        violations: List[Dict] = []

        # Thesis 2: no middlemen
        cut = float(action.get("middleman_cut", 0.0))
        if cut > 0.0:
            violations.append({
                "thesis": 2,
                "rule": "Пряма угода",
                "detail": f"middleman_cut={cut*100:.1f}% — посередник заборонений",
            })

        # Thesis 7: no parasites
        contrib = float(action.get("contribution", 1.0))
        if contrib <= 0.0:
            violations.append({
                "thesis": 7,
                "rule": "Нульовий паразит",
                "detail": "contribution=0 — паразитна дія видаляється",
            })

        # Thesis 8: public trace
        if not action.get("public_trace", True):
            violations.append({
                "thesis": 8,
                "rule": "Прозорість потоку",
                "detail": "public_trace=False — дія не публічна",
            })

        # Thesis 1: discreteness must be zero
        disc = float(action.get("discreteness_level", 0.0))
        if disc > 0.0:
            violations.append({
                "thesis": 1,
                "rule": "Нульова дискретність",
                "detail": f"discreteness_level={disc} > 0",
            })

        # Thesis 3: resonance check
        hz = float(action.get("resonance_hz", SCHUMANN_HZ))
        delta = abs(hz - SCHUMANN_HZ)
        coherence = math.exp(-delta / SCHUMANN_HZ)
        freq_status = "RESONANT" if delta <= TOLERANCE_HZ else "ANOMALY"

        if delta > TOLERANCE_HZ:
            violations.append({
                "thesis": 3,
                "rule": "Резонанс Шумана",
                "detail": f"hz={hz} відхиляється від 7.83 на {delta:.3f}Hz",
            })

        valid = len(violations) == 0
        synthesis = "CLEAR" if valid else "VIOLATION"
        if freq_status == "ANOMALY" and valid:
            synthesis = "ANOMALY"

        if not valid:
            logger.warning("СВЕТ: %d порушень | %s", len(violations), violations)

        return SVETResult(
            valid=valid,
            synthesis=synthesis,
            violations=violations,
            coherence=coherence,
            frequency_status=freq_status,
        )

    @staticmethod
    def filter_stream(records: List[Dict]) -> Dict[str, Any]:
        """
        Apply SVET to a batch of records.
        Returns clean records + report.
        """
        clean = []
        blocked = []
        for r in records:
            result = SVETFilter.validate(r)
            if result.valid:
                r["_svet_coherence"] = result.coherence
                clean.append(r)
            else:
                r["_svet_violations"] = result.violations
                blocked.append(r)

        return {
            "total": len(records),
            "passed": len(clean),
            "blocked": len(blocked),
            "clean_records": clean,
            "blocked_records": blocked,
        }


class PragmaLayer:
    """
    Executes PRAGMA emit() statements from a parsed Harmony program.
    Routes synthesized values through SVET, then to registered targets.
    """

    def __init__(self):
        self._targets: Dict[str, Any] = {}

    def register_target(self, path: str, handler):
        """Register a target handler for a dot-path (e.g. 'metatron.kpi_metric')."""
        self._targets[path] = handler
        logger.info("PragmaLayer: registered target '%s'", path)

    def emit(self, value: Any, destination: str, context: Optional[Dict] = None) -> SVETResult:
        """
        Emit a synthesized value to a destination after SVET validation.
        """
        ctx = context or {}
        ctx.setdefault("public_trace", True)
        ctx.setdefault("contribution", 1.0)
        ctx.setdefault("middleman_cut", 0.0)

        result = SVETFilter.validate(ctx)

        if not result.valid:
            logger.error("PragmaLayer: SVET blocked emit to '%s'", destination)
            return result

        handler = self._targets.get(destination)
        if handler:
            handler(value, destination)
            logger.info("PragmaLayer: emitted to '%s' | coherence=%.4f", destination, result.coherence)
        else:
            logger.warning("PragmaLayer: no handler for '%s' — value logged only", destination)

        return result
