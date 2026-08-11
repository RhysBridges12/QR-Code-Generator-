import numpy as np

FINDER_LIKE = ["000010111010000", "111101000101111"]


# decide if a module at (r,c) should flip for pattern p
def mask_condition(r, c, p):
    if p == 0:
        return (r + c) % 2 == 0
    elif p == 1:
        return r % 2 == 0
    elif p == 2:
        return c % 3 == 0
    elif p == 3:
        return (r + c) % 3 == 0
    elif p == 4:
        return ((r // 2) + (c // 3)) % 2 == 0
    elif p == 5:
        return ((r * c) % 2) + ((r * c) % 3) == 0
    elif p == 6:
        return (((r * c) % 2) + ((r * c) % 3)) % 2 == 0
    elif p == 7:
        return (((r + c) % 2) + ((r * c) % 3)) % 2 == 0
    return False

# apply one mask, flip 0/1 bits only
def apply_mask(mat, p):
    n = mat.shape[0]
    m = mat.copy()
    for i in range(n):
        for j in range(n):
            v = mat[i, j]
            if v in (0, 1) and mask_condition(i, j, p):
                m[i, j] = 1 - v
    return m

# score penalty for rows or columns line
def score_line(line):
    run = 1
    pen = 0
    col = line[0]
    for x in line[1:]:
        if x == col:
            run += 1
        else:
            if run >= 5:
                pen += 3 + (run - 5)
            col = x
            run = 1
    if run >= 5:
        pen += 3 + (run - 5)
    return pen

# compute total QR penalty
def score(mat):
    n = mat.shape[0]
    penalty = 0
    for i in range(n):
        penalty += score_line(mat[i, :])
        penalty += score_line(mat[:, i])
    # 2x2 blocks
    for i in range(n - 1):
        for j in range(n - 1):
            b = mat[i:i+2, j:j+2]
            if np.all(b == b[0, 0]):
                penalty += 3
    # finder-like patterns
    for i in range(n):
        row = ''.join(str(int(x)) for x in mat[i, :])
        col = ''.join(str(int(x)) for x in mat[:, i])
        for pat in FINDER_LIKE:
            idx = row.find(pat)
            while idx != -1:
                penalty += 40
                idx = row.find(pat, idx + 1)
            idx = col.find(pat)
            while idx != -1:
                penalty += 40
                idx = col.find(pat, idx + 1)
    # dark/light balance
    dark = int((mat == 1).sum())
    pct = dark * 100 / (n * n)
    penalty += (abs(pct - 50) // 5) * 10
    return int(penalty)

# choose best mask and apply
def mask(self):
    best = None
    best_pen = float('inf')
    best_mask_pattern = None 
    for p in range(8):
        candidate = apply_mask(self.matrix, p)
        pen = score(candidate)
        if pen < best_pen:
            best_pen = pen
            best = candidate
            best_mask_pattern = p 
    self.masked = best
    self.mask_pattern = best_mask_pattern
    return best
