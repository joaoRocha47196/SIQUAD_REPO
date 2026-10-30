// ViewModel 'lacunas' — propriedades sem regras e propriedades nunca projetadas, num HLM.
// Parâmetros: $hlm.

// 1. Sem regras: nenhuma aresta RESTRINGE, ASSOCIADA_A ou LE chega à propriedade
MATCH (h:HLM {nome: $hlm})-[:COMPOSTO_POR*1..2]->()-[:CONTEM]->(p:Propriedade)
WHERE NOT (p)<-[:RESTRINGE]-() AND NOT (p)<-[:ASSOCIADA_A]-() AND NOT (p)<-[:LE]-()
RETURN DISTINCT p.chave AS semRegras;

// 2. Nunca projetadas: nenhuma projeção do HLM tem OBRIGATORIA ou PERMITIDA para aquele caminho
MATCH (h:HLM {nome: $hlm})
MATCH caminho = (h)-[:COMPOSTO_POR*1..2]->()-[:CONTEM]->(p:Propriedade)
WITH h, p, reduce(s = '', r IN relationships(caminho)[0..-1] | s + r.papel + '.') + p.nome AS cam
WHERE NOT EXISTS { MATCH (h)<-[:PROJETA]-(:Projecao)-[o:OBRIGATORIA|PERMITIDA]->(p) WHERE o.caminho = cam }
RETURN cam AS nuncaProjetada ORDER BY cam;
