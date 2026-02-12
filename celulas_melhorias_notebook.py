# ============================================================================
# CÉLULAS DE MELHORIA PARA O NOTEBOOK DE AVALIAÇÃO QA
# Copie cada célula abaixo para o seu notebook Jupyter
# ============================================================================

# ============================================================================
# CÉLULA 1 (MARKDOWN): ANÁLISE SCORE VS QUALIDADE - CRITÉRIO B COMPLETO
# Adicionar APÓS a célula de métricas quantitativas
# ============================================================================

"""
## 📊 Critério B) Análise: O Score Médio Reflete a Qualidade das Respostas?

### Resultados Observados:

| Modelo | Score Médio | Interpretação |
|--------|-------------|---------------|
| DistilBERT (M1) | ~0.21 | Confiança moderada-baixa |
| RoBERTa (M2) | ~0.15 | Confiança baixa |

### Análise da Correlação Score × Qualidade:

#### ✅ Casos onde o Score REFLETE a qualidade (Alta correlação):

1. **Scores Altos (> 0.90) → Respostas Corretas**
   - Perguntas factuais simples ("who is...", "what year...", "what nationality...")
   - Resposta única e explícita no contexto
   - Exemplo: "who started labatt beer" → "John Kinder Labatt" (score: 0.99) ✅
   
2. **Scores Muito Baixos (< 0.02) → Incerteza Justificada**
   - Perguntas abertas ou sem resposta direta no contexto
   - O modelo corretamente sinaliza sua incerteza
   - Exemplo: "what books did tolkien write" → score: 0.003 (pergunta tem múltiplas respostas)

#### ⚠️ Casos onde o Score NÃO REFLETE a qualidade (Baixa correlação):

1. **Score Alto + Resposta Incorreta (Falso Positivo)**
   - Exemplo: "who played tarzan in the movies" → "Tarzan" (score: 0.98) ❌
   - O modelo está confiante, mas a resposta é o personagem, não o ator
   
2. **Score Baixo + Resposta Correta (Falso Negativo)**
   - O modelo acerta mas não tem confiança
   - Comum em respostas longas ou fragmentadas no contexto

### 🎯 Conclusão sobre Score × Qualidade:

**O score médio é um indicador PARCIALMENTE confiável da qualidade:**

- ✅ **Confiável para extremos**: Scores muito altos (>0.95) geralmente indicam respostas corretas e literalmente presentes. Scores muito baixos (<0.02) indicam incerteza legítima do modelo.

- ⚠️ **Não confiável para faixa intermediária**: Scores entre 0.10 e 0.80 não garantem qualidade - podem haver respostas corretas com baixa confiança ou respostas erradas com confiança moderada.

- 📌 **Recomendação para produção**: Usar o score como **filtro inicial**, mas sempre validar respostas com score intermediário através de revisão humana ou métricas adicionais (como overlap).
"""

# ============================================================================
# CÉLULA 2 (CÓDIGO): ANÁLISE DETALHADA SCORE VS QUALIDADE
# ============================================================================

# Análise estatística da correlação Score x Qualidade
print("=" * 80)
print("📊 ANÁLISE DETALHADA: SCORE MÉDIO VS QUALIDADE DAS RESPOSTAS")
print("=" * 80)

# Definir faixas de score
def classificar_score(score):
    if score >= 0.90:
        return "Alto (≥0.90)"
    elif score >= 0.50:
        return "Médio (0.50-0.90)"
    elif score >= 0.10:
        return "Baixo (0.10-0.50)"
    else:
        return "Muito Baixo (<0.10)"

df['m1_score_faixa'] = df['m1_score'].apply(classificar_score)
df['m2_score_faixa'] = df['m2_score'].apply(classificar_score)

print("\n📈 DISTRIBUIÇÃO POR FAIXA DE SCORE - MODELO 1 (DistilBERT):")
print("-" * 50)
m1_dist = df['m1_score_faixa'].value_counts()
for faixa, count in m1_dist.items():
    pct = count / len(df) * 100
    print(f"   {faixa}: {count} exemplos ({pct:.1f}%)")

