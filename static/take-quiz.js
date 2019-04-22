for (let input of document.getElementsByTagName('input')) {
	input.addEventListener('input', (e) => {
		fetch('answer', {method: 'POST', body: new URLSearchParams(`answer=${input.value}`)});
	});
}

const eventSource = new EventSource('new-questions');
let oldScore = 0;
eventSource.addEventListener('message', (e) => {
	const {question: {question, answers}, score} = JSON.parse(e.data);
	if (oldScore !== score) {
		confettiShower(document.querySelector(':checked + label'));
		oldScore = score;
	}
	document.getElementById('question').textContent = question;
	const labels = document.getElementsByTagName('label');
	for (let i = 0; i < 4; i++) {
		labels[i].textContent = answers[i];
	}
	document.querySelector(':checked').checked = false;
	document.getElementById('score').textContent = score;
});
