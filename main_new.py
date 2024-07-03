import pygame as pg


def set_chess(x, y, color):
    if board[x][y] != ' ':
        print('该位置已有棋子')
        return False
    else:
        board[x][y] = color
        return True


def check_win(board):
    for list_str in board:
        if ''.join(list_str).find('O' * 5) != -1:
            print('白棋获胜')
            return 0
        elif ''.join(list_str).find('X' * 5) != -1:
            print('黑棋获胜')
            return 1
    else:
        return -1


def check_win_all(board):
    board_c = [[] for line in range(29)]
    for x in range(15):
        for y in range(15):
            board_c[x - y].append(board[x][y])
    board_d = [[] for line in range(29)]
    for x in range(15):
        for y in range(15):
            board_d[x + y].append(board[x][y])
    return [check_win(board), check_win([list(l) for l in zip(*board)]), check_win(board_c), check_win(board_d)]


def main():
    pg.init()
    clock = pg.time.Clock()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    black = pg.image.load("data/chess_black.png").convert_alpha()
    white = pg.image.load("data/chess_white.png").convert_alpha()
    background = pg.image.load("data/bg.png").convert_alpha()
    objects = []
    pg.display.set_caption("五子棋")
    flag = 0
    going = True
    chess_list = [black, white]
    letter_list = ['X', 'O']
    while going:
        screen.blit(background, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                a, b = round((pos[0] - 27) / 40), round((pos[1] - 27) / 40)
                x, y = max(0, a) if a < 0 else min(a, 14), max(0, b) if b < 0 else min(b, 14)
                if set_chess(x, y, letter_list[flag]):
                    objects.append([chess_list[flag], (9 + x * 40, 9 + y * 40)])
                    flag = [1, 0][flag]
                    if 0 in check_win_all(board) or 1 in check_win_all(board):
                        going = False
        for o in objects:
            screen.blit(o[0], o[1])
        clock.tick(60)
        pg.display.update()


if __name__ == '__main__':
    WIDTH = 615
    HEIGHT = 615
    board = [[' '] * 15 for line in range(15)]
    main()
    pg.quit()