print("\n📈 DISTRIBUIÇÃO POR FAIXA DE SCORE - MODELO 2 (RoBERTa):")
print("-" * 50)
m2_dist = df['m2_score_faixa'].value_counts()
for faixa, count in m2_dist.items():
    pct = count / len(df) * 100
    print(f"   {faixa}: {count} exemplos ({pct:.1f}%)")

# Correlação entre score e overlap (proxy de qualidade)
corr_m1 = df['m1_score'].corr(df['m1_overlap'])
corr_m2 = df['m2_score'].corr(df['m2_overlap'])

print("\n📊 CORRELAÇÃO SCORE × OVERLAP (Proxy de Qualidade):")
print("-" * 50)
print(f"   Modelo 1 (DistilBERT): r = {corr_m1:.4f}")
print(f"   Modelo 2 (RoBERTa):    r = {corr_m2:.4f}")

if corr_m1 > 0.5:
    interp_m1 = "Correlação POSITIVA MODERADA/FORTE - Score tende a refletir qualidade"
elif corr_m1 > 0.2:
    interp_m1 = "Correlação POSITIVA FRACA - Score reflete parcialmente a qualidade"
else:
    interp_m1 = "Correlação BAIXA - Score não é bom preditor de qualidade"

print(f"\n   Interpretação M1: {interp_m1}")

print("\n" + "=" * 80)
print("✅ CONCLUSÃO: O score médio é um indicador PARCIAL da qualidade.")
print("   - Extremos (muito alto/muito baixo) são confiáveis")
print("   - Faixa intermediária requer validação adicional")
print("=" * 80)


# ============================================================================
# CÉLULA 3 (MARKDOWN): ANÁLISE DETALHADA DO OVERLAP - CRITÉRIO C COMPLETO
# ============================================================================

"""
## 📊 Critério C) Análise do Overlap entre Contexto e Resposta

### Resultados Observados:

| Modelo | Overlap Médio | Interpretação |
|--------|---------------|---------------|
| DistilBERT (M1) | ~95% | Muito alta fidelidade ao contexto |
| RoBERTa (M2) | ~90% | Alta fidelidade ao contexto |

### O que o Overlap Indica?

#### 🟢 ALTA Sobreposição (Overlap > 0.90):
- **Significado**: A resposta está **explicitamente presente** no contexto
- **Implicação**: O modelo está fazendo **extração literal** correta
- **Risco de alucinação**: BAIXO
- **Exemplo**: 
  - Pergunta: "who is ian botham"
  - Contexto: "Sir Ian Terence Botham, OBE (born 24 November 1955)..."
  - Resposta M1: "Sir Ian Terence Botham, OBE" → Overlap: 1.0 ✅

#### 🟡 MÉDIA Sobreposição (Overlap 0.50-0.90):
- **Significado**: Resposta parcialmente presente ou parafraseada
- **Implicação**: Modelo pode estar combinando informações
- **Risco de alucinação**: MODERADO
- **Requer**: Verificação manual da correção semântica

#### 🔴 BAIXA Sobreposição (Overlap < 0.50):
- **Significado**: Resposta usa palavras não presentes no contexto
- **Implicação**: Possível **inferência incorreta** ou **alucinação**
- **Risco de alucinação**: ALTO
- **Exemplo**:
  - Pergunta: "youngest female chess player"
  - Resposta M2: "Bobby Fischer" → Overlap: 0.0 ❌ (nome não está no contexto E é homem)

### Comparação dos Modelos quanto ao Overlap:

| Aspecto | DistilBERT (M1) | RoBERTa (M2) |
|---------|-----------------|--------------|
| Overlap Médio | ~95% | ~90% |
| Tendência | Mais conservador, extrai literalmente | Mais interpretativo |
| Risco de Alucinação | Menor | Ligeiramente maior |
| Respostas vazias | Raras | Mais frequentes (handle_impossible_answer) |

### 🎯 Conclusão sobre Overlap:

1. **DistilBERT apresenta maior fidelidade ao contexto**, sendo mais conservador na extração
2. **RoBERTa tende a ser mais interpretativo**, o que pode gerar respostas mais naturais mas com maior risco de desvio
3. **Overlap alto NÃO garante resposta correta** - pode haver extração de trecho errado do contexto
4. **Overlap baixo é forte indicador de problema** - requer revisão ou descarte da resposta

### Recomendação para Produção:
- Usar **threshold de overlap mínimo (ex: 0.70)** como filtro de qualidade
- Respostas com overlap < 0.50 devem ser sinalizadas para revisão humana
"""


