function main() {
    const canvas = document.getElementById("webgl-canvas");
    const gl = canvas.getContext("webgl");

    if (!gl) {
        alert("Unable to initialize WebGL.");
        return;
    }

    function Circle() {
        this.position = {
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height
        };
        this.velocity = {
            x: (Math.random() - 0.5) * 2, // Random velocity between -1 and 1
            y: (Math.random() - 0.5) * 2
        };
        this.radius = Math.random() * 20 + 5; // Random radius between 5 and 25
        this.color = [Math.random(), Math.random(), Math.random(), 1.0];
    }

    Circle.prototype.draw = function() {
        // Set up WebGL to draw this circle, e.g., set uniforms, bind buffers
        // ...
        gl.drawArrays(gl.TRIANGLE_FAN, 0, circleVertexCount);
    };

    Circle.prototype.update = function() {
        // Update circle position based on velocity
        // Check and handle collisions with canvas boundaries
        // ...
    };
    
    function update() {
        // Animation logic
        requestAnimationFrame(update);
        // Update each circle's position and handle collisions
    
        // Clear the canvas
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
        
        // Draw each circle
        circles.forEach(circle => {
            circle.update();
            circle.draw();
        });
    }
    
    // Initialize circles
    const numberOfCircles = 7;
    const circles = [];
    for (let i = 0; i < numberOfCircles; i++) {
        circles.push(new Circle());
    }

    update(); // Start the animation loop
}

window.onload = main;
