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

		x /= mag
		y /= mag
		z /= mag

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
		let x = y * aspect

		this.frustum(-x * near, x * near, -y * near, y * near, near, far)
	}
}

class Model {
	constructor(gl, obj_id) {
		console.log(obj_id)
		let obj_src = document.getElementById(obj_id).innerHTML

		// read OBJ source
		// we do as few checks here as possible, because all this needs to be parsed client-side (if JS was a less horrible language, we could've used something like IVX instead of OBJ)

		let verts = new Float32Array()
		let tex_coords = new Float32Array()
		let normals = new Float32Array()
		let indices = new Float32Array()

		for (let line in obj_src.split('\n')) {
			let bits = line.split()

			let cmd = bits[0]
			let args = bits.slice(1).map(parseFloat)

			if (cmd == 'v') {
				verts.push(...args)
			}

			else if (cmd == 'vt') {
				tex_coords.push(...args)
			}

			else if (cmd == 'vn') {
				normals.push(...args)
			}

			else if (cmd == 'f') {

			}
		}

		// create positions vertex buffer object
		// the reason we're using multiple VBO's instead of a single one and multiple attribute pointers is that it makes reading OBJ's faster & simpler, *maybe* at the expense of driver overhead (I haven't profiled it, so there's a chance it may actually not change anything and the driver will lay things out optimally itself in video memory)

		this.vbo = gl.createBuffer()
		gl.bindBuffer(gl.ARRAY_BUFFER, this.vbo)
		gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW)

		gl.enableVertexAttribArray(0)
		gl.vertexAttribPointer(0, 3, gl.FLOAT, gl.FALSE, verts.BYTES_PER_ELEMENT * 8, verts.BYTES_PER_ELEMENT * 0)

		gl.enableVertexAttribArray(1)
		gl.vertexAttribPointer(1, 2, gl.FLOAT, gl.FALSE, verts.BYTES_PER_ELEMENT * 8, verts.BYTES_PER_ELEMENT * 3)

		gl.enableVertexAttribArray(2)
		gl.vertexAttribPointer(2, 3, gl.FLOAT, gl.FALSE, verts.BYTES_PER_ELEMENT * 8, verts.BYTES_PER_ELEMENT * 5)

		this.ibo = gl.createBuffer()
		gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, this.ibo)
		gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, indices, gl.STATIC_DRAW)
	}
}

// actual rendering code

window.addEventListener("load", function(e) {
	// webgl setup

	let canvas = document.getElementById("paturage")
	let error = document.getElementById("paturage-error")

	let gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

	if (!gl || !(gl instanceof WebGLRenderingContext)) {

		error.hidden = false
		canvas.hidden = true

		return
	}

	let x_res = gl.drawingBufferWidth
	let y_res = gl.drawingBufferHeight

	gl.viewport(0, 0, x_res, y_res)
	gl.clearColor(0.0, 0.5, 0.0, 1.0)
	gl.clear(gl.COLOR_BUFFER_BIT)

	// load shader program

	let vert_shader = gl.createShader(gl.VERTEX_SHADER)
	let frag_shader = gl.createShader(gl.FRAGMENT_SHADER)

	gl.shaderSource(vert_shader, document.getElementById("vert-shader").innerHTML)
	gl.shaderSource(frag_shader, document.getElementById("frag-shader").innerHTML)

	gl.compileShader(vert_shader)
	gl.compileShader(frag_shader)

	let program = gl.createProgram()

	gl.attachShader(program, vert_shader)
	gl.attachShader(program, frag_shader)

	gl.linkProgram(program)

	// MDN detaches the shaders first with 'gl.detachShader'
	// I'm not really sure what purpose this serves

	gl.deleteShader(vert_shader)
	gl.deleteShader(frag_shader)

	if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
		let log = gl.getProgramInfoLog(program)

		error.innerHTML = `Shader error: ${log}`
		error.hidden = false
	}

	let mvp_uniform = gl.getUniformLocation(program, "mvp")

	// matrices

	let p_matrix = new Matrix()
	p_matrix.perspective(6.28 / 4, y_res / x_res, 0.1, 500)

	let mv_matrix = new Matrix()

	mv_matrix.translate(0, 0, -49)
	// mv_matrix.rotate_2d(0.0, 0.0)

	let mvp_matrix = new Matrix(mv_matrix)
	mvp_matrix.multiply(p_matrix)

	// models

	let paturage = new Model(gl, "paturage-obj")

	gl.enableVertexAttribArray(0)
	let buffer = gl.createBuffer()
	gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
	gl.vertexAttribPointer(0, 1, gl.FLOAT, false, 0, 0)

	gl.useProgram(program)
	gl.uniformMatrix4fv(mvp_uniform, false, mvp_matrix.data.flat())

	gl.drawArrays(gl.POINTS, 0, 1)
}, false)
