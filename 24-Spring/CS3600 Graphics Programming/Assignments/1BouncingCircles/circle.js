class Circle {
    constructor(gl, shaderProgram) {
        this.gl = gl;
        this.shaderProgram = shaderProgram;

        // Define properties
        this.position = { x: Math.random() * 2 - 1, y: Math.random() * 2 - 1 }; // Random position
        this.velocity = { x: Math.random() * 0.01 - 0.005, y: Math.random() * 0.01 - 0.005 }; // Random velocity
        this.radius = Math.random() * 0.1 + 0.05; // Random radius between 0.05 and 0.15
        this.color = [Math.random(), Math.random(), Math.random(), 1.0]; // Random color

        // Initialize the vertex buffer
        this.vertexBuffer = this.gl.createBuffer();
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexBuffer);
        const vertices = this.createCircleVertices(64); // Use 64 vertices to approximate the circle
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);

        // Get attribute and uniform locations
        this.positionAttribLocation = this.gl.getAttribLocation(this.shaderProgram, 'vertPosition');
        this.colorUniformLocation = this.gl.getUniformLocation(this.shaderProgram, 'uColor');
    }

    createCircleVertices(numSides) {
        const vertices = [];
        for (let i = 0; i <= numSides; i++) {
            let angle = i * 2 * Math.PI / numSides;
            let x = this.radius * Math.cos(angle);
            let y = this.radius * Math.sin(angle);
            vertices.push(x + this.position.x, y + this.position.y);
        }
        return vertices;
    }

    update() {
        // Update circle position based on velocity
        this.position.x += this.velocity.x;
        this.position.y += this.velocity.y;

        // Simple collision detection with boundaries
        if (this.position.x + this.radius > 1 || this.position.x - this.radius < -1) {
            this.velocity.x *= -1;
        }
        if (this.position.y + this.radius > 1 || this.position.y - this.radius < -1) {
            this.velocity.y *= -1;
        }

        // Update the vertex buffer data
        const vertices = this.createCircleVertices(64);
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexBuffer);
        this.gl.bufferData(this.gl.ARRAY_BUFFER, new Float32Array(vertices), this.gl.STATIC_DRAW);
    }

    draw() {
        // Bind the vertex buffer
        this.gl.bindBuffer(this.gl.ARRAY_BUFFER, this.vertexBuffer);
        this.gl.vertexAttribPointer(this.positionAttribLocation, 2, this.gl.FLOAT, false, 0, 0);
        this.gl.enableVertexAttribArray(this.positionAttribLocation);

        // Set the color uniform
        this.gl.uniform4fv(this.colorUniformLocation, this.color);

        // Draw the circle
        this.gl.drawArrays(this.gl.TRIANGLE_FAN, 0, 65); // 64 vertices + 1 for the loop closure
    }
}

export { Circle, drawCircle };