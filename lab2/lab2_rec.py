import turtle

DEPTH = 5

screen = turtle.Screen()
screen.setup(800, 800)
screen.title(f"Рекурсия")
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.penup()
t.goto(-200, -50)

# Направление зависит от глубины
if DEPTH % 2 == 0:
    t.setheading(0)    # горизонтально
else:
    t.setheading(60)   # под углом

t.pendown()
t.color("purple")
t.pensize(2)


def draw_curve(t, size, depth, direction=1):
    if depth == 0:
        t.forward(size)
    else:
        draw_curve(t, size/2, depth-1, -direction)
        t.right(60 * direction)
        draw_curve(t, size/2, depth-1, direction)
        t.right(60 * direction)
        draw_curve(t, size/2, depth-1, -direction)


draw_curve(t, 300, DEPTH)

t.hideturtle()
screen.exitonclick()