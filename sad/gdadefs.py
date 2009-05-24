# GDA Functions

def dbSemester(semestre, ano):
    # transforma o semestre 1 ou 2 em datas, coerente com o banco
    if semestre == '1': # semestre impar
        return '%s-01-01' % ano
    else: # semestre par
        return '%s-08-01' % ano
    
def counterDecorator(x = [0]):
    def foo(x = [0]):
        ret = x[0]
        x[0] += 1
        return ret
    return foo
