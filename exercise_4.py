def longestPal(s):
    l = len(s)

    # A is the matrix that represents the length of the longest palindromic subsequence in the interval [i,j]
    # for now I initialize it at 0 (i!=j) and 1 (i==j) because at this very fist moment I'll consider only
    # "longestPal" of a single char
    A = []
    for i in range(l):
        rowA = []
        for j in range(l):
            if i == j:
                rowA.append(1)
            else:
                rowA.append(0)
        A.append(rowA)

    # Now I'll check for neighbors char
    for i in range(l - 1):
        if s[i] == s[i + 1]:
            A[i][i + 1] = 2
        else:
            A[i][i + 1] = 1

    # Now I have to fill the matrix with the subinterval lenght: note that the longest Pal length is
    # in position A[0][l-1]: the last element of first row (and for this reason the return is this value)
    for k in range(2, l + 1):
        for i in range(l - k + 1):
            j = i + k - 1
            # I used this print to check every comparison
            # print("s[i],s[j] ", s[i],s[j], " i ",i," j ", j)
            if (s[i] == s[j]):
                A[i][j] = A[i + 1][j - 1] + 2;
            else:
                A[i][j] = max(A[i][j - 1], A[i + 1][j])

    return A[0][l - 1]


s1 = "DATAMININGSAPIENZA"
lp = longestPal(s1)
print(lp)