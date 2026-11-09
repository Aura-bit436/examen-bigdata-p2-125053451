# Examen Parcial 2 – Manejo Masivo de Datos

## 1. Datos del proyecto

- **Matrícula:** 125053451
- **Tema:** Procesamiento masivo de datos con Hadoop Streaming.
- **Pregunta de negocio:** ¿Cuál es el ingreso total (cantidad × precio_unitario) por categoría y mes?

## 2. Objetivo

Procesar un conjunto de datos de ventas de 5 millones de registros para calcular el ingreso total por categoría y mes, utilizando Hadoop Streaming y Python secuencial. Posteriormente, almacenar los resultados en PostgreSQL y consultarlos mediante una API REST.

## 3. Tecnologías utilizadas

- Docker y Docker Compose.
- Hadoop 3.3.6.
- Python 3.
- Hadoop Streaming.
- PostgreSQL 16.
- Flask.
- OpenSSH.
- PowerShell.

## 4. Estructura del proyecto

- `api/`: aplicación Flask y configuración.
- `hadoop/`: Dockerfile de Hadoop.
- `mapreduce/`: Mapper, Reducer y resultados.
- `scripts/`: procesamiento secuencial y carga a PostgreSQL.
- `docker-compose.yml`: configuración de los servicios.
- `generar_dataset.py`: generación del conjunto de datos.
- `ventas_125053451.csv`: datos de ventas.

## 5. Procesamiento de datos

Se utilizó Hadoop Streaming con dos programas:

- **Mapper:** lee los registros, obtiene la categoría y el mes, y calcula el ingreso de cada venta multiplicando la cantidad por el precio unitario.
- **Reducer:** agrupa los ingresos por categoría y mes y calcula el total correspondiente.

Se implementó también un procesamiento secuencial en Python para comparar los resultados.

## 6. Comparación y validación

El conjunto de datos contiene 5,000,000 de registros.

Los resultados de Hadoop y Python se compararon mediante `Compare-Object`. No se encontraron diferencias, por lo que ambos métodos produjeron resultados idénticos.

### 6.1 Tiempos de ejecución

| Método | Tiempo de ejecución |
|---|---:|
| Python secuencial | 18.57 segundos |
| Hadoop Streaming | 58.34 segundos |

En esta prueba, Python secuencial presentó un menor tiempo de ejecución. Hadoop Streaming tuvo mayor tiempo debido a la sobrecarga de inicialización y ejecución del framework en modo local. Sin embargo, ambos métodos generaron resultados idénticos.

## 7. Base de datos y API REST

Los resultados se almacenaron en PostgreSQL. Se insertaron 120 registros correspondientes a las categorías y los meses procesados.

La API desarrollada con Flask permite realizar las siguientes operaciones:

- GET: consultar todos los resultados.
- GET por clave: consultar un resultado específico.
- POST: agregar un resultado.
- PUT: actualizar un resultado.
- DELETE: eliminar un resultado.

## 8. Persistencia

Se configuró un volumen nombrado de Docker para PostgreSQL. Se comprobó que los 120 registros permanecieron almacenados después de ejecutar `docker compose down` y volver a iniciar los servicios.

## 9. Ejecución del proyecto

Para construir e iniciar los servicios:

```powershell
docker compose up --build -d
```

Para consultar el estado de los contenedores:

```powershell
docker compose ps
```

Para consultar los resultados mediante la API:

```powershell
Invoke-RestMethod -Uri http://localhost:5000/resultados
```

Para detener los servicios:

```powershell
docker compose down
```
## Defensa oral

### 10. Cambiar el puerto de la API

En `docker-compose.yml`, dentro del servicio `api`, modificar:

```yaml
ports:
  - "5000:5000"
```

Por ejemplo, cambiarlo a:

```yaml
ports:
  - "5001:5000"
```

Guardar y ejecutar:

```powershell
docker compose up -d --build api
```

Comprobar el acceso:

```powershell
Invoke-RestMethod http://localhost:5001/resultados
```

**Comprobación:** La API debe responder desde el nuevo puerto.

### 10.1. Modificar Mapper o Reducer

Se puede modificar la agregación para calcular el promedio en lugar de la suma o agregar un filtro por mes.

Archivos involucrados:
- `mapreduce/mapper.py`
- `mapreduce/reducer.py`

Para cambiar la suma por promedio, el Reducer debe acumular los ingresos y contar los registros de cada categoría y mes. Al finalizar, divide el total entre la cantidad de registros.

Después de guardar los cambios, ejecutar nuevamente el trabajo Hadoop Streaming utilizando el comando de procesamiento documentado anteriormente.

**Comprobación:** El archivo `part-00000` debe mostrar los nuevos resultados.

### 10.2. Eliminar el volumen y recargar la base de datos

Para demostrar que los resultados pueden cargarse nuevamente:

```powershell
docker compose down -v
```

Levantar los servicios:

```powershell
docker compose up -d --build
```

Copiar el archivo de resultados y el script de carga:

```powershell
docker compose cp .\mapreduce\part-00000 api:/tmp/part-00000
docker compose cp .\scripts\cargar_resultados.py api:/tmp/cargar_resultados.py
```

Ejecutar la carga:

```powershell
docker compose exec api python /tmp/cargar_resultados.py
```

Verificar los registros:

```powershell
docker compose exec db psql -U admin -d examen_bigdata -c "SELECT COUNT(*) FROM resultados;"
```

**Comprobación:** Deben aparecer nuevamente los 120 registros.

**Nota:** El comando `docker compose down -v` elimina el volumen y los datos anteriores de PostgreSQL.

### 10.3. Explicación de Dockerfile y Docker Compose

- **Dockerfile de Hadoop:** instalación y configuración de Java, Hadoop, Python y SSH.
- **Dockerfile de API:** instalación de Python, dependencias y cliente SSH.
- **docker-compose.yml:** configuración de los servicios Hadoop, PostgreSQL y API.
- **Puertos:** permiten acceder a los servicios desde el equipo.
- **Volumen:** conserva los datos de PostgreSQL.
- **Red:** permite la comunicación entre los contenedores.
- **depends_on:** establece la dependencia entre los servicios.

**Nota:** El archivo CSV y las credenciales deben mantenerse fuera del repositorio público cuando corresponda.