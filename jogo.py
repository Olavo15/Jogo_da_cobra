import turtle
import random
import pygame
import threading
import time

pygame.mixer.init()
pygame.mixer.music.load("musc_ELN5cFaO.mp3")
pygame.mixer.music.play(-1)

def draw_spiral():
    h = 0 
    w = 0

    turtle.hideturtle()
    turtle.bgcolor("black")
    turtle.speed(0)
    turtle.pencolor("green")
    turtle.penup()
    turtle.goto(0, 200)
    turtle.pendown()

    while True:
        turtle.forward(h)
        turtle.right(w)
        h += 3
        w += 1
        if w == 200:
            turtle.penup()
            turtle.goto(0, 0)  
            turtle.write("Bem vindos", align="center", font=("Arial", 100, "normal"))
            turtle.color("white")
            turtle.ontimer(turtle.clear, 250) 
            break

if __name__ == "__main__":
    draw_spiral()


pygame.mixer.init()

# Definição das constantes e variáveis globais
WIDTH = 750
HEIGHT = 750
FOOD_SIZE = 20
DELAY = 100
BONUS_FOOD_INTERVAL = 20
bonus_food_time = time.time() + BONUS_FOOD_INTERVAL
bonus_food_pos = None
bonus_food_active = False
offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}
score = 0
is_alive = True

# Função para aumentar a pontuação
def increase_score():
    global score
    if is_alive:
        score += 1
        update_score()

# Função para atualizar o placar na tela
def update_score():
    score_pen.clear()
    score_pen.write("Score: {}".format(score), align="center", font=("Arial", 16, "normal"))

# Função para resetar o jogo
def reset():
    global snake, snake_direction, food_pos, is_alive, score
    is_alive = True
    score = 0
    update_score()
    snake = [[0, 0], [0, 20], [0, 40], [0, 50], [0, 60]]
    snake_direction = "up"
    food_pos = get_random_food_pos()
    food.goto(food_pos)
    draw_snake()
    move_snake()

# Função para desenhar a cobra
def draw_snake():
    for segment in snake:
        pen.goto(segment[0], segment[1])
        pen.stamp()

# Função para movimentar a cobra
def move_snake():
    global snake_direction, is_alive
    new_head = snake[-1].copy()
    new_head[0] = snake[-1][0] + offsets[snake_direction][0]
    new_head[1] = snake[-1][1] + offsets[snake_direction][1]

    if new_head in snake[:-1]:
        is_alive = False
        game_over()
    else:
        snake.append(new_head)
        if not food_collision():
            snake.pop(0)
        else:
            increase_score()
            # eating_sound.play()  # Reproduz o som de comer quando a comida é coletada

    if snake[-1][0] > WIDTH / 2:
        snake[-1][0] -= WIDTH
    elif snake[-1][0] < - WIDTH / 2:
        snake[-1][0] += WIDTH
    elif snake[-1][1] > HEIGHT / 2:
        snake[-1][1] -= HEIGHT
    elif snake[-1][1] < -HEIGHT / 2:
        snake[-1][1] += HEIGHT

    pen.clearstamps()
    draw_snake()
    screen.update()
    if is_alive:
        turtle.ontimer(move_snake, DELAY)

# Função para exibir "Game Over" e oferecer a opção de reiniciar o jogo
def game_over():
    pen.clear()
    pen.goto(0, 0)
    pen.write("Game Over", align="center", font=("Arial", 24, "normal"))
    pen.goto(0, -30)
    pen.write("Pressione R para reiniciar", align="center", font=("Arial", 16, "normal"))
    # collision_sound.play() 

# Função para limpar a tela
def clear_screen():
    pen.clear()

# Função para verificar se houve colisão com a comida
def food_collision():
    global food_pos
    head_x, head_y = snake[-1]
    food_x, food_y = food_pos
    if abs(head_x - food_x) < 1 * FOOD_SIZE and abs(head_y - food_y) < 1 * FOOD_SIZE:
        food_pos = get_random_food_pos()
        food.goto(food_pos)
        return True
    return False

# Função para gerar uma posição aleatória para a comida
def get_random_food_pos():
    x = random.randint(-WIDTH // 2 + FOOD_SIZE, WIDTH // 2 - FOOD_SIZE)
    y = random.randint(-HEIGHT // 2 + FOOD_SIZE, HEIGHT // 2 - FOOD_SIZE)
    return (x, y)

# Funções para movimentar a cobra nas direções
def go_up():
    global snake_direction
    if snake_direction != "down":
        snake_direction = "up"

def go_right():
    global snake_direction
    if snake_direction != "left":
        snake_direction = "right"

def go_down():
    global snake_direction
    if snake_direction != "up":
        snake_direction = "down"

def go_left():
    global snake_direction
    if snake_direction != "right":
        snake_direction = "left"

def restart():
    if not is_alive:
        reset()
        clear_screen()

screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake Game")
screen.bgcolor("#024959")
screen.tracer(0)

snake_color = "green"
snake_shape = "square"
pen = turtle.Turtle(snake_shape)
pen.penup()
pen.color(snake_color)


food = turtle.Turtle()
food.shape("circle")
food.color("red")
food.shapesize(FOOD_SIZE / 20)
food.penup()

score_pen = turtle.Turtle()  
score_pen.penup()
score_pen.color("white")
score_pen.goto(0, HEIGHT // 2 - 40)  
score_pen.hideturtle()  
update_score()

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_right, "Right")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(restart, "r")

reset()

turtle.done()
