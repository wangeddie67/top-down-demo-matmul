"""
MKN Loop of matrix multiplex.
"""

from manim import *

config.frame_height = 8 + 4
config.frame_width = 24 + 8

class MatmulKnmkn(Scene):
    """MKN loop of matrix multiplex"""

    M = 8
    N = 8
    K = 8
    Space = 2
    N_slice = 4
    K_slice = 4

    def construct(self):
        # Tile
        title = Text("Matrix Multiplex, KNMKN").move_to(UP * (self.N/2 + 2))
        # Grid
        left_rect = Rectangle(color=GREEN, height=self.M, width=self.K,
                              grid_xstep=1.0, grid_ystep=1.0) \
            .move_to(LEFT * (self.N + self.Space))
        right_rect = Rectangle(color=GREEN, height=self.K, width=self.N,
                               grid_xstep=1.0, grid_ystep=1.0) 
        dest_rect = Rectangle(color=GREEN, height=self.M, width=self.N,
                              grid_xstep=1.0, grid_ystep=1.0) \
            .move_to(RIGHT * (self.N + self.Space))
        left_slice_rect = Rectangle(color=RED, height=self.M, width=self.K,
                              grid_xstep=self.K_slice) \
            .move_to(LEFT * (self.N + self.Space))
        right_slice_rect = Rectangle(color=RED, height=self.K, width=self.N,
                               grid_xstep=self.N_slice, grid_ystep=self.K_slice) 
        dest_slice_rect = Rectangle(color=RED, height=self.M, width=self.N,
                              grid_xstep=self.N_slice) \
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
        self.play(Create(left_slice_rect), Create(right_slice_rect), Create(dest_slice_rect))
        self.play(FadeIn(m_mark_1), FadeIn(m_mark_2),
                  FadeIn(n_mark_1), FadeIn(n_mark_2),
                  FadeIn(k_mark_1), FadeIn(k_mark_2))
        self.wait()

        left_rect_base = LEFT * (self.N + self.N / 2 + self.Space) + UP * (self.N / 2)
        right_rect_base = LEFT * (self.N / 2) + UP * (self.N / 2)
        dest_rect_base = RIGHT * (self.N - self.N / 2 + self.Space) + UP * (self.N / 2)

        # Loop N
        left_rect_zero = left_rect_base + DOWN * 0.5 + RIGHT * 0.5
        right_rect_zero = right_rect_base + DOWN * 0.5 + RIGHT * 0.5
        dest_rect_zero = dest_rect_base + DOWN * 0.5 + RIGHT * 0.5

        left_elem = Rectangle(color=BLUE, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(right_rect_zero)
        dest_elem = Rectangle(color=YELLOW, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(dest_rect_zero)

        subtitle = Text("Inner Loop N").move_to(DOWN * (self.N/2 + 1))
        index = Text("N=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem), FadeIn(dest_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ni in range(1, self.N_slice):
            dest_elem_t = Rectangle(color=YELLOW, height=1.0, width=ni + 1,
                                    fill_opacity=0.5) \
                .move_to(dest_rect_zero + RIGHT * 0.5 * ni)
            index_t = Text(f"N={ni}").move_to(DOWN * (self.N/2 + 2))
            self.play(right_elem.animate.shift(RIGHT),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop K
        left_rect_zero = left_rect_base + DOWN * 0.5 + RIGHT * 0.5
        right_rect_zero = right_rect_base + DOWN * 0.5 + RIGHT * self.N_slice / 2
        dest_rect_zero = dest_rect_base + DOWN * 0.5 + RIGHT * self.N_slice / 2

        left_elem = Rectangle(color=BLUE, height=1.0, width=1.0, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=1.0, width=self.N_slice, fill_opacity=0.5) \
            .move_to(right_rect_zero)

        subtitle = Text("Inner Loop K").move_to(DOWN * (self.N/2 + 1))
        index = Text("K=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ki in range(1, self.K_slice):
            dest_elem_t = Rectangle(color=YELLOW, height=1.0, width=self.N_slice,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero)
            index_t = Text(f"K={ki}").move_to(DOWN * (self.N/2 + 2))
            self.play(left_elem.animate.shift(RIGHT),
                      right_elem.animate.shift(DOWN),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop M
        left_rect_zero = left_rect_base + DOWN * 0.5 + RIGHT * self.K_slice / 2
        right_rect_zero = right_rect_base + RIGHT * self.N_slice / 2 + DOWN * self.K_slice / 2
        dest_rect_zero = dest_rect_base + DOWN * 0.5 + RIGHT * self.N_slice / 2

        left_elem = Rectangle(color=BLUE, height=1.0, width=self.K_slice, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=self.K_slice, width=self.N_slice, fill_opacity=0.5) \
            .move_to(right_rect_zero)

        subtitle = Text("Loop M").move_to(DOWN * (self.N/2 + 1))
        index = Text("M=0").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for mi in range(1, self.M):
            dest_elem_t = Rectangle(color=YELLOW, height=mi + 1, width=self.N_slice,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero + DOWN * 0.5 * mi)
            index_t = Text(f"M={mi}").move_to(DOWN * (self.N/2 + 2))
            self.play(left_elem.animate.shift(DOWN),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop N
        left_rect_zero = left_rect_base + RIGHT * self.K_slice / 2 + DOWN * self.M / 2
        right_rect_zero = right_rect_base + RIGHT * self.N_slice / 2 + DOWN * self.K_slice / 2
        dest_rect_zero = dest_rect_base + DOWN * self.M / 2

        left_elem = Rectangle(color=BLUE, height=self.M, width=self.K_slice, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=self.K_slice, width=self.N_slice, fill_opacity=0.5) \
            .move_to(right_rect_zero)

        subtitle = Text("Outer Loop N").move_to(DOWN * (self.N/2 + 1))
        index = Text(f"N={ni - self.N_slice + 1}~{ni}").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ni in range(ni + self.N_slice, self.N, self.N_slice):
            dest_elem_t = Rectangle(color=YELLOW, height=self.M, width=ni + 1,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero + RIGHT * 0.5 * (ni + 1))
            index_t = Text(f"N={ni - self.N_slice + 1}~{ni}").move_to(DOWN * (self.N/2 + 2))
            self.play(right_elem.animate.shift(RIGHT * self.N_slice),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem),
                  FadeOut(subtitle), FadeOut(index))

        # Loop K
        left_rect_zero = left_rect_base + RIGHT * self.K_slice / 2 + DOWN * self.M / 2
        right_rect_zero = right_rect_base + RIGHT * self.N / 2 + DOWN * self.K_slice / 2
        dest_rect_zero = dest_rect_base + RIGHT * self.N / 2 + DOWN * self.M / 2

        left_elem = Rectangle(color=BLUE, height=self.M, width=self.K_slice, fill_opacity=0.5) \
            .move_to(left_rect_zero)
        right_elem = Rectangle(color=BLUE, height=self.K_slice, width=self.N, fill_opacity=0.5) \
            .move_to(right_rect_zero)

        subtitle = Text("Outer Loop K").move_to(DOWN * (self.N/2 + 1))
        index = Text(f"K={ki - self.K_slice + 1}~{ki}").move_to(DOWN * (self.N/2 + 2))

        self.play(FadeIn(left_elem), FadeIn(right_elem),
                  FadeIn(subtitle), FadeIn(index))
        self.wait()

        for ki in range(ki + self.K_slice, self.K, self.K_slice):
            dest_elem_t = Rectangle(color=YELLOW, height=self.M, width=self.N,
                                    fill_opacity=0.5 + ki/(self.K*2)) \
                .move_to(dest_rect_zero)
            index_t = Text(f"K={ki - self.K_slice + 1}~{ki}").move_to(DOWN * (self.N/2 + 2))
            self.play(left_elem.animate.shift(RIGHT * self.K_slice),
                      right_elem.animate.shift(DOWN * self.K_slice),
                      Transform(dest_elem, dest_elem_t),
                      Transform(index, index_t))
            self.wait()

        self.play(FadeOut(left_elem), FadeOut(right_elem), FadeOut(dest_elem),
                  FadeOut(subtitle), FadeOut(index))


