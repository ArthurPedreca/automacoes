import turtle
import random

# ----------------
# CONFIGURAÇÕES
# ----------------

# Título do gráfico
TITLE_X = 0
TITLE_Y = 130

# Sistema de coordenadas (tela vai de -400 a +400 no X, e -300 a +300 no Y)
WORLD_LEFT   = -400
WORLD_BOTTOM = -300
WORLD_RIGHT  =  400
WORLD_TOP    =  300

# Botão "Resetar" (canto superior direito)
BTN_X = 260     # X do canto esquerdo do botão
BTN_Y = 250     # Y do canto inferior do botão
BTN_W = 100     # Largura do botão
BTN_H = 30      # Altura do botão

def desenhar_grafico_barras(valores):
    """Desenha um gráfico de barras usando a lista de valores."""
    t = turtle.Turtle()
    t.speed("fastest")
    t.color("white")  # Cor padrão da caneta

    bar_width = 40
    gap = 10
    escala = 1

    # Posição inicial do gráfico
    base_x, base_y = -200, -200
    t.penup()
    t.goto(base_x, base_y)
    t.pendown()

    for valor in valores:
        # Sorteia cor para cada barra
        r = random.random()
        g = random.random()
        b = random.random()
        t.color(r, g, b)

        # Desenha a barra (retângulo)
        t.begin_fill()
        t.left(90)
        t.forward(valor * escala)
        t.right(90)
        t.forward(bar_width)
        t.right(90)
        t.forward(valor * escala)
        t.left(90)
        t.end_fill()

        # Escreve o valor acima da barra
        t.penup()
        t.left(90)
        t.forward(valor * escala + 10)
        t.color("white")
        t.write(str(valor), align="center", font=("Arial", 10, "normal"))
        t.backward(valor * escala + 10)
        t.right(90)
        t.backward(bar_width)
        t.pendown()

        # Avança para a próxima barra
        t.penup()
        t.forward(bar_width + gap)
        t.pendown()

def criar_grafico():
    """Pede valores via caixa de diálogo e desenha o gráfico."""
    screen = turtle.Screen()
    valores_string = screen.textinput(
        "Entrada de Dados",
        "Digite os valores (ex: 10,20,30):"
    )
    if valores_string:
        # Converte a string em lista de inteiros (separados por vírgula)
        valores = list(map(int, valores_string.replace(" ", "").split(",")))

        # Título do gráfico
        t_title = turtle.Turtle()
        t_title.hideturtle()
        t_title.penup()
        t_title.color("white")
        t_title.goto(TITLE_X, TITLE_Y)
        t_title.write("Meu Gráfico de Barras", align="center", font=("Arial", 16, "bold"))

        # Desenha o gráfico
        desenhar_grafico_barras(valores)

def desenhar_botao_resetar():
    """Desenha o botão cinza com texto 'Resetar' no canto superior direito."""
    t_btn = turtle.Turtle()
    t_btn.speed("fastest")
    t_btn.penup()
    t_btn.goto(BTN_X, BTN_Y)       # Canto inferior esquerdo do botão
    t_btn.color("white", "gray")   # Cor da caneta e do preenchimento
    t_btn.pendown()

    # Desenha o retângulo do botão
    t_btn.begin_fill()
    for side in [BTN_W, BTN_H, BTN_W, BTN_H]:
        t_btn.forward(side)
        t_btn.right(90)
    t_btn.end_fill()

    # Centraliza o texto dentro do retângulo
    t_btn.penup()
    meio_x = BTN_X + BTN_W / 2
    meio_y = BTN_Y + BTN_H / 2
    t_btn.goto(meio_x, meio_y - 6)  # Ajuste para o texto ficar bem centrado
    t_btn.color("black")
    t_btn.write("Resetar", align="center", font=("Arial", 12, "bold"))

    t_btn.hideturtle()
    # Retorna a cor para branco (se precisar desenhar algo depois)
    t_btn.color("white")

def verificar_click_botao_reset(x, y):
    """
    Verifica se o clique (x, y) está dentro do botão 'Resetar'.
    Se sim, limpa a tela e chama 'main()' para refazer o gráfico.
    """
    if (BTN_X <= x <= BTN_X + BTN_W) and (BTN_Y <= y <= BTN_Y + BTN_H):
        turtle.clearscreen()
        main()

def main():
    """Função principal: configura a tela, desenha o gráfico e em seguida o botão."""
    screen = turtle.Screen()
    screen.clear()
    screen.title("Gerador de Gráficos")
    screen.setup(width=800, height=600)

    # Define coordenadas fixas (ajuda a prever onde fica o botão)
    screen.setworldcoordinates(WORLD_LEFT, WORLD_BOTTOM, WORLD_RIGHT, WORLD_TOP)
    
    # Fundo preto
    screen.bgcolor("black")

    # 1) Cria o gráfico
    criar_grafico()

    # 2) Depois que o gráfico é criado, desenha o botão "Resetar"
    desenhar_botao_resetar()

    # 3) Ativa detecção de cliques
    screen.listen()
    screen.onclick(verificar_click_botao_reset)

    turtle.done()

if __name__ == "__main__":
    main()
