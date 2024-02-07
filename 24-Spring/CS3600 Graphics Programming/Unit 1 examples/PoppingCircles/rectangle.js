class Rectangle{
    constructor(color, degrees, x, y, dx, dy, size){
        this.color = color;
        this.degrees = degrees;
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.size = size;
    }

    update(DT, xlow, xhigh, ylow, yhigh){
        const degreesPerSecond = 0;
        this.degrees += degreesPerSecond*DT;

        if (this.x+this.dx*DT+this.size > xhigh)
            this.dx = -this.dx;
        if (this.x+this.dx*DT-this.size < xlow)
            this.dx = -this.dx;
        if (this.y+this.dy*DT+this.size > yhigh)
            this.dy = -this.dy;
        if (this.y+this.dy*DT-this.size < ylow)
            this.dy = -this.dy;

        this.x += this.dx*DT;
        this.y += this.dy*DT;
    }
    draw(gl, shaderProgram){
        drawRectangle(gl, shaderProgram, this.color, this.degrees, this.x, this.y, this.size);
    }
    
}

function drawRectangle(gl, shaderProgram, color, degrees, x, y, size){
    const vertices = CreateSquareVertices();

    const vertexBufferObject = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, vertexBufferObject);
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(vertices), gl.STATIC_DRAW);

	const positionAttribLocation = gl.getAttribLocation(shaderProgram, 'vertPosition');
	gl.vertexAttribPointer(
		positionAttribLocation, // Attribute location
		2, // Number of elements per attribute
		gl.FLOAT, // Type of elements
		gl.FALSE,
		2 * Float32Array.BYTES_PER_ELEMENT, // Size of an individual vertex
		0 // Offset from the beginning of a single vertex to this attribute
	);
	gl.enableVertexAttribArray(positionAttribLocation);


	const colorUniformLocation = gl.getUniformLocation(shaderProgram, "uColor");
	gl.uniform4fv(colorUniformLocation, color);

	const modelViewMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uModelViewMatrix");
	const modelViewMatrix = mat4.create();
    mat4.translate(modelViewMatrix, modelViewMatrix, [x,y,0]);
    mat4.scale(modelViewMatrix, modelViewMatrix, [size, size, 1])
    mat4.rotate(modelViewMatrix, modelViewMatrix, (degrees*Math.PI/180), [0,0,1]);
    gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, modelViewMatrix);

    // Starts the Shader Program, which draws one frame to the screen.
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
}

function CreateSquareVertices(){
	const positions = [-1,1, -1,-1, +1,+1, +1,-1];
	return positions;
}

export {drawRectangle, Rectangle};