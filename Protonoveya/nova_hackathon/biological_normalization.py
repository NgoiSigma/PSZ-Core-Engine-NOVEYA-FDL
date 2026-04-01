"""
Biological Normalization — "Clover Property" (Властивість конюшини)
/Protonoveya/biological_normalization.py

The Clover Property: like a three-leaf clover, every system state
has three aspects that must be simultaneously alive:
  🍀 Leaf 1 — RESONANCE    (frequency coherence)
  🍀 Leaf 2 — FLOW         (unobstructed transfer, no parasites)
  🍀 Leaf 3 — SYNTHESIS    (dialectical resolution, not suppression)

When all three leaves are healthy, the system is in biological norm.
A single wilted leaf triggers normalization.

Basis: FDL Protocol Nebi-Ula, Thesis 9 (Self-healing)
       + meridian theory of continuous information flow
       + 432 Hz creative frequency alignment
"""

from __future__ import annotations
import math
import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)

SCHUMANN_HZ     = 7.83
CREATIVE_HZ     = 432.0
TOLERANCE       = 0.5
GOLDEN_RATIO    = 1.6180339887    # φ — growth coefficient


@dataclass
class CloverLeaf:
    name: str          # resonance | flow | synthesis
    value: float       # 0.0 → 1.0 (health score)
    status: str        # HEALTHY | WILTED | RECOVERING
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_healthy(self) -> bool:
        return self.value >= 0.618    # φ - 1 threshold


@dataclass
class CloverState:
    resonance: CloverLeaf
    flow: CloverLeaf
    synthesis: CloverLeaf

    @property
    def overall_health(self) -> float:
        """Geometric mean — all three leaves must be alive."""
        return (self.resonance.value * self.flow.value * self.synthesis.value) ** (1/3)

    @property
    def biological_norm(self) -> bool:
        return all([
            self.resonance.is_healthy,
            self.flow.is_healthy,
            self.synthesis.is_healthy,
        ])

    def to_dict(self) -> Dict:
        return {
            "overall_health": round(self.overall_health, 4),
            "biological_norm": self.biological_norm,
            "leaves": {
                "resonance":  self._leaf_dict(self.resonance),
                "flow":       self._leaf_dict(self.flow),
                "synthesis":  self._leaf_dict(self.synthesis),
            },
        }

    @staticmethod
    def _leaf_dict(leaf: CloverLeaf) -> Dict:
        return {"value": round(leaf.value, 4), "status": leaf.status, "details": leaf.details}


