# Biblioteca municipal: empréstimos e reservas

Uma biblioteca municipal regista as obras do seu catálogo, os exemplares de cada obra, os leitores, os empréstimos e as reservas. Os dados servem o balcão de atendimento (empréstimos e devoluções), o portal do leitor (reservas) e a troca de registos com a rede de bibliotecas do concelho.

## Obra

Uma obra é um título do catálogo, independente do número de exemplares.

- isbn (texto, opcional): número ISBN-13 da obra, sem hífenes. Deve ter 13 algarismos e começar por 978 ou 979.
- titulo (texto, obrigatório): título da obra.
- autores (texto, um ou mais): nome de cada autor, na forma "Apelido, Nome".
- anoEdicao (inteiro, opcional): ano da edição. Não pode ser posterior ao ano corrente.
- editora (texto, opcional): nome da editora.
- tipo (texto, obrigatório): tipo de obra. Valores: LIVRO, REVISTA, DVD, AUDIOLIVRO, MAPA.
- classificacao (texto, obrigatório): cota segundo a Classificação Decimal Universal, por exemplo 821.134.3-31.

Uma revista não tem ISBN; nesse caso o ISSN é obrigatório.

- issn (texto, opcional): número ISSN, na forma 0000-0000.

## Exemplar

Cada exemplar é uma cópia física de uma obra.

- codigoBarras (texto, obrigatório): código de barras do exemplar, com 10 algarismos.
- estado (texto, obrigatório): estado do exemplar. Valores: DISPONIVEL, EMPRESTADO, RESERVADO, EM_REPARACAO, ABATIDO.
- dataAquisicao (data, obrigatório): data em que o exemplar entrou na biblioteca.
- localizacao (texto, opcional): sala e estante.
- consultaLocal (booleano, obrigatório): verdadeiro quando o exemplar só pode ser consultado na biblioteca.

Um exemplar de consulta local nunca pode ser emprestado. Um exemplar abatido não pode ter empréstimos nem reservas.

## Leitor

- numeroLeitor (texto, obrigatório): número do cartão de leitor, na forma L seguido de 6 algarismos.
- nome (texto, obrigatório): nome completo.
- dataNascimento (data, obrigatório): data de nascimento.
- email (texto, opcional): endereço de correio eletrónico.
- telefone (texto, opcional): número de telefone com 9 algarismos.
- morada: rua, código postal, localidade e país.
- categoria (texto, obrigatório): categoria do leitor. Valores: ADULTO, JUVENIL, INFANTIL, SENIOR.
- dataValidade (data, obrigatório): data até à qual o cartão é válido.

O leitor tem de indicar pelo menos um contacto: o email ou o telefone. Um leitor com menos de 12 anos é da categoria INFANTIL e entre 12 e 17 anos é JUVENIL. Um leitor infantil ou juvenil tem de ter um responsável, com nome e contacto.

## Emprestimo

- numero (texto, obrigatório): número do empréstimo.
- dataEmprestimo (data, obrigatório): data em que o exemplar foi levantado.
- dataPrevistaDevolucao (data, obrigatório): data em que deve ser devolvido.
- dataDevolucao (data, opcional): data em que foi devolvido.
- renovacoes (inteiro, obrigatório): número de renovações já feitas.
- leitor e exemplar: o leitor que levou o exemplar.

A data prevista de devolução é posterior à data do empréstimo e no máximo 30 dias depois; para DVD o prazo é de 7 dias. A data de devolução, quando existe, não pode ser anterior à data do empréstimo. Um empréstimo pode ser renovado no máximo 2 vezes. O cartão do leitor tem de estar válido na data do empréstimo. Um leitor INFANTIL só pode ter 3 empréstimos em simultâneo; os outros, 6.

## Reserva

- dataReserva (data, obrigatório): data em que a reserva foi feita.
- estado (texto, obrigatório): Valores: ATIVA, SATISFEITA, CANCELADA, EXPIRADA.
- dataLimiteLevantamento (data, opcional): data até à qual o leitor pode levantar o exemplar.
- leitor e obra: quem reserva e o quê.

Uma reserva SATISFEITA tem de ter a data limite de levantamento, que é no máximo 5 dias depois de o exemplar ficar disponível. Só se reserva uma obra sem exemplares disponíveis.

## Troca com a rede de bibliotecas

Os registos enviados à rede levam a obra, os exemplares e o código da biblioteca, com 4 algarismos. O portal do leitor só mostra a obra e os exemplares disponíveis, sem dados dos leitores.
