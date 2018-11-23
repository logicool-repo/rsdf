#include <stdio.h>
#include <math.h>

float calculateRSD(float data[]);

int main()
{
    float data[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    printf("Relative Standard Deviation = %.6f\n", calculateRSD(data));

    return 0;
}

float calculateRSD(float data[])
{
    float sum0 = 0.0, sum1 = 0.0, mean, mean_sq, rel_std = 0.0;

    int i;
    for(i=0; i<9; ++i)
    {
        sum0 += data[i];
        sum1 += pow(data[i], 2);
    }

    mean = sum0/9;
    mean_sq = sum1/9;

    rel_std = sqrt(mean_sq - pow(mean, 2))/mean;
    return rel_std;
}