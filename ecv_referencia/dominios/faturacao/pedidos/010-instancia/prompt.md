# Criar uma instância de teste

Escreva uma instância JSON de um modelo de dados para testar a validação. A instância segue a estrutura abaixo (as chaves são os nomes das propriedades e os papéis das composições; uma composição repetível é uma lista). Use só as propriedades listadas e respeite os valores fixados.

## Cenário

perfil PERFILTESTE (projeção TESTE) do HLM DocumentoFaturacao

## O que se pretende

Quero criar uma isntancia de testes para este perfil que passe a todas as regras

## Estrutura (caminho: tipo, estado na projeção)

- CabecalhoDocumento (SM CabecalhoDocumento, cardinalidade 1..1)
- CabecalhoDocumento.tipoDocumento: texto, fixado no perfil = "381" — Código do tipo funcional do documento (UNCL 1001 ou código AT)
- CabecalhoDocumento.moeda: texto, fixado no perfil = "EUR" — Moeda em que estão os montantes do documento (ISO 4217 alfa-3)
- Fornecedor (SM Fornecedor, cardinalidade 1..1)
- Fornecedor.Morada (USM Morada, cardinalidade 1..1)
- Fornecedor.Morada.pais: texto, fixado no perfil = "PT" — País da morada (código ISO de duas letras)
- LinhaDocumento (SM LinhaDocumento, cardinalidade 1..*)
- LinhaDocumento.Encargo (USM DescontoEncargo, cardinalidade 0..*)
- LinhaDocumento.Encargo.montante: decimal, obrigatório — Montante do desconto ou do encargo, sem impostos
- LinhaDocumento.Encargo.montanteBase: decimal, obrigatório — Montante base sobre o qual incide a percentagem
- LinhaDocumento.Encargo.motivo: texto, obrigatório — Descrição em texto do motivo do desconto ou do encargo
- Metainformacao (SM Metainformacao, cardinalidade 0..1)
- Metainformacao.origemModelo: texto, permitido — Fonte do modelo de dados (norma, sistema ou repositório)
- Metainformacao.referenciaOrigem: texto, permitido — Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)

## Regras que se aplicam

