#version 100

attribute vec3 a_pos;
attribute vec2 a_tex_coord;
attribute vec3 a_normal;

uniform mat4 u_mvp;

void main(void) {
	gl_Position = u_mvp * vec4(a_pos, 1.0);
}
