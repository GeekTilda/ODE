import math
from decimal import Decimal, getcontext

getcontext().prec = 25

def euler(x, yVec, h):
    y = [None]*2
    y[0] = yVec[0] + h*yVec[1]
    y[1] = yVec[1] - h*yVec[0]
    x = x + h
    return x,y

def main():
    itertation = 1
    piApprox = Decimal(3)
    while abs(piApprox - Decimal(math.pi)) > 1e-13:
        h = Decimal(1/(2**itertation))
        yVec = [Decimal(1),Decimal(0)]
        x = Decimal(0)
        while yVec[0] > 0:
            prevX = x
            prevYVec = yVec
            x,yVec = euler(x,yVec,h)
        k = (prevYVec[0] - yVec[0]) / (prevX-x)
        m = yVec[0] - k*x
        piApprox = -2*m/k
        print(piApprox)
        itertation += 1
    print(abs(Decimal(math.pi)-piApprox))

main()