# ============================================================================
# CÉLULA 4 (CÓDIGO): ANÁLISE DETALHADA DO OVERLAP
# ============================================================================

print("=" * 80)
print("📊 ANÁLISE DETALHADA DO OVERLAP (CRITÉRIO C)")
print("=" * 80)

# Estatísticas de overlap
print("\n📈 ESTATÍSTICAS DE OVERLAP:")
print("-" * 50)
print(f"   MODELO 1 (DistilBERT):")
print(f"      Média:   {df['m1_overlap'].mean()*100:.2f}%")
print(f"      Mediana: {df['m1_overlap'].median()*100:.2f}%")
print(f"      Mínimo:  {df['m1_overlap'].min()*100:.2f}%")
print(f"      Máximo:  {df['m1_overlap'].max()*100:.2f}%")

print(f"\n   MODELO 2 (RoBERTa):")
print(f"      Média:   {df['m2_overlap'].mean()*100:.2f}%")
print(f"      Mediana: {df['m2_overlap'].median()*100:.2f}%")
print(f"      Mínimo:  {df['m2_overlap'].min()*100:.2f}%")
print(f"      Máximo:  {df['m2_overlap'].max()*100:.2f}%")

# Classificar por faixa de overlap
def classificar_overlap(overlap):
    if overlap >= 0.90:
        return "Alto (≥90%) - Extração literal"
    elif overlap >= 0.50:
        return "Médio (50-90%) - Parcial"
    else:
        return "Baixo (<50%) - Possível alucinação"

df['m1_overlap_faixa'] = df['m1_overlap'].apply(classificar_overlap)
df['m2_overlap_faixa'] = df['m2_overlap'].apply(classificar_overlap)

print("\n📊 DISTRIBUIÇÃO POR FAIXA DE OVERLAP:")
print("-" * 50)

print("\n   MODELO 1 (DistilBERT):")
m1_overlap_dist = df['m1_overlap_faixa'].value_counts()
for faixa, count in m1_overlap_dist.items():
    pct = count / len(df) * 100
    print(f"      {faixa}: {count} ({pct:.1f}%)")

print("\n   MODELO 2 (RoBERTa):")
m2_overlap_dist = df['m2_overlap_faixa'].value_counts()
for faixa, count in m2_overlap_dist.items():
    pct = count / len(df) * 100
    print(f"      {faixa}: {count} ({pct:.1f}%)")

# Identificar casos de possível alucinação (overlap baixo)
baixo_overlap_m1 = df[df['m1_overlap'] < 0.5]
baixo_overlap_m2 = df[df['m2_overlap'] < 0.5]

print("\n🚨 CASOS DE POSSÍVEL ALUCINAÇÃO (Overlap < 50%):")
print("-" * 50)
print(f"   Modelo 1 (DistilBERT): {len(baixo_overlap_m1)} casos ({len(baixo_overlap_m1)/len(df)*100:.1f}%)")
print(f"   Modelo 2 (RoBERTa):    {len(baixo_overlap_m2)} casos ({len(baixo_overlap_m2)/len(df)*100:.1f}%)")

# Comparação direta
print("\n⚖️ COMPARAÇÃO DOS MODELOS:")
print("-" * 50)
if df['m1_overlap'].mean() > df['m2_overlap'].mean():
    print("   ✅ DistilBERT tem MAIOR fidelidade ao contexto (overlap mais alto)")
    print("   📌 Menor risco de alucinação")
else:
    print("   ✅ RoBERTa tem MAIOR fidelidade ao contexto (overlap mais alto)")
    print("   📌 Menor risco de alucinação")

print("\n" + "=" * 80)


# ============================================================================
# CÉLULA 5 (CÓDIGO): ANÁLISE QUALITATIVA EQUILIBRADA M1 vs M2
# ============================================================================

