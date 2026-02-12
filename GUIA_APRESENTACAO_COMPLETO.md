# Avaliacao de Modelos de Question Answering: DistilBERT vs RoBERTa

## Contexto do Trabalho

Este trabalho avalia dois modelos de Question Answering (QA) extractivos para determinar qual seria mais adequado para uso em producao. Os modelos avaliados sao:

- **Modelo 1 (M1)**: DistilBERT (distilbert-base-cased-distilled-squad) — versao compacta e otimizada do BERT
- **Modelo 2 (M2)**: RoBERTa (deepset/roberta-base-squad2) — versao robusta do BERT com treinamento otimizado

Ambos foram testados sobre **1.000 perguntas** do dataset DBpedia Shard 007, que contem pares de pergunta, texto-fonte e titulo extraidos da base de conhecimento DBpedia.

A avaliacao segue quatro criterios obrigatorios: A, B, C e D.

---

## Criterio A — Tamanho Medio das Perguntas

### Resultado

O tamanho medio das perguntas no dataset e de **4,80 palavras**. Esse valor e identico para ambos os modelos porque e uma propriedade do dataset, nao do modelo.

### Interpretacao

O dataset DBpedia Shard 007 e composto por perguntas curtas e objetivas. Exemplos tipicos: "who is ian botham", "what year was the jacquard loom invented", "what nationality is lleyton hewitt". Sao perguntas no estilo "quem e", "o que e", "quando foi", que pedem uma resposta factual unica.

### Por que isso importa

Perguntas curtas e diretas favorecem modelos extractivos como DistilBERT e RoBERTa. A intencao da pergunta fica clara e a resposta geralmente esta explicita no texto-fonte. Isso explica por que ambos os modelos alcancaram indices de overlap elevados (acima de 78%). Se o dataset tivesse perguntas longas, complexas ou multi-hop (que exigem cruzar informacoes de varios trechos), os resultados poderiam ser bem diferentes.

### Limitacao

O Criterio A serve como contextualizacao do cenario de avaliacao. Ele nao diferencia os modelos entre si, mas e essencial para entender o ambiente em que os resultados foram obtidos.

---

## Criterio B — O Score Medio Reflete a Qualidade das Respostas?

### Resultados

| Modelo | Score Medio | Interpretacao |
|--------|-------------|---------------|
| DistilBERT (M1) | 0.4131 | Confianca moderada |
| RoBERTa (M2) | 0.3310 | Confianca moderada-baixa |

O score representa a confianca que o modelo tem na resposta que ele extraiu. Vai de 0 (nenhuma confianca) a 1 (confianca maxima).

### O score e confiavel?

A resposta e: **parcialmente**. Funciona bem nos extremos, mas falha na faixa intermediaria.

**Quando o score e confiavel:**

- Scores muito altos (acima de 0.95) geralmente indicam respostas corretas. Exemplo: "who started labatt beer" recebeu score 0.99 e a resposta "John Kinder Labatt" esta correta e literalmente presente no texto.
- Scores muito baixos (abaixo de 0.02) indicam que o modelo reconhece sua incerteza. Exemplo: "what books did tolkien write" recebeu score 0.003 porque a pergunta tem multiplas respostas validas e o modelo nao consegue selecionar uma unica.

**Quando o score nao e confiavel:**

- Score alto com resposta errada (falso positivo): "who played tarzan in the movies" recebeu score 0.98, mas a resposta foi "Tarzan" (o personagem), quando a pergunta pede o nome do ator. O modelo esta confiante, mas errou.
- Score baixo com resposta correta (falso negativo): o modelo acerta, mas nao tem confianca, geralmente porque a resposta esta fragmentada no texto.

### Conclusao do Criterio B

O score medio do DistilBERT (0.4131) e superior ao do RoBERTa (0.3310), indicando que o DistilBERT tende a ser mais confiante em suas respostas. Porem, o score sozinho nao e suficiente para garantir qualidade. Em producao, deve ser usado como filtro inicial combinado com outras metricas como o overlap.

---

