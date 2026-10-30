// ViewModel 'projecoes' — matriz de projeções de um HLM e valores fixados pelos perfis.
// Parâmetros: $hlm (ex.: "Dispositivo").

// 1. Para cada caminho de propriedade, a marca em cada projeção (OBRIGATORIA / PERMITIDA; ausente = excluída)
MATCH (h:HLM {nome: $hlm})<-[:PROJETA]-(pj:Projecao)-[r:OBRIGATORIA|PERMITIDA]->(p:Propriedade)
RETURN r.caminho AS caminho, collect({projecao: pj.nome, marca: type(r)}) AS celulas
ORDER BY caminho;

// 2. Perfis que usam as projeções do HLM e o que fixam
MATCH (h:HLM {nome: $hlm})<-[:PROJETA]-(pj:Projecao)<-[:USA]-(pf:Perfil)
OPTIONAL MATCH (pf)-[f:FIXA]->(x)
RETURN pf.nome AS perfil, pj.nome AS projecao,
       [i IN collect({alvo: coalesce(f.caminho, x.nome), tipo: labels(x)[0], valor: f.valor}) WHERE i.alvo IS NOT NULL] AS fixa
ORDER BY perfil;
