import { initShaderProgram } from "./shader.js";
import { storeQuad, drawUVVertices } from "./shapes2d.js";

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
	gl.enable(gl.DEPTH_TEST); // Enable depth testing
	gl.depthFunc(gl.LEQUAL); // Near things obscure far things

	//
	// Create shaders
	// 
	const shaderProgram = initShaderProgram(gl, await (await fetch("uvTriangles.vs")).text(), await (await fetch("uvTriangles.fs")).text());

	// Load a texture and move it to the gpu
	gl.activeTexture(gl.TEXTURE0);
	gl.bindTexture(gl.TEXTURE_2D, loadTexture(gl, 'wall-4-granite-TEX.jpg'));
	gl.uniform1i(gl.getUniformLocation(shaderProgram, "uTexture0"), 0);

	gl.activeTexture(gl.TEXTURE1);
	gl.bindTexture(gl.TEXTURE_2D, loadTexture(gl, 'sandra512.jpg'));
	gl.uniform1i(gl.getUniformLocation(shaderProgram, "uTexture1"), 1);

	gl.activeTexture(gl.TEXTURE3);// Do we need this?

	//
	// Create content to display
	//

	const colorUniformLocation = gl.getUniformLocation(shaderProgram, "uColor");
	const theColor = [0, 0, 1, 1];
	gl.uniform4fv(
		colorUniformLocation,
		theColor
	);


	//
	// load a modelview matrix onto the shader
	// 
	const modelViewMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uModelViewMatrix");
	const identityMatrix = mat4.create();
	gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, identityMatrix);

	//
	// Register Listeners
	//



	//
	// Main render loop
	//
	let previousTime = 0;
	function redraw(currentTime) {
		currentTime *= .001; // milliseconds to seconds
		let DT = currentTime - previousTime;
		if (DT > .5)
			DT = .5;
		previousTime = currentTime;


		//
		// Setup projection matrix
		//
		setObservationView(gl, shaderProgram, canvas.clientWidth / canvas.clientHeight)


		//
		// Draw
		//
		gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

		const vertices = [];
		let H = 2;
		let u1 = 0; let v1 = H;
		let u2 = H; let v2 = H;
		let u3 = H; let v3 = 0;
		let u4 = 0; let v4 = 0;
		let i = 0; // index as to which texture map to use
		storeQuad(vertices,
			0, 0, 0, u1, v1, i,
			10, 0, 0, u2, v2, i,
			10, 10, 0, u3, v3, i,
			0, 10, 0, u4, v4, i);
		i = 2;
		storeQuad(vertices,
			11, 0, 0, u1, v1, i,
			21, 0, 0, u2, v2, i,
			21, 10, 0, u3, v3, i,
			11, 10, 0, u4, v4, i);
	
		drawUVVertices(gl, shaderProgram, vertices, gl.TRIANGLES);

		requestAnimationFrame(redraw);
	}
	requestAnimationFrame(redraw);
};


function setObservationView(gl, shaderProgram, canvasAspect) {
	const projectionMatrix = mat4.create();
	const fov = 90 * Math.PI / 180;
	const near = 1;
	const far = 1000;
	mat4.perspective(projectionMatrix, fov, canvasAspect, near, far);
	const WIDTH = 10;
	const HEIGHT = 10;
	const lookAtMatrix = mat4.create();
	mat4.lookAt(lookAtMatrix, [WIDTH / 2, -HEIGHT / 10, HEIGHT], [WIDTH / 2, HEIGHT / 2, 0], [0, 0, 1]);
	mat4.multiply(projectionMatrix, projectionMatrix, lookAtMatrix);

	const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
	gl.uniformMatrix4fv(projectionMatrixUniformLocation, false, projectionMatrix);
}


function loadTexture(gl, url) {
	const texture = gl.createTexture();
	gl.bindTexture(gl.TEXTURE_2D, texture);

	// Fill the texture with a 1x1 blue pixel while waiting for the image to load
	gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array([0, 0, 255, 255]));

	const image = new Image();
	image.onload = function () {
		gl.bindTexture(gl.TEXTURE_2D, texture);
		gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
		gl.generateMipmap(gl.TEXTURE_2D);
	};
	image.src = url;

	return texture;
}

