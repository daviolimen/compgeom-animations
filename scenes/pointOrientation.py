from manim import *
import numpy as np

class PointOrientation(Scene):
    def demonstration(self):
        title = Text("Demonstrando a Fórmula")
        title.to_edge(UP)
        self.play(Create(title))
        self.wait(1)

        m2tex = MathTex(r"m_1=\frac{B_y - A_y}{B_x-A_x}", font_size=50)
        m1tex = MathTex(r"m_2=\frac{C_y-A_y}{C_x-A_x}", font_size=50)
        m1tex.center().shift(LEFT*3)
        m2tex.center().shift(RIGHT*3)
        groupedtex = VGroup(m1tex, m2tex)
        self.play(Create(groupedtex))
        self.wait(1)

        combineTex = MathTex(r"m_2-m_1=\frac{C_y-A_y}{C_x-A_x}-\frac{B_y - A_y}{B_x-A_x}=0", font_size=50)
        self.play(TransformMatchingShapes(groupedtex, combineTex, run_time=3))
        self.wait(1)

        developTex = MathTex(r"m_2-m_1=\frac{(C_y-A_y)(B_x-A_x)-(B_y-A_y)(C_x-A_x)}{(C_x-A_x)(B_x-A_x)}=0", font_size=50)
        self.play(TransformMatchingShapes(combineTex, developTex, run_time = 3))
        self.wait(3)

        endTex = MathTex(r"(C_y-A_y)(B_x-A_x)-(B_y-A_y)(C_x-A_x)=0", font_size=50)
        self.play(FadeOut(developTex))
        self.play(FadeIn(endTex))
        self.wait(5)

    def geometry(self):
        title = Text("Orientação de Ponto")
        title.to_edge(UP)
        self.play(Create(title))
        self.wait(1)

        axes = Axes(
            x_range=[-4,4,1],
            y_range=[-3,3,1],
            x_length=8,
            y_length=6,
            axis_config={"color": GREY}
        )
        axes.shift(DOWN*0.5)
        self.play(Create(axes, run_time=3))

        p1 = np.array([-2, -1, 0])
        p2 = np.array([2, 1, 0])

        p1Dot = Dot(axes.c2p(*p1[:2]), color=BLUE, radius=0.1)
        p2Dot = Dot(axes.c2p(*p2[:2]), color=BLUE, radius=0.1)
        p1Label = MathTex("A", font_size=24, color=BLUE).next_to(p1Dot, DOWN)
        p2Label = MathTex("B", font_size=24, color=BLUE).next_to(p2Dot, UP)
        vectorp1p2 = Arrow(p1Dot.get_center(), p2Dot.get_center(), buff=0.1, color=BLUE)

        self.play(
            FadeIn(p1Dot),
            FadeIn(p2Dot),
            Write(p1Label),
            Write(p2Label),
            Create(vectorp1p2),
            run_time=2
        )

        self.wait(3)

        point = (np.array([0, 0, 0]), "COLLINEAR", YELLOW)
        pointDot = Dot(axes.c2p(*point[0][:2]), color=WHITE, radius=0.12)
        pointLabel = MathTex("C", font_size=24, color=WHITE).next_to(pointDot, UP)
        vectorp1p = Arrow(p1Dot.get_center(), pointDot.get_center(), buff=0.1, color=WHITE)

        self.play(FadeIn(pointDot), Write(pointLabel), Create(vectorp1p))
        self.wait(5)
        self.clear()

        self.demonstration()
        self.clear()

        self.add(
            title, axes, p1Dot, p2Dot, p1Label, p2Label, pointDot, pointLabel, vectorp1p2, vectorp1p
        )

        formulaTitle = Text("Fórmula: ", font_size=32, color=YELLOW)
        formulaTitle.to_edge(LEFT).shift(UP*3)
        formula = MathTex(
            r"\alpha=(C_y-A_y)(B_x-A_x)-(B_y-A_y)(C_x-A_x)",
            font_size=24
        )
        formula.next_to(formulaTitle, DOWN, aligned_edge=LEFT)
        interpretation = Group(
            MathTex(r"\alpha > 0\rightarrow \text{Anti-Horário}", font_size=20, color=GREEN),
            MathTex(r"\alpha < 0\rightarrow \text{Horário}", font_size=20, color=RED),
            MathTex(r"\alpha = 0\rightarrow \text{Colinear}", font_size=20, color=YELLOW)
        ).arrange(DOWN, aligned_edge=LEFT)
        interpretation.next_to(formula, DOWN, aligned_edge=LEFT)

        self.play(FadeIn(formulaTitle))
        self.play(Write(formula))
        self.play(FadeIn(interpretation))
        self.wait(2)

        testPoints = [
            (np.array([0, 0, 0]), "COLLINEAR", YELLOW),
            (np.array([-1, 1.5, 0]), "LEFT", GREEN),
            (np.array([1, -1.5, 0]), "RIGHT", RED),
            (np.array([3, 2, 0]), "LEFT", GREEN),
            (np.array([-3, -2, 0]), "RIGHT", RED)
        ]

        for i, (pos, ori, col) in enumerate(testPoints):
            newPointDot = Dot(axes.c2p(*pos[:2]), color=WHITE, radius=0.12)
            self.play(
                pointDot.animate.move_to(newPointDot),
                pointLabel.animate.next_to(newPointDot, UP),
                vectorp1p.animate.become(Arrow(p1Dot.get_center(), newPointDot.get_center(), buff=0.1, color=WHITE)),
            )

            calculation_text = Text("Cálculo:", font_size=24).to_edge(RIGHT).shift(UP*3)
            result_text = MathTex(rf"\alpha=({pos[1]}-{p1[1] if p1[1] > 0 else f"({p1[1]})"}) \cdot ({p2[0]}-{p1[0] if p1[0] > 0 else f"({p1[0]})"})-({p2[1]}-{p1[1] if p1[1] > 0 else f"({p1[1]})"}) \cdot ({pos[0]}-{p1[0] if p1[0] > 0 else f"({p1[0]})"})", font_size=18).next_to(calculation_text, DOWN, aligned_edge=RIGHT)
            self.play(FadeIn(calculation_text))
            self.play(FadeIn(result_text))
            self.wait(2)
            result_calculated = MathTex(rf"\alpha={(pos[1]-p1[1])*(p2[0]-p1[0])-(p2[1]-p1[1])*(pos[0]-p1[0])}", font_size=18, color=col).next_to(calculation_text, DOWN, aligned_edge=RIGHT)
            self.play(Transform(result_text, result_calculated))
            self.wait(2)
            if ori == "LEFT":
                direction_label = MathTex(r"\alpha > 0\rightarrow \text{Anti-Horário}", font_size=18, color=GREEN)
            elif ori == "RIGHT":
                direction_label = MathTex(r"\alpha < 0\rightarrow \text{Horário}", font_size=18, color=RED)
            else:
                direction_label = MathTex(r"\alpha = 0\rightarrow \text{Colinear}", font_size=18, color=YELLOW)
            direction_label.next_to(result_calculated, DOWN, aligned_edge=RIGHT)
            self.play(FadeIn(direction_label))
            self.wait(2)
            # Calculate angle between vectors
            vec1 = p2 - p1
            vec2 = pos - p1

            if ori == "LEFT":
                setinha = CurvedArrow(p2Dot.get_center(), newPointDot.get_center(), radius=5, color=col)
            elif ori == "RIGHT":  # RIGHT
                setinha = CurvedArrow(p2Dot.get_center(), newPointDot.get_center(), radius=-5, color=col)

            if (ori != "COLLINEAR"):
                self.play(Create(setinha))
            self.wait(2)
            self.play(FadeOut(result_calculated), FadeOut(direction_label), FadeOut(result_text))
            if (ori != "COLLINEAR"):
                self.play(FadeOut(setinha))
            self.wait(2)

    def construct(self):
        self.geometry()