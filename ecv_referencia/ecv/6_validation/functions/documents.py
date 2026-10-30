"""Identification numbers, document codes, chained hashes and signatures."""
import hashlib
import hmac
import re

from . import implements
from .support import Unavailable, context


@implements("digitoControloValido")
def check_digit_valid(nif, *, contexts):
    """Verdadeira quando o dígito de controlo (módulo 11) do NIF está correto."""
    if nif is None:
        raise Unavailable("falta o NIF")
    s = str(nif)
    if not re.fullmatch(r"[0-9]{9}", s):
        return False
    total = sum(int(s[i]) * (9 - i) for i in range(8))
    digit = 11 - total % 11
    return int(s[8]) == (0 if digit >= 10 else digit)


@implements("atcudValido")
def atcud_valid(atcud, series, *, contexts):
    """Verdadeira quando o ATCUD pertence a uma série comunicada à AT e corresponde ao seu código de validação.

    The context seriesComunicadasAT is a dict {series: validation code} (or 'a=b,c=d'); the ATCUD has the
    form <validation code>-<sequence number>."""
    if atcud is None or series is None:
        raise Unavailable("falta o ATCUD ou a série")
    communicated = context(contexts, "seriesComunicadasAT")
    if isinstance(communicated, str):
        communicated = dict(x.split("=", 1) for x in communicated.split(",") if "=" in x)
    m = re.fullmatch(r"([A-Z0-9]{8,})-([0-9]+)", str(atcud))
    return bool(m) and communicated.get(str(series)) == m.group(1)


@implements("hashEncadeadoValido")
def chained_hash_valid(number, issue_date, total, document_hash, *, contexts):
    """Verdadeira quando o hash do documento deriva do número, da data, do total e do hash do documento anterior.

    Reference implementation (the AT one uses an RSA signature): the SHA-256, in hex, of
    '<dataEmissao>;<numero>;<total with two decimals>;<hashAnterior>'."""
    if None in (number, issue_date, total, document_hash):
        raise Unavailable("falta um dos campos do hash")
    previous = context(contexts, "hashAnterior")
    expected = hashlib.sha256(f"{issue_date};{number};{float(total):.2f};{previous}".encode()).hexdigest()
    return str(document_hash).lower() == expected


@implements("assinaturaValida")
def signature_valid(message, signature, *, contexts):
    """Verdadeira quando a assinatura (HMAC-SHA256) corresponde à mensagem e à chave do dispositivo."""
    if message is None or signature is None:
        raise Unavailable("falta a mensagem ou a assinatura")
    key = str(context(contexts, "chaveDispositivo")).encode()
    return hmac.compare_digest(hmac.new(key, str(message).encode(), hashlib.sha256).hexdigest(), str(signature).lower())
