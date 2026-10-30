# Pedido de alterações (contexto focado) → operações

## Objetivo

Traduzir um pedido de alterações, escrito em linguagem natural, numa lista de operações do vocabulário fechado. O código aplica-as de forma determinística às declarações do domínio. O contexto abaixo foi escolhido pela pessoa: são as entidades a que o pedido se refere (e as que ajudam a escrever as operações). Não alteres nada que o pedido não diga; se for ambíguo, escolhe a interpretação mínima e explica-a em `notas`. Se precisares de uma entidade que não está no contexto, usa o índice; se faltar informação, pede-a em `notas` em vez de a inventar.

Camada: B · Projeções (RE)

Declarar as utilizações de cada HLM (projeções) com as propriedades obrigatórias e permitidas: as regras estruturais.

Princípios:
- A obrigatoriedade de uma propriedade numa utilização exprime-se na projeção, não numa regra.
- Uma projeção por utilização real (fatura eletrónica CIUS-PT, nota de crédito, exportação FM); não se inventam utilizações.
- Caminhos a partir do HLM; X.* para tudo abaixo de X; um caminho não pode ser obrigatório e permitido ao mesmo tempo.
- Regras de presença condicionais ('se existir X, então Y é obrigatório') não são projeções: são RIR (com uma função de presença).

## Pedido

Se a o valor da fatura for menos que 1000 ent a propriedade de estado tipoDeValor deve ser SMALL se for acime de 1000 deve ser BIG

## Informação adicional (outra fonte)

(nenhuma)

## Contexto escolhido (as entidades, tal como estão nas declarações)

