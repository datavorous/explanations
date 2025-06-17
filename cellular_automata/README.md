## sigmoid - logistic functions

```py
k = 1
populate = lambda n: [[uniform(0,1) for x in range(n)] for _ in range(n)]

def sigmoid(x, k=1, x0=4):
    # takes a number x and passes it through a sigmoid curve, which outputs a value between 0 and 1
    return 1 / (1 + math.exp(-k * (x - x0)))

def apply_rule(matrix, y, x, k=0.1):
    '''
    it adds up the 8 neighboring cell values around position (y, x),
    and uses a sigmoid function to convert the sum into a probability p
    IF THE SUM IS::
    1. near 4 (the center x0), p ≈ 0.5.
    2. much less than 4, p is close to 0.
    3. much more than 4, p is close to 1.

    a random number between 0 and 1 is generated.
    if it's less than p, return 1 (cell becomes alive) else die
    '''
    theSum = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][x+1] + matrix[y][x-1] + matrix[y][x+1] + matrix[y+1][x-1] + matrix[y+1][x] + matrix[y+1][x+1]
    # P from sig centered at 4
    p = sigmoid(theSum, k=k, x0=4)
    return 1 if random() < p else 0
```


https://github.com/user-attachments/assets/3d5fe05d-30d8-4aec-94fb-6a73401e193e

