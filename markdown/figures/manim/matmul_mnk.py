"""
MNK Loop of matrix multiplex.
"""

from manim import *

config.frame_height = 8 + 4
config.frame_width = 24 + 8

class MatmulMnk(Scene):
    """MNK loop of matrix multiplex"""

    M = 8
    N = 8
    K = 8
    Space = 2

    def construct(self):
        # Tile
        title = Text("Matrix Multiplex, MNK").move_to(UP * (self.N/2 + 2))
        # Grid
        left_rect = Rectangle(color=GREEN, height=self.M, width=self.K,
                              grid_xstep=1.0, grid_ystep=1.0) \
            .move_to(LEFT * (self.N + self.Space))
        right_rect = Rectangle(color=GREEN, height=self.K, width=self.N,
                               grid_xstep=1.0, grid_ystep=1.0) 
        dest_rect = Rectangle(color=GREEN, height=self.M, width=self.N,
                              grid_xstep=1.0, grid_ystep=1.0) \
            .move_to(RIGHT * (self.N + self.Space))
        # Mark
        m_mark_1 = Text("M").move_to(LEFT * (self.N + self.Space + self.N/2 + 0.5))
        m_mark_2 = Text("M").move_to(RIGHT * (self.N + self.Space - self.N/2 - 0.5))
        n_mark_1 = Text("N").move_to(UP * (self.N/2 + 0.5))
        n_mark_2 = Text("N").move_to(RIGHT * (self.N + self.Space) + UP * (self.N/2 + 0.5))
        k_mark_1 = Text("K").move_to(LEFT * (self.N + self.Space) + UP * (self.N/2 + 0.5))
        k_mark_2 = Text("K").move_to(LEFT * (self.N/2 + 0.5))

        self.play(FadeIn(title))
        self.play(Create(left_rect), Create(right_rect), Create(dest_rect))
        self.play(FadeIn(m_mark_1), FadeIn(m_mark_2),
                  FadeIn(n_mark_1), FadeIn(n_mark_2),
                  FadeIn(k_mark_1), FadeIn(k_mark_2))
        self.wait()

        # Loop K
        left_rect_zero = LEFT * (self.N + self.N / 2 + self.Space - 0.5) + UP * (self.N / 2 - 0.5)
        right_rect_zero = LEFT * (self.N / 2 - 0.5) + UP * (self.N / 2 - 0.5)
        dest_rect_zero = RIGHT * (self.N - self.N / 2 + self.Space + 0.5) + UP * (self.N / 2 - 0.5)

        left_elem = Rectangle(color=BLUE, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(right_rect_zero)
        dest_elem = Rectangle(color=YELLOW, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(dest_rect_zero)

        subtitle = Text("Loop K").move_to(DOWN * (self.N/2 + 1))
        index = Text("K=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem), FadeIn(dest_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ki in range(1, self.K):
            dest_elem_t = Rectangle(color=YELLOW, height=1.0, width=1.0,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero)
            index_t = Text(f"K={ki}").move_to(DOWN * (self.N/2 + 2))
            self.play(left_elem.animate.move_to(left_rect_zero + RIGHT * ki),
                      right_elem.animate.move_to(right_rect_zero + DOWN * ki),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop N
        left_rect_zero = LEFT * (self.N + self.Space) + UP * (self.N / 2 - 0.5)
        right_rect_zero = LEFT * (self.N / 2 - 0.5)
        dest_rect_zero = RIGHT * (self.N - self.N / 2 + self.Space + 0.5) + UP * (self.N / 2 - 0.5)

        left_elem = Rectangle(color=BLUE, height=1.0, width=self.K, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=self.K, width=1.0, fill_opacity=0.5) \
            .move_to(right_rect_zero)

        subtitle = Text("Loop N").move_to(DOWN * (self.N/2 + 1))
        index = Text("N=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ni in range(1, self.N):
            dest_elem_t = Rectangle(color=YELLOW, height=1.0, width=ni + 1,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero + RIGHT * 0.5 * ni)
            index_t = Text(f"N={ni}").move_to(DOWN * (self.N/2 + 2))
            self.play(right_elem.animate.move_to(right_rect_zero + RIGHT * ni),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop M
        left_rect_zero = LEFT * (self.N + self.Space) + UP * (self.N / 2 - 0.5)
        dest_rect_zero = RIGHT * (self.N + self.Space) + UP * (self.N / 2 - 0.5)

        left_elem = Rectangle(color=BLUE, height=1.0, width=self.K, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=self.K, width=self.N, fill_opacity=0.5)

        subtitle = Text("Loop M").move_to(DOWN * (self.N/2 + 1))
        index = Text("M=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for mi in range(1, self.N):
            dest_elem_t = Rectangle(color=YELLOW, height=mi + 1, width=self.N,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero + DOWN * 0.5 * mi)
            index_t = Text(f"M={mi}").move_to(DOWN * (self.N/2 + 2))
            self.play(left_elem.animate.move_to(left_rect_zero + DOWN * mi),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem), FadeOut(dest_elem),
                  FadeOut(subtitle), FadeOut(index))


