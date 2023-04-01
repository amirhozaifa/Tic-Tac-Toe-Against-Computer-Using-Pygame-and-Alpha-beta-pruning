import pygame
import tic_tac_toe
import copy
import os

WIN_DIM = (500, 500)

WIN = pygame.display.set_mode(WIN_DIM)
pygame.display.set_caption("Tic Tac Toe")

BG_COL = (255, 255, 255)
CELL_COL = (200, 200, 200)
CELL_DIM = (100, 100)
RESTART_BUTTON_DIM = (50, 50)
RESTART_BUTTON_POS = (WIN_DIM[0] - RESTART_BUTTON_DIM[0] - 10, 10)
PASS_BUTTON_DIM = (65, 30)
PASS_BUTTON_POS = (10, 10)

X_SYM_IMG = pygame.image.load(os.path.join('Assets','x.png'))
X_SYM = pygame.transform.scale(X_SYM_IMG, CELL_DIM)
O_SYM_IMG = pygame.image.load(os.path.join('Assets','o.png'))
O_SYM = pygame.transform.scale(O_SYM_IMG, CELL_DIM)
WON_IMG = pygame.image.load(os.path.join('Assets','won.png'))
LOST_IMG = pygame.image.load(os.path.join('Assets','lost.png'))
DRAW_IMG = pygame.image.load(os.path.join('Assets','draw.png'))
RESTART_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','restart.png')), RESTART_BUTTON_DIM)
PASS_IMG = pygame.transform.scale(pygame.image.load(os.path.join('Assets','pass.png')), PASS_BUTTON_DIM)

USER_SYM = 'x'
COMP_SYM = 'o'

EMP_CELL_RECTS = []

state = []
restart_game = False
is_first_move_done = False
is_game_running = True
EMPTY_STATE = []

def draw_window():
    global state
    global is_game_running
    global is_first_move_done
    
    WIN.fill(BG_COL)
    WIN.blit(RESTART_IMG, RESTART_BUTTON_POS)
    
    if not is_first_move_done:
        WIN.blit(PASS_IMG, PASS_BUTTON_POS)
    
    
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(WIN, CELL_COL, EMP_CELL_RECTS[i][j])
            if state[i][j] == 'x': 
                WIN.blit(X_SYM, (EMP_CELL_RECTS[i][j].x, EMP_CELL_RECTS[i][j].y))
            elif state[i][j] == 'o': 
                WIN.blit(O_SYM, (EMP_CELL_RECTS[i][j].x, EMP_CELL_RECTS[i][j].y))
    
    if not is_game_running:
            if tic_tac_toe.result == 0:
                WIN.blit(DRAW_IMG, (EMP_CELL_RECTS[0][0].x, 10))
            elif tic_tac_toe.result == 1:
                WIN.blit(WON_IMG, (EMP_CELL_RECTS[0][0].x, 10))
            else:
                WIN.blit(LOST_IMG, (EMP_CELL_RECTS[0][0].x, 10))
    pygame.display.update()
    

def create_rects():
    global state
    START_POS = (80, 120)
    GAP = 20
    
    for i in range(3):
        cell_rect = pygame.Rect((START_POS[0], START_POS[1] + (CELL_DIM[1] + GAP) * i), CELL_DIM)
        EMP_CELL_RECTS.append([])
        for j in range(3):
            EMP_CELL_RECTS[i].append(copy.deepcopy(cell_rect))
            cell_rect.x += CELL_DIM[0] + GAP
    

def get_pressed(take_move):
    global state
    global restart_game
    global USER_SYM
    global COMP_SYM
    
    if pygame.mouse.get_pressed()[0]:
        x, y = pygame.mouse.get_pos()
        if RESTART_BUTTON_POS[0] <= x and x <= RESTART_BUTTON_POS[0] + RESTART_BUTTON_DIM[0] and RESTART_BUTTON_POS[1] <= y and y <= RESTART_BUTTON_POS[1] + RESTART_BUTTON_DIM[1]:
            restart_game = True
            return False
        if PASS_BUTTON_POS[0] <= x and x <= PASS_BUTTON_POS[0] + PASS_BUTTON_DIM[0] and PASS_BUTTON_POS[1] <= y and y <= PASS_BUTTON_POS[1] + PASS_BUTTON_DIM[1] and not is_first_move_done:
            USER_SYM = 'o'
            COMP_SYM = 'x'
            return True
            
        if take_move:
            for i in range(3):
                if EMP_CELL_RECTS[i][0].y <= y and y <= EMP_CELL_RECTS[i][0].y + CELL_DIM[1]:
                    for j in range(3):
                        if EMP_CELL_RECTS[i][j].x <= x and x <= EMP_CELL_RECTS[i][j].x + CELL_DIM[0] and state[i][j] == '_':
                            state[i][j] = USER_SYM
                            return True                        
    return False    

def reset_game():
    global state
    global restart_game
    global is_game_running
    global is_first_move_done
    global USER_SYM
    global COMP_SYM
    
    restart_game = False
    state = copy.deepcopy(EMPTY_STATE)
    is_game_running = True
    is_first_move_done = False
    
    USER_SYM = 'x'
    COMP_SYM = 'o'
    

def main():
    global state
    global restart_game
    global is_game_running
    global is_first_move_done
    global USER_SYM
    global COMP_SYM
    
   
    for i in range(3):
        EMPTY_STATE.append(["_", "_", "_"])
        
    reset_game()
        
    create_rects()
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw_window()
        
        if is_game_running:
            if get_pressed(True):
                is_first_move_done = True
                if tic_tac_toe.is_complete(state, "Min" if COMP_SYM == 'o' else "Max"):
                    is_game_running = False
                state = tic_tac_toe.computer_move(state, "Min" if COMP_SYM == 'o' else "Max")
                if tic_tac_toe.is_complete(state, "Min" if COMP_SYM == 'o' else "Max"):
                    is_game_running = False
        else:
            get_pressed(False)
            
        if restart_game:
            reset_game()
            
    pygame.quit()
        
if __name__ == "__main__":
    main()