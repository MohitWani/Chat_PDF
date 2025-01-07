from langchain_community.embeddings import GPT4AllEmbeddings

#get the relevant docs by similarity search.
def get_relavant_doc(query,db):
    
    query_embedding = GPT4AllEmbeddings().embed_query(query)
    
    similar_docs = db.similarity_search_by_vector(query_embedding)

    return similar_docs