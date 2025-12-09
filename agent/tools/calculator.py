# agent/tools/calculator.py
import re
_CALC_RE = re.compile(r"^(?:calc|calculate|calculator)\s*[:\-]?\s*([0-9+\-*/().\s]+)$", re.I)
def extract_expression(text: str):
    if not text:
        return None
    m = _CALC_RE.search(text.strip())
    if m:
        return m.group(1).strip()
    if re.fullmatch(r"[0-9+\-*/ ().]+", text.strip()):
        return text.strip()
    return None
def safe_eval_math(expr: str):
    expr = expr.strip()
    if not re.fullmatch(r"[0-9+\-*/ ().]+", expr):
        return {"error": "unsafe expression or unsupported characters"}
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return {"result": str(result)}
    except Exception as e:
        return {"error": f"evaluation error: {e}"}
