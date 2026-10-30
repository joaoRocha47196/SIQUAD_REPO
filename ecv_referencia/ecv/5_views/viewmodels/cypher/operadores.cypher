// ViewModel 'operadores' — restrições e termos por operador; propriedades tratadas como enumerados.
// Parâmetros: nenhum.

// 1. Por operador
CALL () {
  MATCH (rs:Restricao)
  RETURN rs.operador AS operador, 'restrição' AS onde, rs.regra AS regra, rs.descricao AS texto
  UNION ALL
  MATCH (c:CondicaoAplicabilidade)-[t:TERMO]->()
  RETURN t.operador AS operador, 'termo' AS onde, c.regra AS regra, t.texto AS texto
  UNION ALL
  MATCH (c:CondicaoAplicabilidade)-[ch:CHAMA]->()
  RETURN ch.operador AS operador, 'termo' AS onde, c.regra AS regra, ch.chamada AS texto
}
RETURN operador, onde, regra, texto ORDER BY operador, regra;

// 2. Enumerados: propriedades com uma RP IN
MATCH (p:Propriedade)<-[:ASSOCIADA_A]-(:RP)-[:RESTRITA_POR]->(rs:Restricao {operador: 'IN'})
RETURN p.chave AS propriedade, rs.valor AS valores ORDER BY propriedade;
