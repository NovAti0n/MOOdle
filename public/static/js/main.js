var ctx = document.getElementById('graph').getContext('2d');




const regex = /(\[\(|\)\]|&#39;| |\)|\(|,\)|\[|\])/g
let n_data = data.replace(regex, '')
n_data = n_data.split(',')

let  labels = [];
let graph_name = ""
let chart_data = []
let chart_type


switch(chart_id)
{
	case '0':
		console.log("Chart 0")
		graph_name = "Nombre de vêlages par jour sur une période"
		chart_type = "bar"

		for(let i = 0 ; i < n_data.length; i+=2)
		{
			labels.push(n_data[i])
			chart_data.push(parseInt(n_data[i+1]))
		}

		break;
	case '1':
		graph_name = "animaux nés en période de pleine lune"
		chart_type = "doughnut"

		labels.push("Full moon")
		labels.push("Not full moon")

		chart_data.push(parseInt(n_data[0]))
		chart_data.push(parseInt(n_data[1]))
		break;

	case '2':
		graph_name = "distribution des races dans la ferme"
		chart_type = "bar"
		//TODO ajouter la data
		break;

}


chart_opt = {responsive: false};


if(chart_type)
{
	const _data =
	{
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

		var myChart = new Chart(ctx,
		{
			type: chart_type,   // le type du graphique
			options:chart_opt,
			data: _data,

		});

}

