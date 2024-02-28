import { initShaderProgram } from "./shader.js";
import { drawCircle, drawRectangle, drawTriangle, drawLineStrip } from "./shapes2d.js";
import { randomDouble } from "./random.js";
import { Maze} from "./maze.js";

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
	// Create content to display
	//
	const WIDTH = 5;
	const HEIGHT = 4;
	const m = new Maze(WIDTH, HEIGHT);
	
	//
	// load a projection matrix onto the shader
	// 
	const margin = 0.5;
	let xlow = 0.0-margin;
	let xhigh = WIDTH+margin;
	let ylow = 0.0-margin;
	let yhigh = HEIGHT+margin;

	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	const projectionMatrix = mat4.create();
	const aspect = canvas.clientWidth / canvas.clientHeight;
	const width = xhigh-xlow;
	const height = yhigh-ylow;
	if(aspect >= width/height){
		const newWidth = aspect*height;
		const xmid = (xlow+xhigh)/2;
		const xLowNew = xmid - newWidth/2;
		const xhighNew = xmid + newWidth/2;
		mat4.ortho(projectionMatrix, xLowNew, xhighNew, ylow, yhigh, -1, 1);
	}
	
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);

	//
	// load a modelview matrix onto the shader
	// 
	const modelViewMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uModelViewMatrix");
	const modelViewMatrix = mat4.create();
    gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, modelViewMatrix);

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

		m.draw(gl, shaderProgram);
		
		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};

