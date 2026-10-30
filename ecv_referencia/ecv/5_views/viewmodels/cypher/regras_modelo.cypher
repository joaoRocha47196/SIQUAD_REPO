// ViewModel 'modelo' com regras — as regras que vivem em cada nó (modelo ou propriedade) da árvore de um modelo,
// com a restrição (alvo, operador, valor), a condição (termos) e a mensagem em campos separados.
// Parâmetros: $nivel ("HLM", "SM" ou "USM"), $nome.
MATCH (raiz {nome: $nome}) WHERE $nivel IN labels(raiz)
MATCH caminho = (raiz)-[:COMPOSTO_POR*0..]->(m)
WITH m, reduce(s = '', r IN relationships(caminho) | s + CASE s WHEN '' THEN '' ELSE '.' END + r.papel) AS prefixo
OPTIONAL MATCH (m)-[:CONTEM]->(p:Propriedade)
WITH m, prefixo, collect(p) AS props
UNWIND [m] + props AS no
MATCH (r:Regra)-[:ASSOCIADA_A]->(no)
OPTIONAL MATCH (r)-[:RESTRITA_POR]->(rs:Restricao)
OPTIONAL MATCH (rs)-[rg:RESTRINGE]->(alvo:Propriedade)
OPTIONAL MATCH (rs)-[ch:CHAMA]->(f:Funcao)
OPTIONAL MATCH (r)-[:CONDICIONADA_POR]->(c:CondicaoAplicabilidade)
RETURN CASE WHEN no:Propriedade THEN CASE prefixo WHEN '' THEN no.nome ELSE prefixo + '.' + no.nome END
            ELSE prefixo END AS caminho,
       [l IN labels(r) WHERE l <> 'Regra'][0] AS tipo, r.id AS regra,
       c.descricao AS condicao, rs.forma AS forma, alvo.chave AS alvo, rg.operador AS operador, rg.valor AS valor,
       ch.chamada AS funcao, coalesce(rs.mensagem, r.mensagem) AS mensagem,
       CASE WHEN r:RIC THEN r.conclusaoTipo + ' ' + r.conclusaoValor END AS conclusao,
       r.contextosExternos AS contextos
ORDER BY caminho, tipo, regra;
