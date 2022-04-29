#version 100

precision mediump float;
precision lowp int;

uniform sampler2D u_sampler;
uniform float u_shadow;

varying vec3 pos;
varying vec2 tex_coord;
varying vec3 normal;

varying vec4 world_pos;
varying float shading;

void main(void) {
	vec4 texel = texture2D(u_sampler, tex_coord.ts);

	if (u_shadow > 0.0) {
		gl_FragColor = vec4(0.0, 0.0, 0.0, u_shadow - texel.r);
	}

	else {
		float dist = dot(world_pos.xz, world_pos.xz);
		float fade = 1.0 - dist / 25.0;

		gl_FragColor = texel * fade * vec4(vec3(shading), 1.0); // * vec4(normal, 1.0);
	}
}
