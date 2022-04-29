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

class Model {
	constructor(gl, model, tex_path) {
		// load model

		this.index_count = model.indices.length
		let float_size = model.vertices.BYTES_PER_ELEMENT

		this.vbo = gl.createBuffer()
		gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo)
		gl.bufferData(gl.ARRAY_BUFFER, model.vertices, gl.STATIC_DRAW)

		gl.enableVertexAttribArray(0)
		gl.vertexAttribPointer(0, 3, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 0)

		gl.enableVertexAttribArray(1)
		gl.vertexAttribPointer(1, 2, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 3)

		gl.enableVertexAttribArray(2)
		gl.vertexAttribPointer(2, 3, gl.FLOAT, gl.FALSE, float_size * 8, float_size * 5)

		this.ibo = gl.createBuffer()
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibo)
		gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, model.indices, gl.STATIC_DRAW)

		// load texture

		let tex = gl.createTexture()
		this.tex = tex

		const image = new Image()
		image.src = tex_path

		image.onload = function() {
			gl.bindTexture(gl.TEXTURE_2D, tex)
			gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, image)

			// WebGL 1.0 can be picky about non-POT textures, but here, all our textures are guaranteed POT

			gl.generateMipmap(gl.TEXTURE_2D)
		}
	}

	draw(gl, sampler_uniform) {
		// bind texture

		gl.activeTexture(gl.TEXTURE0)
		gl.bindTexture(gl.TEXTURE_2D, this.tex)
		gl.uniform1i(sampler_uniform, 0)

		// draw buffers

		gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo)
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibo)

		gl.drawElements(gl.TRIANGLES, this.index_count, gl.UNSIGNED_SHORT, 0)
	}
}

// actual rendering code

var gl
var program

var mvp_matrix

var mvp_uniform
var sampler_uniform

var paturage

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

		let pos_attr = this.gl.getAttribLocation(this.program, "a_pos")
		let tex_coord_attr = this.gl.getAttribLocation(this.program, "a_tex_coord")
		let normal_attr = this.gl.getAttribLocation(this.program, "a_normal")

		this.mvp_uniform = this.gl.getUniformLocation(this.program, "u_mvp")
		this.sampler_uniform = this.gl.getUniformLocation(this.program, "u_sampler")

		// models

		this.paturage = new Model(this.gl, paturage_model, "/textures/paturage.png")

		// loop

		this.prev = 0
		requestAnimationFrame((now) => this.render(now))
	}

	render(now) {
		// timing

		const dt = (now - this.prev) / 1000
		this.prev = now

		// create matrices

		let p_matrix = new Matrix()
		p_matrix.perspective(6.28 / 4, this.y_res / this.x_res, 0.1, 500)

		let mv_matrix = new Matrix()

		mv_matrix.translate(0, 0, -6)
		mv_matrix.rotate_2d(now / 1000, -0.5)

		mvp_matrix = new Matrix(mv_matrix)
		mvp_matrix.multiply(p_matrix)

		// actually render

		this.gl.clearColor(0.0, 0.0, 0.0, 0.0)
		this.gl.clear(this.gl.COLOR_BUFFER_BIT | this.gl.DEPTH_BUFFER_BIT)

		this.gl.useProgram(this.program)
		this.gl.uniformMatrix4fv(this.mvp_uniform, false, mvp_matrix.data.flat())

		this.paturage.draw(this.gl, this.sampler_uniform)

		requestAnimationFrame((now) => this.render(now))
	}
}

window.addEventListener("load", function(e) {
	new Paturage()
}, false)
