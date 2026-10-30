# Criar uma instância de teste

Escreva uma instância JSON de um modelo de dados para testar a validação. A instância segue a estrutura abaixo (as chaves são os nomes das propriedades e os papéis das composições; uma composição repetível é uma lista). Use só as propriedades listadas e respeite os valores fixados.

## Cenário

perfil EmissaoAutofaturacao (projeção FaturaCiusPt) do HLM DocumentoFaturacao

## O que se pretende

Deve estar de acordo com algumas regras e falhar noutras para testar a validacao

## Estrutura (caminho: tipo, estado na projeção)

- CabecalhoDocumento (SM CabecalhoDocumento, cardinalidade 1..1)
- CabecalhoDocumento.numero: texto, obrigatório — Número de referência do documento, atribuído pelo fornecedor
- CabecalhoDocumento.dataEmissao: data, obrigatório — Data de emissão do documento
- CabecalhoDocumento.tipoDocumento: texto, fixado no perfil = "389" — Código do tipo funcional do documento (UNCL 1001 ou código AT)
- CabecalhoDocumento.moeda: texto, fixado no perfil = "EUR" — Moeda em que estão os montantes do documento (ISO 4217 alfa-3)
- CabecalhoDocumento.moedaIva: texto, permitido — Moeda usada para a contabilidade e as declarações de IVA no país do vendedor
- CabecalhoDocumento.dataIva: data, permitido — Data em que o IVA se torna exigível, quando difere da data de emissão
- CabecalhoDocumento.codigoDataIva: texto, permitido — Código da data em que o IVA se torna exigível
- CabecalhoDocumento.dataVencimento: data, permitido — Data de vencimento do pagamento
- CabecalhoDocumento.referenciaCliente: texto, permitido — Referência atribuída pelo cliente
- CabecalhoDocumento.numeroCompromisso: texto, permitido — Número do compromisso orçamental do adquirente público
- CabecalhoDocumento.condicoesPagamento: texto, permitido — Descrição das condições de pagamento
- CabecalhoDocumento.tipoProcesso: texto, permitido — Tipo de processo de negócio em que o documento se insere
- CabecalhoDocumento.identificadorEspecificacao: texto, obrigatório — Identificador da customização CIUS-PT seguida, que permite ao recetor validar o documento
- ReferenciasDocumento (SM ReferenciasDocumento, cardinalidade 0..1)
- ReferenciasDocumento.projeto: texto, permitido — Número do projeto
- ReferenciasDocumento.contrato: texto, permitido — Número do contrato
- ReferenciasDocumento.encomenda: texto, permitido — Número da nota de encomenda do adquirente
- ReferenciasDocumento.ordemVenda: texto, permitido — Número da ordem de venda emitida pelo fornecedor
- ReferenciasDocumento.avisoRececao: texto, permitido — Número do aviso de receção
- ReferenciasDocumento.avisoEnvio: texto, permitido — Referência do aviso de expedição
- ReferenciasDocumento.acordoQuadro: texto, permitido — Número do acordo-quadro ou do lote do concurso
- ReferenciasDocumento.processoRegisto: texto, permitido — Identificador do processo de registo de entrada do documento no adquirente
- NotaDocumento (SM NotaDocumento, cardinalidade 0..*)
- NotaDocumento.assunto: texto, permitido — Assunto da nota
- NotaDocumento.texto: texto, obrigatório — Texto da nota, com informação não estruturada sobre o documento
- DocumentosAnteriores (SM DocumentosAnteriores, cardinalidade 0..1)
- DocumentosAnteriores.ReferenciaDocumento (USM ReferenciaDocumento, cardinalidade 0..*)
- DocumentosAnteriores.ReferenciaDocumento.numero: texto, obrigatório — Número de referência do documento referido
- DocumentosAnteriores.ReferenciaDocumento.dataEmissao: data, permitido — Data de emissão do documento referido
- Fornecedor (SM Fornecedor, cardinalidade 1..1)
- Fornecedor.registoFiscal: texto, permitido — Identificação do local do fornecedor para fins fiscais ou referência ao seu estatuto fiscal
- Fornecedor.capitalSocial: texto, permitido — Informação sobre o capital social e a forma jurídica do fornecedor
- Fornecedor.enderecoEletronico: texto, permitido — Endereço eletrónico de receção de documentos do fornecedor
- Fornecedor.pontoContacto: texto, permitido — Pessoa ou serviço de contacto do fornecedor
- Fornecedor.SujeitoPassivo (USM SujeitoPassivo, cardinalidade 1..1)
- Fornecedor.SujeitoPassivo.nome: texto, obrigatório — Nome formal completo ou denominação social registada
- Fornecedor.SujeitoPassivo.nomeComercial: texto, permitido — Nome comercial pelo qual a parte é conhecida
- Fornecedor.SujeitoPassivo.identificador: texto, permitido — Identificador da parte segundo um esquema de identificação (ex.: GLN, identificação bancária)
- Fornecedor.SujeitoPassivo.identificadorRegisto: texto, permitido — Identificador do registo comercial (conservatória) da parte
- Fornecedor.SujeitoPassivo.identificadorIva: texto, obrigatório — Número de identificação fiscal para efeitos de IVA, precedido do código ISO 3166-1 alfa-2 do país
- Fornecedor.Morada (USM Morada, cardinalidade 1..1)
- Fornecedor.Morada.rua: texto, obrigatório — Arruamento e número de porta
- Fornecedor.Morada.codigoPostal: texto, obrigatório — Código postal da morada
- Fornecedor.Morada.localidade: texto, obrigatório — Localidade da morada (em maiúsculas, sem acentos)
- Fornecedor.Morada.freguesia: texto, permitido — Freguesia da morada (só para moradas em Lisboa)
- Fornecedor.Morada.pais: texto, fixado no perfil = "PT" — País da morada (código ISO de duas letras)
- Fornecedor.ComplementoMorada (USM ComplementoMorada, cardinalidade 0..1)
- Fornecedor.ComplementoMorada.linha2: texto, permitido — Segunda linha da morada
- Fornecedor.ComplementoMorada.linha3: texto, permitido — Linha de endereço adicional, que complementa a linha principal
- Fornecedor.ComplementoMorada.regiao: texto, permitido — Região ou província da morada
- Fornecedor.ContactoTelefonico (USM ContactoTelefonico, cardinalidade 0..1)
- Fornecedor.ContactoTelefonico.telefone: texto, permitido — Número de telefone (rede fixa ou geral)
- Fornecedor.Contacto (USM Contacto, cardinalidade 0..1)
- Fornecedor.Contacto.email: texto, permitido — Endereço de correio eletrónico
- Adquirente (SM Adquirente, cardinalidade 1..1)
- Adquirente.enderecoEletronico: texto, permitido — Endereço eletrónico de receção de documentos do adquirente
- Adquirente.pontoContacto: texto, permitido — Pessoa ou serviço de contacto do adquirente
- Adquirente.SujeitoPassivo (USM SujeitoPassivo, cardinalidade 1..1)
- Adquirente.SujeitoPassivo.nome: texto, obrigatório — Nome formal completo ou denominação social registada
- Adquirente.SujeitoPassivo.nomeComercial: texto, permitido — Nome comercial pelo qual a parte é conhecida
- Adquirente.SujeitoPassivo.identificador: texto, permitido — Identificador da parte segundo um esquema de identificação (ex.: GLN, identificação bancária)
- Adquirente.SujeitoPassivo.identificadorRegisto: texto, permitido — Identificador do registo comercial (conservatória) da parte
- Adquirente.SujeitoPassivo.identificadorIva: texto, obrigatório — Número de identificação fiscal para efeitos de IVA, precedido do código ISO 3166-1 alfa-2 do país
- Adquirente.Morada (USM Morada, cardinalidade 1..1)
- Adquirente.Morada.rua: texto, permitido — Arruamento e número de porta
- Adquirente.Morada.codigoPostal: texto, permitido — Código postal da morada
- Adquirente.Morada.localidade: texto, permitido — Localidade da morada (em maiúsculas, sem acentos)
- Adquirente.Morada.freguesia: texto, permitido — Freguesia da morada (só para moradas em Lisboa)
- Adquirente.Morada.pais: texto, obrigatório — País da morada (código ISO de duas letras)
- Adquirente.ComplementoMorada (USM ComplementoMorada, cardinalidade 0..1)
- Adquirente.ComplementoMorada.linha2: texto, permitido — Segunda linha da morada
- Adquirente.ComplementoMorada.linha3: texto, permitido — Linha de endereço adicional, que complementa a linha principal
- Adquirente.ComplementoMorada.regiao: texto, permitido — Região ou província da morada
- Adquirente.ContactoTelefonico (USM ContactoTelefonico, cardinalidade 0..1)
- Adquirente.ContactoTelefonico.telefone: texto, permitido — Número de telefone (rede fixa ou geral)
- Adquirente.Contacto (USM Contacto, cardinalidade 0..1)
- Adquirente.Contacto.email: texto, permitido — Endereço de correio eletrónico
- RecebedorPagamento (SM RecebedorPagamento, cardinalidade 0..1)
- RecebedorPagamento.SujeitoPassivo (USM SujeitoPassivo, cardinalidade 1..1)
- RecebedorPagamento.SujeitoPassivo.nome: texto, obrigatório — Nome formal completo ou denominação social registada
- RecebedorPagamento.SujeitoPassivo.identificador: texto, permitido — Identificador da parte segundo um esquema de identificação (ex.: GLN, identificação bancária)
- RecebedorPagamento.SujeitoPassivo.identificadorRegisto: texto, permitido — Identificador do registo comercial (conservatória) da parte
- RepresentanteFiscal (SM RepresentanteFiscal, cardinalidade 0..1)
- RepresentanteFiscal.SujeitoPassivo (USM SujeitoPassivo, cardinalidade 1..1)
- RepresentanteFiscal.SujeitoPassivo.nome: texto, obrigatório — Nome formal completo ou denominação social registada
- RepresentanteFiscal.SujeitoPassivo.identificadorIva: texto, obrigatório — Número de identificação fiscal para efeitos de IVA, precedido do código ISO 3166-1 alfa-2 do país
- RepresentanteFiscal.Morada (USM Morada, cardinalidade 1..1)
- RepresentanteFiscal.Morada.rua: texto, permitido — Arruamento e número de porta
- RepresentanteFiscal.Morada.codigoPostal: texto, permitido — Código postal da morada
- RepresentanteFiscal.Morada.localidade: texto, permitido — Localidade da morada (em maiúsculas, sem acentos)
- RepresentanteFiscal.Morada.freguesia: texto, permitido — Freguesia da morada (só para moradas em Lisboa)
- RepresentanteFiscal.Morada.pais: texto, obrigatório — País da morada (código ISO de duas letras)
- RepresentanteFiscal.ComplementoMorada (USM ComplementoMorada, cardinalidade 0..1)
- RepresentanteFiscal.ComplementoMorada.linha2: texto, permitido — Segunda linha da morada
- RepresentanteFiscal.ComplementoMorada.linha3: texto, permitido — Linha de endereço adicional, que complementa a linha principal
- RepresentanteFiscal.ComplementoMorada.regiao: texto, permitido — Região ou província da morada
- LocalEntrega (SM LocalEntrega, cardinalidade 0..*)
- LocalEntrega.nomeLocal: texto, permitido — Nome da parte ou do local de entrega
- LocalEntrega.identificadorLocal: texto, permitido — Identificador do local onde os bens ou serviços são entregues
- LocalEntrega.dataEntrega: data, permitido — Data efetiva da entrega
- LocalEntrega.Morada (USM Morada, cardinalidade 0..1)
- LocalEntrega.Morada.rua: texto, obrigatório — Arruamento e número de porta
- LocalEntrega.Morada.codigoPostal: texto, obrigatório — Código postal da morada
- LocalEntrega.Morada.localidade: texto, obrigatório — Localidade da morada (em maiúsculas, sem acentos)
- LocalEntrega.Morada.freguesia: texto, permitido — Freguesia da morada (só para moradas em Lisboa)
- LocalEntrega.Morada.pais: texto, obrigatório — País da morada (código ISO de duas letras)
- LocalEntrega.ComplementoMorada (USM ComplementoMorada, cardinalidade 0..1)
- LocalEntrega.ComplementoMorada.linha2: texto, permitido — Segunda linha da morada
- LocalEntrega.ComplementoMorada.linha3: texto, permitido — Linha de endereço adicional, que complementa a linha principal
- LocalEntrega.ComplementoMorada.regiao: texto, permitido — Região ou província da morada
- PeriodoFaturacao (SM PeriodoFaturacao, cardinalidade 0..1)
- PeriodoFaturacao.Periodo (USM Periodo, cardinalidade 1..1)
- PeriodoFaturacao.Periodo.dataInicio: data, permitido — Data em que o período começa
- PeriodoFaturacao.Periodo.dataFim: data, permitido — Data em que o período acaba
- Pagamento (SM Pagamento, cardinalidade 0..1)
- Pagamento.meioPagamento: texto, obrigatório — Código do meio de pagamento (UNCL 4461 ou código nacional)
- Pagamento.detalhePagamento: texto, permitido — Descrição do pagamento (ex.: pagamento por ATM)
- Pagamento.referenciaPagamento: texto, permitido — Referência de pagamento por ATM ou DUC
- Pagamento.ContaBancaria (USM ContaBancaria, cardinalidade 0..*)
- Pagamento.ContaBancaria.iban: texto, obrigatório — Identificador da conta (código IBAN)
- Pagamento.ContaBancaria.nomeConta: texto, permitido — Nome da conta para a qual o pagamento deve ser feito
- Pagamento.ContaBancaria.bic: texto, permitido — Código da instituição bancária (BIC/SWIFT)
- Pagamento.CartaoPagamento (USM CartaoPagamento, cardinalidade 0..1)
- Pagamento.CartaoPagamento.numeroConta: texto, obrigatório — Número principal da conta do cartão (PAN)
- Pagamento.CartaoPagamento.titular: texto, permitido — Nome do titular do cartão
- Pagamento.DebitoDireto (USM DebitoDireto, cardinalidade 0..1)
- Pagamento.DebitoDireto.referenciaMandato: texto, permitido — Identificador único do mandato de débito direto atribuído pelo beneficiário
- Pagamento.DebitoDireto.identificadorCredor: texto, permitido — Identificador do credor atribuído pelo banco
- Pagamento.DebitoDireto.contaDebitada: texto, permitido — Conta a debitar pelo débito direto
- Desconto (SM DescontoEncargoDocumento, cardinalidade 0..*)
- Desconto.DescontoEncargo (USM DescontoEncargo, cardinalidade 1..1)
- Desconto.DescontoEncargo.montante: decimal, obrigatório — Montante do desconto ou do encargo, sem impostos
- Desconto.DescontoEncargo.montanteBase: decimal, permitido — Montante base sobre o qual incide a percentagem
- Desconto.DescontoEncargo.percentagem: decimal, permitido — Percentagem aplicada ao montante base
- Desconto.DescontoEncargo.motivo: texto, permitido — Descrição em texto do motivo do desconto ou do encargo
- Desconto.DescontoEncargo.codigoMotivo: texto, permitido — Código do motivo (UNCL 5189 para descontos, UNCL 7161 para encargos)
- Desconto.CategoriaIva (USM CategoriaIva, cardinalidade 1..1)
- Desconto.CategoriaIva.codigoCategoria: texto, obrigatório — Código da categoria de IVA (UN/ECE 5305 com os códigos portugueses NOR, INT, RED, ISE, OUT)
- Desconto.CategoriaIva.taxa: decimal, obrigatório — Taxa de IVA, em percentagem
- Encargo (SM DescontoEncargoDocumento, cardinalidade 0..*)
- Encargo.DescontoEncargo (USM DescontoEncargo, cardinalidade 1..1)
- Encargo.DescontoEncargo.montante: decimal, obrigatório — Montante do desconto ou do encargo, sem impostos
- Encargo.DescontoEncargo.montanteBase: decimal, permitido — Montante base sobre o qual incide a percentagem
- Encargo.DescontoEncargo.percentagem: decimal, permitido — Percentagem aplicada ao montante base
- Encargo.DescontoEncargo.motivo: texto, permitido — Descrição em texto do motivo do desconto ou do encargo
- Encargo.DescontoEncargo.codigoMotivo: texto, permitido — Código do motivo (UNCL 5189 para descontos, UNCL 7161 para encargos)
- Encargo.CategoriaIva (USM CategoriaIva, cardinalidade 1..1)
- Encargo.CategoriaIva.codigoCategoria: texto, obrigatório — Código da categoria de IVA (UN/ECE 5305 com os códigos portugueses NOR, INT, RED, ISE, OUT)
- Encargo.CategoriaIva.taxa: decimal, obrigatório — Taxa de IVA, em percentagem
- Totais (SM Totais, cardinalidade 1..1)
- Totais.somaLinhas: decimal, obrigatório — Soma dos montantes líquidos das linhas, sem imposto
- Totais.totalDescontos: decimal, permitido — Soma dos descontos ao nível do documento
- Totais.totalEncargos: decimal, permitido — Soma dos encargos ao nível do documento
- Totais.totalSemIva: decimal, obrigatório — Total do documento sem IVA
- Totais.totalIva: decimal, obrigatório — Total do IVA do documento
- Totais.totalIvaMoedaContabilistica: decimal, permitido — Total do IVA na moeda aceite ou exigida no país do fornecedor
- Totais.totalComIva: decimal, obrigatório — Total do documento com IVA
- Totais.valorPago: decimal, permitido — Soma dos montantes já pagos, a deduzir do valor a pagar
- Totais.arredondamento: decimal, permitido — Montante de arredondamento aplicado ao total com IVA
- Totais.valorPagar: decimal, obrigatório — Valor a pagar
- DecomposicaoIva (SM DecomposicaoIva, cardinalidade 1..*)
- DecomposicaoIva.baseTributavel: decimal, obrigatório — Base de incidência da taxa de IVA neste subtotal
- DecomposicaoIva.montanteImposto: decimal, obrigatório — Imposto calculado sobre a base de incidência
- DecomposicaoIva.CategoriaIva (USM CategoriaIva, cardinalidade 1..1)
- DecomposicaoIva.CategoriaIva.codigoCategoria: texto, obrigatório — Código da categoria de IVA (UN/ECE 5305 com os códigos portugueses NOR, INT, RED, ISE, OUT)
- DecomposicaoIva.CategoriaIva.taxa: decimal, obrigatório — Taxa de IVA, em percentagem
- DecomposicaoIva.CategoriaIva.motivoIsencao: texto, permitido — Descrição em texto do motivo de isenção de IVA
- DecomposicaoIva.CategoriaIva.codigoMotivoIsencao: texto, permitido — Código do motivo de isenção de IVA
- DocumentoSuporte (SM DocumentoSuporte, cardinalidade 0..*)
- DocumentoSuporte.referencia: texto, obrigatório — Identificador do documento de suporte
- DocumentoSuporte.descricao: texto, permitido — Descrição do documento de suporte
- DocumentoSuporte.localizacaoExterna: texto, permitido — Endereço (URI) de um documento guardado externamente
- DocumentoSuporte.anexo: texto, permitido — Conteúdo do documento anexado, codificado em base 64
- DocumentoSuporte.tipoMime: texto, permitido — Tipo MIME do documento anexado
- DocumentoSuporte.nomeFicheiro: texto, permitido — Nome do ficheiro anexado
- LinhaDocumento (SM LinhaDocumento, cardinalidade 1..*)
- LinhaDocumento.identificador: texto, obrigatório — Identificador único da linha no documento, atribuído pelo fornecedor
- LinhaDocumento.nota: texto, permitido — Observação em texto livre sobre a linha
- LinhaDocumento.identificadorObjeto: texto, permitido — Identificador do objeto em que a linha se baseia, dado pelo fornecedor
- LinhaDocumento.quantidade: decimal, obrigatório — Quantidade faturada do bem ou serviço
- LinhaDocumento.unidadeMedida: texto, obrigatório — Unidade de medida da quantidade faturada (UN/ECE Rec. 20 e 21)
- LinhaDocumento.montanteLiquido: decimal, obrigatório — Montante da linha sem IVA, já com os descontos e encargos da linha
- LinhaDocumento.referenciaLinhaEncomenda: texto, permitido — Referência da linha da nota de encomenda do cliente
- LinhaDocumento.numeroCompromisso: texto, permitido — Número do compromisso associado à linha
- LinhaDocumento.Artigo (USM Artigo, cardinalidade 1..1)
- LinhaDocumento.Artigo.nome: texto, obrigatório — Designação do bem ou serviço
- LinhaDocumento.Artigo.descricao: texto, permitido — Descrição detalhada do bem ou serviço
- LinhaDocumento.Artigo.codigo: texto, permitido — Código do artigo atribuído pelo vendedor
- LinhaDocumento.Artigo.codigoComprador: texto, permitido — Código do artigo atribuído pelo comprador
- LinhaDocumento.Artigo.codigoBarras: texto, permitido — Identificador normalizado do artigo (EAN/GTIN)
- LinhaDocumento.Artigo.classificacao: texto, permitido — Código de classificação da mercadoria (ex.: CPV)
- LinhaDocumento.Artigo.paisOrigem: texto, permitido — País de origem do artigo (código ISO 3166-1 alfa-2)
- LinhaDocumento.Preco (USM Preco, cardinalidade 1..1)
- LinhaDocumento.Preco.precoLiquido: decimal, obrigatório — Preço do item depois do desconto, por quantidade base
- LinhaDocumento.Preco.descontoPreco: decimal, permitido — Desconto sobre o preço do item
- LinhaDocumento.Preco.precoBruto: decimal, permitido — Preço do item antes do desconto
- LinhaDocumento.Preco.quantidadeBase: decimal, permitido — Número de unidades a que o preço se refere (ex.: 15 € por 10 litros)
- LinhaDocumento.Preco.unidadeQuantidadeBase: texto, permitido — Unidade de medida da quantidade base (UN/ECE Rec. 20 e 21)
- LinhaDocumento.CategoriaIva (USM CategoriaIva, cardinalidade 1..1)
- LinhaDocumento.CategoriaIva.codigoCategoria: texto, obrigatório — Código da categoria de IVA (UN/ECE 5305 com os códigos portugueses NOR, INT, RED, ISE, OUT)
- LinhaDocumento.CategoriaIva.taxa: decimal, obrigatório — Taxa de IVA, em percentagem
- LinhaDocumento.CategoriaIva.motivoIsencao: texto, permitido — Descrição em texto do motivo de isenção de IVA
- LinhaDocumento.CategoriaIva.codigoMotivoIsencao: texto, permitido — Código do motivo de isenção de IVA
- LinhaDocumento.Periodo (USM Periodo, cardinalidade 0..1)
- LinhaDocumento.Periodo.dataInicio: data, permitido — Data em que o período começa
- LinhaDocumento.Periodo.dataFim: data, permitido — Data em que o período acaba
- LinhaDocumento.Desconto (USM DescontoEncargo, cardinalidade 0..*)
- LinhaDocumento.Desconto.montante: decimal, obrigatório — Montante do desconto ou do encargo, sem impostos
- LinhaDocumento.Desconto.montanteBase: decimal, permitido — Montante base sobre o qual incide a percentagem
- LinhaDocumento.Desconto.percentagem: decimal, permitido — Percentagem aplicada ao montante base
- LinhaDocumento.Desconto.motivo: texto, permitido — Descrição em texto do motivo do desconto ou do encargo
- LinhaDocumento.Desconto.codigoMotivo: texto, permitido — Código do motivo (UNCL 5189 para descontos, UNCL 7161 para encargos)
- LinhaDocumento.Encargo (USM DescontoEncargo, cardinalidade 0..*)
- LinhaDocumento.Encargo.montante: decimal, obrigatório — Montante do desconto ou do encargo, sem impostos
- LinhaDocumento.Encargo.montanteBase: decimal, permitido — Montante base sobre o qual incide a percentagem
- LinhaDocumento.Encargo.percentagem: decimal, permitido — Percentagem aplicada ao montante base
- LinhaDocumento.Encargo.motivo: texto, permitido — Descrição em texto do motivo do desconto ou do encargo
- LinhaDocumento.Encargo.codigoMotivo: texto, permitido — Código do motivo (UNCL 5189 para descontos, UNCL 7161 para encargos)
- LinhaDocumento.AtributoArtigo (USM AtributoArtigo, cardinalidade 0..*)
- LinhaDocumento.AtributoArtigo.nome: texto, obrigatório — Nome ou tipo da propriedade adicional
- LinhaDocumento.AtributoArtigo.valor: texto, obrigatório — Valor da propriedade adicional
- Metainformacao (SM Metainformacao, cardinalidade 0..1)
- Metainformacao.origemModelo: texto, permitido — Fonte do modelo de dados (norma, sistema ou repositório)
- Metainformacao.versaoOrigem: texto, permitido — Versão da fonte usada
- Metainformacao.referenciaOrigem: texto, permitido — Identificador da entidade na fonte (ex.: BG-0 Invoice, Device)
- Metainformacao.utilizacao: texto, permitido — Finalidade ou contexto de utilização do modelo
- Metainformacao.dominio: texto, permitido — Domínio a que o modelo pertence
- Metainformacao.observacoes: texto, permitido — Outra metainformação relevante sobre o modelo

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
- RP-REF-PROJETO (RP): ReferenciasDocumento.projeto tem entre 1 e 50 caracteres [em: ReferenciasDocumento]
- RP-REF-CONTRATO (RP): ReferenciasDocumento.contrato tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-ENCOMENDA (RP): ReferenciasDocumento.encomenda tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-ORDEMVENDA (RP): ReferenciasDocumento.ordemVenda tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-RECECAO (RP): ReferenciasDocumento.avisoRececao tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-ENVIO (RP): ReferenciasDocumento.avisoEnvio tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-ACORDO (RP): ReferenciasDocumento.acordoQuadro tem entre 1 e 20 caracteres [em: ReferenciasDocumento]
- RP-REF-PROCESSO (RP): ReferenciasDocumento.processoRegisto tem entre 1 e 50 caracteres [em: ReferenciasDocumento]
- RP-NOTA-TEXTO (RP): NotaDocumento.texto tem entre 1 e 500 caracteres [em: NotaDocumento]
- RP-REFDOC-NUMERO (RP): ReferenciaDocumento.numero tem entre 1 e 50 caracteres [em: DocumentosAnteriores.ReferenciaDocumento]
- RP-FORN-REGFISCAL (RP): Fornecedor.registoFiscal tem entre 1 e 50 caracteres [em: Fornecedor]
- RP-FORN-CAPITAL (RP): Fornecedor.capitalSocial tem entre 1 e 200 caracteres [em: Fornecedor]
- RP-FORN-ENDELET (RP): Fornecedor.enderecoEletronico tem entre 1 e 50 caracteres [em: Fornecedor]
- RP-FORN-CONTACTO (RP): Fornecedor.pontoContacto tem entre 1 e 200 caracteres [em: Fornecedor]
- RP-SP-NOME (RP): SujeitoPassivo.nome tem entre 1 e 200 caracteres [em: Adquirente.SujeitoPassivo, Fornecedor.SujeitoPassivo, RecebedorPagamento.SujeitoPassivo, RepresentanteFiscal.SujeitoPassivo]
- RP-SP-NOMECOM (RP): SujeitoPassivo.nomeComercial tem entre 1 e 200 caracteres [em: Adquirente.SujeitoPassivo, Fornecedor.SujeitoPassivo, RecebedorPagamento.SujeitoPassivo, RepresentanteFiscal.SujeitoPassivo]
- RP-SP-IDENT (RP): SujeitoPassivo.identificador tem entre 1 e 50 caracteres [em: Adquirente.SujeitoPassivo, Fornecedor.SujeitoPassivo, RecebedorPagamento.SujeitoPassivo, RepresentanteFiscal.SujeitoPassivo]
- RP-SP-REGISTO (RP): SujeitoPassivo.identificadorRegisto tem entre 1 e 200 caracteres [em: Adquirente.SujeitoPassivo, Fornecedor.SujeitoPassivo, RecebedorPagamento.SujeitoPassivo, RepresentanteFiscal.SujeitoPassivo]
- RP-SP-IVA (RP): SujeitoPassivo.identificadorIva segue o padrão ^[A-Z]{2}.{1,48}$ [em: Adquirente.SujeitoPassivo, Fornecedor.SujeitoPassivo, RecebedorPagamento.SujeitoPassivo, RepresentanteFiscal.SujeitoPassivo]
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
- RP-CMOR-LINHA2 (RP): ComplementoMorada.linha2 tem entre 1 e 200 caracteres [em: Adquirente.ComplementoMorada, Fornecedor.ComplementoMorada, LocalEntrega.ComplementoMorada, RepresentanteFiscal.ComplementoMorada]
- RP-CMOR-LINHA3 (RP): ComplementoMorada.linha3 tem entre 1 e 200 caracteres [em: Adquirente.ComplementoMorada, Fornecedor.ComplementoMorada, LocalEntrega.ComplementoMorada, RepresentanteFiscal.ComplementoMorada]
- RP-CMOR-REGIAO (RP): ComplementoMorada.regiao tem entre 1 e 200 caracteres [em: Adquirente.ComplementoMorada, Fornecedor.ComplementoMorada, LocalEntrega.ComplementoMorada, RepresentanteFiscal.ComplementoMorada]
- RP-TELEFONE (RP): ContactoTelefonico.telefone tem entre 1 e 200 caracteres [em: Adquirente.ContactoTelefonico, Fornecedor.ContactoTelefonico]
- RP-EMAIL (RP): Contacto.email segue o padrão ^[a-z0-9._-]+@[a-z0-9-]+(\.[a-z0-9-]+)+$ [em: Adquirente.Contacto, Fornecedor.Contacto]
- RP-ADQ-ENDELET (RP): Adquirente.enderecoEletronico tem entre 1 e 50 caracteres [em: Adquirente]
- RP-ADQ-CONTACTO (RP): Adquirente.pontoContacto tem entre 1 e 200 caracteres [em: Adquirente]
- RP-LENT-IDENT (RP): localEntregaIdentificado(LocalEntrega.nomeLocal, LocalEntrega.identificadorLocal, LocalEntrega.dataEntrega, LocalEntrega.Morada.rua) [em: LocalEntrega]
- RP-LENT-NOME (RP): LocalEntrega.nomeLocal tem entre 1 e 200 caracteres [em: LocalEntrega]
- RP-LENT-IDLOCAL (RP): LocalEntrega.identificadorLocal tem entre 1 e 50 caracteres [em: LocalEntrega]
- RP-PERIODO-DATA (RP): algumPresente(Periodo.dataInicio, Periodo.dataFim) [em: LinhaDocumento.Periodo, PeriodoFaturacao.Periodo]
- RP-PERIODO-ORDEM (RP): naoAnteriorA(Periodo.dataFim, Periodo.dataInicio) [em: LinhaDocumento.Periodo, PeriodoFaturacao.Periodo]
- RIR-PAG-IBAN (RIR): Se Pagamento.meioPagamento ∈ {30, 58} → colecaoNaoVazia(Pagamento.ContaBancaria.iban) [em: Pagamento]
- RP-PAG-MEIO (RP): Pagamento.meioPagamento ∈ {30, 48, 49, 57, 58, 59, CC, CD, CH, CI, CO, CS, DE, LC, MB, NU, OU, PR, TB, TR} [em: Pagamento]
- RP-PAG-DETALHE (RP): Pagamento.detalhePagamento tem entre 1 e 150 caracteres [em: Pagamento]
- RP-PAG-REF (RP): Pagamento.referenciaPagamento segue o padrão ^#REFERENCE@(ATM|DUC)PAYMENT#.{1,20}#$ [em: Pagamento]
- RP-CONTA-IBAN (RP): ContaBancaria.iban tem entre 1 e 50 caracteres [em: Pagamento.ContaBancaria]
- RP-CONTA-NOME (RP): ContaBancaria.nomeConta tem entre 1 e 200 caracteres [em: Pagamento.ContaBancaria]
- RP-CONTA-BIC (RP): ContaBancaria.bic tem entre 1 e 50 caracteres [em: Pagamento.ContaBancaria]
- RP-CARTAO-PAN (RP): CartaoPagamento.numeroConta tem entre 1 e 200 caracteres [em: Pagamento.CartaoPagamento]
- RP-CARTAO-TITULAR (RP): CartaoPagamento.titular tem entre 1 e 200 caracteres [em: Pagamento.CartaoPagamento]
- RP-DD-MANDATO (RP): DebitoDireto.referenciaMandato tem entre 1 e 50 caracteres [em: Pagamento.DebitoDireto]
- RP-DD-CONTA (RP): DebitoDireto.contaDebitada tem entre 1 e 50 caracteres [em: Pagamento.DebitoDireto]
- RP-DE-CALCULO (RP): produtoPercentualIgualA(DescontoEncargo.montanteBase, DescontoEncargo.percentagem, DescontoEncargo.montante, 1) [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-JUSTIFICADO (RP): algumPresente(DescontoEncargo.motivo, DescontoEncargo.codigoMotivo) [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-MONTANTE (RP): DescontoEncargo.montante ≥ 0 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-BASE (RP): DescontoEncargo.montanteBase ≥ 0 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-PERC (RP): DescontoEncargo.percentagem entre 0 e 100 [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-MOTIVO (RP): DescontoEncargo.motivo tem entre 1 e 200 caracteres [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RP-DE-CODMOTIVO (RP): DescontoEncargo.codigoMotivo segue o padrão ^[A-Z0-9]{1,3}$ [em: Desconto.DescontoEncargo, Encargo.DescontoEncargo, LinhaDocumento.Desconto, LinhaDocumento.Encargo]
- RIR-IVA-TAXA-ISENTA (RIR): Se CategoriaIva.codigoCategoria ∈ {E, ISE} → CategoriaIva.taxa = 0 [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RIR-IVA-TAXA-POSITIVA (RIR): Se CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → CategoriaIva.taxa > 0 [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RP-IVA-CATEGORIA (RP): CategoriaIva.codigoCategoria ∈ {AA, S, E, RED, INT, NOR, ISE, OUT, NA, Z, AE, IC, G, O} [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RP-IVA-TAXA (RP): CategoriaIva.taxa entre 0 e 100 [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RP-IVA-MOTIVO (RP): CategoriaIva.motivoIsencao tem entre 1 e 200 caracteres [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RP-IVA-CODMOTIVO (RP): CategoriaIva.codigoMotivoIsencao tem entre 1 e 5 caracteres [em: DecomposicaoIva.CategoriaIva, Desconto.CategoriaIva, Encargo.CategoriaIva, LinhaDocumento.CategoriaIva]
- RP-TOT-COMIVA (RP): somaParcelasIgualA(Totais.totalSemIva, Totais.totalIva, Totais.totalComIva, 1) [em: Totais]
- RP-TOT-PAGAR (RP): saldoIgualA(Totais.totalComIva, Totais.valorPago, Totais.arredondamento, Totais.valorPagar, 1) [em: Totais]
- RP-TOT-SEMIVA (RP): saldoIgualA(Totais.somaLinhas, Totais.totalDescontos, Totais.totalEncargos, Totais.totalSemIva, 1) [em: Totais]
- RP-TOT-DESC-POS (RP): Totais.totalDescontos ≥ 0 [em: Totais]
- RP-TOT-ENC-POS (RP): Totais.totalEncargos ≥ 0 [em: Totais]
- RP-TOT-SEMIVA-POS (RP): Totais.totalSemIva ≥ 0 [em: Totais]
- RP-TOT-COMIVA-POS (RP): Totais.totalComIva ≥ 0 [em: Totais]
- RP-TOT-PAGO-POS (RP): Totais.valorPago ≥ 0 [em: Totais]
- RP-TOT-PAGAR-POS (RP): Totais.valorPagar ≥ 0 [em: Totais]
- RP-DECOMP-IMPOSTO (RP): produtoPercentualIgualA(DecomposicaoIva.baseTributavel, DecomposicaoIva.CategoriaIva.taxa, DecomposicaoIva.montanteImposto, 1) [em: DecomposicaoIva]
- RIR-DECOMP-ISENCAO (RIR): Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {E, ISE} → algumPresente(DecomposicaoIva.CategoriaIva.motivoIsencao, DecomposicaoIva.CategoriaIva.codigoMotivoIsencao) [em: DecomposicaoIva]
- RIR-DECOMP-ISENTO (RIR): Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {E, ISE} → DecomposicaoIva.montanteImposto = 0 [em: DecomposicaoIva]
- RIR-DECOMP-SEM-ISENCAO (RIR): Se DecomposicaoIva.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(DecomposicaoIva.CategoriaIva.motivoIsencao, DecomposicaoIva.CategoriaIva.codigoMotivoIsencao) [em: DecomposicaoIva]
- RP-SUP-CONTEUDO (RP): algumPresente(DocumentoSuporte.localizacaoExterna, DocumentoSuporte.anexo) [em: DocumentoSuporte]
- RIR-SUP-FICHEIRO (RIR): Se existe(DocumentoSuporte.anexo) → existe(DocumentoSuporte.nomeFicheiro) [em: DocumentoSuporte]
- RIR-SUP-MIME (RIR): Se existe(DocumentoSuporte.anexo) → existe(DocumentoSuporte.tipoMime) [em: DocumentoSuporte]
- RP-SUP-REF (RP): DocumentoSuporte.referencia tem entre 1 e 50 caracteres [em: DocumentoSuporte]
- RP-SUP-DESC (RP): DocumentoSuporte.descricao tem entre 1 e 200 caracteres [em: DocumentoSuporte]
- RP-SUP-URI (RP): DocumentoSuporte.localizacaoExterna tem entre 1 e 200 caracteres [em: DocumentoSuporte]
- RP-SUP-ANEXO (RP): DocumentoSuporte.anexo tem entre 1 e 6826666 caracteres [em: DocumentoSuporte]
- RP-SUP-MIME (RP): DocumentoSuporte.tipoMime ∈ {text/plain, image/png, image/jpeg, application/pdf, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document, application/vnd.ms-excel, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/xml, text/xml, text/csv} [em: DocumentoSuporte]
- RP-SUP-FICHEIRO (RP): DocumentoSuporte.nomeFicheiro tem entre 1 e 50 caracteres [em: DocumentoSuporte]
- RP-LIN-MONTANTE (RP): montanteLinhaCoerente(LinhaDocumento.quantidade, LinhaDocumento.Preco.precoLiquido, LinhaDocumento.Preco.quantidadeBase, LinhaDocumento.Desconto.montante, LinhaDocumento.Encargo.montante, LinhaDocumento.montanteLiquido, 1) [em: LinhaDocumento]
- RIR-LIN-ISENCAO (RIR): Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {E, ISE} → algumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao) [em: LinhaDocumento]
- RIR-LIN-SEM-ISENCAO (RIR): Se LinhaDocumento.CategoriaIva.codigoCategoria ∈ {S, NOR, AA, RED, INT} → nenhumPresente(LinhaDocumento.CategoriaIva.motivoIsencao, LinhaDocumento.CategoriaIva.codigoMotivoIsencao) [em: LinhaDocumento]
- RP-LIN-ID (RP): LinhaDocumento.identificador tem entre 1 e 50 caracteres [em: LinhaDocumento]
- RP-LIN-NOTA (RP): LinhaDocumento.nota tem entre 1 e 500 caracteres [em: LinhaDocumento]
- RP-LIN-OBJETO (RP): LinhaDocumento.identificadorObjeto tem entre 1 e 50 caracteres [em: LinhaDocumento]
- RP-LIN-UNIDADE (RP): LinhaDocumento.unidadeMedida segue o padrão ^[A-Z0-9]{1,3}$ [em: LinhaDocumento]
- RP-LIN-REFENC (RP): LinhaDocumento.referenciaLinhaEncomenda tem entre 1 e 20 caracteres [em: LinhaDocumento]
- RP-LIN-COMPROMISSO (RP): LinhaDocumento.numeroCompromisso tem entre 1 e 200 caracteres [em: LinhaDocumento]
- RP-ART-NOME (RP): Artigo.nome tem entre 1 e 200 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-DESC (RP): Artigo.descricao tem entre 1 e 200 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-CODIGO (RP): Artigo.codigo tem entre 1 e 50 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-CODCOMP (RP): Artigo.codigoComprador tem entre 1 e 50 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-CODBARRAS (RP): Artigo.codigoBarras tem entre 1 e 50 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-CLASSIF (RP): Artigo.classificacao tem entre 1 e 50 caracteres [em: LinhaDocumento.Artigo]
- RP-ART-PAIS (RP): Artigo.paisOrigem segue o padrão ^[A-Z]{2}$ [em: LinhaDocumento.Artigo]
- RP-PRECO-CALCULO (RP): somaParcelasIgualA(Preco.precoLiquido, Preco.descontoPreco, Preco.precoBruto, 1) [em: LinhaDocumento.Preco]
- RP-PRECO-LIQ (RP): Preco.precoLiquido ≥ 0 [em: LinhaDocumento.Preco]
- RP-PRECO-DESC (RP): Preco.descontoPreco ≥ 0 [em: LinhaDocumento.Preco]
- RP-PRECO-BRUTO (RP): Preco.precoBruto ≥ 0 [em: LinhaDocumento.Preco]
- RP-PRECO-QBASE (RP): Preco.quantidadeBase > 0 [em: LinhaDocumento.Preco]
- RP-PRECO-UNIDADE (RP): Preco.unidadeQuantidadeBase segue o padrão ^[A-Z0-9]{1,3}$ [em: LinhaDocumento.Preco]
- RP-ATRIB-NOME (RP): AtributoArtigo.nome tem entre 1 e 200 caracteres [em: LinhaDocumento.AtributoArtigo]
- RP-ATRIB-VALOR (RP): AtributoArtigo.valor tem entre 1 e 200 caracteres [em: LinhaDocumento.AtributoArtigo]

## Contextos externos

(nenhum)

## Esqueleto (a completar)

```json
{
 "descricao": "",
 "perfil": "EmissaoAutofaturacao",
 "contextos": {},
 "instancia": {
  "CabecalhoDocumento": {
   "numero": "",
   "dataEmissao": "AAAA-MM-DD",
   "tipoDocumento": "389",
   "moeda": "EUR",
   "moedaIva": "",
   "dataIva": "AAAA-MM-DD",
   "codigoDataIva": "",
   "dataVencimento": "AAAA-MM-DD",
   "referenciaCliente": "",
   "numeroCompromisso": "",
   "condicoesPagamento": "",
   "tipoProcesso": "",
   "identificadorEspecificacao": ""
  },
  "ReferenciasDocumento": {
   "projeto": "",
   "contrato": "",
   "encomenda": "",
   "ordemVenda": "",
   "avisoRececao": "",
   "avisoEnvio": "",
   "acordoQuadro": "",
   "processoRegisto": ""
  },
  "NotaDocumento": [
   {
    "assunto": "",
    "texto": ""
   }
  ],
  "DocumentosAnteriores": {
   "ReferenciaDocumento": [
    {
     "numero": "",
     "dataEmissao": "AAAA-MM-DD"
    }
   ]
  },
  "Fornecedor": {
   "registoFiscal": "",
   "capitalSocial": "",
   "enderecoEletronico": "",
   "pontoContacto": "",
   "SujeitoPassivo": {
    "nome": "",
    "nomeComercial": "",
    "identificador": "",
    "identificadorRegisto": "",
    "identificadorIva": ""
   },
   "Morada": {
    "rua": "",
    "codigoPostal": "",
    "localidade": "",
    "freguesia": "",
    "pais": "PT"
   },
   "ComplementoMorada": {
    "linha2": "",
    "linha3": "",
    "regiao": ""
   },
   "ContactoTelefonico": {
    "telefone": ""
   },
   "Contacto": {
    "email": ""
   }
  },
  "Adquirente": {
   "enderecoEletronico": "",
   "pontoContacto": "",
   "SujeitoPassivo": {
    "nome": "",
    "nomeComercial": "",
    "identificador": "",
    "identificadorRegisto": "",
    "identificadorIva": ""
   },
   "Morada": {
    "rua": "",
    "codigoPostal": "",
    "localidade": "",
    "freguesia": "",
    "pais": ""
   },
   "ComplementoMorada": {
    "linha2": "",
    "linha3": "",
    "regiao": ""
   },
   "ContactoTelefonico": {
    "telefone": ""
   },
   "Contacto": {
    "email": ""
   }
  },
  "RecebedorPagamento": {
   "SujeitoPassivo": {
    "nome": "",
    "identificador": "",
    "identificadorRegisto": ""
   }
  },
  "RepresentanteFiscal": {
   "SujeitoPassivo": {
    "nome": "",
    "identificadorIva": ""
   },
   "Morada": {
    "rua": "",
    "codigoPostal": "",
    "localidade": "",
    "freguesia": "",
    "pais": ""
   },
   "ComplementoMorada": {
    "linha2": "",
    "linha3": "",
    "regiao": ""
   }
  },
  "LocalEntrega": [
   {
    "nomeLocal": "",
    "identificadorLocal": "",
    "dataEntrega": "AAAA-MM-DD",
    "Morada": {
     "rua": "",
     "codigoPostal": "",
     "localidade": "",
     "freguesia": "",
     "pais": ""
    },
    "ComplementoMorada": {
     "linha2": "",
     "linha3": "",
     "regiao": ""
    }
   }
  ],
  "PeriodoFaturacao": {
   "Periodo": {
    "dataInicio": "AAAA-MM-DD",
    "dataFim": "AAAA-MM-DD"
   }
  },
  "Pagamento": {
   "meioPagamento": "",
   "detalhePagamento": "",
   "referenciaPagamento": "",
   "ContaBancaria": [
    {
     "iban": "",
     "nomeConta": "",
     "bic": ""
    }
   ],
   "CartaoPagamento": {
    "numeroConta": "",
    "titular": ""
   },
   "DebitoDireto": {
    "referenciaMandato": "",
    "identificadorCredor": "",
    "contaDebitada": ""
   }
  },
  "Desconto": [
   {
    "DescontoEncargo": {
     "montante": 0.0,
     "montanteBase": 0.0,
     "percentagem": 0.0,
     "motivo": "",
     "codigoMotivo": ""
    },
    "CategoriaIva": {
     "codigoCategoria": "",
     "taxa": 0.0
    }
   }
  ],
  "Encargo": [
   {
    "DescontoEncargo": {
     "montante": 0.0,
     "montanteBase": 0.0,
     "percentagem": 0.0,
     "motivo": "",
     "codigoMotivo": ""
    },
    "CategoriaIva": {
     "codigoCategoria": "",
     "taxa": 0.0
    }
   }
  ],
  "Totais": {
   "somaLinhas": 0.0,
   "totalDescontos": 0.0,
   "totalEncargos": 0.0,
   "totalSemIva": 0.0,
   "totalIva": 0.0,
   "totalIvaMoedaContabilistica": 0.0,
   "totalComIva": 0.0,
   "valorPago": 0.0,
   "arredondamento": 0.0,
   "valorPagar": 0.0
  },
  "DecomposicaoIva": [
   {
    "baseTributavel": 0.0,
    "montanteImposto": 0.0,
    "CategoriaIva": {
     "codigoCategoria": "",
     "taxa": 0.0,
     "motivoIsencao": "",
     "codigoMotivoIsencao": ""
    }
   }
  ],
  "DocumentoSuporte": [
   {
    "referencia": "",
    "descricao": "",
    "localizacaoExterna": "",
    "anexo": "",
    "tipoMime": "",
    "nomeFicheiro": ""
   }
  ],
  "LinhaDocumento": [
   {
    "identificador": "",
    "nota": "",
    "identificadorObjeto": "",
    "quantidade": 0.0,
    "unidadeMedida": "",
    "montanteLiquido": 0.0,
    "referenciaLinhaEncomenda": "",
    "numeroCompromisso": "",
    "Artigo": {
     "nome": "",
     "descricao": "",
     "codigo": "",
     "codigoComprador": "",
     "codigoBarras": "",
     "classificacao": "",
     "paisOrigem": ""
    },
    "Preco": {
     "precoLiquido": 0.0,
     "descontoPreco": 0.0,
     "precoBruto": 0.0,
     "quantidadeBase": 0.0,
     "unidadeQuantidadeBase": ""
    },
    "CategoriaIva": {
     "codigoCategoria": "",
     "taxa": 0.0,
     "motivoIsencao": "",
     "codigoMotivoIsencao": ""
    },
    "Periodo": {
     "dataInicio": "AAAA-MM-DD",
     "dataFim": "AAAA-MM-DD"
    },
    "Desconto": [
     {
      "montante": 0.0,
      "montanteBase": 0.0,
      "percentagem": 0.0,
      "motivo": "",
      "codigoMotivo": ""
     }
    ],
    "Encargo": [
     {
      "montante": 0.0,
      "montanteBase": 0.0,
      "percentagem": 0.0,
      "motivo": "",
      "codigoMotivo": ""
     }
    ],
    "AtributoArtigo": [
     {
      "nome": "",
      "valor": ""
     }
    ]
   }
  ],
  "Metainformacao": {
   "origemModelo": "",
   "versaoOrigem": "",
   "referenciaOrigem": "",
   "utilizacao": "",
   "dominio": "",
   "observacoes": ""
  }
 }
}
```

## O que responder

Só o JSON, com a forma do esqueleto: `{"descricao": "<o que a instância testa>", "perfil" ou "hlm", "contextos": {...}, "instancia": {...}}`. Se o pedido é uma instância com erros, diga na descrição que regras devem falhar e porquê.
