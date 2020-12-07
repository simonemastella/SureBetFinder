print("!!! usa il punto non la virgola !!!")
q1=float(input("Prima quota: "))
q2=float(input("Seconda quota: "))
puntata= float(input("Quanto vuoi puntare? "))
var = (1/q1) + (1/q2)
quanto1=puntata/(q1*var)
quanto2=puntata/(q2*var)
profitto=(quanto1*q1)-puntata
print("\nSulla quota 1: {}\nSulla quota 2: {}\nProfitto atteso: {}".format(quanto1,quanto2,profitto))