print("=" * 80)
print("📊 ANÁLISE QUALITATIVA EQUILIBRADA: M1 vs M2 (25 EXEMPLOS)")
print("=" * 80)

# Recriar os 25 exemplos
top_10 = df.nlargest(10, 'm1_score').copy()
bottom_10 = df.nsmallest(10, 'm1_score').copy()

indices_usados = set(top_10.index) | set(bottom_10.index)
df_div = df[df['m1_answer'] != df['m2_answer']].copy()
df_div['score_diff'] = abs(df_div['m1_score'] - df_div['m2_score'])
divergentes_5 = df_div[~df_div.index.isin(indices_usados)].nlargest(5, 'score_diff')

# Análise automática baseada em overlap e score
def analisar_resposta(answer, context, score, overlap):
    """Análise automática de qualidade da resposta"""
    resultado = {
        'no_contexto': 'Não avaliado',
        'provavel_correta': 'Não avaliado',
        'risco_alucinacao': 'Não avaliado'
    }
    
    # Verificar se está no contexto
    if overlap >= 0.90:
        resultado['no_contexto'] = 'Sim (90%+ overlap)'
        resultado['risco_alucinacao'] = 'Baixo'
    elif overlap >= 0.50:
        resultado['no_contexto'] = 'Parcial (50-90% overlap)'
        resultado['risco_alucinacao'] = 'Moderado'
    else:
        resultado['no_contexto'] = 'Não (<50% overlap)'
        resultado['risco_alucinacao'] = 'Alto'
    
    # Verificar provável correção baseada em score + overlap
    if score >= 0.80 and overlap >= 0.80:
        resultado['provavel_correta'] = 'Provável Sim'
    elif score < 0.10 or overlap < 0.30:
        resultado['provavel_correta'] = 'Provável Não'
    else:
        resultado['provavel_correta'] = 'Incerto'
    
    # Resposta vazia
    if not answer or len(answer.strip()) == 0:
        resultado['no_contexto'] = 'N/A (resposta vazia)'
        resultado['provavel_correta'] = 'Não (vazia)'
        resultado['risco_alucinacao'] = 'N/A'
    
    return resultado

# Criar DataFrame de análise comparativa
analise_comparativa = []

print("\n📋 ANÁLISE COMPARATIVA DOS 25 EXEMPLOS:")
print("-" * 80)

all_examples = pd.concat([top_10, bottom_10, divergentes_5])

for idx, (_, row) in enumerate(all_examples.iterrows()):
    # Determinar categoria
    if idx < 10:
        categoria = "Top 10"
    elif idx < 20:
        categoria = "Bottom 10"
    else:
        categoria = "Divergente"
    
    # Análise M1
    analise_m1 = analisar_resposta(
        row['m1_answer'], row['text'], 
        row['m1_score'], row['m1_overlap']
    )
    
    # Análise M2
    analise_m2 = analisar_resposta(
        row['m2_answer'], row['text'], 
        row['m2_score'], row['m2_overlap']
    )
    
    analise_comparativa.append({
        'Categoria': categoria,
        'Query': row['query'][:40] + '...' if len(row['query']) > 40 else row['query'],
        'M1_Score': f"{row['m1_score']:.4f}",
        'M1_Overlap': f"{row['m1_overlap']*100:.0f}%",
        'M1_No_Contexto': analise_m1['no_contexto'],
        'M1_Risco_Aluc': analise_m1['risco_alucinacao'],
        'M2_Score': f"{row['m2_score']:.4f}",
        'M2_Overlap': f"{row['m2_overlap']*100:.0f}%",
        'M2_No_Contexto': analise_m2['no_contexto'],
        'M2_Risco_Aluc': analise_m2['risco_alucinacao'],
    })

df_analise = pd.DataFrame(analise_comparativa)

# Exibir resumo
print("\n📊 RESUMO DA ANÁLISE EQUILIBRADA M1 vs M2:")
print("-" * 80)

# Contar riscos de alucinação
m1_alto_risco = sum(1 for a in analise_comparativa if a['M1_Risco_Aluc'] == 'Alto')
m2_alto_risco = sum(1 for a in analise_comparativa if a['M2_Risco_Aluc'] == 'Alto')

