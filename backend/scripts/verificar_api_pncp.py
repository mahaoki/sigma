import requests

BASE_URL = "https://pncp.gov.br/api/consulta/v1/contratacoes"

MODALIDADES = {
    1: "Leilão - Eletrônico",
    2: "Diálogo Competitivo",
    3: "Concurso",
    4: "Concorrência - Eletrônica",
    5: "Concorrência - Presencial",
    6: "Pregão - Eletrônico",
    7: "Pregão - Presencial",
    8: "Dispensa",
    9: "Inexigibilidade",
    10: "Manifestação de Interesse",
    11: "Pré-qualificação",
    12: "Credenciamento",
    13: "Leilão - Presencial"
}

def consultar(endpoint: str, modalidade: int, data: str, pagina: int = 1) -> int:
    params = {
        "codigoModalidadeContratacao": modalidade,
        "dataInicial": data,
        "dataFinal": data,
        "pagina": pagina
    }

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
        if response.status_code == 204:
            return 0  # resposta sem conteúdo (No Content)
        data = response.json()
        return data.get("totalRegistros", 0)
    except Exception as e:
        print(f"[ERRO] {endpoint} - Modalidade {modalidade}: {e}")
        return 0  # ✅ retorna 0 no lugar de -1 para manter a tabela limpa


def comparar(data: str):
    print(f"\n🔍 Comparando contratações no período {data}...\n")
    print(f"{'Modalidade':<32} {'Publicações':>12} {'Atualizações':>14}")
    print("-" * 62)

    total_pub = total_atu = 0

    for cod, nome in MODALIDADES.items():
        pub = consultar("publicacao", cod, data)
        atu = consultar("atualizacao", cod, data)

        total_pub += pub
        total_atu += atu

        print(f"{nome:<32} {pub:>12} {atu:>14}")

    print("-" * 62)
    print(f"{'TOTAL':<32} {total_pub:>12} {total_atu:>14}\n")

if __name__ == "__main__":
    data = input("Informe a data (YYYYMMDD): ").strip()

    if not data.isdigit() or len(data) != 8:
        print("⚠️  Data inválida. Use o formato YYYYMMDD.")
    else:
        comparar(data)