- RP-IVA-BASE (RP): baseTributavelCoerente(DecomposicaoIva, LinhaDocumento, Desconto, Encargo, 1) [em: (raiz)]
- RP-IVA-DECOMP (RP): categoriasIvaDecompostas(LinhaDocumento.CategoriaIva.codigoCategoria, Desconto.CategoriaIva.codigoCategoria, Encargo.CategoriaIva.codigoCategoria, DecomposicaoIva.CategoriaIva.codigoCategoria) [em: (raiz)]
- RP-LENT-MORADA (RP): colecaoNaoVazia(LocalEntrega.Morada.rua) [em: (raiz)]
- RP-LIN-UNICAS (RP): valoresTextoUnicos(LinhaDocumento.identificador) [em: (raiz)]
- RP-SOMA-DESCONTOS (RP): somaIgualATolerancia(Desconto.DescontoEncargo.montante, Totais.totalDescontos, 1) [em: (raiz)]
- RP-SOMA-ENCARGOS (RP): somaIgualATolerancia(Encargo.DescontoEncargo.montante, Totais.totalEncargos, 1) [em: (raiz)]
- RP-SOMA-IVA (RP): somaIgualATolerancia(DecomposicaoIva.montanteImposto, Totais.totalIva, 1) [em: (raiz)]
- RP-SOMA-LINHAS (RP): somaIgualATolerancia(LinhaDocumento.montanteLiquido, Totais.somaLinhas, 1) [em: (raiz)]
- RIR-PAGAMENTO-PRAZO (RIR): Se Totais.valorPagar > 0 → algumPresente(CabecalhoDocumento.dataVencimento, CabecalhoDocumento.condicoesPagamento) [em: (raiz)]
- RIR-REFANT-NC (RIR): Se CabecalhoDocumento.tipoDocumento ∈ {381, NC} → colecaoNaoVazia(DocumentosAnteriores.ReferenciaDocumento.numero) [em: (raiz)]
- RIR-REFANT-ND (RIR): Se CabecalhoDocumento.tipoDocumento ∈ {383, ND} → colecaoNaoVazia(DocumentosAnteriores.ReferenciaDocumento.numero) [em: (raiz)]
- RIR-TOT-DESCONTOS (RIR): Se colecaoNaoVazia(Desconto.DescontoEncargo.montante) → existe(Totais.totalDescontos) [em: (raiz)]
- RIR-TOT-ENCARGOS (RIR): Se colecaoNaoVazia(Encargo.DescontoEncargo.montante) → existe(Totais.totalEncargos) [em: (raiz)]
- RP-DOC-DATAIVA (RP): mutuamenteExclusivos(CabecalhoDocumento.dataIva, CabecalhoDocumento.codigoDataIva) [em: CabecalhoDocumento]
- RP-DOC-NUMERO (RP): CabecalhoDocumento.numero tem entre 1 e 50 caracteres [em: CabecalhoDocumento]
- RP-DOC-TIPO (RP): CabecalhoDocumento.tipoDocumento ∈ {380, 381, 383, 386, 389, FT, FS, FR, ND, NC, RP, RE, CS, LD, RA} [em: CabecalhoDocumento]
- RP-DOC-MOEDA (RP): CabecalhoDocumento.moeda segue o padrão ^[A-Z]{3}$ [em: CabecalhoDocumento]
- RP-DOC-MOEDAIVA (RP): CabecalhoDocumento.moedaIva segue o padrão ^[A-Z]{3}$ [em: CabecalhoDocumento]
- RP-DOC-CODDATAIVA (RP): CabecalhoDocumento.codigoDataIva ∈ {3, 35, 432} [em: CabecalhoDocumento]
- RP-DOC-REFCLIENTE (RP): CabecalhoDocumento.referenciaCliente tem entre 1 e 50 caracteres [em: CabecalhoDocumento]
- RP-DOC-COMPROMISSO (RP): CabecalhoDocumento.numeroCompromisso tem entre 1 e 50 caracteres [em: CabecalhoDocumento]
- RP-DOC-CONDPAG (RP): CabecalhoDocumento.condicoesPagamento tem entre 1 e 200 caracteres [em: CabecalhoDocumento]
- RP-DOC-PROCESSO (RP): CabecalhoDocumento.tipoProcesso tem entre 1 e 50 caracteres [em: CabecalhoDocumento]
- RP-DOC-ESPEC (RP): CabecalhoDocumento.identificadorEspecificacao segue o padrão ^urn:cen\.eu:en16931:2017#compliant#urn:feap\.gov\.pt:CIUS-PT:.{1,10}$ [em: CabecalhoDocumento]
- RP-FORN-REGFISCAL (RP): Fornecedor.registoFiscal tem entre 1 e 50 caracteres [em: Fornecedor]
- RP-FORN-CAPITAL (RP): Fornecedor.capitalSocial tem entre 1 e 200 caracteres [em: Fornecedor]
- RP-FORN-ENDELET (RP): Fornecedor.enderecoEletronico tem entre 1 e 50 caracteres [em: Fornecedor]
- RP-TESTE (RP): Fornecedor.enderecoEletronico ≠ email@gmail.com [em: Fornecedor]
- RP-FORN-CONTACTO (RP): Fornecedor.pontoContacto tem entre 1 e 200 caracteres [em: Fornecedor]
- RIR-CP-ES (RIR): Se Morada.pais = ES → Morada.codigoPostal segue o padrão ^[0-5][0-9]{4}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-GB (RIR): Se Morada.pais = GB → Morada.codigoPostal segue o padrão ^[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-AJUDA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AJUDA → Morada.codigoPostal segue o padrão ^(1300|1349)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-ALCANTARA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALCANTARA → Morada.codigoPostal segue o padrão ^(1300|1350)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-ALVALADE (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ALVALADE → Morada.codigoPostal segue o padrão ^(1700|1749)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-AREEIRO (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AREEIRO → Morada.codigoPostal segue o padrão ^(1000|1049)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-ARROIOS (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ARROIOS → Morada.codigoPostal segue o padrão ^(1150|1169)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-AVENIDAS-NOVAS (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = AVENIDAS_NOVAS → Morada.codigoPostal segue o padrão ^(1050|1069)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-BEATO (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BEATO → Morada.codigoPostal segue o padrão ^(1900|1949)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-BELEM (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BELEM → Morada.codigoPostal segue o padrão ^(1400|1449)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-BENFICA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = BENFICA → Morada.codigoPostal segue o padrão ^(1500|1549)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-CAMPO-DE-OURIQUE (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPO_DE_OURIQUE → Morada.codigoPostal segue o padrão ^(1250|1350)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-CAMPOLIDE (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CAMPOLIDE → Morada.codigoPostal segue o padrão ^(1070|1099)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-CARNIDE (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = CARNIDE → Morada.codigoPostal segue o padrão ^(1600|1649)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-ESTRELA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = ESTRELA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-LUMIAR (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = LUMIAR → Morada.codigoPostal segue o padrão ^(1600|1750)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-MARVILA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MARVILA → Morada.codigoPostal segue o padrão ^(1800|1949)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-MISERICORDIA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = MISERICORDIA → Morada.codigoPostal segue o padrão ^(1200|1249)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-OLIVAIS (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = OLIVAIS → Morada.codigoPostal segue o padrão ^(1800|1885)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-PARQUE-DAS-NACOES (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PARQUE_DAS_NACOES → Morada.codigoPostal segue o padrão ^(1990|1998)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-PENHA-DE-FRANCA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = PENHA_DE_FRANCA → Morada.codigoPostal segue o padrão ^(1170|1199)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-SANTA-CLARA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_CLARA → Morada.codigoPostal segue o padrão ^(1750|1769)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-SANTA-MARIA-MAIOR (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTA_MARIA_MAIOR → Morada.codigoPostal segue o padrão ^(1100|1149)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-SANTO-ANTONIO (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SANTO_ANTONIO → Morada.codigoPostal segue o padrão ^(1250|1269)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_DOMINGOS_DE_BENFICA → Morada.codigoPostal segue o padrão ^(1500|1600)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-LX-SAO-VICENTE (RIR): Se Morada.pais = PT e Morada.localidade = LISBOA e Morada.freguesia = SAO_VICENTE → Morada.codigoPostal segue o padrão ^(1100|1170)-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RIR-CP-PT (RIR): Se Morada.pais = PT → Morada.codigoPostal segue o padrão ^[1-9][0-9]{3}-[0-9]{3}$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RP-CP (RP): Morada.codigoPostal segue o padrão ^([1-9][0-9]{3}-[0-9]{3}|[0-5][0-9]{4}|[A-Z]{1,2}[0-9][0-9A-Z]? [0-9][A-Z]{2})$ [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RP-FREGUESIA (RP): Morada.freguesia ∈ {AJUDA, ALCANTARA, ALVALADE, AREEIRO, ARROIOS, AVENIDAS_NOVAS, BEATO, BELEM, BENFICA, CAMPO_DE_OURIQUE, CAMPOLIDE, CARNIDE, ESTRELA, LUMIAR, MARVILA, MISERICORDIA, OLIVAIS, PARQUE_DAS_NACOES, PENHA_DE_FRANCA, SANTA_CLARA, SANTA_MARIA_MAIOR, SANTO_ANTONIO, SAO_DOMINGOS_DE_BENFICA, SAO_VICENTE} [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RP-PAIS (RP): Morada.pais ∈ {PT, ES, GB} [em: Adquirente.Morada, Fornecedor.Morada, LocalEntrega.Morada, RepresentanteFiscal.Morada]
- RP-DE-CALCULO (RP): produtoPercentualIgualA(DescontoEncargo.montanteBase, DescontoEncargo.percentagem, DescontoEncargo.montante, 1) [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-JUSTIFICADO (RP): algumPresente(DescontoEncargo.motivo, DescontoEncargo.codigoMotivo) [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-MONTANTE (RP): DescontoEncargo.montante ≥ 0 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-BASE (RP): DescontoEncargo.montanteBase ≥ 0 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-PERC (RP): DescontoEncargo.percentagem entre 0 e 100 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-MOTIVO (RP): DescontoEncargo.motivo tem entre 1 e 200 caracteres [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-CODMOTIVO (RP): DescontoEncargo.codigoMotivo segue o padrão ^[A-Z0-9]{1,3}$ [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-LIN-MONTANTE (RP): montanteLinhaCoerente(LinhaDocumento.quantidade, LinhaDocumento.Preco.precoLiquido, LinhaDocumento.Preco.quantidadeBase, LinhaDocumento.Desconto.montante, LinhaDocumento.Encargo.montante, LinhaDocumento.montanteLiquido, 1) [em: LinhaDocumento]
- RIR-LIN-ISENCAO (RIR): Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {E, ISE} → algumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao) [em: LinhaDocumento]
- RIR-LIN-SEM-ISENCAO (RIR): Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao) [em: LinhaDocumento]
- RP-LIN-ID (RP): LinhaDocumento.identificador tem entre 1 e 50 caracteres [em: LinhaDocumento]
- RP-LIN-NOTA (RP): LinhaDocumento.nota tem entre 1 e 500 caracteres [em: LinhaDocumento]
- RP-LIN-OBJETO (RP): LinhaDocumento.identificadorObjeto tem entre 1 e 50 caracteres [em: LinhaDocumento]
- RP-LIN-UNIDADE (RP): LinhaDocumento.unidadeMedida segue o padrão ^[A-Z0-9]{1,3}$ [em: LinhaDocumento]
- RP-LIN-REFENC (RP): LinhaDocumento.referenciaLinhaEncomenda tem entre 1 e 20 caracteres [em: LinhaDocumento]
- RP-LIN-COMPROMISSO (RP): LinhaDocumento.numeroCompromisso tem entre 1 e 200 caracteres [em: LinhaDocumento]

## Contextos externos

(nenhum)

## Esqueleto (a completar)

```json
{
 "descricao": "",
 "perfil": "PERFILTESTE",
 "contextos": {},
 "instancia": {
  "CabecalhoDocumento": {
   "tipoDocumento": "381",
   "moeda": "EUR"
  },
  "Fornecedor": {
   "Morada": {
    "pais": "PT"
   }
  },
  "LinhaDocumento": [
   {
    "Encargo": [
     {
      "montante": 0.0,
      "montanteBase": 0.0,
      "motivo": ""
     }
    ]
   }
  ],
  "Metainformacao": {
   "origemModelo": "",
   "referenciaOrigem": ""
  }
 }
}
```

## O que responder

Só o JSON, com a forma do esqueleto: `{"descricao": "<o que a instância testa>", "perfil" ou "hlm", "contextos": {...}, "instancia": {...}}`. Se o pedido é uma instância com erros, diga na descrição que regras devem falhar e porquê.
