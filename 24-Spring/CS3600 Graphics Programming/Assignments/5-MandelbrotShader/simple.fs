precision highp float;
uniform vec4 uColor;
varying vec2 fragPosition;

const int MAX_ITER = 1000;

int MandelbrotTest(float cr, float ci)
{
    int count = 0;

    float zr = 0.;
    float zi = 0.;
    float zrsqr = 0.;
    float zisqr = 0.;

    for (int i=0; i<MAX_ITER; i++){
      zi = zr * zi;
      zi += zi;
      zi += ci;
      zr = zrsqr - zisqr + cr;
      zrsqr = zr * zr;
      zisqr = zi * zi;
		
      //the fewer iterations it takes to diverge, the farther from the set
      if (zrsqr + zisqr > 4.0) 
        break;
      count++;
    }

    return count;
}

void main() {
    int count = MandelbrotTest(fragPosition[0], fragPosition[1]);
    float t = float(count) / float(MAX_ITER); // Normalized iteration count

    // Interpolate between colors based on the normalized iteration count
    if (count == MAX_ITER) {
        gl_FragColor = vec4(0., 0., 0., 1.); // Black for points inside the set
    } else if (t < 0.1) {
        gl_FragColor = mix(vec4(1.0, 0.0, 0.0, 1.0), vec4(1.0, 0.5, 0.0, 1.0), t / 0.1);
    } else if (t < 0.2) {
        gl_FragColor = mix(vec4(1.0, 0.5, 0.0, 1.0), vec4(1.0, 1.0, 0.0, 1.0), (t - 0.1) / 0.1);
    } else if (t < 0.3) {
    gl_FragColor = mix(vec4(0.5, 1.0, 0.0, 1.0), vec4(0.0, 1.0, 0.5, 1.0), (t - 0.2) / 0.1);
    } else if (t < 0.4) {
        gl_FragColor = mix(vec4(0.0, 1.0, 0.5, 1.0), vec4(0.0, 1.0, 1.0, 1.0), (t - 0.3) / 0.1);
    } else if (t < 0.5) {
        gl_FragColor = mix(vec4(0.0, 1.0, 1.0, 1.0), vec4(0.0, 0.5, 1.0, 1.0), (t - 0.4) / 0.1);
    } else if (t < 0.6) {
        gl_FragColor = mix(vec4(0.0, 0.5, 1.0, 1.0), vec4(0.0, 0.0, 1.0, 1.0), (t - 0.5) / 0.1);
    } else if (t < 0.7) {
        gl_FragColor = mix(vec4(0.0, 0.0, 1.0, 1.0), vec4(0.5, 0.0, 1.0, 1.0), (t - 0.6) / 0.1);
    } else if (t < 0.8) {
        gl_FragColor = mix(vec4(0.5, 0.0, 1.0, 1.0), vec4(1.0, 0.0, 1.0, 1.0), (t - 0.7) / 0.1);
    } else if (t < 0.9) {
        gl_FragColor = mix(vec4(1.0, 0.0, 1.0, 1.0), vec4(1.0, 0.0, 0.5, 1.0), (t - 0.8) / 0.1);
    } else {
        gl_FragColor = mix(vec4(1.0, 0.0, 0.5, 1.0), vec4(1.0, 0.0, 0.0, 1.0), (t - 0.9) / 0.1);
    }
}
