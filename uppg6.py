import math

def euler(x, yVec, h):
    y = [None]*2
    y[0] = yVec[0] + h*yVec[1]
    y[1] = yVec[1] - h*yVec[0]
    x = x + h
    return x,y

def main():
    itertation = 1
    piApprox = 3
    while abs(piApprox - math.pi) > 1e-20:
        h = 1/(2**itertation)
        yVec = [1,0]
        x = 0
        while yVec[0] > 0:
            prevX = x
            prevYVec = yVec
            x,yVec = euler(x,yVec,h)
        k = (prevYVec[0] - yVec[0]) / (prevX-x)
        m = yVec[0] - k*x
        piApprox = -2*m/k
        print(piApprox)
        itertation += 1
    print(abs(math.pi-piApprox))

main()
