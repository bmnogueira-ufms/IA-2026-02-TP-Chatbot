"""Análise exploratória do CSV de treino do Rui.

Uso:
    python analise_exploratoria.py dados/treino.csv
    python analise_exploratoria.py dados/treino.csv --saida figuras_eda

Espera colunas: texto, intencao, origem (humano/llm). A coluna escopo é
derivada de intencao se não existir.
Gera: gráficos PNG + resumo.md na pasta de saída e imprime tudo no terminal.
"""
import argparse
import os
import re
import unicodedata
from collections import Counter

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STOPWORDS = set("""a o as os um uma uns umas de do da dos das em no na nos nas por para pra com sem
e ou que se te me eu tu voce vc ele ela nos eles elas meu minha seu sua isso isto esse essa este esta
ao aos la ja so mas ate sobre tem ter tinha ha vai vou ser sao eh e é foi qual quais como onde quando
quanto quanta quem tambem muito mais menos hoje""".split())

# vocabulário do domínio, usado só para achar negativos difíceis de forma simples
VOCAB_DOMINIO = set("""ru restaurante refeicao almoco janta jantar cafe horario horarios cardapio
ficha fichas subsidio preco valor comer comida prato bandeja pix""".split())


def norm(s):
    s = unicodedata.normalize("NFKD", str(s).lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", " ", s)


def tokens(s):
    return [t for t in norm(s).split() if t not in STOPWORDS and len(t) > 1]


def escopo_de(intencao):
    return {"chitchat": "chitchat", "fora_dominio": "fora_dominio"}.get(intencao, "dominio")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--saida", default="figuras_eda")
    ap.add_argument("--top", type=int, default=10, help="palavras por intenção")
    ap.add_argument("--n-neg", type=int, default=15, help="negativos difíceis a mostrar")
    a = ap.parse_args()

    os.makedirs(a.saida, exist_ok=True)
    df = pd.read_csv(a.csv).dropna(subset=["texto", "intencao"]).copy()
    if "escopo" not in df.columns:
        df["escopo"] = df["intencao"].map(escopo_de)
    if "origem" not in df.columns:
        df["origem"] = "desconhecida"
    df["n_chars"] = df["texto"].str.len()
    df["n_palavras"] = df["texto"].str.split().str.len()

    md = [f"# Análise exploratória\n\nTotal de exemplos: **{len(df)}**\n"]

    # 1. Distribuição
    md.append("## 1. Distribuição por classe e origem\n")
    t = pd.crosstab(df["intencao"], df["origem"], margins=True)
    md.append(t.to_markdown() + "\n")
    t.drop("All").drop(columns="All").plot(kind="barh", stacked=True, figsize=(8, 4))
    plt.title("Exemplos por intenção e origem")
    plt.tight_layout()
    plt.savefig(f"{a.saida}/01_distribuicao.png", dpi=150)
    plt.close()

    # 2. Tamanho das mensagens
    md.append("## 2. Tamanho das mensagens por classe\n")
    tam = df.groupby("intencao")[["n_palavras", "n_chars"]].agg(["mean", "median", "max"]).round(1)
    md.append(tam.to_markdown() + "\n")
    ordem = df.groupby("intencao")["n_palavras"].median().sort_values().index
    df.boxplot(column="n_palavras", by="intencao", positions=None, figsize=(9, 4.5), rot=30)
    plt.suptitle("")
    plt.title("Palavras por mensagem, por intenção")
    plt.ylabel("nº de palavras")
    plt.tight_layout()
    plt.savefig(f"{a.saida}/02_tamanho_por_intencao.png", dpi=150)
    plt.close()

    # 3. Palavras mais frequentes por intenção
    md.append(f"## 3. Palavras mais frequentes por intenção (top {a.top}, sem stopwords)\n")
    for it, g in df.groupby("intencao"):
        c = Counter(w for t_ in g["texto"] for w in tokens(t_))
        top = ", ".join(f"{w} ({n})" for w, n in c.most_common(a.top))
        md.append(f"- **{it}**: {top}")
    md.append("")

    # 4. Negativos difíceis (verificação leve)
    md.append("## 4. Exemplos de negativos difíceis (fora_dominio parecidos com domínio)\n")
    md.append("Critério simples: fora_dominio com maior similaridade TF-IDF a algum exemplo de "
              "domínio, ou que contém vocabulário do RU. Sem verificação manual.\n")
    fora = df[df["intencao"] == "fora_dominio"].reset_index(drop=True)
    dom = df[df["escopo"] == "dominio"].reset_index(drop=True)
    if len(fora) and len(dom):
        vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(2, 4)).fit(df["texto"].map(norm))
        sim = cosine_similarity(vec.transform(fora["texto"].map(norm)),
                                vec.transform(dom["texto"].map(norm)))
        fora["sim_max"] = sim.max(axis=1)
        fora["parecido_com"] = dom["texto"].iloc[sim.argmax(axis=1)].values
        fora["tem_vocab"] = fora["texto"].map(lambda s: bool(VOCAB_DOMINIO & set(norm(s).split())))
        dif = fora.sort_values(["tem_vocab", "sim_max"], ascending=False).head(a.n_neg)
        md.append("| fora_dominio | mais parecido com (domínio) | sim. | vocab RU |")
        md.append("|---|---|---|---|")
        for _, r in dif.iterrows():
            md.append(f"| {r.texto} | {r.parecido_com} | {r.sim_max:.2f} | {'sim' if r.tem_vocab else 'não'} |")
        md.append(f"\nfora_dominio com vocabulário do RU: **{int(fora['tem_vocab'].sum())}** de {len(fora)}.\n")
    else:
        md.append("Sem exemplos suficientes de fora_dominio ou domínio.\n")

    # 5. Humano vs LLM
    md.append("## 5. Frases humanas vs LLM\n")
    if df["origem"].nunique() > 1 and {"humano", "llm"} <= set(df["origem"]):
        res = df.groupby("origem")[["n_palavras", "n_chars"]].agg(["mean", "median"]).round(1)
        md.append(res.to_markdown() + "\n")

        def taxa(f):
            return df.groupby("origem")["texto"].apply(lambda s: s.map(f).mean()).round(3)

        feats = pd.DataFrame({
            "termina com ?": taxa(lambda s: s.strip().endswith("?")),
            "tem maiúscula inicial": taxa(lambda s: s.strip()[:1].isupper()),
            "tem acento": taxa(lambda s: any(unicodedata.combining(c) or c == "ç"
                                                   for c in unicodedata.normalize("NFKD", s.lower()))),
            "tem pontuação final": taxa(lambda s: s.strip()[-1:] in ".!?"),
            "menciona 'RU'": taxa(lambda s: bool(re.search(r"\bru\b", s.lower()))),
            "tem gíria/abrev. (vc, pq, tb, blz, tmj, kk)":
                taxa(lambda s: bool(re.search(r"\b(vc|pq|tb|blz|tmj|kk+|vlw|td|q)\b", s.lower()))),
        })
        md.append("Proporção de frases com cada traço:\n")
        md.append(feats.to_markdown() + "\n")

        vocab = {o: Counter(w for t_ in g["texto"] for w in tokens(t_)) for o, g in df.groupby("origem")}
        for o in ("humano", "llm"):
            outro = "llm" if o == "humano" else "humano"
            tot_o, tot_x = sum(vocab[o].values()), sum(vocab[outro].values())
            score = {w: (n / tot_o) / ((vocab[outro].get(w, 0) + 1) / tot_x)
                     for w, n in vocab[o].items() if n >= 3}
            top = sorted(score, key=score.get, reverse=True)[:a.top]
            md.append(f"- Palavras mais típicas de **{o}** (vs {outro}): {', '.join(top)}")
        md.append("")

        cruz = pd.crosstab(df["intencao"], df["origem"], normalize="columns").round(3)
        md.append("Proporção de cada intenção dentro de cada origem:\n")
        md.append(cruz.to_markdown() + "\n")
        df.boxplot(column="n_palavras", by="origem", figsize=(5, 4))
        plt.suptitle("")
        plt.title("Palavras por mensagem: humano vs LLM")
        plt.tight_layout()
        plt.savefig(f"{a.saida}/03_humano_vs_llm.png", dpi=150)
        plt.close()
    else:
        md.append("A coluna origem não tem as duas origens (humano e llm); seção ignorada.\n")

    texto = "\n".join(md)
    with open(f"{a.saida}/resumo.md", "w", encoding="utf-8") as f:
        f.write(texto)
    print(texto)
    print(f"\nArquivos salvos em: {a.saida}/")


if __name__ == "__main__":
    main()