## Criterio C — Analise do Overlap (Fidelidade ao Texto-Fonte)

### Resultados

| Aspecto | DistilBERT (M1) | RoBERTa (M2) |
|---------|-----------------|--------------|
| Overlap Medio | 83,71% | 78,41% |
| Alta fidelidade (overlap >= 90%) | 62,6% dos casos | 53,3% dos casos |
| Possivel alucinacao (overlap < 50%) | 7,7% dos casos | 12,2% dos casos |

O overlap mede quanto da resposta do modelo esta presente no texto-fonte original. Um overlap de 100% significa que todas as palavras da resposta vieram do texto. Um overlap de 0% significa que nenhuma palavra veio do texto (possivel alucinacao).

### O que cada faixa de overlap indica

**Overlap alto (acima de 90%):** A resposta foi extraida diretamente do texto. E o comportamento esperado de um modelo extractivo. Exemplo: "who is ian botham" com resposta "Sir Ian Terence Botham, OBE" e overlap 1.0 — a resposta esta literalmente no texto.

**Overlap medio (entre 50% e 90%):** A resposta e parcialmente baseada no texto, mas o modelo pode ter combinado trechos ou parafraseado. Requer verificacao manual.

**Overlap baixo (abaixo de 50%):** A resposta usa palavras que nao estao no texto. Forte indicador de alucinacao ou erro. Exemplo grave do RoBERTa: para a pergunta "youngest female chess player", respondeu "Bobby Fischer". Bobby Fischer e homem e seu nome nem estava no contexto sobre a jogadora Judit Polgar. Isso e uma alucinacao clara.

### Conclusao do Criterio C

O DistilBERT e mais conservador e fiel ao texto original. Ele extrai respostas mais literais, o que reduz o risco de alucinacao. O RoBERTa tende a "interpretar" mais, o que em alguns casos gera respostas mais completas, mas em outros gera erros graves. Para um sistema em producao onde confiabilidade importa, a estrategia conservadora do DistilBERT e preferivel.

---

## Criterio D — Avaliacao Qualitativa de 25 Exemplos

A avaliacao qualitativa foi conduzida sobre 25 exemplos selecionados: os 10 com maior score do M1, os 10 com menor score do M1 e 5 exemplos onde os modelos deram respostas diferentes.

### Top 10 — Exemplos com Maior Confianca

Estes sao os exemplos onde o DistilBERT teve score acima de 0.98. Na revisao manual, observou-se que:

- Todas as respostas estavam corretas para perguntas factuais diretas
- As respostas eram curtas, precisas e extraidas diretamente do texto
- Exemplos: "who started labatt beer" com resposta "John Kinder Labatt" (score 0.99), "what nationality is lleyton hewitt" com resposta "Australian" (score 0.99), "what year was the jacquard loom invented" com resposta "1801" (score 0.99)
- O padrao e claro: perguntas do tipo "quem", "quando", "qual" com resposta unica e explicita no texto sao o ponto forte do DistilBERT

**Conclusao do Top 10:** O DistilBERT demonstra 100% de acerto em perguntas factuais simples quando tem alta confianca. Nesses casos, o score e um indicador confiavel.

### Bottom 10 — Exemplos com Menor Confianca

Estes sao exemplos onde o DistilBERT teve score abaixo de 0.016. Na revisao manual:

- As perguntas eram ambiguas, abertas ou sem resposta direta no texto
- Exemplos: "what books did tolkien write" (score 0.003, pergunta com multiplas respostas), "what is a latte liberal" (score 0.005, conceito abstrato), "what are the three components of a laser" (score 0.007, resposta longa)
- O modelo sinalizou corretamente sua incerteza com scores baixos

**Conclusao do Bottom 10:** O baixo score do DistilBERT e um sinal confiavel de que a pergunta e dificil ou a resposta nao e adequada. Isso e util em producao para filtrar respostas de baixa qualidade.

### 5 Exemplos Divergentes — Quando os Modelos Discordaram

Estes sao os casos mais interessantes porque revelam as diferencas de comportamento entre os modelos:

