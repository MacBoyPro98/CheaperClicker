for (let input of document.getElementsByTagName('input')) {
	input.addEventListener('input', (e) => {
		fetch('answer', {method: 'POST', body: new URLSearchParams(`answer=${input.value}`)});
	});
}

const eventSource = new EventSource('new-questions');
let oldQuestion, oldAnswers = [], oldScore = 0;
eventSource.addEventListener('message', (e) => {
	const {question: {question, answers}, score} = JSON.parse(e.data);
	if (oldQuestion === question
		&& oldAnswers[0] === answers[0]
		&& oldAnswers[1] === answers[1]
		&& oldAnswers[2] === answers[2]
		&& oldAnswers[3] === answers[3]
		&& oldScore === score) {
		return;
	}
	const checkedAnswer = document.querySelector(':checked');
	if (checkedAnswer && oldScore !== score) {
		confettiShower(document.querySelector(':checked + label'));
	}
	oldQuestion = question;
	oldAnswers = answers;
	oldScore = score;
	document.getElementById('question').textContent = question;
	const labels = document.getElementsByTagName('label');
	for (let i = 0; i < 4; i++) {
		labels[i].textContent = answers[i];
	}
	if (checkedAnswer) {
		checkedAnswer.checked = false;
	}
	document.getElementById('score').textContent = score;
});
