// ViewModel 'modelo' — a árvore de um modelo (HLM, SM ou USM) até às folhas, e quem o usa.
// Parâmetros: $nivel ("HLM", "SM" ou "USM"), $nome (ex.: "Dispositivo", "Cliente", "Morada").

// 1. Árvore: cada modelo alcançado por COMPOSTO_POR, com o caminho (papéis), a cardinalidade e as propriedades
MATCH (raiz {nome: $nome}) WHERE $nivel IN labels(raiz)
MATCH caminho = (raiz)-[:COMPOSTO_POR*0..]->(m)
WITH m, relationships(caminho) AS rs
WITH m, reduce(s = '', r IN rs | s + CASE s WHEN '' THEN '' ELSE '.' END + r.papel) AS caminho,
     CASE size(rs) WHEN 0 THEN null ELSE last(rs).cardinalidade END AS cardinalidade
OPTIONAL MATCH (m)-[c:CONTEM]->(p:Propriedade)
WITH m, caminho, cardinalidade, p, c ORDER BY c.ordem
RETURN caminho, labels(m)[0] AS nivel, m.nome AS modelo, cardinalidade, m.descricao AS descricao,
       [x IN collect(p) | {nome: x.nome, tipo: x.tipo, descricao: x.descricao}] AS propriedades
ORDER BY caminho;

// 2. Quem usa o modelo: os caminhos de composição desde cada HLM (vazio para um HLM)
MATCH (raiz {nome: $nome}) WHERE $nivel IN labels(raiz)
MATCH caminho = (h:HLM)-[:COMPOSTO_POR*1..]->(raiz)
RETURN h.nome AS hlm, [n IN nodes(caminho) | n.nome] AS modelos, [r IN relationships(caminho) | r.papel] AS papeis
ORDER BY hlm;

// 3. Projeções (só para um HLM)
MATCH (raiz:HLM {nome: $nome})<-[:PROJETA]-(pj:Projecao)
OPTIONAL MATCH (pf:Perfil)-[:USA]->(pj)
RETURN pj.nome AS projecao, pj.descricao AS descricao, collect(pf.nome) AS perfis
ORDER BY projecao;
