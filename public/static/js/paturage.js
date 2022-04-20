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

	gl.enableVertexAttribArray(0)
	let buffer = gl.createBuffer()
	gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
	gl.vertexAttribPointer(0, 1, gl.FLOAT, false, 0, 0)

	gl.useProgram(program)
	gl.drawArrays(gl.POINTS, 0, 1)
}, false)
