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
	gl.clearColor(0.04, 0.51, 0.51, 1.0);
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
	let zoomLevel = 1.0;
	const zoomSpeed = 0.1;

	addEventListener("click", click);
	function click(event) {
		console.log("click");
		const xWorld = xlow + event.offsetX / gl.canvas.clientWidth * (xhigh - xlow);
		const yWorld = ylow + (gl.canvas.clientHeight - event.offsetY) / gl.canvas.clientHeight * (yhigh - ylow);
		// Do whatever you want here, in World Coordinates.
	}

	addEventListener("mousewheel", mousewheel);
	function mousewheel(event) {
		console.log("mousewheel");
		// Determine the direction of the scroll (up or down)
		const direction = event.deltaY < 0 ? 1 : -1;

		// Adjust the zoom level
		zoomLevel *= 1.0 + direction * zoomSpeed;
		zoomLevel = Math.max(0.1, Math.min(100, zoomLevel)); // clamp the zoom level to prevent inverting the view or zooming too far

		// Adjust projection bounds based on the new zoom level
		const width = (xhigh - xlow) / zoomLevel;
		const height = (yhigh - ylow) / zoomLevel;
		const centerX = (xlow + xhigh) / 2;
		const centerY = (ylow + yhigh) / 2;

		xlow = centerX - width / 2;
		xhigh = centerX + width / 2;
		ylow = centerY - height / 2;
		yhigh = centerY + height / 2;

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

