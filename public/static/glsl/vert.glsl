#version 100

uniform mat4 mvp;

void main(void) {
	gl_Position = mvp * vec4(0.0, 0.0, 0.0, 1.0);
	gl_PointSize = gl_Position.w;
}