```json
{
 "caminhosDoHlm": [
  "CabecalhoDocumento.numero",
  "CabecalhoDocumento.dataEmissao",
  "CabecalhoDocumento.tipoDocumento",
  "CabecalhoDocumento.moeda",
  "CabecalhoDocumento.moedaIva",
  "CabecalhoDocumento.dataIva",
  "CabecalhoDocumento.codigoDataIva",
  "CabecalhoDocumento.dataVencimento",
  "CabecalhoDocumento.referenciaCliente",
  "CabecalhoDocumento.numeroCompromisso",
  "CabecalhoDocumento.condicoesPagamento",
  "CabecalhoDocumento.tipoProcesso",
  "CabecalhoDocumento.identificadorEspecificacao",
  "ReferenciasDocumento.projeto",
  "ReferenciasDocumento.contrato",
  "ReferenciasDocumento.encomenda",
  "ReferenciasDocumento.ordemVenda",
  "ReferenciasDocumento.avisoRececao",
  "ReferenciasDocumento.avisoEnvio",
  "ReferenciasDocumento.acordoQuadro",
  "ReferenciasDocumento.processoRegisto",
  "NotaDocumento.assunto",
  "NotaDocumento.texto",
  "DocumentosAnteriores.ReferenciaDocumento.numero",
  "DocumentosAnteriores.ReferenciaDocumento.dataEmissao",
  "Fornecedor.registoFiscal",
  "Fornecedor.capitalSocial",
  "Fornecedor.enderecoEletronico",
  "Fornecedor.pontoContacto",
  "Fornecedor.SujeitoPassivo.nome",
  "Fornecedor.SujeitoPassivo.nomeComercial",
  "Fornecedor.SujeitoPassivo.identificador",
  "Fornecedor.SujeitoPassivo.identificadorRegisto",
  "Fornecedor.SujeitoPassivo.identificadorIva",
  "Fornecedor.Morada.rua",
  "Fornecedor.Morada.codigoPostal",
  "Fornecedor.Morada.localidade",
  "Fornecedor.Morada.freguesia",
  "Fornecedor.Morada.pais",
  "Fornecedor.ComplementoMorada.linha2",
  "Fornecedor.ComplementoMorada.linha3",
  "Fornecedor.ComplementoMorada.regiao",
  "Fornecedor.ContactoTelefonico.telefone",
  "Fornecedor.ContactoTelefonico.telemovel",
  "Fornecedor.Contacto.email",
  "Adquirente.enderecoEletronico",
  "Adquirente.pontoContacto",
  "Adquirente.SujeitoPassivo.nome",
  "Adquirente.SujeitoPassivo.nomeComercial",
  "Adquirente.SujeitoPassivo.identificador",
  "Adquirente.SujeitoPassivo.identificadorRegisto",
  "Adquirente.SujeitoPassivo.identificadorIva",
  "Adquirente.Morada.rua",
  "Adquirente.Morada.codigoPostal",
  "Adquirente.Morada.localidade",
  "Adquirente.Morada.freguesia",
  "Adquirente.Morada.pais",
  "Adquirente.ComplementoMorada.linha2",
  "Adquirente.ComplementoMorada.linha3",
  "Adquirente.ComplementoMorada.regiao",
  "Adquirente.ContactoTelefonico.telefone",
  "Adquirente.ContactoTelefonico.telemovel",
  "Adquirente.Contacto.email",
  "RecebedorPagamento.SujeitoPassivo.nome",
  "RecebedorPagamento.SujeitoPassivo.nomeComercial",
  "RecebedorPagamento.SujeitoPassivo.identificador",
  "RecebedorPagamento.SujeitoPassivo.identificadorRegisto",
  "RecebedorPagamento.SujeitoPassivo.identificadorIva",
  "RepresentanteFiscal.SujeitoPassivo.nome",
  "RepresentanteFiscal.SujeitoPassivo.nomeComercial",
  "RepresentanteFiscal.SujeitoPassivo.identificador",
  "RepresentanteFiscal.SujeitoPassivo.identificadorRegisto",
  "RepresentanteFiscal.SujeitoPassivo.identificadorIva",
  "RepresentanteFiscal.Morada.rua",
  "RepresentanteFiscal.Morada.codigoPostal",
  "RepresentanteFiscal.Morada.localidade",
  "RepresentanteFiscal.Morada.freguesia",
  "RepresentanteFiscal.Morada.pais",
  "RepresentanteFiscal.ComplementoMorada.linha2",
  "RepresentanteFiscal.ComplementoMorada.linha3",
  "RepresentanteFiscal.ComplementoMorada.regiao",
  "LocalEntrega.nomeLocal",
  "LocalEntrega.identificadorLocal",
  "LocalEntrega.dataEntrega",
  "LocalEntrega.Morada.rua",
  "LocalEntrega.Morada.codigoPostal",
  "LocalEntrega.Morada.localidade",
  "LocalEntrega.Morada.freguesia",
  "LocalEntrega.Morada.pais",
  "LocalEntrega.ComplementoMorada.linha2",
  "LocalEntrega.ComplementoMorada.linha3",
  "LocalEntrega.ComplementoMorada.regiao",
  "PeriodoFaturacao.Periodo.dataInicio",
  "PeriodoFaturacao.Periodo.dataFim",
  "Pagamento.meioPagamento",
  "Pagamento.detalhePagamento",
  "Pagamento.referenciaPagamento",
  "Pagamento.ContaBancaria.iban",
  "Pagamento.ContaBancaria.nomeConta",
  "Pagamento.ContaBancaria.bic",
  "Pagamento.CartaoPagamento.numeroConta",
  "Pagamento.CartaoPagamento.titular",
  "Pagamento.DebitoDireto.referenciaMandato",
  "Pagamento.DebitoDireto.identificadorCredor",
  "Pagamento.DebitoDireto.contaDebitada",
  "Desconto.DescontoEncargo.montante",
  "Desconto.DescontoEncargo.montanteBase",
  "Desconto.DescontoEncargo.percentagem",
  "Desconto.DescontoEncargo.motivo",
  "Desconto.DescontoEncargo.codigoMotivo",
  "Desconto.CategoriaIva.codigoCategoria",
  "Desconto.CategoriaIva.taxa",
  "Desconto.CategoriaIva.motivoIsencao",
  "Desconto.CategoriaIva.codigoMotivoIsencao",
  "Encargo.DescontoEncargo.montante",
  "Encargo.DescontoEncargo.montanteBase",
  "Encargo.DescontoEncargo.percentagem",
  "Encargo.DescontoEncargo.motivo",
  "Encargo.DescontoEncargo.codigoMotivo",
  "Encargo.CategoriaIva.codigoCategoria",
  "Encargo.CategoriaIva.taxa",
  "Encargo.CategoriaIva.motivoIsencao",
  "Encargo.CategoriaIva.codigoMotivoIsencao",
  "Totais.somaLinhas",
  "Totais.totalDescontos",
  "Totais.totalEncargos",
  "Totais.totalSemIva",
  "Totais.totalIva",
  "Totais.totalIvaMoedaContabilistica",
  "Totais.totalComIva",
  "Totais.valorPago",
  "Totais.arredondamento",
  "Totais.valorPagar",
  "DecomposicaoIva.baseTributavel",
  "DecomposicaoIva.montanteImposto",
  "DecomposicaoIva.CategoriaIva.codigoCategoria",
  "DecomposicaoIva.CategoriaIva.taxa",
  "DecomposicaoIva.CategoriaIva.motivoIsencao",
  "DecomposicaoIva.CategoriaIva.codigoMotivoIsencao",
  "DocumentoSuporte.referencia",
  "DocumentoSuporte.descricao",
  "DocumentoSuporte.localizacaoExterna",
  "DocumentoSuporte.anexo",
  "DocumentoSuporte.tipoMime",
  "DocumentoSuporte.nomeFicheiro",
  "LinhaDocumento.identificador",
  "LinhaDocumento.nota",
  "LinhaDocumento.identificadorObjeto",
  "LinhaDocumento.quantidade",
  "LinhaDocumento.unidadeMedida",
  "LinhaDocumento.montanteLiquido",
  "LinhaDocumento.referenciaLinhaEncomenda",
  "LinhaDocumento.numeroCompromisso",
  "LinhaDocumento.Artigo.nome",
  "LinhaDocumento.Artigo.descricao",
  "LinhaDocumento.Artigo.codigo",
  "LinhaDocumento.Artigo.codigoComprador",
  "LinhaDocumento.Artigo.codigoBarras",
  "LinhaDocumento.Artigo.classificacao",
  "LinhaDocumento.Artigo.paisOrigem",
  "LinhaDocumento.Preco.precoLiquido",
  "LinhaDocumento.Preco.descontoPreco",
  "LinhaDocumento.Preco.precoBruto",
  "LinhaDocumento.Preco.quantidadeBase",
  "LinhaDocumento.Preco.unidadeQuantidadeBase",
  "LinhaDocumento.CategoriaIva.codigoCategoria",
  "LinhaDocumento.CategoriaIva.taxa",
  "LinhaDocumento.CategoriaIva.motivoIsencao",
  "LinhaDocumento.CategoriaIva.codigoMotivoIsencao",
  "LinhaDocumento.Periodo.dataInicio",
  "LinhaDocumento.Periodo.dataFim",
  "LinhaDocumento.Desconto.montante",
  "LinhaDocumento.Desconto.montanteBase",
  "LinhaDocumento.Desconto.percentagem",
  "LinhaDocumento.Desconto.motivo",
  "LinhaDocumento.Desconto.codigoMotivo",
  "LinhaDocumento.Encargo.montante",
  "LinhaDocumento.Encargo.montanteBase",
  "LinhaDocumento.Encargo.percentagem",
  "LinhaDocumento.Encargo.motivo",
  "LinhaDocumento.Encargo.codigoMotivo",
  "LinhaDocumento.AtributoArtigo.nome",
  "LinhaDocumento.AtributoArtigo.valor",
  "Metainformacao.origemModelo",
  "Metainformacao.versaoOrigem",
  "Metainformacao.referenciaOrigem",
  "Metainformacao.utilizacao",
  "Metainformacao.dominio",
  "Metainformacao.observacoes"
 ]
}
```

