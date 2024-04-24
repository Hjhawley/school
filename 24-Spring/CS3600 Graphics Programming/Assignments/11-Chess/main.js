import { initShaderProgram } from "./shader.js";
import { ChessSet } from "./chessSet.js";

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
	gl.enable(gl.DEPTH_TEST); // Enable depth testing
	gl.depthFunc(gl.LEQUAL); // Near things obscure far things
	gl.enable(gl.CULL_FACE);

	//
	// Setup keyboard events:
	//

	window.addEventListener("keydown", keyDown);
	function keyDown(event) {
	}
	window.addEventListener("keyup", keyUp);
	function keyUp(event) {
	}

	//
	// Create shader
	// 
	const shaderProgram = initShaderProgram(gl, await (await fetch("textureNormalTriangles.vs")).text(), await (await fetch("textureNormalTriangles.fs")).text());
	//	SetShaderAttributes(gl, shaderProgram);

	gl.activeTexture(gl.TEXTURE0);
	gl.uniform1i(gl.getUniformLocation(shaderProgram, "uTexture"), 0);
	// const blackTexture = loadTexture(gl, 'pieces/PiezasAjedrezDiffuseMarmolBlackBrighter.png', [80, 80, 80, 255]);
	// const whiteTexture = loadTexture(gl, 'pieces/PiezasAjedrezDiffuseMarmol.png', [220, 220, 220, 255]);
	// const boardTexture = loadTexture(gl, 'pieces/TableroDiffuse01.png', [255, 171, 0, 255]);


	//
	// load a modelview matrix and normatMatrixonto the shader
	// 
	const modelViewMatrix = mat4.create();
	gl.uniformMatrix4fv(gl.getUniformLocation(shaderProgram, "uModelViewMatrix"), false, modelViewMatrix);

	const normalMatrix = mat3.create();
	mat3.normalFromMat4(normalMatrix, modelViewMatrix);
	gl.uniformMatrix3fv(gl.getUniformLocation(shaderProgram, "uNormalMatrix"), false, normalMatrix);

	//
	// Other shader variables:
	// 
	function setLightDirection(x, y, z) {
		gl.uniform3fv(
			gl.getUniformLocation(shaderProgram, "uLightDirection"),
			[x, y, z]
		);
	}
	//setLightDirection(0, -1, -1);
	setLightDirection(1, -1, -1);

	const eye = [0, 10, -6];
	const at = [0, 0, 0];
	const up = [0, 1, 0];

	setObservationView(gl, shaderProgram, eye, at, up, canvas.clientWidth / canvas.clientHeight)


	//
	// Create content to display
	//

	const c = new ChessSet(gl);
	await c.init(gl);

	window.addEventListener("resize", reportWindowSize);
	function reportWindowSize() {
		const clarity = 1.0; // use 4.0 for better looking textures
		gl.canvas.width = gl.canvas.clientWidth * clarity;
		gl.canvas.height = gl.canvas.clientHeight * clarity;
		gl.viewport(0, 0, gl.canvas.width, gl.canvas.height);
	}
	reportWindowSize();

	//
	// Main render loop
	//
	let previousTime = 0;
	let frameCounter = 0;
	function redraw(currentTime) {
		currentTime *= .001; // milliseconds to seconds
		let DT = currentTime - previousTime;
		if (DT > .5)
			DT = .5;
		frameCounter += 1;
		if (Math.floor(currentTime) != Math.floor(previousTime)) {
			console.log(frameCounter);
			frameCounter = 0;
		}
		previousTime = currentTime;

		//
		// Draw
		//
		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
		setObservationView(gl, shaderProgram, eye, at, up, canvas.clientWidth / canvas.clientHeight)

		c.draw(gl, shaderProgram, currentTime);

		//s.draw(gl, shaderProgram);

		//g.draw(gl, shaderProgram);

		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};

function setObservationView(gl, shaderProgram, eye, at, up, canvasAspect) {
	const projectionMatrix = mat4.create();
	const fov = 60 * Math.PI / 180;
	const near = 1;
	const far = 100;
	mat4.perspective(projectionMatrix, fov, canvasAspect, near, far);

	const lookAtMatrix = mat4.create();
	mat4.lookAt(lookAtMatrix, eye, at, up);
	mat4.multiply(projectionMatrix, projectionMatrix, lookAtMatrix);

	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);

	gl.uniform3fv(
		gl.getUniformLocation(shaderProgram, "uEyePosition"),
		eye
	);
}

