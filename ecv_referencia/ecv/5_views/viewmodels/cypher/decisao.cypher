// ViewModel 'decisao' (matriz e árvore) — as RIR que restringem uma propriedade e os seus fatores discriminantes.
// Parâmetros: $alvo (chave da propriedade, ex.: "USM:Medicao.valor").
// A matriz (linhas, colunas, células) e a árvore organizam estas linhas; ver vistas/viewmodels/decisao.py.

// 1. Cada RIR: termos da condição (propriedade, operador, valor) e o valor exigido ao alvo
MATCH (alvo:Propriedade {chave: $alvo})<-[rg:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(r:RIR)
MATCH (r)-[:CONDICIONADA_POR]->(c:CondicaoAplicabilidade)-[t:TERMO]->(d:Propriedade)
WITH r, rg, t, d ORDER BY t.ordem
RETURN r.id AS regra, collect({propriedade: d.nome, operador: t.operador, valor: t.valor}) AS termos,
       rg.operador AS operador, rg.valor AS valor, rg.minimo AS minimo, rg.maximo AS maximo
ORDER BY regra;

// 2. Valores plausíveis das propriedades discriminantes (RP com IN)
MATCH (alvo:Propriedade {chave: $alvo})<-[:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(:RIR)
      -[:CONDICIONADA_POR]->(:CondicaoAplicabilidade)-[:TERMO]->(d:Propriedade)
WITH DISTINCT d
OPTIONAL MATCH (d)<-[:ASSOCIADA_A]-(:RP)-[:RESTRITA_POR]->(rs:Restricao {operador: 'IN'})
RETURN d.chave AS propriedade, rs.valor AS plausiveis;

// 3. RP do alvo (o que pode tomar, sempre)
MATCH (alvo:Propriedade {chave: $alvo})<-[rg:RESTRINGE]-(rs:Restricao)<-[:RESTRITA_POR]-(r:RP)
RETURN r.id AS regra, rg.texto AS restricao, rs.mensagem AS mensagem;
