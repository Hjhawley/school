import { initShaderProgram } from "./shader.js";
import { Circle } from "./circle.js";
import { randomDouble, myRandom } from "./random.js";
main();
async function main() {
	console.log('This is working');

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
	let shaderProgram = initShaderProgram(gl, vertexShaderText, fragmentShaderText);

	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	const aspect = canvas.clientWidth / canvas.clientHeight;
	const projectionMatrix = mat4.create();
	const yhigh = 10;
	const ylow = -yhigh;
	const xlow = ylow * aspect;
	const xhigh = yhigh * aspect;
	mat4.ortho(projectionMatrix, xlow, xhigh, ylow, yhigh, -1, 1);
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);

	const NUM_CIRCLES = 7;
	const circleList = [];
	let tries = 0;
	while(circleList.length<NUM_CIRCLES && tries < 10000){
		tries += 1;
		const size=randomDouble(1,2);
		const x=randomDouble(xlow+size, xhigh-size);
		const y=randomDouble(ylow+size, yhigh-size);
		AddNewCircle(x,y,size);
	}

	function AddNewCircle(x,y,size){
		const color = [myRandom(), myRandom(), myRandom(), 1];
		let dx = randomDouble(1,3);
		let dy = randomDouble(1,3);
		if (myRandom()>.5)
			dx = -dx;
		if (myRandom()>.5)
			dy = -dy;
		const c = new Circle(color, x, y, dx, dy, size);
		let intersect = false;
		for(let i=0; i<circleList.length; i++){
			const distance = (x-circleList[i].x)**2 + (y-circleList[i].y)**2;
			if (distance < (size+circleList[i].size)**2){
				intersect = true;
				console.log("intersects");
			}
		}
		if (!intersect){
			circleList.push(c)
		}
	}

	//
	// Main render loop
	//
	let previousTime = 0;
	function redraw(currentTime){
		currentTime *= .001; // milliseconds to seconds
		let DT = currentTime - previousTime;
		previousTime = currentTime;
		if(DT > .1)
			DT = .1;

		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

		for(let i=0; i<circleList.length; i++){
			circleList[i].update0();
		}
		for(let reps=0; reps<circleList.length; reps++){
			for(let i=0; i<circleList.length; i++){
				circleList[i].update1(DT, xlow, xhigh, ylow, yhigh, circleList, i);
			}
		}
		for(let i=0; i<circleList.length; i++){
			circleList[i].update2(DT);
		}

		for(let i=0; i<circleList.length; i++){
			circleList[i].draw(gl, shaderProgram);
		}
		
		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};

