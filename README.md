
# Sistema de gestión de inventario para pequeñas empresas (SGIPE)
Integracion de servicos de AWS con proyecto en C# como DEMO de proyecto final de la asignatura Cloud Computing.


## Servicios integrados
1. DynamoDB: Tabla donde se almacenan los datos en formato JSON
2. AWS Lambda: Servicio serverless donde se ejecutan  acciones y lógicas en función de la petición recibida por API GATEWAY.
3. API Gateway: Se encarga de recibir el archivo JSON y el tipo de HTTP Request (PUT, GET, DELETE). Para posteriormente ejecutar la integracion con Lambda.
4. C#: Lenguaje de programación base, donde se encuentra el formulario para ejecutar las acciones CRUD. 
## Funcionamiento

El usuario encontrará un formulario con los campos:
"IdProducto"
"Descripcion"
"Estado"
"Existencias"
"Nombre"
"PrecioCompra"
"PrecioVenta"
y con botones: "Buscar", "Guardar", "Eliminar"

1. Para guardar un registro:
Diligencia los datos en las casillas correspondientes y haga click en el boton "Guardar".

2. Para actualizar un registro:
Digite en el campo "IdProducto" el identificador del producto y actualice los campos deseados, finalmente haga click en el boton "Guardar".

3. Para eliminar un registro:
Debe de digitar en "IdProducto" el identificador del producto y luego pulsar el boton "Eliminar".

4. Para consultar un registro:
En la casilla de destinada a las busquedas, digite el "IdProducto" y de click en "Buscar".

5. Para consultar todos los registros:
Haga click en el botón "Buscar" sin haber diligenciado ningún campo.