## Índice do que existe (nomes, para referir entidades fora do contexto)

- HLM DocumentoFaturacao — compõe: CabecalhoDocumento:CabecalhoDocumento, ReferenciasDocumento:ReferenciasDocumento, NotaDocumento:NotaDocumento, DocumentosAnteriores:DocumentosAnteriores, Fornecedor:Fornecedor, Adquirente:Adquirente, RecebedorPagamento:RecebedorPagamento, RepresentanteFiscal:RepresentanteFiscal, LocalEntrega:LocalEntrega, PeriodoFaturacao:PeriodoFaturacao, Pagamento:Pagamento, Desconto:DescontoEncargoDocumento, Encargo:DescontoEncargoDocumento, Totais:Totais, DecomposicaoIva:DecomposicaoIva, DocumentoSuporte:DocumentoSuporte, LinhaDocumento:LinhaDocumento, Metainformacao:Metainformacao
- HLM EntregaTST — compõe: DadosEntrega:DadosEntrega, Comprador:ClienteVenda, Destinatario:ClienteVenda, LinhaEntrega:LinhaEntrega, ConfirmacaoEntrega:ConfirmacaoEntrega, Metainformacao:Metainformacao
- HLM ExportacaoFm — compõe: CabecalhoExportacao:CabecalhoExportacao, Vendedor:Vendedor, ClienteVenda:ClienteVenda, SaldoCliente:SaldoCliente, ArtigoStock:ArtigoStock, ProdutoVeiculo:ProdutoVeiculo, Zona:Zona, Auxiliar:Auxiliar, Configuracao:Configuracao, Metainformacao:Metainformacao
- HLM MensagemEstado — compõe: CabecalhoMensagem:CabecalhoMensagem, Emissor:ParteMensagem, Recetor:ParteMensagem, RespostaDocumento:RespostaDocumento, Metainformacao:Metainformacao
- SM Metainformacao — propriedades: origemModelo, versaoOrigem, referenciaOrigem, utilizacao, dominio, observacoes
- SM CabecalhoDocumento — propriedades: numero, dataEmissao, tipoDocumento, moeda, moedaIva, dataIva, codigoDataIva, dataVencimento, referenciaCliente, numeroCompromisso, condicoesPagamento, tipoProcesso, identificadorEspecificacao
- SM ReferenciasDocumento — propriedades: projeto, contrato, encomenda, ordemVenda, avisoRececao, avisoEnvio, acordoQuadro, processoRegisto
- SM NotaDocumento — propriedades: assunto, texto
- SM DocumentosAnteriores — compõe: ReferenciaDocumento:ReferenciaDocumento
- SM Fornecedor — propriedades: registoFiscal, capitalSocial, enderecoEletronico, pontoContacto — compõe: SujeitoPassivo:SujeitoPassivo, Morada:Morada, ComplementoMorada:ComplementoMorada, ContactoTelefonico:ContactoTelefonico, Contacto:Contacto
- SM Adquirente — propriedades: enderecoEletronico, pontoContacto — compõe: SujeitoPassivo:SujeitoPassivo, Morada:Morada, ComplementoMorada:ComplementoMorada, ContactoTelefonico:ContactoTelefonico, Contacto:Contacto
- SM RecebedorPagamento — compõe: SujeitoPassivo:SujeitoPassivo
- SM RepresentanteFiscal — compõe: SujeitoPassivo:SujeitoPassivo, Morada:Morada, ComplementoMorada:ComplementoMorada
- SM LocalEntrega — propriedades: nomeLocal, identificadorLocal, dataEntrega — compõe: Morada:Morada, ComplementoMorada:ComplementoMorada
- SM PeriodoFaturacao — compõe: Periodo:Periodo
- SM Pagamento — propriedades: meioPagamento, detalhePagamento, referenciaPagamento — compõe: ContaBancaria:ContaBancaria, CartaoPagamento:CartaoPagamento, DebitoDireto:DebitoDireto
- SM DescontoEncargoDocumento — compõe: DescontoEncargo:DescontoEncargo, CategoriaIva:CategoriaIva
- SM Totais — propriedades: somaLinhas, totalDescontos, totalEncargos, totalSemIva, totalIva, totalIvaMoedaContabilistica, totalComIva, valorPago, arredondamento, valorPagar
- SM DecomposicaoIva — propriedades: baseTributavel, montanteImposto — compõe: CategoriaIva:CategoriaIva
- SM DocumentoSuporte — propriedades: referencia, descricao, localizacaoExterna, anexo, tipoMime, nomeFicheiro
- SM LinhaDocumento — propriedades: identificador, nota, identificadorObjeto, quantidade, unidadeMedida, montanteLiquido, referenciaLinhaEncomenda, numeroCompromisso — compõe: Artigo:Artigo, Preco:Preco, CategoriaIva:CategoriaIva, Periodo:Periodo, Desconto:DescontoEncargo, Encargo:DescontoEncargo, AtributoArtigo:AtributoArtigo
- SM ClienteVenda — propriedades: codigo, designacaoPostal, designacaoPostalSegundoTitular, zona, localCobranca, observacoes, codigoVendedor, numeroOrdem, dataNascimento, diaRecebimento, novo, dataRegisto — compõe: Entidade:Entidade, Morada:Morada, Contacto:Contacto, ContactoTelefonico:ContactoTelefonico, CartaoCidadao:DocumentoIdentificacao, SegundoTitular:Entidade, MoradaSegundoTitular:Morada, ContactoSegundoTitular:ContactoTelefonico, CartaoCidadaoSegundoTitular:DocumentoIdentificacao
- SM DadosEntrega — propriedades: numeroEntrega, numeroFatura, numeroGuiaTransporte, numeroContrato, numeroDocumentoVenda, tipoDocumento, estado, data, dataRegisto
- SM LinhaEntrega — propriedades: numeroSerie, quantidade, precoPersonalizado, descontoPersonalizado — compõe: Artigo:Artigo
- SM ConfirmacaoEntrega — propriedades: documentoConfirmado, contratoConfirmado, entregaConfirmada, precoOriginal, sinal, prestacao
- SM Vendedor — propriedades: codigo, dataRegisto, designacaoPostal, numeroUltimoCliente, serie, dataInicioSerie, numeroDigitosSerie, prefixoAtcud, comissaoVendaPronto, comissaoVendaPrestacao, comissaoCobranca, numeroGuiaTransporte, numeroGuiaTransporteExtra, codigoFamiliaExtra, trataRecebimentos, nifEmissor — compõe: Entidade:Entidade, Morada:Morada, ContactoTelefonico:ContactoTelefonico, Veiculo:Veiculo, NumeracaoDocumento:NumeracaoDocumento
- SM CabecalhoExportacao — propriedades: nomeFicheiro, tamanhoFicheiro, dataModificacao, numeroClientes, numeroArtigos, numeroEntregas, numeroLinhasEntrega, numeroArtigosVeiculo, numeroZonas
- SM SaldoCliente — propriedades: codigoCliente, saldo, totalVendas, saldoInicial, pagoSaldoInicial, dataSaldoInicial
- SM ArtigoStock — propriedades: codigoAuxiliar, referencia, unidadeMedida, dataRegisto, formaArtigo, precoVendaComIva, precoVendaSemIva, precoVenda2ComIva, precoVenda2SemIva, precoPublico, desconto1, desconto2, taxaIva, ecoTaxa, precoCusto, descontoCusto, precoCustoSemIva, precoCustoComIva, precoCusto2SemIva, precoCusto2ComIva, quantidadeStock, quantidadeStockFora, peso, codigoFamilia, descricaoFamilia, codigoFornecedor, nomeFornecedor, servico, exportaObservacoes, observacoes, emVeiculo, matriculaVeiculo — compõe: Artigo:Artigo
- SM ProdutoVeiculo — propriedades: matricula, codigoArtigo, quantidadeTotal, quantidadeNormal, quantidadeFora
- SM Zona — propriedades: codigo, nome
- SM Auxiliar — propriedades: identificador, texto
- SM Configuracao — compõe: ParametroEmpresa:ParametroConfiguracao, ParametroAplicacao:ParametroConfiguracao, ParametroVendedor:ParametroConfiguracao
- SM CabecalhoMensagem — propriedades: identificadorEspecificacao, numero, dataEmissao, horaEmissao, nota
- SM ParteMensagem — compõe: SujeitoPassivo:SujeitoPassivo, Morada:Morada, Contacto:Contacto
- SM RespostaDocumento — propriedades: codigoResposta, descricaoResposta, uuidDocumento, tipoDocumento, estadoDocumento — compõe: ReferenciaDocumento:ReferenciaDocumento
- USM SujeitoPassivo — propriedades: nome, nomeComercial, identificador, identificadorRegisto, identificadorIva
- USM Morada — propriedades: rua, codigoPostal, localidade, freguesia, pais
- USM ComplementoMorada — propriedades: linha2, linha3, regiao
- USM Contacto — propriedades: email
- USM ContactoTelefonico — propriedades: telefone, telemovel
- USM ReferenciaDocumento — propriedades: numero, dataEmissao
- USM Periodo — propriedades: dataInicio, dataFim
- USM ContaBancaria — propriedades: iban, nomeConta, bic
- USM CartaoPagamento — propriedades: numeroConta, titular
- USM DebitoDireto — propriedades: referenciaMandato, identificadorCredor, contaDebitada
- USM DescontoEncargo — propriedades: montante, montanteBase, percentagem, motivo, codigoMotivo
- USM CategoriaIva — propriedades: codigoCategoria, taxa, motivoIsencao, codigoMotivoIsencao
- USM Preco — propriedades: precoLiquido, descontoPreco, precoBruto, quantidadeBase, unidadeQuantidadeBase
- USM Artigo — propriedades: nome, descricao, codigo, codigoComprador, codigoBarras, classificacao, paisOrigem
- USM AtributoArtigo — propriedades: nome, valor
- USM Entidade — propriedades: nif, nome
- USM DocumentoIdentificacao — propriedades: numero, dataValidade
- USM Veiculo — propriedades: matricula, marca, modelo
- USM NumeracaoDocumento — propriedades: tipoDocumento, ultimoNumero, dataUltimo, prefixoAtcud
- USM ParametroConfiguracao — propriedades: nome, valor
- regras RIR: RIR-PAGAMENTO-PRAZO, RIR-REFANT-ND, RIR-REFANT-NC, RIR-TOT-DESCONTOS, RIR-TOT-ENCARGOS, RIR-PAG-IBAN, RIR-DECOMP-ISENTO, RIR-DECOMP-ISENCAO, RIR-DECOMP-SEM-ISENCAO, RIR-SUP-MIME, RIR-SUP-FICHEIRO, RIR-LIN-ISENCAO, RIR-LIN-SEM-ISENCAO, RIR-CP-PT, RIR-CP-ES, RIR-CP-GB, RIR-CP-LX-AJUDA, RIR-CP-LX-ALCANTARA, RIR-CP-LX-ALVALADE, RIR-CP-LX-AREEIRO, RIR-CP-LX-ARROIOS, RIR-CP-LX-AVENIDAS-NOVAS, RIR-CP-LX-BEATO, RIR-CP-LX-BELEM, RIR-CP-LX-BENFICA, RIR-CP-LX-CAMPO-DE-OURIQUE, RIR-CP-LX-CAMPOLIDE, RIR-CP-LX-CARNIDE, RIR-CP-LX-ESTRELA, RIR-CP-LX-LUMIAR, RIR-CP-LX-MARVILA, RIR-CP-LX-MISERICORDIA, RIR-CP-LX-OLIVAIS, RIR-CP-LX-PARQUE-DAS-NACOES, RIR-CP-LX-PENHA-DE-FRANCA, RIR-CP-LX-SANTA-CLARA, RIR-CP-LX-SANTA-MARIA-MAIOR, RIR-CP-LX-SANTO-ANTONIO, RIR-CP-LX-SAO-DOMINGOS-DE-BENFICA, RIR-CP-LX-SAO-VICENTE, RIR-IVA-TAXA-ISENTA, RIR-IVA-TAXA-POSITIVA
- regras RP: RP-SOMA-LINHAS, RP-SOMA-DESCONTOS, RP-SOMA-ENCARGOS, RP-SOMA-IVA, RP-IVA-BASE, RP-IVA-DECOMP, RP-LIN-UNICAS, RP-LENT-MORADA, RP-DOC-DATAIVA, RP-DOC-NUMERO, RP-DOC-TIPO, RP-DOC-MOEDA, RP-DOC-MOEDAIVA, RP-DOC-CODDATAIVA, RP-DOC-REFCLIENTE, RP-DOC-COMPROMISSO, RP-DOC-CONDPAG, RP-DOC-PROCESSO, RP-DOC-ESPEC, RP-REF-PROJETO, RP-REF-CONTRATO, RP-REF-ENCOMENDA, RP-REF-ORDEMVENDA, RP-REF-RECECAO, RP-REF-ENVIO, RP-REF-ACORDO, RP-REF-PROCESSO, RP-NOTA-TEXTO, RP-FORN-REGFISCAL, RP-FORN-CAPITAL, RP-FORN-ENDELET, RP-FORN-CONTACTO, RP-ADQ-ENDELET, RP-ADQ-CONTACTO, RP-LENT-IDENT, RP-LENT-NOME, RP-LENT-IDLOCAL, RP-PAG-MEIO, RP-PAG-DETALHE, RP-PAG-REF, RP-TOT-COMIVA, RP-TOT-SEMIVA, RP-TOT-PAGAR, RP-TOT-DESC-POS, RP-TOT-ENC-POS, RP-TOT-SEMIVA-POS, RP-TOT-COMIVA-POS, RP-TOT-PAGO-POS, RP-TOT-PAGAR-POS, RP-DECOMP-IMPOSTO, RP-SUP-CONTEUDO, RP-SUP-REF, RP-SUP-DESC, RP-SUP-URI, RP-SUP-ANEXO, RP-SUP-MIME, RP-SUP-FICHEIRO, RP-LIN-MONTANTE, RP-LIN-ID, RP-LIN-NOTA, RP-LIN-OBJETO, RP-LIN-UNIDADE, RP-LIN-REFENC, RP-LIN-COMPROMISSO, RP-SP-NOME, RP-SP-NOMECOM, RP-SP-IDENT, RP-SP-REGISTO, RP-SP-IVA, RP-CP, RP-FREGUESIA, RP-PAIS, RP-CMOR-LINHA2, RP-CMOR-LINHA3, RP-CMOR-REGIAO, RP-EMAIL, RP-TELEFONE, RP-REFDOC-NUMERO, RP-PERIODO-ORDEM, RP-PERIODO-DATA, RP-CONTA-IBAN, RP-CONTA-NOME, RP-CONTA-BIC, RP-CARTAO-PAN, RP-CARTAO-TITULAR, RP-DD-MANDATO, RP-DD-CONTA, RP-DE-JUSTIFICADO, RP-DE-CALCULO, RP-DE-MONTANTE, RP-DE-BASE, RP-DE-PERC, RP-DE-MOTIVO, RP-DE-CODMOTIVO, RP-IVA-CATEGORIA, RP-IVA-TAXA, RP-IVA-MOTIVO, RP-IVA-CODMOTIVO, RP-PRECO-CALCULO, RP-PRECO-LIQ, RP-PRECO-DESC, RP-PRECO-BRUTO, RP-PRECO-QBASE, RP-PRECO-UNIDADE, RP-ART-NOME, RP-ART-DESC, RP-ART-CODIGO, RP-ART-CODCOMP, RP-ART-CODBARRAS, RP-ART-CLASSIF, RP-ART-PAIS, RP-ATRIB-NOME, RP-ATRIB-VALOR, RP-CLI-NOME, RP-CLI-NIF, RP-CLI-RUA, RP-CLI-LOCALIDADE, RP-CLI-CP, RP-CLI-EMAIL, RP-CLI-TELEFONE, RP-CLI-TELEMOVEL, RP-CLI-CC, RP-CLI-NOME2, RP-CLI-NIF2, RP-CLI-RUA2, RP-CLI-LOCALIDADE2, RP-CLI-CP2, RP-CLI-TELEFONE2, RP-CLI-CC2, RP-CLI-ZONA, RP-CLI-COBRANCA, RP-ENTFM-ESTADO, RP-NIF, RP-NIF-DC, RP-VEND-NOME, RP-VEND-NIF, RP-VEND-RUA, RP-VEND-LOCALIDADE, RP-VEND-CP, RP-VEND-TELEFONE, RP-VEND-TELEMOVEL, RP-VEND-SERIE, RP-VEND-DIGITOS, RP-VEND-ATCUD, RP-VEND-FAMEXTRA, RP-VEND-NIFEMISSOR, RP-STK-CODIGO, RP-STK-EAN, RP-STK-DESCRICAO, RP-STK-AUXILIAR, RP-STK-REFERENCIA, RP-STK-UNIDADE, RP-STK-FAMILIA, RP-STK-DESCFAMILIA, RP-STK-FORNECEDOR, RP-PRV-MATRICULA, RP-PRV-ARTIGO, RP-AUX-TEXTO, RP-VEIC-MATRICULA, RP-VEIC-MARCA, RP-VEIC-MODELO, RP-NUM-TIPO, RP-NUM-ATCUD, RP-MSG-HORA, RP-RESP-TIPODOC
- projeções: FaturaCiusPt, NotaCreditoCiusPt, EntregaFm, ExportacaoDiariaFm, MensagemEstadoCiusPt
- perfis: EmissaoFaturaCiusPt, EmissaoFaturaIsenta, EmissaoNotaDebito, EmissaoFaturaAdiantamento, EmissaoAutofaturacao, EmissaoNotaCredito, EntregaPortugal, ExportacaoDiariaVendedor, RespostaAdquirente
- funções: algumPresente, nenhumPresente, existe, colecaoNaoVazia, mutuamenteExclusivos, naoAnteriorA, somaIgualATolerancia, somaParcelasIgualA, saldoIgualA, produtoPercentualIgualA, montanteLinhaCoerente, baseTributavelCoerente, categoriasIvaDecompostas, valoresTextoUnicos, localEntregaIdentificado, digitoControloValido

