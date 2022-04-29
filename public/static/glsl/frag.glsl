#version 100

precision lowp float;
precision lowp int;

uniform sampler2D u_sampler;

varying vec3 pos;
varying vec2 tex_coord;
varying vec3 normal;

void main(void) {
	float dist = dot(pos, pos);
	gl_FragColor = texture2D(u_sampler, tex_coord.ts) * (1.0 - dist / 25.0);
}
