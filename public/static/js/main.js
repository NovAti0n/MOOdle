

var ctx = document.getElementById('graph').getContext('2d');

/**/


console.log(chart_id)


//reaplace character encoding


//TODO use regex

const regex = /(\[\(|\)\]|&#39;| )/g
n_data = data.replace(regex, '')
console.log(n_data)
console.log(n_data.split(','))
chart_opt = {responsive: false};



/*
Id:
0 - Nombre de velages par jour
*/

switch(chart_id)
{
	case '0':
			break;

}


const labels = ["pouet"];

const _data = {
labels: labels,
datasets: [{
	label: 'My First Dataset',
	data: [65, 59, 80, 81, 56, 55, 40],
	fill: false,
	borderColor: 'rgb(75, 192, 192)',
	tension: 0.1
}]
};

const config = {
	type: 'line',
	data: _data,
  };

var myChart = new Chart(ctx, {
	type: 'line',   // le type du graphique
	options:chart_opt,
	data: _data,
});
console.log(n_data)
