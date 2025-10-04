#include <iostream>
#include <cmath>
#include <functional>
using namespace std;

double integral(std::function<double(double)> P, double x0, double x1, int steps=1000){
    double dx = (x1 - x0)/steps;
    double area = 0;
    for(int i=0;i<steps;i++){
        double xi = x0 + i*dx;
        area += P(xi)*dx;
    }
    return area;
}

void ABSM_Grudge_Machine(double x0, double n0, double n1, std::function<double(double)> P, double &x1, double &D){
    x1 = x0;
    double Q = integral(P, x0, x1);
    double n_mean = (n0+n1)/2;
    double n = n_mean + Q;
    x1 = (n*x0 + n1 - n0)/n;
    D = (n*x1+n0) - (n*x0+n1);
}

int main(){
    double x1, D;
    ABSM_Grudge_Machine(5, 0.1, 0.2, [](double x){ return sin(x); }, x1, D);
    std::cout << "x1 = " << x1 << ", D = " << D << std::endl;
}