# 五子棋基础功能，文字提示，悔棋和恢复功能
import pygame as pg
import os


# 棋子类
class GameObject:
    # 具有棋子的图像、类别和坐标三个属性
    def __init__(self, image, color, pos):
        self.image = image
        self.color = color
        self.pos = image.get_rect(center=pos)


# 按钮类，生成了悔棋按钮和恢复按钮
class Button(object):
    # 具有图像surface，宽高和坐标属性
    def __init__(self, text, color, x=None, y=None):
        self.surface = font_big.render(text, True, color)
        self.WIDTH = self.surface.get_width()
        self.HEIGHT = self.surface.get_height()
        self.x = x
        self.y = y

    # 这个方法用于确定鼠标是否点击了对应的按钮
    def check_click(self, position):
        x_match = self.x < position[0] < self.x + self.WIDTH
        y_match = self.y < position[1] < self.y + self.HEIGHT
        if x_match and y_match:
            return True
        else:
            return False


def main(board_inner):
    pg.init()
    # 一系列数据初始化
    clock = pg.time.Clock()  # pygame时钟
    objects = []  # 下棋记录列表
    recover_objects = []  # 恢复棋子时用到的列表，即悔棋记录列表
    ob_list = [objects, recover_objects]  # 将以上两个列表放到一个列表中，主要是增强抽象度，简少了代码行数
    screen = pg.display.set_mode((WIDTH, HEIGHT))  # 游戏窗口
    black = pg.image.load("data/chess_black.png").convert_alpha()  # 黑棋棋子图像
    white = pg.image.load("data/chess_white.png").convert_alpha()  # 白棋棋子图像
    background = pg.image.load("data/bg.png").convert_alpha()  # 棋盘背景图像
    regret_button = Button('悔棋', RED, 665, 200)  # 创建悔棋按钮
    recover_button = Button('恢复', BLUE, 665, 300)  # 创建恢复按钮
    restart_button = Button('重新开始', GREEN, 625, 400)  # 创建重新开始按钮
    screen.blit(regret_button.surface, (regret_button.x, regret_button.y))  # 把悔棋按钮打印游戏窗口
    screen.blit(recover_button.surface, (recover_button.x, recover_button.y))  # 把恢复按钮打印游戏窗口
    screen.blit(restart_button.surface, (restart_button.x, restart_button.y))  # 把重新开始按钮打印游戏窗口
    pg.display.set_caption("五子棋")  # 窗体的标题
    flag = 0  # 回合变量，用于识别当前是哪一方回合
    going = True  # 主循环变量，用于控制主循环继续或者结束
    chess_list = [black, white]  # 棋子图像列表，主要是增强抽象度，简少了代码行数
    letter_list = ['X', 'O']  # 棋子类型列表，主要是增强抽象度，简少了代码行数
    word_list = ['黑棋', '白棋']  # 棋子文字名称列表，主要是增强抽象度，简少了代码行数
    word_color = [(0, 0, 0), (255, 255, 255)]  # 棋子文字颜色列表，主要是增强抽象度，简少了代码行数

    # 游戏主循环
    while going:
        screen.blit(background, (0, 0))  # 将棋盘背景打印到游戏窗口
        text = font.render("{}回合".format(word_list[flag]), True, word_color[flag])  # 创建一个文本对象，显示当前是哪方的回合
        text_pos = text.get_rect(centerx=background.get_width() / 2, y=2)  # 确定文本对象的显示位置
        screen.blit(text, text_pos)  # 将文本对象打印到游戏窗口
        # 通过循环不断识别玩家操作
        for event in pg.event.get():
            # 如果关闭窗口，主循环结束
            if event.type == pg.QUIT:
                going = False
            # 如果点击键盘ESC键，主循环结束
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            # 如果玩家进行了鼠标点击操作
            elif event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()  # 获取鼠标点击坐标
                # 如果点击了悔棋按钮或者恢复按钮
                if regret_button.check_click(pos) or recover_button.check_click(pos):
                    index = 0 if regret_button.check_click(pos) else 1  # 点击悔棋按钮index = 0，点击恢复按钮index = 1
                    # 对指定列表进行判空操作，然后对下棋记录列表或者悔棋记录列表进行操作
                    if ob_list[index]:
                        # print(ob_list[index][-1].pos)
                        # 将游戏/悔棋记录列表里的图像坐标，转化为board坐标
                        x, y = [round((p + 18 - 27) / 40) for p in ob_list[index][-1].pos[:2]]
                        # print(y, x)
                        # 如果是悔棋操作，则board指定元素值恢复为' '；如果是恢复操作，则指定坐标board指定元素重新赋值
                        board_inner[y][x] = ' ' if index == 0 else ob_list[index][-1].color
                        ob_list[index - 1].append(ob_list[index][-1])  # 将游戏/悔棋记录列表的最后一个值添加到悔棋/下棋记录列表
                        ob_list[index].pop()  # 将游戏/悔棋记录列表的最后一个值删除
                        flag = [1, 0][flag]  # 变更回合方
                elif restart_button.check_click(pos):
                    hint_text = font.render("游戏重新开始", True, word_color[flag])  # 提示文案
                    hint_text_pos = hint_text.get_rect(centerx=background.get_width() / 2, y=200)  # 提示文案位置
                    screen.blit(hint_text, hint_text_pos)  # 把提示文案打印到游戏窗口
                    pg.display.update()  # 对游戏窗口进行刷新
                    pg.time.delay(1000)  # 暂停0.3秒，保证文案能够清晰展示
                    board_inner = [[' '] * 15 for _ in range(15)]  # 对board进行初始化
                    objects.clear()  # 下棋记录列表初始化
                    recover_objects.clear()  # 悔棋记录列表初始化
                    flag = 0  # flag初始化
                    continue  # 通过continue跳过下一行代码，从而保证flag赋值不会异常
                else:
                    # 若用户点击的不是悔棋、恢复按钮，则进行落子操作
                    a, b = round((pos[0] - 27) / 40), round((pos[1] - 27) / 40)  # 将用户鼠标点击位置的坐标，换算为board坐标
                    # 若坐标非法（即点击到了黑色区域），则不做处理
                    if a >= 15 or b >= 15:
                        continue
                    else:
                        x, y = max(0, a) if a < 0 else min(a, 14), max(0, b) if b < 0 else min(b, 14)  # 将a、b进行处理得到x和y
                        # 若落子操作合法，则进行落子
                        if set_chess(board_inner, y, x, letter_list[flag]):
                            # 下棋记录列表添加指定棋子
                            objects.append(GameObject(chess_list[flag], letter_list[flag], (27 + x * 40, 27 + y * 40)))
                            # 一旦成功落子，则将悔棋记录列表清空；不这么做，一旦在悔棋和恢复中间掺杂落子操作，就会有问题
                            recover_objects.clear()
                            # 判断是否出现获胜方
                            if 0 in check_win_all(board_inner) or 1 in check_win_all(board_inner):
                                # 将下棋记录的棋子打印到游戏窗口
                                for o in objects:
                                    screen.blit(o.image, o.pos)
                                # 根据flag获取到当前获胜方，生成获胜文案
                                win_text = font.render("{}获胜，游戏5秒后重新开始".format(word_list[flag]), True,
                                                       word_color[flag])
                                # 设定获胜文案的位置
                                win_text_pos = win_text.get_rect(centerx=background.get_width() / 2, y=200)
                                screen.blit(win_text, win_text_pos)  # 把获胜文案打印到游戏窗口
                                pg.display.update()  # 对游戏窗口进行刷新
                                pg.time.delay(5000)  # 暂停5秒，保证文案能够清晰展示
                                board_inner = [[' '] * 15 for _ in range(15)]  # 对board进行初始化
                                objects.clear()  # 下棋记录列表初始化
                                recover_objects.clear()  # 悔棋记录列表初始化
                                flag = 0  # flag初始化
                                continue  # 通过continue跳过下一行代码，从而保证flag赋值不会异常
                            flag = [1, 0][flag]
                        # 若落子位置已经有棋子，则进行提示
                        else:
                            hint_text = font.render("该位置已有棋子", True, word_color[flag])  # 提示文案
                            hint_text_pos = hint_text.get_rect(centerx=background.get_width() / 2, y=200)  # 提示文案位置
                            # 将下棋记录的棋子打印到游戏窗口
                            for o in objects:
                                screen.blit(o.image, o.pos)
                            screen.blit(hint_text, hint_text_pos)  # 把提示文案打印到游戏窗口
                            pg.display.update()  # 对游戏窗口进行刷新
                            pg.time.delay(300)  # 暂停0.3秒，保证文案能够清晰展示
        # 将下棋记录的棋子打印到游戏窗口
        for o in objects:
            screen.blit(o.image, o.pos)
        clock.tick(60)  # 游戏帧率每秒60帧
        pg.display.update()  # 对游戏窗口进行刷新


