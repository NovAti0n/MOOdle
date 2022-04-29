#version 100

precision lowp float;

attribute vec3 a_pos;
attribute vec2 a_tex_coord;
attribute vec3 a_normal;

uniform mat4 u_mvp;

varying vec3 pos;
varying vec2 tex_coord;
varying vec3 normal;

void main(void) {
	tex_coord = a_tex_coord;
	normal = a_normal;

	pos = a_pos;
	gl_Position = u_mvp * vec4(a_pos, 1.0);
}
