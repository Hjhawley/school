/**
 * Creates and compiles a shader.
 *
 * @param {WebGLRenderingContext} gl - The WebGL context.
 * @param {number} type - The type of the shader (gl.VERTEX_SHADER or gl.FRAGMENT_SHADER).
 * @param {string} source - The GLSL source code for the shader.
 * @return {WebGLShader} The compiled shader.
 */
function loadShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  // Check if shader compiled successfully
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
      alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
      gl.deleteShader(shader);
      return null;
  }

  return shader;
}

/**
* Initializes a shader program by linking a vertex and a fragment shader.
*
* @param {WebGLRenderingContext} gl - The WebGL context.
* @param {string} vertexShaderSource - The GLSL source code for the vertex shader.
* @param {string} fragmentShaderSource - The GLSL source code for the fragment shader.
* @return {WebGLProgram} The shader program.
*/
function initShaderProgram(gl, vertexShaderSource, fragmentShaderSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  // Create the shader program
  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // Check if program was linked successfully
  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
      alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
      return null;
  }

  return shaderProgram;
}

export { initShaderProgram };
