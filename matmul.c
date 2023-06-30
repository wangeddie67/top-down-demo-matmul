
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define M 2048
#define N 2048
#define K 2048

int main()
{
  float* left  ;
  float* right ;
  float* result;

  left = (float*)malloc(M*K*sizeof(float));
  right= (float*)malloc(K*N*sizeof(float));
  result=(float*)malloc(M*N*sizeof(float));

  int mi = 0;
  int ni = 0;
  int ki = 0;

  for (mi = 0; mi < M; mi ++)
  {
    for (ni = 0; ni < N; ni ++)
    {
      for (ki = 0; ki < K; ki ++)
      {
        result[mi * N + ni] = result[mi * N + ni] + left[mi * K + ki] * right[ki * N + ni];
      }
    }
  }

  return result[0];
}
