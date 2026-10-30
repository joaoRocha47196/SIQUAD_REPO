# Dados de teste

Ficheiros para experimentar as operações da aplicação com dados que não vêm das fontes dos domínios. Nenhum contém dados pessoais.

| Ficheiro | Para quê | Onde se usa |
|---|---|---|
| `csv/codigos_postais_lisboa.csv` | Os códigos postais admitidos em cada freguesia de Lisboa (prefixos ilustrativos dos CTT): uma RIR por linha, "se país, localidade e freguesia → o código postal segue o padrão" | Alterações › Tabela CSV: modelo `USM:Morada`, coluna alvo `codigoPostal`, operador `PATTERN` (domínio `faturacao` ou âmbito `exemplos`) |
| `csv/codigo_postal_por_pais.csv` | O formato do código postal de cada país: uma RIR por linha | Alterações › Tabela CSV: `USM:Morada`, alvo `codigoPostal`, `PATTERN`; ou como "informação adicional" de um pedido em linguagem natural (camada D) |
| `csv/taxa_iva_por_categoria.csv` | As taxas de IVA admitidas em cada categoria (lista separada por `\|`) | Alterações › Tabela CSV: modelo `CategoriaIva` (domínio `faturacao`), alvo `taxa`, operador `IN` |
| `linguagem_natural/regras_condicionais.md` | Nove pedidos de regras condicionais em linguagem natural, para os domínios `faturacao` e `iot` | Alterações › D › Pedido em linguagem natural (com o modelo escolhido, o prompt leva só esse contexto) |
| `biblioteca/descricao_biblioteca.md` | A descrição de um domínio só em linguagem natural (obras, exemplares, leitores, empréstimos, reservas), sem esquema de origem | Domínio `dominios/biblioteca`: fonte com o adaptador `texto.markdown`; a extração já foi feita e aceite e o pedido de geração (fase G) está em `dominios/biblioteca/pedidos/` |

## Testar a geração com outro LLM

1. Escolher o domínio `biblioteca` no seletor de âmbito.
2. Pedidos ao LLM › o pedido da fase G: copiar o `prompt.md` para o LLM a testar (o prompt tem a especificação, o inventário extraído do texto e o próprio texto).
3. Colar a resposta e Registar: as verificações da geração mostram a cobertura dos elementos e das regras, e as vistas de cada declaração ficam disponíveis logo a seguir.
4. Comparar as respostas de modelos diferentes pela cobertura, pelo número de regras de cada tipo e pelas funções declaradas.

## Formato da descrição em linguagem natural (adaptador `texto.markdown`)

Nada é obrigatório, mas o adaptador aproveita esta estrutura: `## Nome` abre um grupo (um modelo candidato); cada item `- nome (tipo, obrigatório|opcional|um ou mais): descrição. Valores: A, B, C` é um elemento; cada frase com "deve", "tem de", "só", "não pode", "se", "quando", "no máximo"… é uma regra candidata. O texto completo segue no prompt da geração, tal como foi escrito.
