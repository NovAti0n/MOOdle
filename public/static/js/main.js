var ctx = document.getElementById('graph').getContext('2d');

/**/





var myChart = new Chart(ctx, {
	type: 'bar',   // le type du graphique
	options:{responsive: false},
	data: {        // les données
        labels: ['Jean', 'Martine', 'Michel', 'Jules', 'Louise', 'Dominique'],
        datasets: [{
                    label: 'votes',
                    data: [12, 19, 3, 5, 2, 3]
                   }]
	       }
         }
	);

console.log("teste lalalal")
