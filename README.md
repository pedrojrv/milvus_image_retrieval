# Installing Milvus

On Mac, it is unsupported to make directories in the `/home` folder. I changed it to a personally made folder in `/Users/pedrovicentevaldez/Desktop/milvus`. Additionally, I had to change docker preferences to allow for 4gb of memory access. 

The docker run options used in the above command are defined as follows:
- `-d`: Runs container in the background and prints container ID.
- `--name`: Assigns a name to the container.
- `-p`: Publishes a container’s port(s) to the host.
- `-v`: Mounts the directory into the container.


```bash
docker run -d --name milvus_cpu_1.0.0 \
-p 19530:19530 \
-p 19121:19121 \
-v /Users/pedrovicentevaldez/Desktop/milvus/db:/var/lib/milvus/db \
-v /Users/pedrovicentevaldez/Desktop/milvus/conf:/var/lib/milvus/conf \
-v /Users/pedrovicentevaldez/Desktop/milvus/logs:/var/lib/milvus/logs \
-v /Users/pedrovicentevaldez/Desktop/milvus/wal:/var/lib/milvus/wal \
milvusdb/milvus:1.0.0-cpu-d030521-1ea92e
```

Clicked on https://github.com/milvus-io/pymilvus/blob/1.0.1/examples/example.py in the https://milvus.io/docs/example_code.md page. The link is broken. The correct link is https://github.com/milvus-io/pymilvus/blob/master/examples/example.py or https://github.com/milvus-io/pymilvus/blob/1.0/examples/example.py
