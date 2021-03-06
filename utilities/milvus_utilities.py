import numpy as np
import os
from shutil import copyfile
from milvus import Milvus, IndexType, MetricType, Status

def create_collection(client, collection_name, embedding_dim, reset=False):
    """Creates a milvus collection.

    Args:
        client (object): milvus client.
        collection_name (str): given name for the collection to create.
        embedding_dim (int): dimensionality of the vectors to be hosted in the collection.
        reset (bool, optional): If True, the collection will be removed and re-created if it already exists. Defaults to False.

    Returns:
        None
    """    
    status, ok = client.has_collection(collection_name)
    param = {
        'collection_name': collection_name,
        'dimension': embedding_dim,
        'metric_type': MetricType.L2  # optional
    }
    if ok:
        print("Collection already exists!")
        if reset:
            print("Resetting collection...")
            status = client.drop_collection(collection_name)
            client.create_collection(param)
            print("Succesfully created collection!")
    else:
        client.create_collection(param)
        print("Succesfully created collection!")
    return None


def insert_embeddings(client, collection_name, embedding_vectors, buffer_size=256):
    """Given a milvus client, the embedding_vectors will be inserted into the given collection.

    Args:
        client (object): milvus client.
        collection_name (str): name of the collection.
        embedding_vectors (np.array): numpy array of vectors to insert into the collection.
        buffer_size (int, optional): buffer size specified in the server_config.yaml file. Defaults to 256.

    Returns:
        list: milvus ids of all inserted vectors.
    """    
    embedding_size_mb = embedding_vectors.nbytes * 1e-6
    if embedding_size_mb > buffer_size:
        chunks = np.ceil(embedding_size_mb/buffer_size)
        print("Warning: Embeddings size are above the buffer size. Will insert recursively.")
        array_chunks = np.array_split(embedding_vectors, chunks)
        
        all_ids = []
        for i in array_chunks:
            status, ids = client.insert(collection_name=collection_name, records=i)
            if not status.OK():
                print("Insert failed: {}".format(status))  
                raise
            else:
                print("Insertion succesfull.")
                all_ids.extend(ids)
    else:
        status, all_ids = client.insert(collection_name=collection_name, records=embedding_vectors)
        if not status.OK():
            print("Insert failed: {}".format(status))
            raise
        else:
            print("Insertion succesfull.")
    return all_ids


def download_nearest_files(results, inventory, path):
    """Downloads the nearest neighbor files for a given result.

    The inventory argument must be a pandas DataFrame and must at least contain two features named
    image_path and milvus_id. The former representing the path to the images in the filesystem and 
    the latter representing the assigned milvus ids.

    Args:
        results (milvus.client.abstract.TopKQueryResult): resulting object from milvus query.
        inventory (pd.DataFrame): Dataframe containing the image inventory. Read above for more information.
        path (str): Path-like string indicating directory where the files will be saved to.

    Returns:
        None
    """    
    if not os.path.isdir(path):
        os.makedirs(path)

    for i in results.id_array[0]:
        resulting_df = inventory[inventory.milvus_ids == i]
        image_path = resulting_df.image_path.values[0]
        image_name = os.path.basename(image_path)
        new_path = os.path.join(path, image_name)
        copyfile(image_path, new_path)
    return None