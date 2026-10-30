// ViewModel 'perfil' — seleção estática: estado de cada termo das condições face aos valores fixados no perfil.
// Parâmetros: $perfil (ex.: "RefrigeracaoLote").
// Termo: verdadeiro/falso (EQUALS resolvido pelo valor fixado), dinâmico (propriedade projetada), indisponível.
// A classificação completa (todos os operadores, estado da regra) está em vistas/viewmodels/perfis.py.
MATCH (pf:Perfil {nome: $perfil})-[:USA]->(pj:Projecao)-[:PROJETA]->(h:HLM)
OPTIONAL MATCH (pf)-[f:FIXA]->(:Propriedade)
WITH pj, h, collect({caminho: f.caminho, valor: f.valor}) AS fixados
MATCH caminho = (h)-[:COMPOSTO_POR*0..2]->(m)
WITH pj, fixados, m, reduce(s = '', r IN relationships(caminho) | s + CASE s WHEN '' THEN '' ELSE '.' END + r.papel) AS prefixo
OPTIONAL MATCH (m)-[:CONTEM]->(prop:Propriedade)
WITH pj, fixados, prefixo, m, collect(prop) AS props
UNWIND [m] + props AS no
MATCH (r:Regra)-[:ASSOCIADA_A]->(no)
MATCH (r)-[:CONDICIONADA_POR]->(:CondicaoAplicabilidade)-[t:TERMO]->(:Propriedade)
WITH pj, fixados, r, t, CASE prefixo WHEN '' THEN t.caminho ELSE prefixo + '.' + t.caminho END AS absoluto
WITH pj, r, t, absoluto, [x IN fixados WHERE x.caminho = absoluto | x.valor][0] AS fixado
OPTIONAL MATCH (pj)-[o:OBRIGATORIA|PERMITIDA {caminho: absoluto}]->()
RETURN r.id AS regra, t.texto AS termo, absoluto AS caminho, fixado,
       CASE WHEN fixado IS NOT NULL THEN
              CASE WHEN t.operador = 'EQUALS' THEN CASE WHEN fixado = t.valor THEN 'verdadeiro' ELSE 'falso' END
                   ELSE 'resolvido pelo perfil' END
            WHEN o IS NOT NULL THEN 'dinâmico'
            ELSE 'indisponível' END AS estado
ORDER BY regra, caminho;
