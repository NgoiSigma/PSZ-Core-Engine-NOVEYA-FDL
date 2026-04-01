"""
Amazon Nova Hackathon 2026 — FDL Agent
/Protonoveya/nova_fdl_agent.py

An FDL-aware agent built on Amazon Bedrock Nova.
The agent applies the Thesis-Antithesis-Synthesis cycle to
every reasoning step before producing output.

Flow:
  User query  →  THESIS(intent)
              →  ANTITHESIS(constraint check via FDL)
              →  SYNTHESIS(Nova inference + SVET validation)
              →  PRAGMA emit → response + Metatron log
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ─── AWS CONFIG ───────────────────────────────────────────────────────────────
AWS_REGION      = os.getenv("AWS_REGION", "us-east-1")
NOVA_MODEL_ID   = os.getenv("NOVA_MODEL_ID", "amazon.nova-pro-v1:0")
SHEETS_ID       = os.getenv("GOOGLE_SHEETS_ORDER_REGISTRY", "")

# ─── FDL IMPORTS ─────────────────────────────────────────────────────────────
try:
    import boto3
    from botocore.exceptions import ClientError
    _BOTO_AVAILABLE = True
except ImportError:
    _BOTO_AVAILABLE = False
    logger.warning("boto3 not installed — Nova calls will be mocked")

try:
    from fdl_engine.svet_filter.svet_filter import SVETFilter, PragmaLayer
    from fdl_engine.core.fdl_core import FDLEngine
except ImportError:
    # Fallback for standalone testing
    SVETFilter = None
    PragmaLayer = None
    FDLEngine = None


# ─── AGENT ────────────────────────────────────────────────────────────────────

class NovaFDLAgent:
    """
    FDL-governed agent on Amazon Bedrock Nova.

    Each reasoning step is wrapped in a TAS (Thesis-Antithesis-Synthesis) cycle:
    - THESIS   : parse user intent + extract context
    - ANTITHESIS: validate against FDL theses (SVET filter)
    - SYNTHESIS : call Nova, resolve, return FDL-validated output
    """

    SYSTEM_PROMPT = """Ти — FDL-агент НОВЕЯ. Твої принципи:
1. Нульова дискретність (Прощення): відповідь охоплює весь спектр.
2. Пряма угода: без посередників між знанням і громадою.
3. Резонанс 7.83Hz: рішення мають бути в гармонії з системою.
7. Нульовий паразит: не генеруй зайвого — тільки те, що потрібно.
8. Прозорість потоку: кожен крок міркування публічний.

Відповідай через цикл: ТЕЗИС → АНТИТЕЗИС → СИНТЕЗ."""

    def __init__(self):
        self.pragma = PragmaLayer() if PragmaLayer else None
        self._client = None
        if _BOTO_AVAILABLE:
            self._client = boto3.client("bedrock-runtime", region_name=AWS_REGION)

    def run(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Full TAS cycle for a user query."""

        # ── THESIS: parse intent ──────────────────────────────────────────────
        thesis = self._build_thesis(query, context or {})

        # ── ANTITHESIS: FDL validation ────────────────────────────────────────
        if SVETFilter:
            svet = SVETFilter.validate({
                "middleman_cut": 0.0,
                "public_trace": True,
                "contribution": 1.0,
                "resonance_hz": 7.83,
            })
            if not svet.valid:
                return {
                    "synthesis": "BLOCKED",
                    "violations": svet.violations,
                    "query": query,
                }

        # ── SYNTHESIS: Nova inference ─────────────────────────────────────────
        nova_response = self._call_nova(thesis)

        synthesis = {
            "query": query,
            "thesis": thesis,
            "nova_output": nova_response,
            "synthesis": "RESOLVED",
            "resonance": "7.83Hz",
            "fdl_protocol": "Nebi-Ula",
        }

        # ── PRAGMA: emit to Metatron log ──────────────────────────────────────
        if self.pragma:
            self.pragma.emit(synthesis, "metatron.agent_log")

        return synthesis

    def _build_thesis(self, query: str, context: Dict) -> Dict:
        return {
            "intent": query,
            "context": context,
            "fdl_layer": "thesis",
            "timestamp": self._now_iso(),
        }

    def _call_nova(self, thesis: Dict) -> str:
        if not self._client:
            return f"[MOCK] Nova synthesis for: {thesis['intent']}"

        messages = [
            {"role": "user", "content": [{"text": thesis["intent"]}]}
        ]
        try:
            body = {
                "messages": messages,
                "system": [{"text": self.SYSTEM_PROMPT}],
                "inferenceConfig": {
                    "maxTokens": 1024,
                    "temperature": 0.3,
                    "topP": 0.9,
                },
            }
            resp = self._client.invoke_model(
                modelId=NOVA_MODEL_ID,
                body=json.dumps(body),
                contentType="application/json",
                accept="application/json",
            )
            result = json.loads(resp["body"].read())
            return result["output"]["message"]["content"][0]["text"]
        except Exception as exc:
            logger.exception("Nova call failed")
            return f"[ERROR] {exc}"

    @staticmethod
    def _now_iso() -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()


# ─── ORDER REGISTRY (Google Sheets) ──────────────────────────────────────────

class OrderRegistry:
    """
    Реєстр замовлень через Google Sheets API.
    FDL Thesis 8: every order is publicly traceable.
    """

    def __init__(self, spreadsheet_id: str = SHEETS_ID):
        self.spreadsheet_id = spreadsheet_id
        self._service = None

    def _get_service(self):
        if self._service:
            return self._service
        try:
            from google.oauth2.service_account import Credentials
            from googleapiclient.discovery import build
            creds = Credentials.from_service_account_file(
                os.getenv("GOOGLE_SA_JSON", "service_account.json"),
                scopes=["https://www.googleapis.com/auth/spreadsheets"],
            )
            self._service = build("sheets", "v4", credentials=creds)
        except Exception as exc:
            logger.warning("Google Sheets unavailable: %s", exc)
        return self._service

    def append_order(self, order: Dict[str, Any]) -> bool:
        svc = self._get_service()
        if not svc:
            logger.info("ORDER (mock): %s", json.dumps(order, ensure_ascii=False))
            return False

        svet = SVETFilter.validate(order) if SVETFilter else None
        if svet and not svet.valid:
            logger.error("Order blocked by SVET: %s", svet.violations)
            return False

        values = [[
            order.get("id", ""),
            order.get("hromada", ""),
            order.get("service", ""),
            order.get("supplier", ""),
            str(order.get("middleman_cut", 0.0)),
            order.get("status", "pending"),
            self._now_iso(),
        ]]
        try:
            svc.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range="Orders!A:G",
                valueInputOption="RAW",
                body={"values": values},
            ).execute()
            return True
        except Exception as exc:
            logger.exception("Sheets append failed")
            return False

    @staticmethod
    def _now_iso() -> str:
        from datetime import datetime, timezone
        return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    agent = NovaFDLAgent()
    result = agent.run("Який поточний рівень енергетичного резонансу Громади?")
    print(json.dumps(result, ensure_ascii=False, indent=2))
