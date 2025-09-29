import turtle

def sierpinski_arrowhead_lsystem(order):
    if order % 2 == 0:
        axiom = "A"
    else:
        axiom = "A"
    
    rules = {
        'A': "B-A-B",
        'B': "A+B+A"
    }
    
    current_string = axiom
    for _ in range(order):
        next_string = ""
        for char in current_string:
            next_string += rules.get(char, char)
        current_string = next_string
    
    return current_string

def draw_sierpinski_arrowhead(t, instructions, angle, length):
    for cmd in instructions:
        if cmd == 'A' or cmd == 'B':
            t.forward(length)
        elif cmd == '+':
            t.left(angle)
        elif cmd == '-':
            t.right(angle)

def main():
    screen = turtle.Screen()
    screen.setup(700, 700)
    screen.title("L-система")
    screen.bgcolor("white")
    
    t = turtle.Turtle()
    t.speed(0)
    t.penup()
    
    # Центрируем и настраиваем начальную позицию
    t.goto(-200, -100)
    t.setheading(0)
    t.pendown()
    t.pensize(2)
    t.color("blue")
    
    order = 5  # Порядок кривой 
    angle = 60  # Угол 60 градусов для треугольника
    
    # Автоматический подбор длины в зависимости от порядка
    base_length = 400 / (2 ** order)
    if base_length < 5:
        base_length = 5
    
    instructions = sierpinski_arrowhead_lsystem(order)
    print(f"Порядок: {order}, Длина инструкций: {len(instructions)}")
    
    # Настраиваем начальный угол в зависимости от четности порядка
    if order % 2 == 0:
        t.setheading(0)   # Четный порядок - начинаем горизонтально
    else:
        t.setheading(60)  # Нечетный порядок - начинаем под углом
    
    draw_sierpinski_arrowhead(t, instructions, angle, base_length)
    
    t.hideturtle()
    screen.exitonclick()

if __name__ == "__main__":
    main()