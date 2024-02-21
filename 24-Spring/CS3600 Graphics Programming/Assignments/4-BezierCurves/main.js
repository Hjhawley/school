import { initShaderProgram } from "./shader.js";
import { drawCircle, drawRectangle, drawTriangle, drawLineStrip } from "./shapes2d.js";
import { randomDouble } from "./random.js";

main();

let selectedPointIndex = -1; // Index of the selected control point, -1 if none
let selectedCurveIndex = -1; // Index of the selected Bezier curve, -1 if none
let curveOffset = 5; // Adjust

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
	const aspect = canvas.clientWidth / canvas.clientHeight;
	const projectionMatrix = mat4.create();
	let yhigh = 10;
	let ylow = -yhigh;
	let xlow = ylow;
	let xhigh = yhigh;
	if(aspect>=1){
		xlow *= aspect;
		xhigh *= aspect;
	}
	else{
		ylow /= aspect;
		yhigh /= aspect;
	}
	mat4.ortho(projectionMatrix, xlow, xhigh, ylow, yhigh, -1, 1);
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);

	//
	// load a modelview matrix onto the shader
	// 
	const modelViewMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uModelViewMatrix");
	const modelViewMatrix = mat4.create();
    gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, modelViewMatrix);

	//
	// Create content to display
	//
	class Point2 {
		constructor(x, y) {
		  this.x = x;
		  this.y = y;
		}
	  }
	  
	class Bezier {
		constructor(points) {
		  this.points = points; // An array of 4 Point2 objects
		  this.color = [randomDouble(0, 1), randomDouble(0, 1), randomDouble(0, 1), 1];
		}
	  
		evaluate(t) {
		  const p0 = this.points[0],
				p1 = this.points[1],
				p2 = this.points[2],
				p3 = this.points[3];
	  
		  const x = Math.pow(1 - t, 3) * p0.x +
					3 * Math.pow(1 - t, 2) * t * p1.x +
					3 * (1 - t) * Math.pow(t, 2) * p2.x +
					Math.pow(t, 3) * p3.x;
	  
		  const y = Math.pow(1 - t, 3) * p0.y +
					3 * Math.pow(1 - t, 2) * t * p1.y +
					3 * (1 - t) * Math.pow(t, 2) * p2.y +
					Math.pow(t, 3) * p3.y;
	  
		  return new Point2(x, y);
		}

		drawCurve(gl, shaderProgram) {
			const pointsForCurve = [];
			for (let i = 0; i <= 20; i++) {
				let t = i / 20;
				let p = this.evaluate(t);
				pointsForCurve.push(p.x, p.y);
			}
			drawLineStrip(gl, shaderProgram, pointsForCurve, this.color);
		}

		drawControlPoints(gl, shaderProgram) {
			this.points.forEach(point => {
			drawCircle(gl, shaderProgram, point.x, point.y, 0.2, this.color); // Red control points
			});
		}

		isPicked(x, y) {
			const pickingRadius = 0.5; // Adjust
			for (let i = 0; i < this.points.length; i++) {
				const dx = x - this.points[i].x;
				const dy = y - this.points[i].y;
				if (Math.sqrt(dx * dx + dy * dy) < pickingRadius) {
					return i;
				}
			}
			return -1;
		}

		setPoint(i, x, y) {
			if (i >= 0 && i < this.points.length) {
			this.points[i].x = x;
			this.points[i].y = y;
			}
		}
	  }
	
	let bezierCurves = [];

	bezierCurves.push(new Bezier([
        new Point2(-5, -5),
        new Point2(-2, 5),
        new Point2(2, -5),
        new Point2(5, 5)
    ]));

	/*
	addEventListener("click", click);
	function click(event) {
		console.log("click");
		const xWorld = xlow + event.clientX / gl.canvas.clientWidth * (xhigh - xlow);
		const yWorld = ylow + (gl.canvas.clientHeight - event.clientY) / gl.canvas.clientHeight * (yhigh - ylow);
		// Do whatever you want here, in World Coordinates.
	}*/

	canvas.addEventListener('mousedown', mousedown);
	function mousedown(event) {
		const rect = canvas.getBoundingClientRect();
		const xWorld = xlow + (event.clientX - rect.left) / canvas.clientWidth * (xhigh - xlow);
		const yWorld = yhigh - (event.clientY - rect.top) / canvas.clientHeight * (yhigh - ylow);
		selectedPointIndex = -1; // Reset to -1 before checking
		selectedCurveIndex = -1; // Reset to -1 before checking
		bezierCurves.forEach((curve, index) => {
			const pickedIndex = curve.isPicked(xWorld, yWorld);
			if (pickedIndex !== -1) {
				selectedCurveIndex = index;
				selectedPointIndex = pickedIndex;
			}
		});
	}    
	
	canvas.addEventListener('mousemove', mousemove);
	function mousemove(event) {
		if (selectedCurveIndex !== -1 && selectedPointIndex !== -1) {
			const rect = canvas.getBoundingClientRect();
			const xWorld = xlow + (event.clientX - rect.left) / canvas.clientWidth * (xhigh - xlow);
			const yWorld = yhigh - (event.clientY - rect.top) / canvas.clientHeight * (yhigh - ylow);
			bezierCurves[selectedCurveIndex].setPoint(selectedPointIndex, xWorld, yWorld);
		}
	}    
	
	canvas.addEventListener('mouseup', mouseup);
	function mouseup(event) {
		selectedCurveIndex = -1;
		selectedPointIndex = -1;
	}	

	function setupAddCurveButton() {
		const addButton = document.getElementById('addBezierCurve');
		addButton.addEventListener('click', () => {
			const newPoints = [
				new Point2(randomDouble(-curveOffset, curveOffset) - 5, randomDouble(-curveOffset, curveOffset) - 5),
            	new Point2(randomDouble(-curveOffset, curveOffset) - 2, randomDouble(-curveOffset, curveOffset) + 5),
            	new Point2(randomDouble(-curveOffset, curveOffset) + 2, randomDouble(-curveOffset, curveOffset) - 5),
            	new Point2(randomDouble(-curveOffset, curveOffset) + 5, randomDouble(-curveOffset, curveOffset) + 5)
			];
			const newCurve = new Bezier(newPoints);
			bezierCurves.push(newCurve);
		});
	}
	
	setupAddCurveButton();
	
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

		/*
		drawCircle(gl, shaderProgram, 5,5,1);
		drawRectangle(gl, shaderProgram, 0,0,2,1, [1,0,0,1]); // override the default color with red.
		drawTriangle(gl, shaderProgram, -1,0, -1,2, -2,3);
		drawLineStrip(gl, shaderProgram, [0,0,-1,-1,-2,-1])*/

		bezierCurves.forEach(curve => {
			curve.drawCurve(gl, shaderProgram);
			curve.drawControlPoints(gl, shaderProgram);
		});
		
		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};
