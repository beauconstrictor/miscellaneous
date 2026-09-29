from pathlib import Path
import moderngl
import pygame

VIEWPORT      = 3
ZOOM_RATE     = 0.01
RESOLUTION    = 1920, 1080

PARAMETER_2      = 2
PARAMETER_2_RATE = 0.05

class MandelbrotExplorer:
    def __init__(self) -> None:
        self.viewport   = VIEWPORT
        self.centre     = [0, 0]
        self.parameter  = [0, 0]
        self.parameter2 = 2

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
            shift = pygame.key.get_mods() & pygame.KMOD_SHIFT

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEWHEEL and shift:
                    if event.y > 0:
                        self.parameter2 += PARAMETER_2_RATE
                    if event.y < 0:
                        self.parameter2 -= PARAMETER_2_RATE

                elif event.type == pygame.MOUSEWHEEL:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    mouse_x -= RESOLUTION[0] / 2
                    mouse_y -= RESOLUTION[1] / 2
                    dist_per_pixel = self.viewport / RESOLUTION[1]

                    mouse_world_x = self.centre[0] + mouse_x * dist_per_pixel
                    mouse_world_y = self.centre[1] - mouse_y * dist_per_pixel

                    if event.y > 0:
                        self.viewport /= 1 + ZOOM_RATE
                    elif event.y < 0:
                        self.viewport *= 1 + ZOOM_RATE

                    dist_per_pixel = self.viewport / RESOLUTION[1]
                    new_mouse_world_x = self.centre[0] + mouse_x * dist_per_pixel
                    new_mouse_world_y = self.centre[1] - mouse_y * dist_per_pixel

                    self.centre[0] += mouse_world_x - new_mouse_world_x
                    self.centre[1] += mouse_world_y - new_mouse_world_y


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    dragging = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging = False
                elif event.type == pygame.MOUSEMOTION and dragging:
                    dx, dy = event.rel
                    dist_per_pixel = self.viewport / RESOLUTION[1]

                    if shift:
                        self.parameter[0] -= dx * dist_per_pixel
                        self.parameter[1] += dy * dist_per_pixel
                    else:
                        self.centre[0] -= dx * dist_per_pixel
                        self.centre[1] += dy * dist_per_pixel

            self.prog["centre"].value = self.centre
            self.prog["viewport"].value = self.viewport
            self.prog["parameter"].value = self.parameter
            self.prog["parameter2"].value = self.parameter2
            self.vao.render(moderngl.TRIANGLES, vertices=3)

            fps = clock.get_fps()
            pygame.display.set_caption(f"FPS: {fps:.1f}")

            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    explorer = MandelbrotExplorer()
    explorer.run()
