import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Productos')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    http_method = event.get('requestContext', {}).get('http', {}).get('method')
    path_parameters = event.get('pathParameters')
    
    if http_method == 'GET':
        if path_parameters and 'id' in path_parameters:
            return get_producto_by_id(path_parameters['id'])
        return get_all_productos()
    elif http_method == 'PUT':
        return handle_put(event)
    elif http_method == 'DELETE':
        if path_parameters and 'id' in path_parameters:
            return handle_delete(path_parameters['id'])
    
    return {
        'statusCode': 400,
        'body': json.dumps({'message': 'Método no soportado'})
    }

def get_producto_by_id(producto_id):
    try:
        # Intentamos primero como string
        response = table.get_item(
            Key={
                'IdProducto': str(producto_id)  # Convertimos a string
            }
        )
        
        item = response.get('Item')
        
        # Si no encontramos con string, intentamos con número
        if not item:
            try:
                response = table.get_item(
                    Key={
                        'IdProducto': int(producto_id)  # Convertimos a número
                    }
                )
                item = response.get('Item')
            except (ValueError, TypeError):
                # Si no se puede convertir a número, ignoramos este intento
                pass
        
        if item:
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps(item, cls=DecimalEncoder)
            }
        else:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': f'Producto con ID {producto_id} no encontrado'
                })
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Error al obtener el producto',
                'error': str(e)
            })
        }

def get_all_productos():
    try:
        response = table.scan()
        items = response.get('Items', [])
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(items, cls=DecimalEncoder)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Error al obtener los productos',
                'error': str(e)
            })
        }

def handle_put(event):
    """
    Actualiza un registro existente o inserta uno nuevo.
    """
    data = json.loads(event.get('body', '{}'))
    if not data.get('IdProducto'):
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "IdProducto es requerido"})
        }

    # Verificar si el producto ya existe
    existing_item = table.get_item(Key={'IdProducto': data['IdProducto']})

    if 'Item' in existing_item:
        # Actualizar los campos existentes
        update_expression = "SET "
        expression_attributes = {}

        for key, value in data.items():
            if key != "IdProducto":
                update_expression += f"{key} = :{key}, "
                expression_attributes[f":{key}"] = value

        # Eliminar la coma al final
        update_expression = update_expression.rstrip(", ")

        # Ejecutar la actualización
        table.update_item(
            Key={'IdProducto': data['IdProducto']},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attributes
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Producto actualizado con éxito"})
        }
    else:
        # Insertar un nuevo producto si no existe
        if 'FechaRegistro' not in data:
            data['FechaRegistro'] = datetime.utcnow().isoformat()

        table.put_item(Item=data)

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Producto insertado con éxito"})
        }

def handle_delete(producto_id):
    try:
        # Primero verificamos si el producto existe
        response = table.get_item(
            Key={
                'IdProducto': str(producto_id)
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': f'No se encontró el producto con ID: {producto_id}'
                })
            }
        
        # Si el producto existe, lo eliminamos
        table.delete_item(
            Key={
                'IdProducto': str(producto_id)
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': f'Producto con ID {producto_id} eliminado exitosamente'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Error al eliminar el producto',
                'error': str(e)
            })
        }