
def connected(A):
    n = len(A)

    if n == 1:
        return True

    if not connected([row[0:n-1] for row in A[0:n-1]]):
        return False

    for j in range(n-1):
        if A[n-1][j]:
            return True
    return False


print(connected(
    [[0, 0, 1],
     [0, 0, 1],
     [1, 1, 0],]
))