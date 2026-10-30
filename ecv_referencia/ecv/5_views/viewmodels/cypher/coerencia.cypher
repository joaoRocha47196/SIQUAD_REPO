// ViewModel 'coerencia' — problemas de coerência entre regras.
// Parâmetros: nenhum. Os valores estão guardados em JSON (texto); a pertença verifica-se por contenção do texto.

// 1. Termos EQUALS cujo valor não pertence aos valores plausíveis (RP IN) da propriedade: a regra nunca se aplica
MATCH (c:CondicaoAplicabilidade)-[t:TERMO {operador: 'EQUALS'}]->(p:Propriedade)
      <-[:ASSOCIADA_A]-(:RP)-[:RESTRITA_POR]->(rs:Restricao {operador: 'IN'})
WHERE NOT rs.valor CONTAINS t.valor
RETURN c.regra AS regra, p.chave AS propriedade, t.valor AS valor, rs.valor AS plausiveis;

// 2. Pares de regras com gamas sem valor comum sobre a mesma propriedade e condições compatíveis
MATCH (p:Propriedade)<-[a:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(ra:Regra),
      (p)<-[b:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(rb:Regra)
WHERE ra.id < rb.id AND a.minimo IS NOT NULL AND b.minimo IS NOT NULL
  AND (a.maximo < b.minimo OR b.maximo < a.minimo)
  AND NOT EXISTS {
    MATCH (ra)-[:CONDICIONADA_POR]->(:CondicaoAplicabilidade)-[ta:TERMO {operador: 'EQUALS'}]->(d:Propriedade)
          <-[tb:TERMO {operador: 'EQUALS'}]-(:CondicaoAplicabilidade)<-[:CONDICIONADA_POR]-(rb)
    WHERE ta.valor <> tb.valor }
RETURN p.chave AS propriedade, ra.id AS regraA, [a.minimo, a.maximo] AS gamaA, rb.id AS regraB, [b.minimo, b.maximo] AS gamaB;

// 3. Regras com exatamente os mesmos termos na condição
MATCH (r:Regra)-[:CONDICIONADA_POR]->(:CondicaoAplicabilidade)-[t:TERMO]->(d:Propriedade)
WITH r, d, t ORDER BY d.chave, t.operador, t.valor
WITH r, collect(d.chave + ' ' + t.operador + ' ' + coalesce(t.valor, t.contexto)) AS assinatura
WITH assinatura, collect(r.id) AS regras
WHERE size(regras) > 1
RETURN assinatura, regras;