**Exemplo 1 — "what is the jazz guitar"**
- DistilBERT: deu uma definicao correta. Melhor: M1.
- RoBERTa: focou em detalhes tecnicos irrelevantes.

**Exemplo 2 — "what river is javari located in"**
- DistilBERT: "The Javary River" — correto e direto. Melhor: M1.
- RoBERTa: "the Amazon" — incorreto, confundiu o rio tributario com o rio principal.

**Exemplo 3 — "youngest female chess player"**
- DistilBERT: resposta tangencial sobre Judit Polgar, nao completamente correta.
- RoBERTa: "Bobby Fischer" — completamente errado. Bobby Fischer e homem e nao e mencionado no contexto. Alucinacao grave. Melhor: nenhum, mas M2 e pior.

**Exemplo 4 — "who makes jupiter computer"**
- DistilBERT: resposta confusa.
- RoBERTa: identificou corretamente a empresa. Melhor: M2.

**Exemplo 5 — "what are jewish holidays"**
- DistilBERT: resposta redundante.
- RoBERTa: resposta mais concisa e adequada. Melhor: M2.

**Resultado geral dos divergentes:** M1 venceu 2, M2 venceu 2, empate 1. Porem, a gravidade dos erros e diferente. O erro mais grave foi do RoBERTa (alucinacao de genero no caso Bobby Fischer), enquanto os erros do DistilBERT foram mais brandos (respostas confusas ou incompletas, mas nunca alucinacoes graves).

---

## Conclusao Final — Modelo Escolhido: DistilBERT

### Tabela Resumo

| Criterio | DistilBERT (M1) | RoBERTa (M2) | Vencedor |
|----------|-----------------|--------------|----------|
| Score Medio | 0.4131 | 0.3310 | DistilBERT |
| Overlap Medio | 83,71% | 78,41% | DistilBERT |
| Alta fidelidade (>= 90%) | 62,6% | 53,3% | DistilBERT |
| Possivel alucinacao (< 50%) | 7,7% | 12,2% | DistilBERT |
| Top 10 qualitativo | 100% acerto | — | DistilBERT |
| Alucinacoes graves | Nenhuma | Sim (Bobby Fischer) | DistilBERT |

### Por que DistilBERT para producao

1. **Maior confianca media** (0.41 vs 0.33): o modelo tende a ser mais assertivo quando tem certeza e mais cauteloso quando nao tem.

2. **Maior fidelidade ao texto** (83,7% vs 78,4%): extrai respostas mais literais do texto-fonte, reduzindo risco de alucinacao.

3. **Menos alucinacoes** (7,7% vs 12,2%): em producao, alucinacao e o pior cenario possivel porque o sistema da uma resposta errada com aparencia de correta.

4. **Analise qualitativa favoravel**: no Top 10 acertou tudo, no Bottom 10 sinalizou incerteza corretamente, e nos divergentes seus erros foram menos graves que os do RoBERTa.

5. **Erros mais seguros**: quando o DistilBERT erra, ele tende a ser impreciso ou incompleto. Quando o RoBERTa erra, ele alucina (inventa informacoes que nao existem no texto). Para producao, um modelo que erra "menos gravemente" e mais seguro.

### Ressalvas

- O RoBERTa pode ser superior para perguntas abertas ou definicionais, onde a capacidade de interpretar alem do texto literal e uma vantagem.
- A avaliacao foi feita em perguntas curtas (media de 4,80 palavras). Em cenarios com perguntas complexas, os resultados podem diferir.
- Nao havia ground truth (respostas corretas de referencia) no dataset, entao a avaliacao qualitativa foi baseada em julgamento manual.

### Arquitetura recomendada para producao

Para um sistema real de QA, a recomendacao e:

1. Receber a pergunta do usuario
2. Processar com DistilBERT
3. Aplicar filtros de qualidade: Score acima de 0.30 e Overlap acima de 0.70
4. Se alta confianca: retornar resposta diretamente
5. Se confianca media: sinalizar para revisao humana
6. Se baixa confianca: rejeitar a resposta e informar ao usuario que nao foi possivel responder com seguranca
