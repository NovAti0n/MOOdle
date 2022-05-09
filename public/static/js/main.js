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
			labels.push(date)
			chart_data.push(data[date])
		}

		break

	case 1:
		graph_name = "Animaux nés en période de pleine lune"
		chart_type = "doughnut"

		labels.push("Pleine lune")
		chart_data.push(parseInt(data[0]))

		labels.push("Hors pleine lune")
		chart_data.push(parseInt(data[1]))

		break

	case 2:
		graph_name = "Distribution des races"
		chart_type = "doughnut"

		for (let breed in data) {
			labels.push(breed)
			chart_data.push(data[breed])
		}

		break
}

chart_opt = {
	responsive: true,
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

if (chart_type) {
	const _data = {
		labels: labels,
		datasets: [{
			label: graph_name,
			data: chart_data,
			borderWidth: 0,
			backgroundColor: [
				"rgb(126, 119, 255)",
				"rgb(255, 52, 221)",
				"rgb(255, 79, 79)",
			],
		}],
	};

	new Chart(ctx, {
		type: chart_type,
		options: chart_opt,
		data: _data,
	});
}
