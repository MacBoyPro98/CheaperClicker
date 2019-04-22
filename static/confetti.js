// https://www.jacobwinters.com/website-confetti/
// This file released under CC0

const particleDiv = document.createElement("div");
Object.assign(particleDiv.style, {
	position: "fixed",
	top: "0", left: "0",
	height: "100%", width: "100%",
	pointerEvents: "none",
});
document.body.appendChild(particleDiv);

let animating = false;

let particles = [];

function spawnParticle(x, y){
	const element = document.createElement("div");
	particleDiv.appendChild(element);
	const height = 5 + Math.random() * 5,
	      width = 5 + Math.random() * 5;
	Object.assign(element.style, {
		position: "absolute",
		height: `${height}px`, width: `${width}px`,
		backgroundColor: `hsl(${Math.random() * 360}, 100%, 50%)`,
		transformOrigin: "center",
	});
	const time = performance.now();
	const particle = {
		ix: x - width / 2, iy: y - height / 2, // Initial position
		ivx: Math.random() * 2 - 1, ivy: Math.random() * -3, // Initial velocity in px/frame
		theta: Math.random() * Math.PI * 2,
		element: element,
		spawnTime: time,
	};
	updateParticle(time)(particle);
	particles.push(particle);
	if(!animating) {
		requestAnimationFrame(updateParticles);
		animating = true;
	}
}

let updateParticle = (time) => (particle) => {
	const age = (time - particle.spawnTime) * 60 / 1000; // Age in frames assuming 60fps
	if(age > 100) {
		particle.element.remove();
		return false;
	}
	const x = particle.ix + particle.ivx * age,
	      y = particle.iy + particle.ivy * age + .075 * age * age;
	particle.element.style.transform = `translateX(${x - scrollX}px) translateY(${y - scrollY}px) rotate(${particle.theta}rad)`;
	return true;
}

function updateParticles(time) {
	particles = particles.filter(updateParticle(time));
	if(!particles.length) {
		animating = false;
	} else {
		requestAnimationFrame(updateParticles);
	}
}

function confettiShower(element) {
	const {left: clientLeft, right: clientRight, top: clientTop} = element.getBoundingClientRect();
	const left = clientLeft + scrollX, right = clientRight + scrollX, top = clientTop + scrollY;
	const steps = ~~((right - left) / 20);
	for(let i = 0; i <= steps; i++) {
		spawnParticle(left + (right - left) * (i / steps), top);
	}
}
