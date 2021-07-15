from bisect import bisect
N_min, N_max = 2, 6
pow10 = [10**n for n in range(0,N_max+1)]
def floorlog10(x): return bisect(pow10, x)-1
prices = set(pow10[N_min:])

def bracket(x,y):
    e = pow10[y]
    a = x // e * e
    return a, a++e

def search(x):
    if x in prices:
        return(9,(x,x))
    n = N_min
    z = [1,1]
    while z[0]:
        z = ww(x,n)
        if not z[0]:
            return(1,(z[1]//10,z[1]))
        if z[0] in prices:
            return(n,z)
        n += 1
        pass
    return(0,(0,0))

print(sorted(list(prices)))

def insert(x):
    if x in prices:
        return

    n = N_min
    z = [1,1]

    prices.add(x)
    
    while z[0]:
        z = ww(x,n)
        if not z[0]:
            break
        if z[0] not in prices:
            prices.add(z[0])
            prices.add(z[1])
            pass
        n += 1
        pass
    pass

print(sorted(list(prices)))
print(sorted(list(prices)))
print(sorted(list(prices)))
print(sorted(list(prices)))
x = 563486
print(x)
print(list(search(x)))
insert(x)
print(list(search(x)))
print(list(search(x-4)))
print(sorted(list(prices)))
print(sorted(list(prices)))
print(sorted(list(prices)))
print(sorted(list(prices)))
        
