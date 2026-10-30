"""IVA category decomposition validation."""

from . import implements

from .support import present





@implements("categoriasIvaDecompostas")

def categorias_iva_decompostas(

    codigosLinhas,

    codigosDescontos,

    codigosEncargos,

    codigosDecomposicao,

    *,

    contexts

):

    """Verdadeira quando cada código de categoria de IVA usado nas linhas, nos descontos e nos encargos aparece na decomposição do IVA."""



    if (

        codigosLinhas is None

        or codigosDescontos is None

        or codigosEncargos is None

        or codigosDecomposicao is None

    ):

        return False



    codigos_utilizados = (

        present(codigosLinhas)

        + present(codigosDescontos)

        + present(codigosEncargos)

    )



    codigos_decompostos = set(present(codigosDecomposicao))



    return all(

        codigo in codigos_decompostos

        for codigo in codigos_utilizados

    )