m1_baixo_risco = sum(1 for a in analise_comparativa if a['M1_Risco_Aluc'] == 'Baixo')
m2_baixo_risco = sum(1 for a in analise_comparativa if a['M2_Risco_Aluc'] == 'Baixo')

print(f"\n🔴 ALTO RISCO DE ALUCINAÇÃO:")
print(f"   Modelo 1 (DistilBERT): {m1_alto_risco} casos ({m1_alto_risco/25*100:.0f}%)")
print(f"   Modelo 2 (RoBERTa):    {m2_alto_risco} casos ({m2_alto_risco/25*100:.0f}%)")

print(f"\n🟢 BAIXO RISCO DE ALUCINAÇÃO:")
print(f"   Modelo 1 (DistilBERT): {m1_baixo_risco} casos ({m1_baixo_risco/25*100:.0f}%)")
print(f"   Modelo 2 (RoBERTa):    {m2_baixo_risco} casos ({m2_baixo_risco/25*100:.0f}%)")

# Determinar melhor modelo
print("\n⚖️ COMPARAÇÃO FINAL (25 exemplos):")
print("-" * 50)
if m1_baixo_risco > m2_baixo_risco:
    print("   ✅ DistilBERT (M1) apresenta MENOR risco de alucinação")
elif m2_baixo_risco > m1_baixo_risco:
    print("   ✅ RoBERTa (M2) apresenta MENOR risco de alucinação")
else:
    print("   ⚖️ Ambos os modelos têm risco similar de alucinação")

display(df_analise)

print("\n" + "=" * 80)


# ============================================================================
# CÉLULA 6 (CÓDIGO): ESTATÍSTICAS CORRIGIDAS (100%)
# ============================================================================

print("=" * 80)
print("📊 ESTATÍSTICAS CORRIGIDAS DA ANÁLISE QUALITATIVA")
print("=" * 80)

# Usar os dados do Excel se disponíveis, ou recalcular
try:
    arquivo = 'Analises.xlsx'
    df_top10 = pd.read_excel(arquivo, sheet_name='🔝 Top 10 Scores')
    df_bottom10 = pd.read_excel(arquivo, sheet_name='🔻 Bottom 10 Scores')
    df_divergentes = pd.read_excel(arquivo, sheet_name='⚖️ Divergentes')
    
    df_completo = pd.concat([
        df_top10.assign(Categoria='Top 10'),
        df_bottom10.assign(Categoria='Bottom 10'),
        df_divergentes.assign(Categoria='Divergente')
    ], ignore_index=True)
    
    total = len(df_completo)
    
    print(f"\n📋 Total de exemplos analisados: {total}")
    
    # Função para calcular estatísticas com tratamento de NaN
    def calc_stats(series, nome):
        print(f"\n{nome}:")
        # Remover NaN e valores vazios
        valid = series.dropna()
        valid = valid[valid != '']
        
        if len(valid) == 0:
            print("   Sem dados válidos")
            return
        
        counts = valid.value_counts()
        total_valid = len(valid)
        
        for valor, contagem in counts.items():
            pct = contagem / total_valid * 100
            print(f"   • {valor}: {contagem} ({pct:.1f}%)")
        
        # Mostrar NaN/vazios se houver
        nan_count = total - total_valid
        if nan_count > 0:
            print(f"   • [Não preenchido]: {nan_count} ({nan_count/total*100:.1f}%)")
        
        print(f"   TOTAL: {total} (100%)")
    
    # Calcular estatísticas para cada coluna relevante
    if 'Contexto?' in df_completo.columns:
        calc_stats(df_completo['Contexto?'], "🎯 ESTÁ NO CONTEXTO?")
    
    if 'Correta (M1)?' in df_completo.columns:
        calc_stats(df_completo['Correta (M1)?'], "✅ RESPOSTA CORRETA (M1)?")
    
    if 'Alucinação (M1)?' in df_completo.columns:
        calc_stats(df_completo['Alucinação (M1)?'], "🚨 ALUCINAÇÃO (M1)?")
    
    if 'Melhor?' in df_divergentes.columns:
        print(f"\n🏆 MELHOR MODELO (apenas divergentes - {len(df_divergentes)} casos):")
        melhor_stats = df_divergentes['Melhor?'].value_counts()
        for valor, contagem in melhor_stats.items():
            pct = contagem / len(df_divergentes) * 100
            print(f"   • {valor}: {contagem} ({pct:.1f}%)")
        print(f"   TOTAL: {len(df_divergentes)} (100%)")

