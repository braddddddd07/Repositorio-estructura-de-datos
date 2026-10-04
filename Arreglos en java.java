import java.util.Scanner;

public class Main {

    private static final String[] MESES = {
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    };

    private static final String[] DEPARTAMENTOS = {"Ropa", "Deportes", "Juguetería"};

    private double[][] matriz;

    // Constructor renombrado a Main
    public Main() {
        this.matriz = new double[12][3];
    }

    public void insertarVenta(String mes, String departamento, double monto) {
        int fila = obtenerIndice(MESES, mes);
        int col = obtenerIndice(DEPARTAMENTOS, departamento);

        if (fila != -1 && col != -1) {
            matriz[fila][col] = monto;
            System.out.printf("[OK] Venta de $%.2f registrada en '%s' para '%s'.\n", monto, DEPARTAMENTOS[col], MESES[fila]);
        } else {
            System.out.println("[ERROR] Mes o departamento no válido.");
        }
    }

    public void buscarElemento(String departamento) {
        int col = obtenerIndice(DEPARTAMENTOS, departamento);

        if (col != -1) {
            System.out.printf("\n--- Ventas registradas para '%s' (Enero - Diciembre) ---\n", DEPARTAMENTOS[col]);
            for (int i = 0; i < MESES.length; i++) {
                System.out.printf(" - %-12s: $%.2f\n", MESES[i], matriz[i][col]);
            }
            System.out.println("-------------------------------------------------------\n");
        } else {
            System.out.println("[ERROR] Departamento no válido.");
        }
    }

    public void eliminarVenta(String mes, String departamento) {
        int fila = obtenerIndice(MESES, mes);
        int col = obtenerIndice(DEPARTAMENTOS, departamento);

        if (fila != -1 && col != -1) {
            matriz[fila][col] = 0.0;
            System.out.printf("[OK] Venta de '%s' en '%s' restablecida a $0.00.\n", DEPARTAMENTOS[col], MESES[fila]);
        } else {
            System.out.println("[ERROR] Mes o departamento no válido.");
        }
    }

    private int obtenerIndice(String[] arreglo, String valor) {
        for (int i = 0; i < arreglo.length; i++) {
            if (arreglo[i].equalsIgnoreCase(valor)) {
                return i;
            }
        }
        return -1;
    }

    public void mostrarMatriz() {
        System.out.println("\n=======================================================");
        System.out.printf("%-12s | %-10s | %-10s | %-10s\n", "Mes", DEPARTAMENTOS[0], DEPARTAMENTOS[1], DEPARTAMENTOS[2]);
        System.out.println("-------------------------------------------------------");
        for (int i = 0; i < MESES.length; i++) {
            System.out.printf("%-12s | $%-9.2f | $%-9.2f | $%-9.2f\n", 
                MESES[i], matriz[i][0], matriz[i][1], matriz[i][2]);
        }
        System.out.println("=======================================================\n");
    }

    public static void main(String[] args) {
        // Instancia actualizada a Main
        Main app = new Main();
        Scanner scanner = new Scanner(System.in);
        boolean ejecucion = true;

        while (ejecucion) {
            System.out.println("\n--- MENÚ DE COMANDOS ---");
            System.out.println(" 1. Insertar venta");
            System.out.println(" 2. Eliminar venta");
            System.out.println(" 3. Buscar elemento");
            System.out.println(" 4. Mostrar matriz");
            System.out.println(" 5. Salir");
            System.out.print("\nEscriba el comando o número a ejecutar: ");

            String comando = scanner.nextLine().trim();

            if (comando.equalsIgnoreCase("1") || comando.equalsIgnoreCase("Insertar venta") || comando.equalsIgnoreCase("Insertar")) {
                boolean continuar = true;
                while (continuar) {
                    System.out.print("Ingrese el mes (ej. Enero): ");
                    String mes = scanner.nextLine().trim();

                    System.out.print("Ingrese el departamento (Ropa, Deportes, Juguetería): ");
                    String dep = scanner.nextLine().trim();

                    System.out.print("Ingrese el monto de la venta: ");
                    try {
                        double monto = Double.parseDouble(scanner.nextLine().trim());
                        app.insertarVenta(mes, dep, monto);
                    } catch (NumberFormatException e) {
                        System.out.println("[ERROR] El monto debe ser un número válido.");
                    }

                    System.out.print("\n¿Desea ingresar otra venta? (s/n): ");
                    String resp = scanner.nextLine().trim();
                    if (!resp.equalsIgnoreCase("s")) {
                        continuar = false;
                    }
                }

            } else if (comando.equalsIgnoreCase("2") || comando.equalsIgnoreCase("Eliminar venta")) {
                System.out.print("Ingrese el mes de la venta a eliminar: ");
                String mes = scanner.nextLine().trim();

                System.out.print("Ingrese el departamento (Ropa, Deportes, Juguetería): ");
                String dep = scanner.nextLine().trim();

                app.eliminarVenta(mes, dep);

            } else if (comando.equalsIgnoreCase("3") || comando.equalsIgnoreCase("Buscar elemento")) {
                System.out.print("Ingrese el departamento a buscar (Ropa, Deportes, Juguetería): ");
                String dep = scanner.nextLine().trim();

                app.buscarElemento(dep);

            } else if (comando.equalsIgnoreCase("4") || comando.equalsIgnoreCase("Mostrar matriz") || comando.equalsIgnoreCase("Mostrar")) {
                app.mostrarMatriz();

            } else if (comando.equalsIgnoreCase("5") || comando.equalsIgnoreCase("Salir")) {
                System.out.println("Programa finalizado.");
                ejecucion = false;

            } else {
                System.out.println("[ERROR] Comando no reconocido.");
            }
        }

        scanner.close();
    }
}