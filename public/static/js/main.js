

var ctx = document.getElementById('graph').getContext('2d');

/**/


console.log(chart_id)


//reaplace character encoding


//TODO use regex

const regex = /(\[\(|\)\]|&#39;| |\)|\()/g
n_data = data.replace(regex, '')
n_data = n_data.split(',')
chart_opt = {responsive: false};

let  labels = [];
let chart_data = []

/*
Id:
0 - Nombre de velages par jour
1 -
2 -
3 -
*/

switch(chart_id)
{
	case '0':
		for(var i = 0 ; i < n_data.length;i+=2)
		{
			labels.push(n_data[i])
			chart_data.push(parseInt(n_data[i+1]))
		}
		break;

}




const _data = {
labels: labels,
datasets: [{
	label: 'Nombre de vêlages par jour sur une période',
	data: chart_data,
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
