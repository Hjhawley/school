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