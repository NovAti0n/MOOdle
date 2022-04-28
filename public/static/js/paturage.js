window.addEventListener("load", function(e) {
	let canvas = document.getElementById("paturage")
	let gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl");

	if (!gl || !(gl instanceof WebGLRenderingContext)) {
		let error = document.getElementById("paturage-error")

		error.hidden = false
		canvas.hidden = true

		return
	}

	let x_res = gl.drawingBufferWidth
	let y_res = gl.drawingBufferHeight

	gl.viewport(0, 0, x_res, y_res)
	gl.clearColor(0.0, 0.5, 0.0, 1.0)
	gl.clear(gl.COLOR_BUFFER_BIT)
}, false)
