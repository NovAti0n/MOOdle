let ctx = document.getElementById('graph').getContext('2d')

let labels = []
let graph_name = ""
let chart_data = []
let chart_type

switch(chart_id) {
	case '0':
		graph_name = "Nombre de velages par jour"
		chart_type = "bar"

		for(let i = 0; i < data.length; i += 2) {
			labels.push(data[i])
			chart_data.push(parseInt(data[i + 1]))
		}

		break;

	case '1':
		graph_name = "Animaux nés en période de pleine lune"
		chart_type = "doughnut"

		labels.push("Pleine lune")
		labels.push("Hors pleine lune")

		chart_data.push(parseInt(data[0]))
		chart_data.push(parseInt(data[1]))

		break;

	case '2':
		graph_name = "Distribution des races"
		chart_type = "doughnut"

		for(let i = 0; i < data.length; i += 2) {
			labels.push(data[i])
			chart_data.push(parseInt(data[i + 1]))
		}

		break;
}


chart_opt = {
	responsive: false,
	plugins: {
		zoom: {
			pan: {enabled:true},
			zoom: {
				wheel: {enabled:true},
				pinch : {enabled:true},
				mode:"xy"
			},
			limits: {
				y : {min: 0, max: 10}
			}
		}
	}
};


if(chart_type) {
	const _data = {
		labels: labels,
		datasets: [{
			label: graph_name,
			data: chart_data,
			fill: false,
			borderColor: 'rgb(75, 192, 192)',
			tension: 0.1,
			backgroundColor: [
				'rgba(255, 99, 132, 0.4)',
				'rgba(255, 159, 64, 0.4)',
				'rgba(255, 205, 86, 0.4)',
				'rgba(75, 192, 192, 0.4)',
				'rgba(54, 162, 235, 0.4)',
				'rgba(153, 102, 255, 0.4)',
				'rgba(201, 203, 207, 0.4)'
			],
			borderColor: [
				'rgb(255, 99, 132)',
				'rgb(255, 159, 64)',
				'rgb(255, 205, 86)',
				'rgb(75, 192, 192)',
				'rgb(54, 162, 235)',
				'rgb(153, 102, 255)',
				'rgb(201, 203, 207)'
			]
		}]
	};

	let myChart = new Chart(ctx, {
		type: chart_type,
		options:chart_opt,
		data: _data,
	});
}
