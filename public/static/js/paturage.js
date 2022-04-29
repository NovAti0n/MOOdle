// matrices are all 4x4,
// and are initialized as the identity matrix

class Matrix {
	constructor(template) {
		if (template) {
			this.data = JSON.parse(JSON.stringify(template.data)) // I hate javascript 🙂
			return
		}

		this.data = [
			[1.0, 0.0, 0.0, 0.0],
			[0.0, 1.0, 0.0, 0.0],
			[0.0, 0.0, 1.0, 0.0],
			[0.0, 0.0, 0.0, 1.0],
		]
	}

	multiply(left) {
		let right = new Matrix(this)

		for (let i = 0; i < 4; i++) {
			for (let j = 0; j < 4; j++) {
				this.data[i][j] =
					left.data[0][j] * right.data[i][0] +
					left.data[1][j] * right.data[i][1] +
					left.data[2][j] * right.data[i][2] +
					left.data[3][j] * right.data[i][3]
			}
		}
	}

	scale(x, y, z) {
		for (let i = 0; i < 4; i++) {
			this.data[0][i] *= x
			this.data[1][i] *= y
			this.data[2][i] *= z
		}
	}

	translate(x, y, z) {
		for (let i = 0; i < 4; i++) {
			this.data[3][i] +=
				this.data[0][i] * x +
				this.data[1][i] * y +
				this.data[2][i] * z
		}
	}

	rotate(theta, x, y, z) {
		// theta represents the angle we want to rotate by
		// xyz represents the eigenvector of the matrix transformation of the rotation

		// normalize xyz

		let mag = Math.sqrt(x * x + y * y + z * z)

		x /= -mag
		y /= -mag
		z /= -mag

		let s = Math.sin(theta)
		let c = Math.cos(theta)
		let one_minus_c = 1 - c

		let xx = x * x, yy = y * y, zz = z * z
		let xy = x * y, yz = y * z, zx = z * x
		let xs = x * s, ys = y * s, zs = z * s

		let rotation = new Matrix()

		rotation.data[0][0] = (one_minus_c * xx) + c
		rotation.data[0][1] = (one_minus_c * xy) - zs
		rotation.data[0][2] = (one_minus_c * zx) + ys

		rotation.data[1][0] = (one_minus_c * xy) + zs
		rotation.data[1][1] = (one_minus_c * yy) + c
		rotation.data[1][2] = (one_minus_c * yz) - xs

		rotation.data[2][0] = (one_minus_c * zx) - ys
		rotation.data[2][1] = (one_minus_c * yz) + xs
		rotation.data[2][2] = (one_minus_c * zz) + c

		rotation.data[3][3] = 1

		rotation.multiply(this)
		this.data = rotation.data

		//this.multiply(rotation)
	}

	rotate_2d(yaw, pitch) {
		this.rotate(yaw, 0, 1, 0)
		this.rotate(-pitch, Math.cos(yaw), 0, Math.sin(yaw))
	}

	frustum(left, right, bottom, top, near, far) {
		let dx = right - left
		let dy = top - bottom
		let dz = far - near

		// clear out matrix

		for (let i = 0; i < 4; i++) {
			for (let j = 0; j < 4; j++) {
				this.data[i][j] = 0
			}
		}

		this.data[0][0] = 2 * near / dx
		this.data[1][1] = 2 * near / dy

		this.data[2][0] = (right + left) / dx
		this.data[2][1] = (top + bottom) / dy
		this.data[2][2] = -(near + far)  / dz

		this.data[2][3] = -1
		this.data[3][2] = -2 * near * far / dz
	}

	perspective(fovy, aspect, near, far) {
		let y = Math.tan(fovy / 2) / 2
		let x = y / aspect

		this.frustum(-x * near, x * near, -y * near, y * near, near, far)
	}
}

var identity = new Matrix()

class Model {
	constructor(gl, model, tex_path) {
		// load model

		this.model = model

		this.vbo = gl.createBuffer()
		gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo)
		gl.bufferData(gl.ARRAY_BUFFER, this.model.vertices, gl.STATIC_DRAW)

