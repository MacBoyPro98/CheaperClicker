for (let input of document.getElementsByTagName('input')) {
	input.addEventListener('input', (e) => {
		fetch('answer', {method: 'POST', body: new URLSearchParams(`answer=${input.value}`)});
	});
}
