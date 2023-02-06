def calculadora(operations: str):
    operations = operations.replace(" ", "")
    soma = 0

    for strs in operations.split("+"):
        subs = strs.split("-")
        if len(subs) == 2:
            soma -= int(subs[1])
        soma += int(subs[0])

    return soma
