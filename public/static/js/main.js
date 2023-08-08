// This Source Form is subject to the terms of the MOOdle OOpen Dairy LicensE, v. 1.0.
// Copyright (c) 2022 Alexis Englebert
// Copyright (c) 2022 Noa Quenon
// Copyright (c) 2022 Aymeric Wibo

// this took me so much time to figure out
// incomprehensible why chartjs doesn't simply have an option to change legend margins

const spacing_plugin = {
	id: "spacing_plugin",
	beforeInit: function(chart, legend, options) {
		const fit = chart.legend.fit

		chart.legend.fit = function() {
			fit.bind(chart.legend)()
			this.height += 32
		}
	}
}

const TAU = 6.28
const SIXTH = TAU / 6

function hsv_to_rgb(h, s, v) {
	let sixth = h / SIXTH

	let c = v * s
	let m = v - c

	let x = c * (1 - Math.abs(sixth % 2 - 1))

	switch (sixth | 0) {
		default:
		case 0: return [ c + m, x + m, 0 + m ]
		case 1: return [ x + m, c + m, 0 + m ]
		case 2: return [ 0 + m, c + m, x + m ]
		case 3: return [ 0 + m, x + m, c + m ]
		case 4: return [ x + m, 0 + m, c + m ]
		case 5: return [ c + m, 0 + m, x + m ]
	}
}

function lerp(x, interval) {
	const [ a, b ] = interval
	return a + (b - a) * x
}

let ctx = document.getElementById("graph").getContext("2d")

let labels = []
let graph_name = ""
let chart_data = []
let chart_type

switch (chart_id) {
	case 0:
		graph_name = "Nombre de velages"
		chart_type = "bar"

		for (let date in data) {
			const [year, month, day] = date.split("-")
			labels.push([day, month, year].join("/"))
			chart_data.push(data[date])
		}

		break

	case 1:
		graph_name = "Animaux nés en période de pleine lune"
		chart_type = "pie"

		labels.push("Pleine lune")
		chart_data.push(parseInt(data[0]))

		labels.push("Hors pleine lune")
		chart_data.push(parseInt(data[1]))

		break

	case 2:
		graph_name = "Distribution des races"
		chart_type = "pie"

		for (let breed in data) {
			labels.push(breed)
			chart_data.push(data[breed])
		}

		break
}

let chart

function create_chart(dark) {
	if (!chart_type) {
		return
	}

	if (chart) {
		chart.destroy()
	}

	chart_opt = {
		responsive: true,
		layout: {
			padding: 32
		},
		plugins: {
			zoom: {
				pan: { enabled: true },
				zoom: {
					wheel: { enabled: true },
					pinch: { enabled: true },
					mode: "xy",
				},
				limits: {
					y: { min: 0, max: 10 },
				},
			},
		},
	};

	let colours = []
	let border_colours = []

	let H_INTERVAL = [ 243, 332 ]
	let S_INTERVAL = [ 0.4, 0.7 ]
	let V_INTERVAL = [ 1.0, 0.9 ]

	if (dark) {
		H_INTERVAL = [ 360, 310 ]
		S_INTERVAL = [ 0.7, 0.8 ]
		V_INTERVAL = [ 1.0, 0.9 ]
	}

	for (let i = 0; i < chart_data.length; i++) {
		const range = chart_data.length == 1 ? 0 : i / (chart_data.length - 1)

		const h = lerp(range, H_INTERVAL) / 360 * TAU
		const s = lerp(range, S_INTERVAL)
		const v = lerp(range, V_INTERVAL)

		const [ r, g, b ] = hsv_to_rgb(h, s, v)

		colours.push(`rgba(${r * 255}, ${g * 255}, ${b * 255}, 1.0)`)
		border_colours.push(`rgba(${r * 255}, ${g * 255}, ${b * 255}, 1.0)`)
	}

	const _data = {
		labels: labels,
		datasets: [{
			label: graph_name,
			data: chart_data,
			borderWidth: 0,
			borderRadius: 8,
			backgroundColor: colours,
			borderColor: border_colours,
			spacing: 4,
			cutout: "70%",
			circumference: colours.length == 3 ? 358 : 360, // hack because chartjs is crappy
		}],
	};

	chart = new Chart(ctx, {
		type: chart_type,
		options: chart_opt,
		data: _data,
		plugins: [ spacing_plugin ]
	});
}

let media = window.matchMedia("(prefers-color-scheme: dark)")
create_chart(media.matches)

media.addEventListener("change", function(media) {
	create_chart(media.matches)
})
