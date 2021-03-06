from flask import Flask, request, render_template
import tensorflow as tf
import pickle
import os
import logging
logging.basicConfig(level=logging.DEBUG)

model_path= "C:\\Users\\nada\\Desktop\\space\\model.h5"
app= Flask(__name__)
model = tf.saved_model.LoadOptions(model_path)
logging.info("hello", model)
image_embeddings = pickle.load(open('image_embeddings.pickle', "rb"))
image_paths = pickle.load(open('image_paths.pickle', "rb"))

@app.route('/')

def home():
    return render_template("space-geeks-demo-project.html")
@app.route('/v1/predict', methods=['GET','POST'])

def predict():
    
    input = [x for x in request.form.values()]
    queries = input[0]
    logging.info("from predict", model)
    query_embedding = model(tf.convert_to_tensor([queries]))
    
    if True:
        image_embeddings = tf.math.l2_normalize(image_embeddings, axis=1)
        query_embedding = tf.math.l2_normalize(query_embedding, axis=1)
    
    dot_similarity = tf.matmul(query_embedding, image_embeddings, transpose_b=True)
    
    results = tf.math.top_k(dot_similarity, 5).indices.numpy()
    output = [[image_paths[idx] for idx in indices] for indices in results]
    logging.info("hello", output)
    return render_template('prediction.html',pred= output)

if __name__ == "__main__":
    port = os.environ.get("PORT",5000)
    app.run(debug=True, host='0.0.0.0', port=port)

#pip freeze > requirements.txt