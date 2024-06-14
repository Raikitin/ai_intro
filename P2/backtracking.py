# checks if the current board configuration is valid (no threats)
def check_valid(liste: list[int]) -> bool:
    for i in range(len(liste)):
        for j in range(len(liste)):
            if i >= j:
                continue
            if liste[i] == liste[j] or liste[i] + i - j == liste[j] or liste[i] - i + j == liste[j]:
                return False
    return True


def backtracking():
    stack: list[list[int]] = [[]]
    count: int = 0
    while len(stack) != 0:
        count += 1
        actual = stack.pop(-1)
        if len(actual) == 8:    # valid configuration (full list lenght)
            print(actual)
            continue
        for i in range(8):
            app = actual.copy()
            app.append(i)
            if check_valid(app):
                stack.append(app)
    print(count)


backtracking()
