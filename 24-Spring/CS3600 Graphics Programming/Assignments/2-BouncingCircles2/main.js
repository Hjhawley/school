import { Circle } from "./circle.js";
import { initShaderProgram } from "./shader.js";
import { collideParticles } from "./collisions.js";

main();
async function main() {
	console.log('This is working');

	//
	// Constants for physics
	//
	const gravity = -10;
	const airFriction = 0.005;
	const collisionFriction = 0.995; // Less than 1 to slow down

	//
	// Init gl
	// 
	const canvas = document.getElementById('glcanvas');
	const gl = canvas.getContext('webgl');

	if (!gl) {
		alert('Your browser does not support WebGL');
	}

	gl.clearColor(0.75, 0.85, 0.8, 1.0);
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

	//
	// Create shaderProgram
	// 
	const vertexShaderText = await (await fetch("simple.vs")).text();
    const fragmentShaderText = await (await fetch("simple.fs")).text();
	let shaderProgram = initShaderProgram(gl, vertexShaderText, fragmentShaderText);
	gl.useProgram(shaderProgram);


	//
	// Set Uniform uProjectionMatrix
	//	
	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	const aspect = canvas.clientWidth / canvas.clientHeight;
	const projectionMatrix = mat4.create();
	const yhigh = 10;
	const ylow = -yhigh;
	const xlow = ylow * aspect;
	const xhigh = yhigh * aspect;
	mat4.ortho(projectionMatrix, xlow, xhigh, ylow, yhigh, -1, 1);
	gl.uniformMatrix4fv(
		projectionMatrixUniformLocation,
		false,
		projectionMatrix
	);

	//
	// Create the objects in the scene:
	//
	const NUM_CIRCLES = 7;
	const circleList = [];
	for (let i = 0; i < NUM_CIRCLES; i++) {
		let overlap, r;
		do {
			overlap = false;
			r = new Circle(xlow, xhigh, ylow, yhigh);
			
			// Check for overlap with existing circles
			for (let j = 0; j < circleList.length; j++) {
				if (isColliding(r, circleList[j])) {
					overlap = true;
					break; 	// Exit the for loop, there's an overlap
				}
			}
			
		} while (overlap); 	// Repeat if we found an overlap
		circleList.push(r); // No overlap found, add the circle to the list
	}

	function isColliding(circle1, circle2) {
		const dx = circle1.x - circle2.x;
		const dy = circle1.y - circle2.y;
		const distance = Math.sqrt(dx * dx + dy * dy);
		return distance < (circle1.size + circle2.size);
	}

	//
	// Main render loop
	//
	let previousTime = 0;
	function redraw(currentTime) {
		currentTime *= 0.001;
		let DT = currentTime - previousTime;
		previousTime = currentTime;
		if(DT > .1){
			DT = .1;
		}
	  
		// Apply gravity and air friction
		circleList.forEach(circle => {
		  circle.dy += gravity * DT; // Gravity
		  circle.dx *= 1 - airFriction; // Air friction
		  circle.dy *= 1 - airFriction;
		});
	  
		// Detect and resolve collisions
		for (let i = 0; i < NUM_CIRCLES - 1; i++) {
		  for (let j = i + 1; j < NUM_CIRCLES; j++) {
			if (isColliding(circleList[i], circleList[j])) {
			  collideParticles(circleList[i], circleList[j], DT, collisionFriction);
			}
		  }
		}
	  
		// Clear the canvas before we start drawing on it.
		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

		// Update the scene
		for (let i = 0; i < NUM_CIRCLES; i++) {
			circleList[i].update(DT, gravity, airFriction);
		}

		// Draw the scene
		for (let i = 0; i < NUM_CIRCLES; i++) {
			circleList[i].draw(gl, shaderProgram);
		}
	  
		requestAnimationFrame(redraw);
	  }

	  requestAnimationFrame(redraw);
};

