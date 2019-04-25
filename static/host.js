document.getElementById('qr').src = QRCode.generatePNG(new URL('login', document.location).toString());


function updateStats(responseCounts) {
	let totalResponses = 0;
	for (let i = 0; i < 4; i++) {
		totalResponses += responseCounts[i];
	}
	for (let i = 0; i < 4; i++) {
		document.querySelector(`.answer.n${i+1} > .bar`).style.height = totalResponses === 0 ? '0' : `${responseCounts[i] / totalResponses * 100}%`;
	}
	document.getElementById('responses').textContent = totalResponses;
}

const eventSource = new EventSource('answer-stats');
eventSource.addEventListener('message', (e) => {
	const responseCounts = JSON.parse(e.data);
	updateStats(responseCounts);
});


function updateQuestion({question, answers}) {
	document.getElementById('question').textContent = question;
	for (let i = 0; i < 4; i++) {
		document.querySelector(`.answer.n${i+1} > .answer-text`).textContent = answers[i];
	}
}

function updateLeaderboard(entries) {
	const tbody = document.createElement('tbody');
	for (let entry of entries) {
		const tr = document.createElement('tr');

		const nameTd = document.createElement('td');
		nameTd.textContent = entry[0];
		tr.appendChild(nameTd);

		const scoreTd = document.createElement('td');
		scoreTd.textContent = entry[1];
		tr.appendChild(scoreTd);

		tbody.appendChild(tr);
	}
	const oldTbody = document.querySelector('#leaderboard tbody');
	oldTbody.parentNode.replaceChild(tbody, oldTbody);
}

async function nextQuestion() {
	const response = await fetch('next-question', {method: 'POST'});
	const {question, leaderboard} = await response.json();
	updateQuestion(question);
	updateLeaderboard(leaderboard);
}


addEventListener('keydown', (e) => {
	if (e.key === 'n') {
		nextQuestion();
	} else if (e.key === 'q') {
		document.body.classList.toggle('qrInvisible');
	} else if (e.key === 's') {
		document.body.classList.toggle('statsInvisible');
	} else if (e.key === 'l') {
		document.body.classList.toggle('leaderboardInvisible');
	}
});
