from pathlib import Path
import moderngl
import pygame

VIEWPORT   = 3
ZOOM_RATE  = 0.01
RESOLUTION = 800, 600

class MandelbrotExplorer:
    def __init__(self) -> None:
        self.centre = [-0.45, 0.0]
        self.viewport = VIEWPORT

        self.set_up_pygame()
        self.set_up_gpu()

    def set_up_pygame(self) -> None:
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
        pygame.display.set_mode(RESOLUTION, pygame.OPENGL | pygame.DOUBLEBUF)

    def set_up_gpu(self) -> None:
        self.ctx = moderngl.create_context()

        frag_shader = (Path(__file__).parent / ".mandelbrot-2.glsl").read_text()
        self.prog = self.ctx.program(
            vertex_shader="""
            #version 330 core
            void main() {
                // single triangle to cover the screen
                vec2 pos = vec2((gl_VertexID << 1) & 2, gl_VertexID & 2);
                gl_Position = vec4(pos * 2.0 - 1.0, 0.0, 1.0);
            }
            """,
            fragment_shader=frag_shader,
        )

        self.prog["resolution"] = RESOLUTION

        self.vao = self.ctx.vertex_array(self.prog, [])

    def run(self) -> None:
        clock = pygame.time.Clock()
        running = True

        dragging = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    if event.y > 0:   self.viewport /= 1 + ZOOM_RATE
                    elif event.y < 0: self.viewport *= 1 + ZOOM_RATE
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    dx, dy = event.rel
    
                    dist_per_pixel = self.viewport / RESOLUTION[1]

                    self.centre[0] -= dx * dist_per_pixel
                    self.centre[1] += dy * dist_per_pixel

            self.prog["centre"].value = self.centre
            self.prog["viewport"].value = self.viewport
            self.vao.render(moderngl.TRIANGLES, vertices=3)

            fps = clock.get_fps()
            pygame.display.set_caption(f"FPS: {fps:.1f}")

            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    explorer = MandelbrotExplorer()
    explorer.run()
