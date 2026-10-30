// ViewModel 'impacto' — regras, projeções e perfis afetados por uma alteração da propriedade.
// Parâmetros: $propriedade (chave, ex.: "SM:Identificacao.tipoDispositivo").

// 1. Regras, com o papel da propriedade em cada uma
CALL () {
  MATCH (p:Propriedade {chave: $propriedade})<-[:RESTRINGE]-(:Restricao)<-[:RESTRITA_POR]-(r:Regra)
  RETURN r.id AS regra, 'alvo da restrição' AS papel
  UNION
  MATCH (p:Propriedade {chave: $propriedade})<-[:TERMO]-(:CondicaoAplicabilidade)<-[:CONDICIONADA_POR]-(r:Regra)
  RETURN r.id AS regra, 'termo da condição' AS papel
  UNION
  MATCH (p:Propriedade {chave: $propriedade})<-[le:LE]-(f:Funcao)
  RETURN le.regra AS regra, 'argumento de ' + f.nome AS papel
  UNION
  MATCH (p:Propriedade {chave: $propriedade})<-[:ASSOCIADA_A]-(r:Regra)
  RETURN r.id AS regra, 'vive na propriedade' AS papel
}
RETURN regra, collect(papel) AS papeis ORDER BY regra;

// 2. Projeções
MATCH (p:Propriedade {chave: $propriedade})<-[o:OBRIGATORIA|PERMITIDA]-(pj:Projecao)
RETURN pj.nome AS projecao, type(o) AS tipo, o.caminho AS caminho ORDER BY projecao, caminho;

// 3. Perfis
MATCH (p:Propriedade {chave: $propriedade})<-[f:FIXA]-(pf:Perfil)
RETURN pf.nome AS perfil, f.caminho AS caminho, f.valor AS valor;
