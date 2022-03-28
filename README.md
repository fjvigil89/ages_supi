# Odoo 14
# Backend SUPI mobile app

Conjunto de módulos para la gestión de las solicitudes desde la aplicación móvil SUPI, que se describen a continuación:

```bash
muk_web_theme: Tema del backend
supi_docs: Conjunto de datos entregados por el cliente para modelación de la arquitectura del sistema
odoo-rest-api: Módulo que habilita las llamadas REST-API en el Odoo para el manejo de funcionalidades en la app móvil
supi_integration: Módulo que contiene la lógica inicial de declaración de modelos en la base de datos.
```



# Instalación del código en el servidor

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

```bash
Reiniciar la instancia del Odoo
```

# Instalación de las apps en la web

Pasos para instalación:

```bash
1- Activar modo desarrollador: Ajustes/Herramientas de desarrollador/ Activar modo desarrollador
2- Menú Aplicaciones/Actualizar lista de aplicaciones/ Actualizar
3- Refrescar la vista del navegador
4- Instalar los 2 módulos que a continuación se muestra
```
![Image text](https://github.com/fjvigil89/ages_supi/blob/master/supi_docs/install_apps.png)



# Diagrama de clases del módulo supi_integration


![Relacion de los modelos Users,Photos,PhotoUpload,Clientes,Quiz, Variables y parametros](https://github.com/fjvigil89/ages_supi/blob/master/supi_docs/DER/diagrama1.png)
![Image text](https://github.com/fjvigil89/ages_supi/blob/master/supi_docs/DER/diagrama2.png)
![Image text](https://github.com/fjvigil89/ages_supi/blob/master/supi_docs/DER/diagrama3.png)
![Image text](https://github.com/fjvigil89/ages_supi/blob/master/supi_docs/DER/diagrama4.png)

## Tecnologías empleadas

* [Odoo](https://www.odoo.com): Version 14


### Autor
Ronny Montano
- [Email: rmontano1992@gmail.com](mailto:rmontano1992@gmail.com?subject=Hi% "Hi!")