def set_chess(board_inner, i, j, color):
    if board_inner[i][j] != ' ':
        print('该位置已有棋子')
        return False
    else:
        board_inner[i][j] = color
        return True


def check_win(board_inner):
    for list_str in board_inner:
        if ''.join(list_str).find('O' * 5) != -1:
            print('白棋获胜')
            return 0
        elif ''.join(list_str).find('X' * 5) != -1:
            print('黑棋获胜')
            return 1
    else:
        return -1


def check_win_all(board_inner):
    board_c = [[] for _ in range(29)]
    for x in range(15):
        for y in range(15):
            board_c[x + y].append(board_inner[x][y])
    board_d = [[] for _ in range(29)]
    for x in range(15):
        for y in range(15):
            board_d[x - y].append(board_inner[x][y])
    return [check_win(board_inner), check_win([list(i) for i in zip(*board_inner)]), check_win(board_c),
            check_win(board_d)]


if __name__ == "__main__":
    pg.init()
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    WIDTH, HEIGHT = 800, 615
    RED = (255, 48, 48)
    BLUE = (65, 105, 225)
    GREEN = (0, 139, 0)
    font = pg.font.Font('font/12345.TTF', 20)
    font_big = pg.font.Font('font/12345.TTF', 40)
    board = [[' '] * 15 for line in range(15)]
    main(board)
    pg.quit()
