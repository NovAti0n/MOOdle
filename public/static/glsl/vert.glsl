#version 100

precision lowp float;

attribute vec3 a_pos;
attribute vec2 a_tex_coord;
attribute vec3 a_normal;

uniform mat4 u_model;
uniform mat4 u_vp;

varying vec3 pos;
varying vec2 tex_coord;
varying vec3 normal;

varying float shading;

void main(void) {
	tex_coord = a_tex_coord;
	normal = a_normal;

	pos = a_pos;
	gl_Position = u_vp * u_model * vec4(a_pos, 1.0);

	// lighting

	vec3 adjusted_normal = (vec4(normal, 1.0) * u_model).xyz;
	vec3 sunlight = vec3(-1.0, 0.0, 1.0);

	vec3 normalized_normal = normalize(adjusted_normal);
	vec3 normalized_sunlight = normalize(sunlight);

	float product = dot(normalized_normal, normalized_sunlight);

	shading = 1.0 - 0.6 * abs(product);
}
