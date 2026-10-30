# documentacao

Esta pasta contém a documentação técnica da implementação de referência e as vistas estáticas. Não é preciso instalar nada para a consultar: basta abrir os ficheiros no navegador.

| Pasta | O que contém |
|---|---|
| `site/` | A documentação técnica, um conjunto de páginas HTML navegáveis (entrada em `site/index.html`). Explica a solução e cada módulo pelo que recebe, pelo que precisa e pelo que produz: a especificação das entidades, a extração das fontes, a geração da declaração com o LLM, o grafo, as vistas, a validação e a aplicação Web. |
| `vistas/` | As vistas geradas a partir das declarações de exemplo (entrada em `vistas/index.html`): cada vista em HTML e o respetivo ViewModel em JSON. Mostram, sem conhecer a tecnologia de origem, como os modelos e as regras estão organizados. |
| `textos/` | Os textos em Markdown que entram na documentação. |
| `catalogo_vistas.json` | O catálogo dos tipos de vista. |

A documentação e as vistas são geradas a partir do próprio código, pelo que não divergem da implementação:

```bash
cd ecv_referencia
python -m ecv documentacao    # documentacao/site/
python -m ecv vistas          # documentacao/vistas/
```
