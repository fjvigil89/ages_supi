# Odoo 14
# Backend SUPI mobile app

Conjunto de módulos para la gestión de las solicitudes desde la aplicación móvil SUPI

# Instalación

Descargar adddons desde el github, clonándolo en el servidor:


```bash
cd /Users/YourUser/supi
git clone https://github.com/fjvigil89/ages_supi.git
```

Localizar el fichero de configuración del Odoo en el servidor, normalmente en:

```bash
/Users/YourUser/.odoo14rc
```

Abrir fichero de configuración ejecutando:

```bash
nano /Users/YourUser/.odoo14rc
```

Añadir al fichero de configuración la ruta de los módulos previamente clonados, modificando el parámetro 

```bash
addons_path = .../odoo-14.0/addons,/Users/YourUser/supi
```

# Diagrama de clases del módulo supi_integration


![Image text](https://github.com/fjvigil89/ages_supi/tree/master/supi_docs/DER/diagrama1.png)
![Image text](https://github.com/fjvigil89/ages_supi/tree/master/supi_docs/DER/diagrama2.png)
![Image text](https://github.com/fjvigil89/ages_supi/tree/master/supi_docs/DER/diagrama3.png)
![Image text](https://github.com/fjvigil89/ages_supi/tree/master/supi_docs/DER/diagrama4.png)