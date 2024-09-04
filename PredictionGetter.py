model1 = tf.keras.models.load_model("my_model.keras")
image_dir = "/content/people_images"

target_size = (128, 128)
for filename in os.listdir(image_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(image_dir, filename)
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0
        predictions = model1.predict(img_array)
        print(f"Prediction for {filename}: {predictions}")
