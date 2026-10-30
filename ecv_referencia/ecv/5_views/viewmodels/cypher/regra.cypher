// ViewModel 'regra' — ficha de uma regra, o subgrafo da regra e a cadeia dos modelos até aos HLM.
// Parâmetros: $id (ex.: "RIR-TEMP-REFRIG-CELSIUS").

// 1. Ficha
MATCH (r:Regra {id: $id})-[:ASSOCIADA_A]->(vive)
OPTIONAL MATCH (r)-[:RESTRITA_POR]->(rs:Restricao)
OPTIONAL MATCH (rs)-[rg:RESTRINGE]->(alvo:Propriedade)
OPTIONAL MATCH (r)-[:CONDICIONADA_POR]->(c:CondicaoAplicabilidade)
RETURN r.id AS id, [l IN labels(r) WHERE l <> 'Regra'][0] AS tipo, r.descricao AS descricao,
       coalesce(vive.chave, vive.nome) AS viveEm, c.descricao AS condicao, rs.descricao AS restricao,
       alvo.chave AS alvo, alvo.descricao AS descricaoAlvo, coalesce(rs.mensagem, r.mensagem) AS mensagem,
       r.contextosExternos AS contextos;

// 2. Subgrafo da regra (para ver no Neo4j Browser em modo grafo)
MATCH (r:Regra {id: $id})
OPTIONAL MATCH p1 = (r)-[:ASSOCIADA_A|RESTRITA_POR|CONDICIONADA_POR]->()
OPTIONAL MATCH p2 = (r)-[:RESTRITA_POR|CONDICIONADA_POR]->()-[:RESTRINGE|TERMO|CHAMA|DEPENDE_DE]->()
OPTIONAL MATCH p3 = (r)-[:RESTRITA_POR|CONDICIONADA_POR]->()-[:CHAMA]->()-[le:LE]->()
WHERE le.regra = $id
OPTIONAL MATCH p4 = (r)-[:RESTRITA_POR|CONDICIONADA_POR]->()-[:CHAMA]->()-[:DEPENDE_DE]->()
RETURN p1, p2, p3, p4;

// 3. Cadeia dos modelos: de cada propriedade envolvida (onde vive, alvo, termos, argumentos) até todos os HLM
MATCH (r:Regra {id: $id})
OPTIONAL MATCH (r)-[:ASSOCIADA_A]->(a)
OPTIONAL MATCH (r)-[:RESTRITA_POR|CONDICIONADA_POR]->()-[:RESTRINGE|TERMO]->(b)
OPTIONAL MATCH (r)-[:RESTRITA_POR|CONDICIONADA_POR]->()-[:CHAMA]->()-[le:LE]->(c) WHERE le.regra = $id
WITH collect(DISTINCT a) + collect(DISTINCT b) + collect(DISTINCT c) AS envolvidos
UNWIND envolvidos AS x
MATCH cadeia = (h:HLM)-[:COMPOSTO_POR*0..]->(m)-[:CONTEM*0..1]->(x)
RETURN cadeia;
