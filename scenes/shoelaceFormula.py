from manim import *
import numpy as np

class ShoelaceFormula(Scene):
    def construct(self):
        title = Text("Fórmula do Cadarço", font_size=40)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))
        self.wait(2)

        axes = Axes(
            x_range=[0, 12, 1],
            y_range=[0, 8, 1],
            x_length=10,
            y_length=6.67,
            axis_config={"color": BLUE},
            x_axis_config={"numbers_to_include": range(0, 13, 2)},
            y_axis_config={"numbers_to_include": range(0, 9, 2)},
        ).to_edge(LEFT)
        self.play(Create(axes, run_time=5))
        self.wait(2)

        vertices = [
            np.array([2, 2, 0]),
            np.array([5, 6, 0]),
            np.array([8, 3, 0]),
            np.array([7, 1, 0]),
            np.array([4, 1, 0]),
        ]
        
        polygon_points = vertices + [vertices[0]]
        
        vertices_adjusted = [axes.c2p(*point[:2]) for point in vertices]
        
        polygon = Polygon(*vertices_adjusted, color=WHITE, fill_opacity=0.5, fill_color=BLUE)
        self.play(Create(polygon))
        self.wait(2)
        
        vertex_labels = []
        for i, point in enumerate(vertices_adjusted, 1):
            label = MathTex(f"(x_{i}, y_{i})", font_size=24)
            pos = DOWN
            match i:
                case 1:
                    pos=LEFT
                case 2:
                    pos=UP
                case 3:
                    pos=RIGHT
                case 4:
                    pos=DOWN
                case 5:
                    pos=DOWN
            label.next_to(point, pos, buff=0.1)
            vertex_labels.append(label)
            self.play(Write(label), run_time=1)
        
        self.wait(2)

        grupoDeTextos = VGroup()
        
        for i in range(len(polygon_points) - 1):
            x1, y1 = polygon_points[i][:2]
            x2, y2 = polygon_points[i+1][:2]
            
            col = GREEN 
            if (x1 <= x2):
                col = GREEN 
            else:
                col = RED 
            
            trap_points = [
                np.array([x1, 0, 0]),
                np.array([x2, 0, 0]),
                np.array([x2, y2, 0]),
                np.array([x1, y1, 0])
            ]

            trap_adjusted = [axes.c2p(*point[:2]) for point in trap_points]
            
            trapezoid = Polygon(*trap_adjusted, 
                             fill_opacity=0.6, 
                             fill_color=col,
                             stroke_width=2)
            
            
            self.play(Create(trapezoid))

            
            totalText = Text("Área do Polígono =", font_size=24).next_to(title, DOWN).shift(RIGHT*4)
            self.play(Write(totalText))
            self.wait(1)

            areaMath2 = MathTex(rf"\frac{{(y_{i+1}+y_{i+2 if i < (len(polygon_points) - 2) else 1})\cdot(x_{i+2 if i < (len(polygon_points) - 2) else 1}-x_{i+1})}}{2} {"+" if i < (len(polygon_points) - 2) else ""}", font_size=24).next_to(totalText, (DOWN + 3 * DOWN * i) if i > 0 else DOWN)
            self.play(Write(areaMath2))
            grupoDeTextos.add(areaMath2)
            self.wait(1)

            self.play(FadeOut(trapezoid))
            self.wait(1)

        formulaInicial = MathTex(r"\frac{\sum_{i=1}^{n} (y_i + y_{i+1})\cdot(x_{i+1}-x_i)}{2}", font_size=36).next_to(totalText, DOWN)
        self.play(TransformMatchingShapes(grupoDeTextos, formulaInicial))
        self.wait(3)
        self.play(FadeOut(formulaInicial))
        formula = MathTex(r"\frac{1}{2}\left| \sum_{i=1}^{n} (x_i y_{i+1} - x_{i+1} y_i) \right|", font_size=36).next_to(totalText, DOWN)
        self.play(Write(formula))
        self.wait(3)

        lastFormula = MathTex(r"\begin{vmatrix}x_1 & x_2 & \cdots & x_n \\y_1 & y_2 & \cdots & y_n\end{vmatrix}", font_size=36).next_to(formula, DOWN)
        lastFormulaStart = MathTex(r"=\frac{1}{2}", font_size=36).next_to(lastFormula, LEFT)
        lastFormulaEnd = MathTex(r"\begin{matrix} x_1 \\ y_1 \end{matrix}", font_size=36).next_to(lastFormula, RIGHT)
        self.play(Write(lastFormulaStart))
        self.play(Write(lastFormula))
        self.play(Write(lastFormulaEnd))
        self.wait(3)

        matrix_center = lastFormula.get_center()
        matrix_width = lastFormula.width
        matrix_height = lastFormula.height
        down_arrows = VGroup()
        for i in range(4):  
            start_x = matrix_center[0] - matrix_width/2 + (i+0.5)*matrix_width/4
            start_y = matrix_center[1] + matrix_height/4
            end_x = matrix_center[0] - matrix_width/2 + (i+1.5)*matrix_width/4
            end_y = matrix_center[1] - matrix_height/4
            arrow = Arrow(
                [start_x, start_y, 0],
                [end_x, end_y, 0],
                buff=0.1,
                color=GREEN,
                stroke_width=3
            )
            down_arrows.add(arrow)

        up_arrows = VGroup()
        for i in range(4):  
            start_x = matrix_center[0] - matrix_width/2 + (i+0.5)*matrix_width/4
            start_y = matrix_center[1] - matrix_height/4
            end_x = matrix_center[0] - matrix_width/2 + (i+1.5)*matrix_width/4
            end_y = matrix_center[1] + matrix_height/4
            arrow = Arrow(
                [start_x, start_y, 0],
                [end_x, end_y, 0],
                buff=0.1,
                color=RED,
                stroke_width=3
            )
            up_arrows.add(arrow)

        self.play(Create(down_arrows), run_time=3)
        self.wait(0.5)
        self.play(Create(up_arrows), run_time=3)
        self.wait(10)