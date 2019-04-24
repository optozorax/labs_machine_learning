from tensorflow.keras.models import model_from_json
import pickle

datadir = "D:/My/programs/labs_machine_learning/"

NAME = "(3x3).128x3-Conv"

#-----------------------------------------------------------------------------
# Загружаем тестовые данные
X_test = pickle.load(open(datadir + "/common/X_test.pickle", "rb"))
y_test = pickle.load(open(datadir + "/common/y_test.pickle", "rb"))

test_data = (X_test, y_test)

# load json and create model
json_file = open(datadir + f'/ilya/models/{NAME}.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(datadir + f"/ilya/models/{NAME}.h5")


print("Loaded model from disk")

# evaluate loaded model on test data
loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
score = loaded_model.evaluate(X_test, y_test, batch_size=8, verbose=0)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))