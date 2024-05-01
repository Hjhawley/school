import { collideParticles } from "./collisions.js";
class Circle{
    constructor(color, x, y, dx, dy, size){
        this.color = color;
        this.size = size;
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.size = size;
    }

    nextx(DT){
        return this.x + this.dx*DT;
    }    
    nexty(DT){
        return this.y + this.dy*DT;
    }

    update0(gravity){
        this.dx += gravity[0];
        this.dy += gravity[1];

        // Air friction:
        const AIR_FRICTION = 0.99;
        this.dx *= AIR_FRICTION;
        this.dy *= AIR_FRICTION;
    }

    update1(DT, xlow, xhigh, ylow, yhigh, circleList, me){        
        const FLOOR_FRICTION = 0.99; // To stop it from "vibrating" on the floor
        // ball-wall
        if (this.x+this.dx*DT+this.size > xhigh)
            this.dx = -Math.abs(this.dx);
        if (this.x+this.dx*DT-this.size < xlow)
            this.dx = Math.abs(this.dx);
        if (this.y+this.dy*DT+this.size > yhigh)
            this.dy = -Math.abs(this.dy);
        if (this.y+this.dy*DT-this.size < ylow)
            this.dy = Math.abs(this.dy)*FLOOR_FRICTION;

        // ball-ball
        const r1 = this.size;
        for(let j=me+1; j<circleList.length; j++){
            const nextx1 = this.x+this.dx*DT;
            const nexty1 = this.y + this.dy*DT;
            const nextx2 = circleList[j].x + circleList[j].dx*DT;
            const nexty2 = circleList[j].y + circleList[j].dy*DT;
            const r2 = circleList[j].size;
            const distance = (nextx2-nextx1)**2 + (nexty2-nexty1)**2;
            if (distance < (r1+r2)**2 && this.color == circleList[j].color){ // Check if colors are the same
                const COLLISION_FRICTION = 0.85;
                collideParticles(this, circleList[j], DT, COLLISION_FRICTION);
            }
        }
    }

    update2(DT){
        this.x += this.dx*DT;
        this.y += this.dy*DT;
    }

    draw(gl, shaderProgram){
        drawCircle(gl, shaderProgram, this.color, this.x, this.y, this.size);
    }
    
}

function drawCircle(gl, shaderProgram, color, x, y, size){
    const sides = 64;
    const vertices = CreateCircleVertices(sides);

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
    gl.uniformMatrix4fv(modelViewMatrixUniformLocation, false, modelViewMatrix);

    // Starts the Shader Program, which draws one frame to the screen.
    gl.drawArrays(gl.TRIANGLE_FAN, 0, sides+2);
}

function CreateCircleVertices(sides){
	const positions = [];
	positions.push(0);
	positions.push(0);
	for(let i=0; i<sides+1; i++){
		const radians = i/sides *2*Math.PI;
		const x= Math.cos(radians);
		const y= Math.sin(radians);
		positions.push(x);
		positions.push(y);
	}
	return positions;
}

export {drawCircle, Circle};