# Análise exploratória

Total de exemplos: **1077**

## 1. Distribuição por classe e origem

| intencao     |   humano |   llm |   massive |   All |
|:-------------|---------:|------:|----------:|------:|
| cardapio     |       49 |    49 |         0 |    98 |
| chitchat     |      190 |     0 |         0 |   190 |
| fichas       |       46 |    49 |         0 |    95 |
| fora_dominio |      203 |    20 |       100 |   323 |
| geral        |       62 |    26 |         0 |    88 |
| horarios     |       50 |    43 |         0 |    93 |
| subsidio     |       56 |    41 |         0 |    97 |
| valores      |       45 |    48 |         0 |    93 |
| All          |      701 |   276 |       100 |  1077 |

## 2. Tamanho das mensagens por classe

| intencao     |   ('n_palavras', 'mean') |   ('n_palavras', 'median') |   ('n_palavras', 'max') |   ('n_chars', 'mean') |   ('n_chars', 'median') |   ('n_chars', 'max') |
|:-------------|-------------------------:|---------------------------:|------------------------:|----------------------:|------------------------:|---------------------:|
| cardapio     |                      8.5 |                          8 |                      23 |                  44   |                    38   |                  120 |
| chitchat     |                      3.5 |                          3 |                      13 |                  17.8 |                    16   |                   72 |
| fichas       |                      9.6 |                          9 |                      24 |                  51.7 |                    45   |                  118 |
| fora_dominio |                      7.6 |                          7 |                      32 |                  40.6 |                    37   |                  199 |
| geral        |                      9.8 |                          8 |                      23 |                  55.4 |                    44.5 |                  152 |
| horarios     |                      8.7 |                          7 |                      24 |                  45.1 |                    35   |                  123 |
| subsidio     |                     10.1 |                          9 |                      23 |                  58   |                    48   |                  145 |
| valores      |                     10.2 |                          9 |                      26 |                  55.7 |                    47   |                  152 |

## 3. Palavras mais frequentes por intenção (top 10, sem stopwords)

- **cardapio**: cardapio (33), almoco (24), ru (18), jantar (15), opcao (15), semana (11), amanha (8), prato (7), comer (7), carne (6)
- **chitchat**: rui (37), ta (17), bom (17), ajuda (12), obrigada (11), demais (11), vlw (10), valeu (10), oi (8), ajudou (8)
- **fichas**: ficha (47), fichas (33), comprar (28), posso (27), usar (17), ru (15), pagar (11), nao (10), tenho (8), vez (7)
- **fora_dominio**: ufms (18), abre (14), horario (14), horas (12), funciona (11), fica (10), facom (10), curso (10), semana (10), faco (10)
- **geral**: ru (48), posso (26), comer (18), contato (11), algum (10), restaurante (10), depois (9), universitario (7), comida (6), fazer (6)
- **horarios**: ru (59), horario (22), abre (21), horas (19), fecha (13), funcionamento (10), almoco (9), jantar (9), funciona (9), restaurante (8)
- **subsidio**: subsidio (51), ru (27), pagar (14), tenho (13), preciso (12), faco (11), direito (11), pedir (11), pedido (11), posso (10)
- **valores**: ru (27), refeicao (22), preco (21), subsidio (21), valor (19), custa (15), almoco (14), estudante (13), estudantes (11), paga (10)

## 4. Exemplos de negativos difíceis (fora_dominio parecidos com domínio)

Critério simples: fora_dominio com maior similaridade TF-IDF a algum exemplo de domínio, ou que contém vocabulário do RU. Sem verificação manual.

| fora_dominio | mais parecido com (domínio) | sim. | vocab RU |
|---|---|---|---|
| Qual o horário de funcionamento do LEAP? | Qual horário de funcionamento do RU? | 0.83 | sim |
| Qual o horário de funcionamento do businho? | Qual horário de funcionamento do RU? | 0.80 | sim |
| Qual o horário de funcionamento do batata? | Qual horário de funcionamento do RU? | 0.79 | sim |
| Tem lugar para esquentar minha comida no corredor central? | Da pra esquentar minha comida no ru/ | 0.62 | sim |
| É verdade que esse é o ru mais caro do Brasil? | é verdade que o almoço é mais caro que a janta? | 0.61 | sim |
| A FACOM funciona em horário normal aos finais de semana? | o RU funciona nos fins de semana | 0.57 | sim |
| O LEAP funciona em horário normal aos finais de semana? | o RU funciona nos fins de semana | 0.54 | sim |
| A reitoria funciona em horário normal aos finais de semana? | o RU funciona nos fins de semana | 0.53 | sim |
| A secretaria funciona em horário normal aos finais de semana? | o RU funciona nos fins de semana | 0.52 | sim |
| como eu peço o subsidio do vale gás? | Preço com subsídio? | 0.51 | sim |
| é vdd que o passe de ônibus é subsidio? | O que é o subsídio? | 0.51 | sim |
| Até que horário a caixa da UFMS funciona? | Até que horas funciona o restaurante? | 0.50 | sim |
| Consigo comer na cantina todo dia? | Consigo ir lá comer na quarta? | 0.50 | sim |
| Que horário fecham os portões do ENEM? | Qual o horário de fechamento do RU? | 0.49 | sim |
| A coordenação de curso funciona em horário normal aos finais de semana? | o RU funciona nos fins de semana | 0.48 | sim |

fora_dominio com vocabulário do RU: **55** de 323.

## 5. Frases humanas vs LLM

| origem   |   ('n_palavras', 'mean') |   ('n_palavras', 'median') |   ('n_chars', 'mean') |   ('n_chars', 'median') |
|:---------|-------------------------:|---------------------------:|----------------------:|------------------------:|
| humano   |                      6.7 |                          6 |                  34.7 |                      34 |
| llm      |                     11.2 |                         10 |                  64.1 |                      53 |
| massive  |                      6.7 |                          6 |                  35.6 |                      30 |

Proporção de frases com cada traço:

| origem   |   termina com ? |   tem maiúscula inicial |   tem acento |   tem pontuação final |   menciona 'RU' |   tem gíria/abrev. (vc, pq, tb, blz, tmj, kk) |
|:---------|----------------:|------------------------:|-------------:|----------------------:|----------------:|----------------------------------------------:|
| humano   |           0.738 |                   0.602 |        0.516 |                 0.773 |           0.158 |                                         0.054 |
| llm      |           0.645 |                   0.764 |        0.761 |                 0.761 |           0.33  |                                         0.018 |
| massive  |           0     |                   0     |        0.65  |                 0.03  |           0     |                                         0     |

- Palavras mais típicas de **humano** (vs llm): ufms, ta, cadunico, bom, cafe, pagar, obrigada, comida, reais, faz
- Palavras mais típicas de **llm** (vs humano): poderia, sabe, saber, cada, aluno, dizer, valores, informar, gostaria, queria

Proporção de cada intenção dentro de cada origem:

| intencao     |   humano |   llm |   massive |
|:-------------|---------:|------:|----------:|
| cardapio     |    0.07  | 0.178 |         0 |
| chitchat     |    0.271 | 0     |         0 |
| fichas       |    0.066 | 0.178 |         0 |
| fora_dominio |    0.29  | 0.072 |         1 |
| geral        |    0.088 | 0.094 |         0 |
| horarios     |    0.071 | 0.156 |         0 |
| subsidio     |    0.08  | 0.149 |         0 |
| valores      |    0.064 | 0.174 |         0 |
