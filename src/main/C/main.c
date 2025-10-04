#include <stdio.h>
#include <math.h>

double P_sine(double x) { return sin(x); }
double P_linear(double x) { return x; }
double P_tanh(double x) { return tanh(x); }
double P_relu(double x) { return x > 0 ? x : 0; }
double P_gaussian(double x, double sigma) { return exp(-x*x/(2*sigma*sigma)); }

double integral(double (*P)(double), double x0, double x1, int steps) {
    double dx = (x1 - x0)/steps;
    double area = 0;
    for(int i=0;i<steps;i++){
        double xi = x0 + i*dx;
        area += P(xi)*dx;
    }
    return area;
}

void ABSM_Grudge_Machine(double x0, double n0, double n1, double (*P)(double), double* x1, double* D) {
    *x1 = x0;
    double Q = integral(P, x0, *x1, 1000);
    double n_mean = (n0 + n1)/2;
    double n = n_mean + Q;
    *x1 = (n*x0 + n1 - n0)/n;
    *D = (n*(*x1)+n0) - (n*x0+n1);
}

int main() {
    double x1, D;
    ABSM_Grudge_Machine(5, 0.1, 0.2, P_sine, &x1, &D);
    printf("x1 = %lf, D = %lf\n", x1, D);
    return 0;
}