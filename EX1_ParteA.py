import asyncio
from pathlib import Path
from time import perf_counter


DIRETORIO = Path("/dados/arquivos")


def contar_linhas_e_palavras(caminho):
    quantidade_linhas = 0
    quantidade_palavras = 0

    with caminho.open("r", encoding="utf-8", errors="ignore") as arquivo:
        for linha in arquivo:
            quantidade_linhas += 1
            quantidade_palavras += len(linha.split())

    return caminho.name, quantidade_linhas, quantidade_palavras


async def processar_arquivo(caminho):
    return await asyncio.to_thread(contar_linhas_e_palavras, caminho)


async def main():
    inicio = perf_counter()

    arquivos = sorted(caminho for caminho in DIRETORIO.iterdir() if caminho.is_file())

    tarefas = [asyncio.create_task(processar_arquivo(arquivo)) for arquivo in arquivos]
    resultados = await asyncio.gather(*tarefas)

    for nome, linhas, palavras in resultados:
        print(nome)
        print(f"Linhas: {linhas}")
        print(f"Palavras: {palavras}")
        print()

    tempo_total = perf_counter() - inicio
    print(f"Tempo total: {tempo_total:.2f} segundos")


if __name__ == "__main__":
    asyncio.run(main())