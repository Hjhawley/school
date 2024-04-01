precision mediump float;

attribute vec3 vertPosition;
attribute vec2 vertUV;
uniform mat4 uModelViewMatrix;
uniform mat4 uProjectionMatrix;
varying vec2 fragUV;

void main() {
    fragUV = vertUV;
    gl_Position = uProjectionMatrix * uModelViewMatrix * vec4(vertPosition, 1.0);
}
