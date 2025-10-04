public class ABSM {
    public static double integral(java.util.function.Function<Double, Double> P, double x0, double x1, int steps){
        double dx = (x1 - x0)/steps;
        double area = 0;
        for(int i=0;i<steps;i++){
            double xi = x0 + i*dx;
            area += P.apply(xi)*dx;
        }
        return area;
    }

    public static double[] ABSM_Grudge_Machine(double x0, double n0, double n1, java.util.function.Function<Double, Double> P){
        double x1 = x0;
        double Q = integral(P, x0, x1, 1000);
        double n_mean = (n0+n1)/2;
        double n = n_mean + Q;
        x1 = (n*x0 + n1 - n0)/n;
        double D = (n*x1+n0) - (n*x0+n1);
        return new double[]{x1,D};
    }

    public static void main(String[] args){
        double[] res = ABSM_Grudge_Machine(5,0.1,0.2, Math::sin);
        System.out.println("x1 = "+res[0]+", D = "+res[1]);
    }
}