## Operações desta camada

- `definir_projecao` (projecao): Cria ou substitui uma projeção (na declaração do seu HLM).
- `remover_projecao` (nome): Remove a projeção.
- `mapear` (fonte, origem, decisao, destino?, motivo?): Regista ou corrige uma entrada do mapeamento.

### Forma dos campos (exemplos)

```json
{"op": "definir_projecao", "projecao": {"nome": "<NomeDaProjecao>", "hlm": "<HLM>", "descricao": "<utilização>", "obrigatorias": [], "permitidas": []}}
```
```json
{"op": "remover_projecao", "nome": null}
```
```json
{"op": "mapear", "fonte": "<fonte>", "origem": "<id no inventário>", "decisao": "mapeado", "destino": "HLM:<Hlm>/<caminho>"}
```

Regras que o código verifica: nomes em português sem acentos (modelos PascalCase, propriedades e funções camelCase, regras TIPO-ASSUNTO[-QUALIFICADOR]); uma RP vive na propriedade e só a lê; uma RIR tem condição (termos com E) e uma restrição com um só alvo, e a condição não lê o alvo; caminhos relativos ao nó onde a regra vive; a mensagem de não conformidade está na restrição; a descrição das regras é derivada pelo código (não a escrevas). Operadores: EQUALS, NOT_EQUALS, IN, RANGE, LT, LTE, GT, GTE, PATTERN, CONTAINS, STARTS_WITH, ENDS_WITH, LENGTH, FUNCTION, EXT_FUNCTION.

## Formato da resposta

```json
{"operacoes": [{"op": "…", "…": "…"}], "notas": ["…"]}
```

Responde só com o JSON, sem texto à volta.
