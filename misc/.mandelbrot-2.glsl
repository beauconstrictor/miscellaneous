#version 330 core

out vec4 fragColor;

uniform vec2 centre;
uniform float viewport;
uniform vec2 resolution;

const int   MAX_I     = 300;
const float THRESHOLD = 4.0;

void main() {
  vec2 p = gl_FragCoord.xy;
  vec2 c = centre + (p - 0.5 * resolution) / resolution.y * viewport;

  int  i = 0;
  vec2 z = vec2(0.0);

  while (i < MAX_I && dot(z, z) <= THRESHOLD) {
    z = vec2(z.x*z.x - z.y*z.y, 2.0 * z.x * z.y) + c;
    i++;
  }

  float log_zn = log(dot(z, z)) * 0.5;
  float nu = log(log_zn / log(2.0)) / log(2.0);
  float smooth_i = float(i) + 1.0 - nu;

  float col = smooth_i / float(MAX_I);

  fragColor = vec4(col, col, col, 1.0);
}
