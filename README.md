# Installing Milvus

On Mac, it is unsupported to make directories in the `/home` folder. I changed it to a personally made folder in `/Users/pedrovicentevaldez/Desktop/milvus`. Additionally, I had to change docker preferences to allow for 4gb of memory access. 

The docker run options used in the above command are defined as follows:
- `-d`: Runs container in the background and prints container ID.
- `--name`: Assigns a name to the container.
- `-p`: Publishes a container’s port(s) to the host.
- `-v`: Mounts the directory into the container.

imagenet_vectors url: https://storage.googleapis.com/milvus_image_retrieval/imagenet_vectors.csv
imagnet data url: https://storage.googleapis.com/milvus_image_retrieval/data.zip


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


# Bugs in Webpage

1. The example code link in the Hello Milvus markdown page (https://milvus.io/docs/example_code.md) is broken. 

```
If you cannot use wget to download the example code, you can also create example.py and copy the example code.
```

The hyperlink is https://github.com/milvus-io/pymilvus/blob/1.0.1/examples/example.py. The correct link should be https://github.com/milvus-io/pymilvus/blob/master/examples/example.py or https://github.com/milvus-io/pymilvus/blob/1.0/examples/example.py if you care about a specific version.



Clicked on https://zilliz.com/sizing-tool/ in the blue box at https://milvus.io/docs/v1.0.0/connect_milvus_python.md. Got a 404 Not Found error.