import numpy as np

if __name__ == '__main__':

    print('Oprindelig matrix:')
    # A = np.array([
    #     [-1, 0, 1, 0, -5],
    #     [0, -2, 0, 1, -5],
    #     [0, 1, -1, 0, 85]
    # ])
    A = np.array([
        [ 2., 1., 1., 0., 0., 0.,-12.],
        [-1.,-2., 0., 1., 0., 0., -2.],
        [ 1.,-3., 0., 0., 1., 0., -1.],
        [-3.,-2., 0., 0., 0., 1.,  0.]
    ])
    # A = np.array([
    #     [ 2.,  1., 1., 0., 0., 0., 0., 0., 12.],
    #     [-1., -2., 0., 1., 0., 0., 0., 0., -4.],
    #     [ 1., -3., 0., 0., 1., 0., 0., 0., -1.],
    #     [-2.,  2., 0., 0., 0., 1., 0., 0.,  9.],
    #     [ 2.,  2., 0., 0., 0., 0., 1., 0., 17.],
    #     [-3., -2., 0., 0., 0., 0., 0., 1.,  0.]
    # ])
    # A = np.array([
    #     [-2., 1., 1., 0., 0., 0., 0., 0., 0., -2.],
    #     [1., 1., 0., 1., 0., 0., 0., 0., 0., 4.],
    #     [-1., -1., 0., 0., 1., 0., 0., 0., 0., -1.],
    #     [2., 1., 0., 0., 0., 1., 0., 0., 0., 6.],
    #     [0., 1., 0., 0., 0., 0., 1., 0., 0., 3.],
    #     [1., 0., 0., 0., 0., 0., 0., 1., 0., 2.],
    #     [-1., -1., 0., 0., 0., 0., 0., 0., 1., 0.]
    # ])
    def erBasal(A,j,i):
        n, m = len(A[0]), len(A)
        for x in range(0,m):
            if x == j: continue
            if A[x][i] != 0:
                return False
        return True


    def pivotSC(A):
        n, m = len(A[0]), len(A)
        mindstB, mindstI, mI, mJ = 0, 0, -1, -1
        for b in range(0, m - 1):
            temp = A[b][n-1]
            if temp < mindstB:
                mindstB, mJ = temp, b
            elif temp == mindstB:            #####
                for k in range(0,n-1):           #
                    if erBasal(A,mJ,k):          #
                        break                    #  Til hvis b værdierne er ens
                    elif erBasal(A,b,k):         #
                        mindstB, mJ = temp, b    #
                        break                #####
        for i in range(0,n-1):
            temp = A[mJ][i]
            if temp < mindstI:
                mindstI, mI = temp, i

        if mindstI == 0:
            print('Systemet er inkonsistent')
            exit(41)
        return 0, mI, mJ

    def pivotSted(A):
        n, m = len(A[0]), len(A)
        global fase1
        # Til fase 1
        for j in range(0, m - 1):
            if A[j][n - 1] < 0:

                if not fase1:
                    print('Fase 1:')
                    fase1 = True
                return pivotSC(A)

        # Til fase 2
        if fase1:
            print('Fase 2:')
            fase1 = False
        ratio, mI, mJ = 99999999999999999999, 0, 0
        for i in range(0, n - 1):
            if A[len(A) - 1][i] < 0:
                ubegranset = True
                for j in range(0, m - 1):
                    if A[j, i] > 0:
                        ubegranset = False
                        temp = ((A[j, n - 1]) / (A[j, i]))
                        if temp < ratio:
                            ratio, mI, mJ = temp, i, j
                if ubegranset:
                    print('Systemet er ubegrænset.')
                    exit(42)
        return ratio, mI, mJ


    def pivot(A, i, j):
        n, m, e = len(A[0]), len(A), A[j][i]
        A[j] = A[j] / e
        for r in range(m):
            if r == j: continue
            A[r] = A[r] - A[r][i] * A[j]


    def check(A):
        # print('checking')
        n, m = len(A[0]), len(A)
        for i in range(n - 1):
            if A[m - 1][i] < 0:
                return False
        return True

    fase1 = False
    done = False

    while not done:
        print(A)
        print('')
        ratio, i, j = pivotSted(A)
        if i == -1 and j == -1:
            print('færdig')
            break
        pivot(A, i, j)
        done = check(A)

    print(A)
