import { initShaderProgram } from "./shader.js";
import { drawCircle, drawRectangle, drawTriangle, drawLineStrip } from "./shapes2d.js";
import { randomDouble } from "./random.js";

main();
async function main() {
	console.log('This is working');

	//
	// start gl
	// 
	const canvas = document.getElementById('glcanvas');
	const gl = canvas.getContext('webgl');
	if (!gl) {
		alert('Your browser does not support WebGL');
	}
	gl.clearColor(0.75, 0.85, 0.8, 1.0);
	gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

	//
	// Create shaders
	// 
	const vertexShaderText = await(await fetch("simple.vs")).text();
	const fragmentShaderText = await(await fetch("simple.fs")).text();
	const shaderProgram = initShaderProgram(gl, vertexShaderText, fragmentShaderText);

	//
	// load a projection matrix onto the shader
	// 
	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	const projectionMatrix = mat4.create();
	let ylow = -1.5;
	let yhigh = 1.5;
	let xlow = -2.5;
	let xhigh = .5;
	mat4.ortho(projectionMatrix, xlow, xhigh, ylow, yhigh, -1, 1);
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);


	//
	// Create content to display
	//


	//
	// Register Listeners
	//
	addEventListener("click", click);
	function click(event) {
		console.log("click");
		const xWorld = xlow + event.offsetX / gl.canvas.clientWidth * (xhigh - xlow);
		const yWorld = ylow + (gl.canvas.clientHeight - event.offsetY) / gl.canvas.clientHeight * (yhigh - ylow);
		// Do whatever you want here, in World Coordinates.
	}

	addEventListener("mousewheel", mousewheel);
	let zoomLevel = 1.0; // Initial zoom level
	const zoomSpeed = 0.1; // Speed of zoom

	function mousewheel(event) {
		event.preventDefault(); // Prevent default scrolling behavior

		// Determine zoom direction
		let direction;
		if (event.deltaY < 0) {
			direction = 1;
		} else {
			direction = -1;
		}

		// Adjust zoom level
		zoomLevel *= (1 + direction * zoomSpeed);
		zoomLevel = Math.max(0.1, Math.min(10, zoomLevel)); // Clamp zoom level

		const centerX = xlow + (xhigh - xlow) / 2;
		const centerY = ylow + (yhigh - ylow) / 2;
		
		// Update projection bounds based on new zoom level
		// This example assumes zoom affects both x and y axis equally
		const aspectRatio = (xhigh - xlow) / (yhigh - ylow);
		const zoomWidth = (2.5 + 0.5) / zoomLevel;
		const zoomHeight = zoomWidth / aspectRatio;

		// After calculating new zoomWidth and zoomHeight
		xlow = centerX - zoomWidth / 2;
		xhigh = centerX + zoomWidth / 2;
		ylow = centerY - zoomHeight / 2;
		yhigh = centerY + zoomHeight / 2;


		// Update the projection matrix
		mat4.ortho(projectionMatrix, xlow, xhigh, ylow, yhigh, -1, 1);
		gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);
	}

	//
	// Main render loop
	//
	let previousTime = 0;
	function redraw(currentTime){
		currentTime *= .001; // milliseconds to seconds
		let DT = currentTime - previousTime;
		if(DT > .1)
			DT = .1;
		previousTime = currentTime;

		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

		drawRectangle(gl, shaderProgram, xlow, ylow, xhigh, yhigh, [1,0,0,1]); // override the default color with red.
		
		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};

