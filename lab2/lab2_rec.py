import turtle

def draw_sierpinski(t, order, size):
    if order == 0:
        for _ in range(3):
            t.forward(size)
            t.left(120)
    else:
        size /= 2
        draw_sierpinski(t, order - 1, size)
        t.forward(size)
        draw_sierpinski(t, order - 1, size)
        t.backward(size)
        t.left(60)
        t.forward(size)
        t.right(60)
        draw_sierpinski(t, order - 1, size)
        t.left(60)
        t.backward(size)
        t.right(60)

def main():
    screen = turtle.Screen()
    screen.setup(800, 800)
    screen.title("Кривая Серпинского - Рекурсивный метод")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    t.goto(-200, -150)
    t.pendown()
    
    order = 4  # Порядок кривой
    size = 400  # Размер базового треугольника
    
    draw_sierpinski(t, order, size)
    
    t.hideturtle()
    screen.exitonclick()

if __name__ == "__main__":
    main()