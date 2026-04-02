import streamlit as st
from datetime import date


def load_data() -> dict:
    return st.session_state["caixinhas_data"]


def save_data(data: dict) -> None:
    pass  # dados já estão em session_state por referência


def get_month_key(year: int, month: int) -> str:
    return f"{year}-{month:02d}"


def ensure_month(data: dict, key: str) -> None:
    if key not in data:
        data[key] = {"entradas": [], "gastos": []}


def add_entrada(data: dict, key: str, descricao: str, valor: float, data_tx: str) -> None:
    ensure_month(data, key)
    data[key]["entradas"].append(
        {"data": data_tx, "descricao": descricao, "valor": valor, "tipo": "entrada"}
    )


def add_gasto(
    data: dict, key: str, descricao: str, categoria: str, valor: float, data_tx: str
) -> None:
    ensure_month(data, key)
    data[key]["gastos"].append(
        {
            "data": data_tx,
            "descricao": descricao,
            "categoria": categoria,
            "valor": valor,
            "tipo": "gasto",
        }
    )


def delete_transaction(data: dict, key: str, tipo: str, index: int) -> None:
    """Remove uma transação pelo índice."""
    if key in data and tipo in data[key]:
        transactions = data[key][tipo]
        if 0 <= index < len(transactions):
            transactions.pop(index)


def get_month_summary(data: dict, key: str) -> dict:
    if key not in data:
        return {"total_entradas": 0.0, "total_gastos": 0.0, "saldo": 0.0, "por_categoria": {}}

    entradas = sum(t["valor"] for t in data[key].get("entradas", []))
    gastos = data[key].get("gastos", [])
    total_gastos = sum(t["valor"] for t in gastos)

    por_categoria: dict[str, float] = {}
    for g in gastos:
        cat = g["categoria"]
        por_categoria[cat] = por_categoria.get(cat, 0.0) + g["valor"]

    return {
        "total_entradas": entradas,
        "total_gastos": total_gastos,
        "saldo": entradas - total_gastos,
        "por_categoria": por_categoria,
    }


def get_history(data: dict, last_n: int = 12) -> list[dict]:
    """Retorna lista de resumos mensais ordenados, até last_n meses."""
    keys = sorted(data.keys())[-last_n:]
    result = []
    for key in keys:
        summary = get_month_summary(data, key)
        summary["mes"] = key
        result.append(summary)
    return result


def get_all_months(data: dict) -> list[str]:
    return sorted(data.keys())
