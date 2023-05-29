#version 300 es

precision mediump float;
precision lowp int;

uniform sampler2D u_sampler;
uniform float u_shadow;

in vec3 pos;
in vec2 tex_coord;
in vec3 normal;

in vec4 world_pos;
in float shading;

out vec4 frag_colour;

void main(void) {
	vec4 texel = texture(u_sampler, tex_coord.ts);

	if (u_shadow > 0.0) {
		frag_colour = vec4(0.0, 0.0, 0.0, u_shadow - texel.r);
	}

	else {
		float dist = dot(world_pos.xz, world_pos.xz);
		float fade = 1.0 - dist / 25.0;

		frag_colour = texel * fade * vec4(vec3(shading), 1.0); // * vec4(normal, 1.0);
	}
}
