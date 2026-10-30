// Apaga todos os nós (e arestas) da ECV, para voltar a carregar.
MATCH (n) WHERE n:HLM OR n:SM OR n:USM OR n:Propriedade OR n:RP OR n:RIR OR n:RIC OR n:Restricao OR n:CondicaoAplicabilidade OR n:Funcao OR n:ContextoExterno OR n:Projecao OR n:Perfil DETACH DELETE n;
