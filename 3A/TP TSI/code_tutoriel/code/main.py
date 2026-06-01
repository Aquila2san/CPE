#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import numpy as np
import os
import pyrr
from ctypes import *
from PIL import Image

class Game(object):
    """ fenêtre GLFW avec openGL """

    def __init__(self):
        self.window = self.init_window()
        self.init_context()
        self.init_programs()
        self.init_data()
        self.X = 0
        self.Y = 0
        self.Z = -5.0
        self.angle_X = 0.0
        self.angle_Y = 0.0
        


    def init_window(self):
        # initialisation de la librairie glfw et du context opengl associé
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et parametrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        window = glfw.create_window(800, 800, 'OpenGL', None, None)
        # parametrage de la fonction de gestion des évènements
        glfw.set_key_callback(window, self.key_callback)
        return window

    def init_context(self):
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        
    def compile_shader(shader_content, shader_type): 
        # compilation d'un shader donn´e selon son type 
        shader_id = GL.glCreateShader(shader_type) 
        GL.glShaderSource(shader_id, shader_content) 
        GL.glCompileShader(shader_id) 
        success = GL.glGetShaderiv(shader_id, GL.GL_COMPILE_STATUS) 
        if not success: 
            log = GL.glGetShaderInfoLog(shader_id).decode('ascii') 
            print(f'{25*"-"}\nError compiling shader: \n\
                {shader_content}\n{5*"-"}\n{log}\n{25*"-"}') 
        return shader_id 
    
    def create_program(vertex_source, fragment_source): 
        # cr´eation d'un programme GPU 
        vs_id = Game.compile_shader(vertex_source, GL.GL_VERTEX_SHADER)
        fs_id = Game.compile_shader(fragment_source, GL.GL_FRAGMENT_SHADER) 
        if vs_id and fs_id: 
            program_id = GL.glCreateProgram() 
            GL.glAttachShader(program_id, vs_id) 
            GL.glAttachShader(program_id, fs_id) 
            GL.glLinkProgram(program_id) 
            success = GL.glGetProgramiv(program_id, GL.GL_LINK_STATUS) 
            if not success: 
                log = GL.glGetProgramInfoLog(program_id).decode('ascii') 
                print(f'{25*"-"}\nError linking program:\n{log}\n{25*"-"}') 
                GL.glDeleteShader(vs_id) 
                GL.glDeleteShader(fs_id) 
            return program_id 
    
    def create_program_from_file(vs_file, fs_file): 
        # cr´eation d'un programme GPU `a partir de fichiers 
        vs_content = open(vs_file, 'r').read() if os.path.exists(vs_file)\
            else print(f'{25*"-"}\nError reading file:\n{vs_file}\n{25*"-"}') 
        fs_content = open(fs_file, 'r').read() if os.path.exists(fs_file)\
            else print(f'{25*"-"}\nError reading file:\n{fs_file}\n{25*"-"}') 
        return Game.create_program(vs_content, fs_content)

    def init_programs(self):
        program = Game.create_program_from_file('phong.vert', 'phong.frag')
        GL.glUseProgram(program)
        pass
        
    def init_data(self):
        sommets = np.array((
            (0.0, 0.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,  0.0, 0.0), # p0
            (1.0, 0.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,  1.0, 0.0), # p1
            (1.0, 1.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,  1.0, 1.0), # p2
            (0.0, 1.0, 1.0,  0.0, 0.0, 1.0,  1.0, 0.0, 0.0,  0.0, 1.0), # p3

            (1.0, 0.0, 0.0,  0.0, 0.0, -1.0, 0.0, 1.0, 0.0,  0.0, 0.0), # p4
            (0.0, 0.0, 0.0,  0.0, 0.0, -1.0, 0.0, 1.0, 0.0,  1.0, 0.0), # p5
            (0.0, 1.0, 0.0,  0.0, 0.0, -1.0, 0.0, 1.0, 0.0,  1.0, 1.0), # p6
            (1.0, 1.0, 0.0,  0.0, 0.0, -1.0, 0.0, 1.0, 0.0,  0.0, 1.0), # p7

            (1.0, 0.0, 1.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0), # p8
            (1.0, 0.0, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,  1.0, 0.0), # p9
            (1.0, 1.0, 0.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,  1.0, 1.0), # p10
            (1.0, 1.0, 1.0,  1.0, 0.0, 0.0,  0.0, 0.0, 1.0,  0.0, 1.0), # p11

            (0.0, 0.0, 0.0, -1.0, 0.0, 0.0,  1.0, 1.0, 0.0,  0.0, 0.0), # p12
            (0.0, 0.0, 1.0, -1.0, 0.0, 0.0,  1.0, 1.0, 0.0,  1.0, 0.0), # p13
            (0.0, 1.0, 1.0, -1.0, 0.0, 0.0,  1.0, 1.0, 0.0,  1.0, 1.0), # p14
            (0.0, 1.0, 0.0, -1.0, 0.0, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0), # p15

            (0.0, 1.0, 1.0,  0.0, 1.0, 0.0,  0.0, 1.0, 1.0,  0.0, 0.0), # p16
            (1.0, 1.0, 1.0,  0.0, 1.0, 0.0,  0.0, 1.0, 1.0,  1.0, 0.0), # p17
            (1.0, 1.0, 0.0,  0.0, 1.0, 0.0,  0.0, 1.0, 1.0,  1.0, 1.0), # p18
            (0.0, 1.0, 0.0,  0.0, 1.0, 0.0,  0.0, 1.0, 1.0,  0.0, 1.0), # p19

            (0.0, 0.0, 0.0,  0.0, -1.0, 0.0, 1.0, 0.0, 1.0,  0.0, 0.0), # p20
            (1.0, 0.0, 0.0,  0.0, -1.0, 0.0, 1.0, 0.0, 1.0,  1.0, 0.0), # p21
            (1.0, 0.0, 1.0,  0.0, -1.0, 0.0, 1.0, 0.0, 1.0,  1.0, 1.0), # p22
            (0.0, 0.0, 1.0,  0.0, -1.0, 0.0, 1.0, 0.0, 1.0,  0.0, 1.0)  # p23
        ), np.float32)
        index = np.array((
            (0, 1, 2),    (0, 2, 3),      # Face avant
            (4, 5, 6),    (4, 6, 7),      # Face arrière
            (8, 9, 10),   (8, 10, 11),    # Face droite
            (12, 13, 14), (12, 14, 15),   # Face gauche
            (16, 17, 18), (16, 18, 19),   # Face supérieure
            (20, 21, 22), (20, 22, 23)    # Face inférieure
        ), np.uint32)
        # attribution d'une liste d'´etat (1 indique la cr´eation d'une seule liste) 
        self.vao = GL.glGenVertexArrays(1) 
        # affectation de la liste d'´etat courante 
        GL.glBindVertexArray(self.vao) 
        # attribution d’un buffer de donn´ees (1 indique la cr´eation d’un seul buffer) 
        vbo = GL.glGenBuffers(1) 
        # affectation du buffer courant 
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        # copie des donnees des sommets sur la carte graphique 
        GL.glBufferData(GL.GL_ARRAY_BUFFER, sommets, GL.GL_STATIC_DRAW)
        # Les deux commandes suivantes sont stock´ees dans l'´etat du vao courant 
        # Active l'utilisation des donn´ees de positions 
        # (le 0 correspond `a la location dans le vertex shader) 
        stride = 11*sizeof(c_float())
        GL.glEnableVertexAttribArray(0) 
        # Indique comment le buffer courant (dernier vbo "bind´e") 
        # est utilis´e pour les positions des sommets 
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, None)
        
        GL.glEnableVertexAttribArray(1) 
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(3 * sizeof(c_float)))
        
        GL.glEnableVertexAttribArray(2) 
        GL.glVertexAttribPointer(2, 3, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(6 * sizeof(c_float)))
        
        GL.glEnableVertexAttribArray(3) 
        GL.glVertexAttribPointer(3, 2, GL.GL_FLOAT, GL.GL_FALSE, stride, c_void_p(9 * sizeof(c_float)))
        # attribution d’un autre buffer de donnees 
        vboi = GL.glGenBuffers(1) 
        # affectation du buffer courant (buffer d’indice) 
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi) 
        # copie des indices sur la carte graphique 
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)
        self.texture_id1 = Game.load_texture('texture.png')
        self.texture_id2 = Game.load_texture('texture2.png')
        pass

    def load_texture(filename):
        if not os.path.exists(filename):
            print(f'{25*"-"}\nError reading file:\n{filename}\n{25*"-"}')
            return 0
        im = Image.open(filename).transpose(Image.Transpose.FLIP_TOP_BOTTOM).convert('RGBA')
        texture_id = GL.glGenTextures(1)
        # s´election de la texture courante `a partir de son identifiant
        GL.glBindTexture(GL.GL_TEXTURE_2D, texture_id)
        # param´etrisation de la texture
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, im.width, im.height, 0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, im.tobytes())
        return texture_id

    def generate_sphere(radius=1.0, lat_segments=16, lon_segments=32):
        vertices = []
        indices = []
        
        for i in range(lat_segments + 1):
            theta = np.pi * i / lat_segments
            sin_theta = np.sin(theta)
            cos_theta = np.cos(theta)
            
            for j in range(lon_segments + 1):
                phi = 2 * np.pi * j / lon_segments
                sin_phi = np.sin(phi)
                cos_phi = np.cos(phi)
                
                # Position (x, y, z)
                x = radius * sin_theta * cos_phi
                y = radius * cos_theta
                z = radius * sin_theta * sin_phi
                
                # Normale
                nx = sin_theta * cos_phi
                ny = cos_theta
                nz = sin_theta * sin_phi
                
                # Coordonnées de texture (u, v)
                u = j / lon_segments
                v = i / lat_segments
                
                # Couleur blanche par défaut (r, g, b)
                r, g, b = 1.0, 1.0, 1.0
                
                # Sommet entrelacé complet
                vertex = [x, y, z, nx, ny, nz, r, g, b, u, v]
                vertices.append(vertex)
                
        for i in range(lat_segments):
            for j in range(lon_segments):
                a = i * (lon_segments + 1) + j
                b = a + lon_segments + 1
                
                indices.append((a, b, a + 1))
                indices.append((a + 1, b, b + 1))
                
        return {
            'interlaced': np.array(vertices, dtype=np.float32),
            'faces': np.array(indices, dtype=np.uint32) # Forcé en uint32 pour correspondre à notre pipeline
        }

    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # gestion du temps
            t = glfw.get_time()
            # choix de la couleur de fond
            GL.glClearColor(0.65, 0, 0.35, 1.0)
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            # récupération des uniform et du porgramme actif
            prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM) 
            loc = GL.glGetUniformLocation(prog, "translation") 
            loc_proj = GL.glGetUniformLocation(prog, "projection")
            loc_rot = GL.glGetUniformLocation(prog, "rotation")
            # déplacement du triangle
            if glfw.get_key(self.window, glfw.KEY_RIGHT)==glfw.PRESS:
                self.X += 0.01
            if glfw.get_key(self.window, glfw.KEY_LEFT)==glfw.PRESS:
                self.X -= 0.01
            if glfw.get_key(self.window, glfw.KEY_UP)==glfw.PRESS:
                self.Y += 0.01
            if glfw.get_key(self.window, glfw.KEY_DOWN)==glfw.PRESS:
                self.Y -= 0.01
            if glfw.get_key(self.window, glfw.KEY_Y) == glfw.PRESS:
                self.Z += 0.01
            if glfw.get_key(self.window, glfw.KEY_H) == glfw.PRESS:
                self.Z -= 0.01
            # rotation du triangle
            if glfw.get_key(self.window, glfw.KEY_I) == glfw.PRESS:
                self.angle_X += 0.01
            if glfw.get_key(self.window, glfw.KEY_K) == glfw.PRESS:
                self.angle_X -= 0.01
            if glfw.get_key(self.window, glfw.KEY_J) == glfw.PRESS:
                self.angle_Y += 0.01
            if glfw.get_key(self.window, glfw.KEY_L) == glfw.PRESS:
                self.angle_Y -= 0.01
            # Calcul des matrices
            proj_matrix = pyrr.matrix44.create_perspective_projection_matrix(50.0, 1.0, 0.5, 10.0)
            rotX_33 = pyrr.matrix33.create_from_x_rotation(self.angle_X)
            rotY_33 = pyrr.matrix33.create_from_y_rotation(self.angle_Y)
            rotX_44 = pyrr.matrix44.create_from_matrix33(rotX_33)
            rotY_44 = pyrr.matrix44.create_from_matrix33(rotY_33)
            rot_mult_44 = pyrr.matrix44.multiply(rotX_44, rotY_44)
            mat_identite = pyrr.matrix44.create_identity()
            # Envoi des données au GPU
            GL.glUniformMatrix4fv(loc_proj, 1, GL.GL_FALSE, proj_matrix)
            GL.glBindVertexArray(self.vao)
            
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, rot_mult_44)
            GL.glUniform4f(loc, self.X, self.Y, self.Z, 1.0)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id1)
            GL.glDrawElements(GL.GL_TRIANGLES, 36, GL.GL_UNSIGNED_INT, None)
            
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, mat_identite)
            GL.glUniform4f(loc, 1.5, 0.0, -5.0, 1.0) 
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id1) 
            GL.glDrawElements(GL.GL_TRIANGLES, 36, GL.GL_UNSIGNED_INT, None)
            
            GL.glUniformMatrix4fv(loc_rot, 1, GL.GL_FALSE, mat_identite)
            GL.glUniform4f(loc, 1.5, -1.2, -5.0, 1.0) 
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id2) 
            GL.glDrawElements(GL.GL_TRIANGLES, 36, GL.GL_UNSIGNED_INT, None)
            
            GL.glEnable(GL.GL_DEPTH_TEST)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
            
                
                
             
    
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'echap'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(win, glfw.TRUE)
        # gestion de la couleur du triangle
        #prog = GL.glGetIntegerv(GL.GL_CURRENT_PROGRAM) 
        #color_trg = GL.glGetUniformLocation(prog, "color_trg")            
        #if key == glfw.KEY_R and action == glfw.PRESS:
        #    GL.glUniform4f(color_trg,1, 0, 0, 0)
        #if key == glfw.KEY_G and action == glfw.PRESS:
        #    GL.glUniform4f(color_trg,0, 1, 0, 0)
        #if key == glfw.KEY_B and action == glfw.PRESS:
        #    GL.glUniform4f(color_trg,0, 0, 1, 0)

def main():
    g = Game()
    g.run()
    glfw.terminate()

if __name__ == '__main__':
    main()