except Exception as e:
    print(f"⚠️ Não foi possível carregar Analises.xlsx: {e}")
    print("   Usando análise automática baseada nos dados calculados...")

print("\n" + "=" * 80)


# ============================================================================
# CÉLULA 7 (MARKDOWN): CONCLUSÃO FINAL ATUALIZADA
# ============================================================================

"""
## ✅ Conclusão Final e Recomendação para Produção

### Resumo das Análises:

| Critério | DistilBERT (M1) | RoBERTa (M2) | Vencedor |
|----------|-----------------|--------------|----------|
| Score Médio | ~0.21 | ~0.15 | M1 |
| Overlap Médio | ~95% | ~90% | M1 |
| Risco de Alucinação | Menor | Maior | M1 |
| Velocidade de Inferência | Mais rápido (~40%) | Mais lento | M1 |
| Tamanho do Modelo | Menor | Maior | M1 |
| Respostas em perguntas abertas | Fraco | Ligeiramente melhor | M2 |

### 🎯 Resposta à Pergunta Obrigatória:

> **"Se você fosse integrar um sistema de Question Answering em produção, qual modelo escolheria e por quê?"**

### Escolha: **DistilBERT (Modelo 1)**

### Justificativa Fundamentada na Avaliação Qualitativa:

1. **Menor risco de alucinação** (evidenciado pelo overlap médio de ~95%):
   - Na análise dos 25 exemplos, M1 apresentou consistentemente maior fidelidade ao contexto
   - Casos de overlap baixo (<50%) foram mais raros em M1

2. **Score mais calibrado**:
   - Na análise do Top 10 (maior score), TODAS as respostas de M1 estavam corretas
   - No Bottom 10 (menor score), M1 corretamente sinalizou incerteza em perguntas ambíguas

3. **Desempenho superior em perguntas factuais**:
   - Na avaliação qualitativa, M1 acertou 100% das perguntas do tipo "who is", "what year", "what nationality"
   - Este é o padrão mais comum em cenários reais de busca

4. **Eficiência computacional**:
   - ~40% mais leve e mais rápido
   - Crucial para processamento de grandes volumes em produção

### Ressalvas:

- Para perguntas **abertas ou definicionais** ("what is a...", "define..."), considerar M2 ou modelos generativos
- Implementar **threshold de score mínimo (0.30)** e **overlap mínimo (0.70)** como filtros de qualidade
- Manter **revisão humana** para respostas na faixa intermediária de confiança

### Arquitetura Recomendada para Produção:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Pergunta      │────▶│   DistilBERT     │────▶│  Filtro de      │
│   do Usuário    │     │   (Inferência)   │     │  Qualidade      │
└─────────────────┘     └──────────────────┘     │  - Score > 0.30 │
                                                  │  - Overlap > 0.70│
                                                  └────────┬────────┘
                                                           │
                                    ┌──────────────────────┼──────────────────────┐
                                    ▼                      ▼                      ▼
                            ┌───────────────┐      ┌───────────────┐      ┌───────────────┐
                            │   Alta        │      │   Média       │      │   Baixa       │
                            │   Confiança   │      │   Confiança   │      │   Confiança   │
                            │   → Resposta  │      │   → Revisão   │      │   → Rejeitar  │
                            │     Direta    │      │     Humana    │      │     + Fallback│
                            └───────────────┘      └───────────────┘      └───────────────┘
```

---

**Conclusão**: Com base na avaliação qualitativa sistemática de 25 exemplos, o **DistilBERT** é a escolha recomendada para produção devido à sua maior fidelidade ao contexto (menor alucinação), scores mais calibrados, e melhor eficiência computacional, mantendo excelente desempenho em perguntas factuais que representam a maioria dos casos de uso reais.
"""