class BiologicalNormalizer:
    """
    Measures and restores biological norm via the Clover Property.

    Each normalization cycle:
    1. Assess all three clover leaves
    2. Identify wilted leaf(ves)
    3. Apply targeted normalization
    4. Verify synthesis restored (Thesis 9: self-healing)
    """

    def assess(self, system_state: Dict[str, Any]) -> CloverState:
        """Assess the biological state of the system."""
        return CloverState(
            resonance  = self._assess_resonance(system_state),
            flow       = self._assess_flow(system_state),
            synthesis  = self._assess_synthesis(system_state),
        )

    def normalize(self, system_state: Dict[str, Any]) -> Tuple[CloverState, Dict]:
        """
        Full normalization cycle.
        Returns (post-normalization state, normalization report).
        """
        before = self.assess(system_state)
        actions = []

        if not before.resonance.is_healthy:
            system_state = self._restore_resonance(system_state)
            actions.append("resonance_restored")

        if not before.flow.is_healthy:
            system_state = self._restore_flow(system_state)
            actions.append("flow_restored")

        if not before.synthesis.is_healthy:
            system_state = self._restore_synthesis(system_state)
            actions.append("synthesis_restored")

        after = self.assess(system_state)

        report = {
            "before_health": round(before.overall_health, 4),
            "after_health":  round(after.overall_health, 4),
            "biological_norm": after.biological_norm,
            "actions": actions,
            "thesis_9": "SELF_HEALED" if actions else "ALREADY_HEALTHY",
        }
        logger.info("BiologicalNorm: %s", report)
        return after, report

    # ── RESONANCE LEAF ────────────────────────────────────────────────────────
    def _assess_resonance(self, state: Dict) -> CloverLeaf:
        hz = float(state.get("resonance_hz", SCHUMANN_HZ))
        delta = abs(hz - SCHUMANN_HZ)
        # Secondary check: 432Hz creative alignment
        delta_creative = abs(hz - CREATIVE_HZ)
        # Coherence: primary Schumann + bonus for 432Hz proximity
        coherence = math.exp(-delta / SCHUMANN_HZ)
        if delta_creative < 5.0:
            coherence = min(1.0, coherence * GOLDEN_RATIO)

        health = coherence
        status = "HEALTHY" if health >= 0.618 else ("RECOVERING" if health >= 0.3 else "WILTED")
        return CloverLeaf("resonance", health, status, {
            "hz": hz, "delta_schumann": round(delta, 4),
            "delta_creative_432": round(delta_creative, 2),
        })

    def _restore_resonance(self, state: Dict) -> Dict:
        """Pull frequency back toward Schumann base."""
        hz = float(state.get("resonance_hz", SCHUMANN_HZ))
        # Gentle correction: move 30% toward Schumann
        corrected = hz + (SCHUMANN_HZ - hz) * 0.3
        state["resonance_hz"] = round(corrected, 4)
        logger.info("Resonance restored: %.4f → %.4f Hz", hz, corrected)
        return state

    # ── FLOW LEAF ─────────────────────────────────────────────────────────────
    def _assess_flow(self, state: Dict) -> CloverLeaf:
        cut = float(state.get("middleman_cut", 0.0))
        contrib = float(state.get("contribution_ratio", 1.0))
        parasite_count = int(state.get("parasite_count", 0))

        # Flow health: penalize middlemen and parasites
        flow = (1.0 - cut) * contrib * math.exp(-parasite_count * 0.1)
        flow = max(0.0, min(1.0, flow))
        status = "HEALTHY" if flow >= 0.618 else ("RECOVERING" if flow >= 0.3 else "WILTED")
        return CloverLeaf("flow", flow, status, {
            "middleman_cut": cut,
            "contribution_ratio": contrib,
            "parasite_count": parasite_count,
        })

    def _restore_flow(self, state: Dict) -> Dict:
        state["middleman_cut"] = 0.0
        state["parasite_count"] = 0
        state.setdefault("contribution_ratio", 1.0)
        logger.info("Flow restored: parasites removed, middleman_cut zeroed")
        return state

    # ── SYNTHESIS LEAF ────────────────────────────────────────────────────────
    def _assess_synthesis(self, state: Dict) -> CloverLeaf:
        disc = float(state.get("discreteness_level", 0.0))
        conflict_ratio = float(state.get("unresolved_conflicts", 0.0))

        # Synthesis health: penalize unresolved conflicts and discreteness
        synthesis = math.exp(-disc) * (1.0 - min(1.0, conflict_ratio))
        status = "HEALTHY" if synthesis >= 0.618 else ("RECOVERING" if synthesis >= 0.3 else "WILTED")
        return CloverLeaf("synthesis", synthesis, status, {
            "discreteness_level": disc,
            "unresolved_conflicts": conflict_ratio,
        })

    def _restore_synthesis(self, state: Dict) -> Dict:
        # Apply Zero Discreteness (Thesis 1)
        state["discreteness_level"] = 0.0
        state["unresolved_conflicts"] = 0.0
        logger.info("Synthesis restored: Zero Discreteness applied")
        return state


if __name__ == "__main__":
    import json
    norm = BiologicalNormalizer()

    # Unhealthy system state
    sick_state = {
        "resonance_hz": 10.5,        # anomaly
        "middleman_cut": 0.3,        # parasite
        "contribution_ratio": 0.4,
        "parasite_count": 3,
        "discreteness_level": 0.8,
        "unresolved_conflicts": 0.6,
    }

    after, report = norm.normalize(sick_state)
    print(json.dumps(report, indent=2))
    print(json.dumps(after.to_dict(), indent=2))
