"""
Triangulo carregando os shaders de arquivos externos usando pathlib.
MCCC007-23 - Computação Gráfica - UFABC
Prof. João Paulo Gois
"""
import sys
from pathlib import Path

import glfw
import moderngl
import numpy as np

def erro_glfw(codigo, descricao):
    print(f"GLFW [{codigo}]: {descricao}", file=sys.stderr)

glfw.set_error_callback(erro_glfw)

if not glfw.init():
    sys.exit("FALHA: glfw nao inicializou")

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

janela = glfw.create_window(800, 600, "Triângulo com Shaders Externos", None, None)
if not janela:
    glfw.terminate()
    sys.exit("FALHA: não foi possível criar a janela")

glfw.make_context_current(janela)
ctx = moderngl.create_context()

# -------------- Lado da GPU: Carregando shaders da pasta 'shaders'
SHADERS = Path(__file__).parent / "shaders"

prog = ctx.program(
    vertex_shader=(SHADERS / "basico.vert").read_text(encoding="utf-8"),
    fragment_shader=(SHADERS / "basico.frag").read_text(encoding="utf-8"),
)

# ------------------- Lado da CPU: Dados do triângulo
vertices = np.array([
    0.0,  0.5, 0.0, 1.0,  1.0, 0.0, 0.0, 1.0,  # v0 topo, vermelho
    -0.5, -0.5, 0.0, 1.0,  0.0, 1.0, 0.0, 1.0,  # v1 esquerda, verde
    0.5, -0.5, 0.0, 1.0,  0.0, 0.0, 1.0, 1.0,  # v2 direita, azul
], dtype='f4')

vbo = ctx.buffer(vertices.tobytes())
vao = ctx.vertex_array(prog, [(vbo, '4f 4f', 'vPosition', 'vColors')])

while not glfw.window_should_close(janela):
    if glfw.get_key(janela, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(janela, True)

    ctx.clear(1.0, 1.0, 1.0, 1.0)
    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(janela)
    glfw.poll_events()

vao.release()
vbo.release()
prog.release()
glfw.terminate()
print("Execucao finalizada.")