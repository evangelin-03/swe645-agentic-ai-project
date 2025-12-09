# agent/langgraph_config.py
"""
SimpleGraph with calculator tool routing and explicit system instruction.
Exports build_agent_graph(client, model_name) for compatibility with main.py
"""
import re
import os
from typing import Optional

# import calculator tool (local)
from agent.tools.calculator import extract_expression, safe_eval_math

# pattern we expect the LLM to use to request the calculator.
_TOOL_CALL_RE = re.compile(r"(?:CALCULATE|CALC|calculator)\s*[:\-]?\s*([0-9+\-*/().\s]+)", re.I)

# System instruction we prepend to every prompt to bias model behavior.
SYSTEM_INSTRUCTION = (
    "System instruction: You are an assistant that can plan and call tools. "
    "When a user requests a calculation, respond using EXACTLY the format: "
    '"CALCULATE: <expression>" with no extra commentary, or return just the expression (e.g. "1+4"). '
    "Only use the calculator for arithmetic; otherwise provide a concise plan. "
    "Do not add extra text when requesting the calculator."
)

class SimpleGraph:
    def __init__(self, client=None, model_name=None):
        self.client = client
        # allow overriding via env var or explicit param
        self.model = model_name or os.getenv("GEMINI_MODEL") or "models/gemini-2.5-pro"

    def _call_llm(self, prompt: str) -> str:
        """
        Call Gemini if available. Prepend a system instruction to encourage
        tool-call formatting for calculations.
        Returns text output (string).
        """
        full_prompt = SYSTEM_INSTRUCTION + "\n\nUser prompt:\n" + prompt
        if self.client is None:
            # Simulated planning if no client
            return f"SIMULATED PLAN for prompt: {prompt}\n1) If expression provided then calculator.\n2) Otherwise answer normally."
        try:
            resp = self.client.models.generate_content(model=self.model, contents=full_prompt)
            # try common response shapes
            if hasattr(resp, "text") and resp.text:
                return resp.text
            try:
                return resp.output[0].content[0].text
            except Exception:
                return str(resp)
        except Exception as e:
            return f"(Gemini API error: {e})"

    def _detect_tool_call(self, text: str) -> Optional[str]:
        """
        Detect if LLM wants the calculator. If so, return the expression string.
        """
        if not text:
            return None
        # direct pattern like "CALCULATE: 1+2" or "calc: 1+2"
        m = _TOOL_CALL_RE.search(text)
        if m:
            return m.group(1).strip()
        # fallback: the calculator helper can extract if the LLM returns just an expression
        expr = extract_expression(text)
        return expr

    def run(self, state: dict) -> dict:
        """
        state contains at least "prompt": str
        Returns dict with keys like "plan" and optional "exec_result".
        """
        prompt = state.get("prompt", "")
        # 1) Ask the LLM for a plan/answer
        plan_text = self._call_llm(prompt)

        # 2) Detect whether the plan indicates a calculator invocation
        expr = self._detect_tool_call(plan_text)

        if expr:
            # 3) Call the calculator tool and return immediate exec_result
            calc_out = safe_eval_math(expr)
            if "result" in calc_out:
                return {"plan": f"Calculator executed: {expr}", "exec_result": calc_out["result"]}
            else:
                return {"plan": f"Calculator error", "exec_result": calc_out.get("error", "unknown error")}
        else:
            # No tool requested — return plan for human review/execution
            return {"plan": plan_text}

# Backwards-compatible factory used by main.py
def build_agent_graph(client=None, model_name=None):
    return SimpleGraph(client=client, model_name=model_name)
