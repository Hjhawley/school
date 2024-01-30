// Import Circle class and shader initialization function
import { Circle } from "./circle.js";
import { initShaderProgram } from "./shader.js";

async function main() {
    const canvas = document.getElementById('glcanvas');
    const gl = canvas.getContext('webgl');

    if (!gl) {
        alert('Your browser does not support WebGL');
        return;
    }

    // Load shaders
    const vertexShaderText = await (await fetch("simple.vs")).text();
    const fragmentShaderText = await (await fetch("simple.fs")).text();
    const shaderProgram = initShaderProgram(gl, vertexShaderText, fragmentShaderText);

    // Use the shader program
    gl.useProgram(shaderProgram);

    // Set up projection matrix uniform
    const projectionMatrixUniformLocation = gl.getUniformLocation(shaderProgram, "uProjectionMatrix");
    // ... [Code to set up the projection matrix] ...

    // Initialize circles
    const numCircles = 10;
    const circles = [];
    for (let i = 0; i < numCircles; i++) {
        circles.push(new Circle(gl, shaderProgram));
    }

    // Animation loop
    function drawScene() {
        gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

        circles.forEach(circle => {
            circle.update(); // Update circle position based on velocity
            circle.draw(); // Draw the circle
        });

        requestAnimationFrame(drawScene);
    }

    drawScene();
}

window.onload = main;
