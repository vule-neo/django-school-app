let star1 = document.getElementById("star-1");
let star2 = document.getElementById("star-2");
let star3 = document.getElementById("star-3");
let star4 = document.getElementById("star-4");
let star5 = document.getElementById("star-5");

star1.addEventListener("click", addOne);
star2.addEventListener("click", addTwo);
star3.addEventListener("click", addThree);
star4.addEventListener("click", addFour);
star5.addEventListener("click", addFive);

let context = {"oneStar": 0, "twoStar": 0, "threeStar": 0, "fourStar": 0, "fiveStar": 0}

function calculateRating() {
	let points = context["oneStar"] + context["twoStar"]*2 + context["threeStar"]*3 + context["fourStar"]*4 + context["fiveStar"]*5
	let numOfVotes = context["oneStar"] + context["twoStar"] + context["threeStar"] + context["fourStar"] + context["fiveStar"]
	let finalRating = points / numOfVotes;
	finalRating = Math.floor(finalRating*100) / 100;

	let ratingElement = document.getElementById("rating").innerText = finalRating;
}

function addOne(){
	context["oneStar"]++;
	calculateRating();
	return context["oneStar"];
}
function addTwo(){
	context["twoStar"]++;
	calculateRating();
	return context["twoStar"];
}
function addThree(){
	context["threeStar"]++;
	calculateRating();
	return context["threeStar"];
}
function addFour(){
	context["fourStar"]++;
	calculateRating();
	return context["fourStar"];
}
function addFive(){
	context["fiveStar"]++;
	calculateRating();
	return context["fiveStar"];
}