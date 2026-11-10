# Examen Parcial 2 - Manejo Masivo de Datos (Big Data)

- **Alumno:** Axel Vladimir Arteaga Salvador
- **Matricula:** 125053083
- **Pregunta Asignada:** 3 - Ticket promedio (ingreso promedio por registro) por tienda.

## Pasos para reproducir
1. Clona el repositorio y colocate en la carpeta del proyecto.
2. Genera el dataset localmente con tu matricula (no se sube al repositorio):
   python3 generar_dataset.py 125053083
3. Levanta toda la infraestructura con un solo comando:
   docker compose up --build -d
4. Ejecuta el Job de Hadoop Streaming:
   docker exec -it hadoop bash -c "cd /data/mapreduce && rm -rf output && time hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-*.jar -input /data/input/ventas_125053083.csv -output /data/mapreduce/output -mapper mapper.py -reducer reducer.py -file mapper.py -file reducer.py"
5. Carga los resultados a la base de datos PostgreSQL:
   docker exec -it api python3 /data/scripts/cargar_resultados.py

## Comparativa de Rendimiento (Parte C2)
- **Hadoop MapReduce:** 24.015s
- **Script Secuencial en Python:** 8.917s
- **Explicacion:** En este escenario con un archivo de ~400 MB (5 millones de registros), el script secuencial fue mas rapido porque lee los datos directamente en un solo proceso sin sobrecarga. Hadoop MapReduce incursiona en latencia de inicializacion de la JVM, levantamiento de contenedores/tareas, serializacion por tuberias estandar (Hadoop Streaming) y ordenamiento en disco (shuffle/spill), lo cual solo se amortiza cuando se manejan decenas de gigabytes o terabytes distribuidos en multiples nodos.

## Verificaciones y Evidencias
- **Hadoop Version:** Hadoop 3.3.6 (ver captura en evidencias/).
- **SSH sin contrasena:** Configurado con llaves RSA en authorized_keys tanto para ssh localhost dentro de hadoop como para ssh usuario@hadoop desde api.
- **Persistencia:** Comprobada ejecutando docker compose down y docker compose up -d, manteniendo los registros intactos en el volumen nombrado pgdata.
- **API Endpoints:**
  - GET http://localhost:8000/resultados
  - GET http://localhost:8000/resultados/T01
  - POST http://localhost:8000/resultados
  - DELETE http://localhost:8000/resultados/{id}

## Parte E - Teoria
1. **Diferencia entre modos de Hadoop y uso de HDFS:** Standalone corre en un solo proceso Java local sin demonios distribuidos; pseudo-distribuido simula un cluster en una sola maquina ejecutando cada demonio de Hadoop en procesos separados; totalmente distribuido reparte el almacenamiento y computo en multiples nodos fisicos/virtuales. HDFS se utiliza en los modos pseudo-distribuido y totalmente distribuido.
2. **Montaje del dataset como volumen vs COPY:** Primero, evita inflar el tamano de la imagen Docker con 400 MB de datos estaticos, acelerando el build y el despliegue. Segundo, desacopla los datos del codigo, permitiendo cambiar o actualizar el archivo CSV sin tener que reconstruir la imagen.
3. **docker compose down vs docker compose down -v:** Con docker compose down se detienen y eliminan los contenedores y redes, pero los datos persisten porque el volumen nombrado (pgdata) se conserva. Con docker compose down -v se eliminan tambien los volumenes, borrando por completo la base de datos.
4. **Por que MapReduce no siempre es mas rapido en 400 MB:** Por el overhead (tiempo de arranque de JVM, creacion de splits, fase de shuffle/sort y escritura intermedia en disco). Conviene usar MapReduce cuando el volumen de datos supera la memoria RAM disponible de una sola maquina (decenas de GB o TB) y se requiere paralelismo horizontal en varios nodos.
5. **CMD vs ENTRYPOINT y COPY vs ADD:** CMD define el comando o parametros por defecto que pueden sobrescribirse facilmente al ejecutar docker run, mientras que ENTRYPOINT fija el ejecutable principal del contenedor. COPY simplemente copia archivos/carpetas locales al contenedor, mientras que ADD ademas permite extraer archivos comprimidos (.tar) automaticamente y descargar archivos desde URLs.
