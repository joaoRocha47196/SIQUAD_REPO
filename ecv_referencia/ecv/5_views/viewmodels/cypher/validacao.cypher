// ViewModel 'validacao' — o cenário e as regras que o motor avalia sobre uma instância.
// Parâmetros: $perfil (ex.: "AuditoriaSetembro2026").
// A avaliação sobre os valores da instância (estrutura, termos, restrições, funções) está em validacao/motor.py;
// esta consulta devolve o que o motor lê do grafo: a projeção, os valores fixados e, por ocorrência, cada regra
// com a restrição e os termos da condição.
MATCH (pf:Perfil {nome: $perfil})-[:USA]->(pj:Projecao)-[:PROJETA]->(h:HLM)
OPTIONAL MATCH (pf)-[f:FIXA]->(alvo)
WITH pf, pj, h, collect({caminho: f.caminho, contexto: CASE WHEN alvo:ContextoExterno THEN alvo.nome END, valor: f.valor}) AS fixados
OPTIONAL MATCH (pj)-[o:OBRIGATORIA]->()
WITH pf, pj, h, fixados, collect(o.caminho) AS obrigatorias
OPTIONAL MATCH (pj)-[p:PERMITIDA]->()
WITH pf, pj, h, fixados, obrigatorias, collect(p.caminho) AS permitidas
MATCH caminho = (h)-[:COMPOSTO_POR*0..4]->(m)
WITH pf, pj, h, fixados, obrigatorias, permitidas, m,
     reduce(s = '', r IN relationships(caminho) | s + CASE s WHEN '' THEN '' ELSE '.' END + r.papel) AS ocorrencia
OPTIONAL MATCH (m)-[:CONTEM]->(prop:Propriedade)
WITH pf, pj, h, fixados, obrigatorias, permitidas, ocorrencia, m, collect(prop) AS props
UNWIND [m] + props AS no
MATCH (r:Regra)-[:ASSOCIADA_A]->(no)
OPTIONAL MATCH (r)-[:RESTRITA_POR]->(rs:Restricao)
OPTIONAL MATCH (rs)-[re:RESTRINGE]->()
OPTIONAL MATCH (rs)-[rc:CHAMA]->(fr:Funcao)
OPTIONAL MATCH (r)-[:CONDICIONADA_POR]->(c:CondicaoAplicabilidade)
OPTIONAL MATCH (c)-[t:TERMO]->()
OPTIONAL MATCH (c)-[tc:CHAMA]->(ft:Funcao)
RETURN pf.nome AS perfil, pj.nome AS projecao, h.nome AS hlm, fixados, obrigatorias, permitidas,
       ocorrencia, r.id AS regra, labels(r) AS tipo,
       coalesce(re.texto, rc.chamada) AS restricao, coalesce(re.caminho, rc.argumentos) AS lidoPelaRestricao,
       [x IN collect(DISTINCT {texto: t.texto, caminho: t.caminho, operador: t.operador, valor: t.valor, contexto: t.contexto})
        WHERE x.texto IS NOT NULL]
       + [x IN collect(DISTINCT {texto: tc.chamada, argumentos: tc.argumentos}) WHERE x.texto IS NOT NULL] AS termos
ORDER BY ocorrencia, regra;
