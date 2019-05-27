import numpy as np

if __name__ == '__main__':

    print('Oprindelig matrix:')
    # Til hvis systemet er inkonsistent
    A = np.array([
        [2., 1., 1., 0., 0., 0., -12.],
        [-1., -2., 0., 1., 0., 0., -2.],
        [1., -3., 0., 0., 1., 0., -1.],
        [-3., -2., 0., 0., 0., 1., 0.]
    ])
    # Til hvis systemet er ubegrænset
    A = np.array([
        [2., 0., 1., 0., 0., 0., 12.],
        [-1., 0., 0., 1., 0., 0., -2.],
        [1., 0., 0., 0., 1., 0., 20.],
        [-1., -1., 0., 0., 0., 1., 0.]
    ])
    # Til eksemplet med simplex
    A = np.array([
        [2., 1., 1., 0., 0., 0., 0., 0., 12.],
        [-1., -2., 0., 1., 0., 0., 0., 0., -4.],
        [1., -3., 0., 0., 1., 0., 0., 0., -1.],
        [-2., 2., 0., 0., 0., 1., 0., 0., 9.],
        [2., 2., 0., 0., 0., 0., 1., 0., 17.],
        [-3., -2., 0., 0., 0., 0., 0., 1., 0.]
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
    def tilDual(A):
        n, m = len(A[0]), len(A)
        dualM: int =  n-m
        dualN: int = m+dualM
        R = np.zeros((dualM, m-1))
        for j in range(n-m-1):
            for i in range(m-1):
                R[j][i]=A[i][j]*-1
        for i in range(m-1):
            R[dualM-1][i] = A[i][n-1]
        R = np.c_[R, np.identity(dualM),np.zeros(3)]
        for j in range(n-m-1):
            R[j][dualN-1] = A[m-1][j]
        return  R
    #A = tilDual(A)

    def erBasal(A, i, j):  # ser om søjle j er basal
        n, m = len(A[0]), len(A)
        for r in range(0, m):
            if r == i: continue
            if A[r][j] != 0:
                return False
        return True


    def pivotSC(A):
        n, m = len(A[0]), len(A)
        mindstB, mindstI, mJ, mI = 0, 0, -1, -1
        for b in range(0, m - 1):
            temp = A[b][n - 1]
            if temp < mindstB:
                mindstB, mI = temp, b
            elif temp == mindstB:  #####
                for k in range(0, n - 1):  #
                    if erBasal(A, mI, k):  #
                        break  # Til hvis b værdierne er ens
                    elif erBasal(A, b, k):  #
                        mindstB, mI = temp, b  #
                        break  #####
        for j in range(0, n - 1):
            temp = A[mI][j]
            if temp < mindstI:
                mindstI, mJ = temp, j
                break

        if mindstI == 0:
            print('Systemet er inkonsistent')
            exit(41)
        return mI, mJ


    def pivotSted(A):
        n, m = len(A[0]), len(A)
        global fase1
        # Til fase 1
        for i in range(0, m - 1):
            if A[i][n - 1] < 0:

                if not fase1:
                    print('Fase 1:')
                    fase1 = True
                return pivotSC(A)

        # Til fase 2
        if fase1:
            print('Fase 2:')
            fase1 = False
        ratio, mJ, mI = 99999999999999999999, 0, 0
        for j in range(0, n - 1):
            if A[len(A) - 1][j] < 0:
                ubegranset = True
                for i in range(0, m - 1):
                    if A[i, j] > 0:
                        ubegranset = False
                        temp = ((A[i, n - 1]) / (A[i, j]))
                        if temp < ratio:
                            ratio, mJ, mI = temp, j, i
                if ubegranset:
                    print('Systemet er ubegrænset.')
                    exit(42)
        return mI, mJ


    def pivot(A, i, j):
        n, m, e = len(A[0]), len(A), A[i][j]
        A[i] = A[i] / e
        for r in range(m):
            if r == i: continue
            A[r] = A[r] - A[r][j] * A[i]


    def check(A):
        # print('checking')
        n, m = len(A[0]), len(A)
        for i in range(n - 1):
            if A[m - 1][i] < 0:
                return False
        return True


    fase1 = False
    done = False
    print(A)
    print('')
    while not done:
        i, j = pivotSted(A)
        print('Pivoterer ved søjle {:d} og række {:d}'.format(i + 1, j + 1))
        if i == -1 and j == -1:
            print('færdig')
            break
        pivot(A, i, j)
        done = check(A)
        print(A)
        print('')