		this.ibo = gl.createBuffer()
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibo)
		gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, this.model.indices, gl.STATIC_DRAW)

		// load texture

		let tex = gl.createTexture()
		this.tex = tex

		const image = new Image()
		image.src = tex_path

		image.onload = function() {
			gl.bindTexture(gl.TEXTURE_2D, tex)
			gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, image)

			gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR)
			gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR)

			// WebGL 1.0 can be picky about non-POT textures, but here, all our textures are guaranteed POT

			gl.generateMipmap(gl.TEXTURE_2D)
		}
	}

	draw(gl, render_state, model_matrix) {
		// bind texture

		gl.activeTexture(gl.TEXTURE0)
		gl.bindTexture(gl.TEXTURE_2D, this.tex)
		gl.uniform1i(render_state.sampler_uniform, 0)

		// set uniforms

		gl.uniformMatrix4fv(render_state.model_uniform, false, model_matrix.data.flat())

		// draw buffers

		let float_size = this.model.vertices.BYTES_PER_ELEMENT

		gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo)
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibo)

		gl.enableVertexAttribArray(render_state.pos_attr)
		gl.enableVertexAttribArray(render_state.tex_coord_attr)
		gl.enableVertexAttribArray(render_state.normal_attr)

		gl.vertexAttribPointer(render_state.pos_attr,       3, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 0)
		gl.vertexAttribPointer(render_state.tex_coord_attr, 2, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 3)
		gl.vertexAttribPointer(render_state.normal_attr,    3, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 5)

		gl.drawElements(gl.TRIANGLES, this.model.indices.length, gl.UNSIGNED_SHORT, 0)
	}
}

const GRAVITY = -32
const JUMP_HEIGHT = 0.7
const BOUNDS = 2
const SHADOW_SIZE = 2

function abs_min(x, y) {
	if (Math.abs(x) < Math.abs(y)) {
		return x;
	}

	return y;
}

class Cow {
	constructor (model, age, shadow) {
		this.model = model
		this.age = age // controls the size of the cow
		this.shadow = shadow

		this.target_rot = Math.random() * 6.28

		this.rot = this.target_rot
		this.pos = [Math.random() * 4 - 2, 0, Math.random() * 4 - 2]

		this.vel = [0, 0, 0]
		this.grounded = false

		this.jump_height = JUMP_HEIGHT
	}

	jump() {
		if (!this.grounded) {
			return
		}

		this.vel[1] = Math.sqrt(-2 * GRAVITY * this.jump_height)
	}

	draw(gl, render_state, dt) {
		// "AI" computation

		if (Math.random() < 0.5 * dt) {
			this.jump()
		}

		this.rot += (this.target_rot - this.rot) * dt * 5

		// physics computation
		// really nothing complicated here, formulas come from a video of mine: https://www.youtube.com/watch?v=YG3Gd7Vr93o
		// first, calculate friction/drag coefficients

		let friction = [1.8, this.vel[1] > 0 ? 0 : 0.4, 1.8]

		if (this.grounded) {
			friction = [3, 3, 3]
		}

		// apply input acceleration & adjust for friction/drag
		// here, we want our cow moving in its rotation direction at all times

		this.vel[0] -= Math.cos(this.target_rot + 6.28 / 4) * friction[0] * dt
		this.vel[2] += Math.sin(this.target_rot + 6.28 / 4) * friction[2] * dt

		// apply velocity, gravity acceleration, and friction/drag

		this.pos = this.pos.map((pos, i) => pos + this.vel[i] * dt)
		this.vel[1] += GRAVITY * dt
		this.vel = this.vel.map((vel, i) => vel - abs_min(vel * friction[i] * dt, vel))

		// check collisions (nothing complicated, just check if we're past ground/boundaries and reset on respective axes)

		this.grounded = false

		if (this.pos[1] < 0) {
			this.grounded = true
			this.pos[1] = 0
		}

		if (this.pos[0] > BOUNDS || this.pos[2] > BOUNDS || this.pos[0] < -BOUNDS || this.pos[2] < -BOUNDS) {
			this.target_rot = Math.random() * 6.28

			this.pos[0] = Math.max(Math.min(this.pos[0], BOUNDS), -BOUNDS)
			this.pos[2] = Math.max(Math.min(this.pos[2], BOUNDS), -BOUNDS)

			this.vel = [0, 0, 0]
		}

		// render

		let model_matrix = new Matrix()
		let scale = 0.1 + this.age / 100

		model_matrix.translate(...this.pos)
		model_matrix.rotate(this.rot, 0, 1, 0)
		model_matrix.scale(scale, scale, scale)

		this.model.draw(gl, render_state, model_matrix)

		gl.uniform1f(render_state.shadow_uniform, 1 - this.pos[1] / this.jump_height * scale)
		gl.enable(gl.BLEND)

		model_matrix.translate(0, (-this.pos[1] + ++render_state.shadow_layer / 1000) / scale, 0)
		this.shadow.draw(gl, render_state, model_matrix)

		gl.uniform1f(render_state.shadow_uniform, -1)
		gl.disable(gl.BLEND)
	}
}

// actual rendering code

