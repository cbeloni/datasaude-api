import ast
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import delete, select

from api.ibge.v1.request.ibge import IbgeFormulaCustomizadaCreate
from app.ibge.models.ibge_formula_customizada_model import IbgeFormulaCustomizada
from core.db.session import session


_ALLOWED_BIN_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod)
_ALLOWED_UNARY_OPS = (ast.UAdd, ast.USub)


def _sanitize_formula_name(name: str) -> str:
    return name.strip().lower().replace(' ', '_')


def _safe_eval_formula(expression: str, values: dict):
    normalized_values = {str(key).lower(): value for key, value in values.items()}

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):
            return Decimal(str(node.n))
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return Decimal(str(node.value))
        if isinstance(node, ast.BinOp) and isinstance(node.op, _ALLOWED_BIN_OPS):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                if right == 0:
                    raise ZeroDivisionError('division by zero')
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return left % right
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, _ALLOWED_UNARY_OPS):
            value = _eval(node.operand)
            return value if isinstance(node.op, ast.UAdd) else -value
        if isinstance(node, ast.Name):
            raw_value = values.get(node.id)
            if raw_value is None:
                raw_value = normalized_values.get(node.id.lower())
            if raw_value is None:
                return Decimal('0')
            return Decimal(str(raw_value))
        raise ValueError('expressão inválida')

    tree = ast.parse(expression, mode='eval')
    return _eval(tree)


async def listar_formulas_customizadas():
    query = select(IbgeFormulaCustomizada).where(IbgeFormulaCustomizada.ativa.is_(True)).order_by(IbgeFormulaCustomizada.nome)
    rows = (await session.execute(query)).scalars().all()
    return rows


async def criar_formula_customizada(payload: IbgeFormulaCustomizadaCreate):
    formula = IbgeFormulaCustomizada(nome=payload.nome.strip(), formula=payload.formula.strip(), ativa=True)
    session.add(formula)
    await session.commit()
    await session.refresh(formula)
    return formula


async def remover_formula_customizada(formula_id: int):
    await session.execute(delete(IbgeFormulaCustomizada).where(IbgeFormulaCustomizada.id == formula_id))
    await session.commit()


async def aplicar_formulas_customizadas(payload: dict):
    formulas = await listar_formulas_customizadas()
    for formula in formulas:
        field_name = _sanitize_formula_name(formula.nome)
        try:
            result = _safe_eval_formula(formula.formula, payload)
            payload[field_name] = result.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except Exception:
            payload[field_name] = None

    return payload
