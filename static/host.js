document.getElementById('qr').src = QRCode.generatePNG(new URL('login', document.location).toString());

function updateStats(responseCounts) {
	let totalResponses = 0;
	for (let i = 0; i < 4; i++) {
		totalResponses += responseCounts[i];
	}
	for (let i = 0; i < 4; i++) {
		document.querySelector(`.answer.n${i+1} > .bar`).style.height = `${responseCounts[i] / totalResponses * 100}%`;
	}
	document.getElementById('responses').textContent = totalResponses;
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

addEventListener('keydown', (e) => {
	if (e.key === 'q') {
		document.body.classList.toggle('qrInvisible');
	} else if (e.key === 's') {
		document.body.classList.toggle('statsInvisible');
	} else if (e.key === 'l') {
		document.body.classList.toggle('leaderboardInvisible');
	}
});

updateStats([2, 17, 0, 1]);
updateLeaderboard([
	["This", 100],
	["is", 50],
	["a", 30],
	["test", 0],
]);
