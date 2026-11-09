# Teoría

### 1. Modos de ejecución de Hadoop

**Standalone:** Hadoop funciona en una sola máquina, sin utilizar HDFS ni procesamiento distribuido.  
**Pseudo-distribuido:** los servicios de Hadoop se ejecutan en una sola máquina como procesos independientes y utiliza HDFS.  
**Totalmente distribuido:** Hadoop trabaja en varias máquinas conectadas, distribuyendo el almacenamiento y procesamiento mediante HDFS.  
HDFS se utiliza en los modos pseudo-distribuido y totalmente distribuido.

### 2. ¿Por qué montar el dataset como volumen y no copiarlo con `COPY`?

Montar el dataset como volumen permite modificar o reemplazar el archivo sin reconstruir la imagen Docker.  
También evita aumentar el tamaño de la imagen y permite compartir los datos entre el equipo y el contenedor.

### 3. Diferencia entre `docker compose down` y `docker compose down -v`

`docker compose down` elimina los contenedores y la red, pero conserva los volúmenes, por lo que los datos de la base de datos permanecen.  
En cambio, `docker compose down -v` también elimina los volúmenes asociados, provocando la pérdida de los datos almacenados en ellos.

### 4. ¿Por qué MapReduce no siempre es más rápido que un script secuencial?

MapReduce necesita tiempo adicional para iniciar procesos, distribuir tareas, ordenar y combinar datos.  
Por eso, con un archivo de 400 MB, un script secuencial puede ser más rápido.  
MapReduce conviene cuando se manejan grandes volúmenes de información, se dispone de varios nodos y el trabajo puede distribuirse.

### 5. Diferencia entre `CMD` y `ENTRYPOINT`, y entre `COPY` y `ADD`

`CMD` establece el comando o los argumentos predeterminados del contenedor, mientras que `ENTRYPOINT` define el ejecutable principal.  
`COPY` copia archivos hacia la imagen Docker.  
`ADD` también copia archivos, pero ofrece funciones adicionales, como extraer archivos comprimidos locales.