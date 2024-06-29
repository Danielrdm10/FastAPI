def validar(f):
    def valida(x, y, a):
        if x<0 or y<0:
            raise ValueError('não deu')
        return f(x, y)
    def valida3(x, y):
        print (x*y)
    
        
    return valida 


@validar
def soma(x,l):
    return x + l

print(soma(1,2,3))