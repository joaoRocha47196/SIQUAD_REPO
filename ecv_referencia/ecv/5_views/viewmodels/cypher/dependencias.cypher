// ViewModel 'dependencias' — que restrições e conclusões implica cada valor desta propriedade?
// Parâmetros: $propriedade (chave, ex.: "SM:Identificacao.tipoDispositivo").

// 1. Valores plausíveis (RP com IN que vivem na propriedade)
MATCH (p:Propriedade {chave: $propriedade})<-[:ASSOCIADA_A]-(:RP)-[:RESTRITA_POR]->(rs:Restricao {operador: 'IN'})
RETURN rs.valor AS plausiveis;

// 2. Cada regra cuja condição lê a propriedade: o termo de foco, a condição completa e os alvos
MATCH (p:Propriedade {chave: $propriedade})<-[t:TERMO]-(c:CondicaoAplicabilidade)<-[:CONDICIONADA_POR]-(r:Regra)
OPTIONAL MATCH (r)-[:RESTRITA_POR]->(rs:Restricao)
OPTIONAL MATCH (rs)-[:RESTRINGE]->(alvo:Propriedade)
OPTIONAL MATCH (rs)-[:CHAMA]->(:Funcao)-[le:LE]->(arg) WHERE le.regra = r.id
RETURN r.id AS regra, [l IN labels(r) WHERE l <> 'Regra'][0] AS tipo, t.operador AS operador, t.valor AS valor,
       t.texto AS termoFoco, c.descricao AS condicao, rs.descricao AS restricao, coalesce(rs.mensagem, r.mensagem) AS mensagem,
       collect(DISTINCT alvo.chave) + collect(DISTINCT coalesce(arg.chave, arg.nome)) AS alvos, r.conclusaoValor AS conclusao
ORDER BY tipo, regra;
