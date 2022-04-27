let chartForm = document.getElementById("chart");

let raceForm = document.getElementById("race")
let PourcentageForm = document.getElementById("percentage")
let familleForm = document.getElementById("family")

if (chartForm.value === 3) {
	raceForm.removeAttribute("hidden");
	PourcentageForm.removeAttribute("hidden");
	familleForm.setAttribute("hidden", "");
} else {
	raceForm.setAttribute("hidden", "");
	PourcentageForm.setAttribute("hidden", "");
	familleForm.removeAttribute("hidden", "");


}
