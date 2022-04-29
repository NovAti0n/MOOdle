#version 100

precision lowp float;
precision lowp int;

uniform sampler2D u_sampler;

varying vec3 pos;
varying vec2 tex_coord;
varying vec3 normal;

varying float shading;

void main(void) {
	float dist = dot(pos, pos);
	float fade = 1.0 - dist / 25.0;

	gl_FragColor = texture2D(u_sampler, tex_coord.ts) * fade * vec4(vec3(shading), 1.0);// * vec4(normal, 1.0);
}
