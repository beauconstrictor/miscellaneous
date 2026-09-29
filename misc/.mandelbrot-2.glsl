#version 330 core

out     vec4  fragColor;

uniform vec2  centre;
uniform float viewport;
uniform vec2  parameter;
uniform float parameter2;
uniform vec2  resolution;
uniform bool  mandelbrot;

const   int   MAX_I     = 300;
const   float THRESHOLD = 100.0;
const   vec3  TINT = vec3(7, 1, 1);

void main() {
  vec2 p = gl_FragCoord.xy;
  vec2 coord = centre + (p - 0.5 * resolution) / resolution.y * viewport;

  int  i = 0;
  vec2 z = mandelbrot ? parameter : coord;
  vec2 c = mandelbrot ? coord : parameter;

  while (i < MAX_I && dot(z, z) <= THRESHOLD) {
    float r = length(z);
    float theta = atan(z.y, z.x);
    z = pow(r, parameter2) * vec2(cos(parameter2 * theta), sin(parameter2  * theta)) + c;

    i++;
  }

  float log_zn = log(dot(z, z)) * 0.5;
  float nu = log(log_zn / log(2.0)) / log(2.0);
  float smooth_i = float(i) + 1.0 - nu;

  float col = smooth_i / float(MAX_I);

  fragColor = vec4(col*TINT.r, col*TINT.g, col*TINT.b, 1.0);
}