class Paturage {
	constructor() {
		// webgl setup

		let canvas = document.getElementById("paturage")
		let error = document.getElementById("paturage-error")

		this.gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

		if (!this.gl || !(this.gl instanceof WebGLRenderingContext)) {

			error.hidden = false
			canvas.hidden = true

			return
		}

		this.x_res = this.gl.drawingBufferWidth
		this.y_res = this.gl.drawingBufferHeight

		this.gl.viewport(0, 0, this.x_res, this.y_res)
		this.gl.enable(this.gl.DEPTH_TEST)
		this.gl.blendFunc(this.gl.SRC_ALPHA, this.gl.ONE_MINUS_SRC_ALPHA)

		// load shader program

		let vert_shader = this.gl.createShader(this.gl.VERTEX_SHADER)
		let frag_shader = this.gl.createShader(this.gl.FRAGMENT_SHADER)

		this.gl.shaderSource(vert_shader, document.getElementById("vert-shader").innerHTML)
		this.gl.shaderSource(frag_shader, document.getElementById("frag-shader").innerHTML)

		this.gl.compileShader(vert_shader)
		this.gl.compileShader(frag_shader)

		this.program = this.gl.createProgram()

		this.gl.attachShader(this.program, vert_shader)
		this.gl.attachShader(this.program, frag_shader)

		this.gl.linkProgram(this.program)

		// MDN detaches the shaders first with 'gl.detachShader'
		// I'm not really sure what purpose this serves

		this.gl.deleteShader(vert_shader)
		this.gl.deleteShader(frag_shader)

		if (!this.gl.getProgramParameter(this.program, this.gl.LINK_STATUS)) {
			let log = this.gl.getProgramInfoLog(this.program)

			error.innerHTML = `Shader error: ${log}`
			error.hidden = false
		}

		// get attribute & uniform locations from program
		// we have to do this for attributes too, because WebGL 1.0 limits us to older shader models

		this.render_state = {
			pos_attr:        0, // this.gl.getAttribLocation (this.program, "a_pos"),
			tex_coord_attr:  1, // this.gl.getAttribLocation (this.program, "a_tex_coord"),
			normal_attr:     2, // this.gl.getAttribLocation (this.program, "a_normal"),

			model_uniform:   this.gl.getUniformLocation(this.program, "u_model"),
			vp_uniform:      this.gl.getUniformLocation(this.program, "u_vp"),
			sampler_uniform: this.gl.getUniformLocation(this.program, "u_sampler"),
			shadow_uniform:  this.gl.getUniformLocation(this.program, "u_shadow")
		}

		// models

		const quad_model = {
			indices: new Uint16Array([0, 1, 2, 2, 3, 0]),
			vertices: new Float32Array([
				-SHADOW_SIZE, 0, -SHADOW_SIZE, 0, 0, 0, 1, 0, // 0
				 SHADOW_SIZE, 0, -SHADOW_SIZE, 1, 0, 0, 1, 0, // 1
				 SHADOW_SIZE, 0,  SHADOW_SIZE, 1, 1, 0, 1, 0, // 2
				-SHADOW_SIZE, 0,  SHADOW_SIZE, 0, 1, 0, 1, 0, // 3
			])
		}

		this.paturage = new Model(this.gl, paturage_model, "/textures/paturage.png")
		this.shadow = new Model(this.gl, quad_model, "/textures/shadow.png")

		this.holstein = new Model(this.gl, holstein_model, "/textures/holstein.png")
		this.jersey = new Model(this.gl, jersey_model, "/textures/jersey.png")
		this.bbb = new Model(this.gl, bbb_model, "/textures/bbb.png")

		// cows

		this.cows = []

		for (let i = 0; i < 50; i++) {
			this.cows.push(new Cow([this.jersey, this.holstein, this.bbb][(Math.random() * 3) | 0], Math.random() * 20, this.shadow))
		}

		// loop

		this.prev = 0
		requestAnimationFrame((now) => this.render(now))
	}

	render(now) {
		// timing

		const dt = (now - this.prev) / 1000
		this.prev = now

		const time = now / 1000

		// create matrices

		let proj_matrix = new Matrix()
		proj_matrix.perspective(6.28 / 4, this.y_res / this.x_res, 0.1, 500)

		let view_matrix = new Matrix()

		view_matrix.translate(0, 0, -6)
		view_matrix.rotate_2d(time / 3, -0.5)

		let vp_matrix = new Matrix(view_matrix)
		vp_matrix.multiply(proj_matrix)

		// actually render

		this.render_state.shadow_layer = 0

		this.gl.clearColor(0.0, 0.0, 0.0, 0.0)
		this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT)

		this.gl.useProgram(this.program)
		this.gl.uniformMatrix4fv(this.render_state.vp_uniform, false, vp_matrix.data.flat())

		this.paturage.draw(this.gl, this.render_state, identity /* no special transformation for paturage */)

		for (let cow of this.cows) {
			cow.draw(this.gl, this.render_state, dt)
		}

		requestAnimationFrame((now) => this.render(now))
	}
}

window.addEventListener("load", function(e) {
	new Paturage()
}, false)
