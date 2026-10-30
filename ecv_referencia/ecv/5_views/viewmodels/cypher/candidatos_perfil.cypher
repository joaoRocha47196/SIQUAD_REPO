// ViewModel 'candidatos_perfil' — propriedades usadas nas condições das RIR que restringem as propriedades dadas.
// Parâmetros: $alvos (lista de chaves, ex.: ["USM:Medicao.valor", "USM:Medicao.unidadeMedida"]).
UNWIND $alvos AS chave
MATCH (a:Propriedade {chave: chave})<-[:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(r:RIR)
      -[:CONDICIONADA_POR]->(:CondicaoAplicabilidade)-[:TERMO]->(d:Propriedade)
RETURN a.nome AS alvo, collect(DISTINCT r.id) AS regras, collect(DISTINCT d.nome) AS propriedades;
