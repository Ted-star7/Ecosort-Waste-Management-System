"""
Part 2 - Waste Material Classification with CNN (transfer learning)  [Owner: Dennis]

Base model: MobileNetV2 (light, fast, strong ImageNet features -> good for a
small 9-class dataset). Swap for EfficientNetB0 by changing BASE below.

Exposes predict_image(path) -> category, the interface Part 5 (integration) calls.
"""
import os
import numpy as np
from . import config as C

BASE = "MobileNetV2"   # or "EfficientNetB0"


def build_model(num_classes=C.NUM_CLASSES, img_size=C.IMG_SIZE, dropout=0.3,
                dense_units=256, fine_tune=False):
    import tensorflow as tf
    from tensorflow.keras import layers, models
    if BASE == "MobileNetV2":
        base = tf.keras.applications.MobileNetV2(
            input_shape=img_size + (3,), include_top=False, weights="imagenet")
        preprocess = tf.keras.applications.mobilenet_v2.preprocess_input
    else:
        base = tf.keras.applications.EfficientNetB0(
            input_shape=img_size + (3,), include_top=False, weights="imagenet")
        preprocess = tf.keras.applications.efficientnet.preprocess_input
    base.trainable = fine_tune   # freeze for stage 1, unfreeze top for stage 2

    # light on-the-fly augmentation helps with the class imbalance + small data
    aug = models.Sequential([
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.1),
        layers.RandomZoom(0.1),
    ], name="augment")

    inputs = tf.keras.Input(shape=img_size + (3,))
    x = aug(inputs)
    x = preprocess(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(dropout)(x)
    x = layers.Dense(dense_units, activation="relu")(x)
    x = layers.Dropout(dropout)(x)
    outputs = layers.Dense(num_classes, activation="softmax")(x)

    model = models.Model(inputs, outputs, name=f"{BASE}_waste_cnn")
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-3),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    return model, base


def compute_class_weights(train_ds):
    """Handle class imbalance (Plastic 921 vs Textile Trash 318)."""
    import tensorflow as tf
    from sklearn.utils.class_weight import compute_class_weight
    y = np.concatenate([y.numpy() for _, y in train_ds])
    cw = compute_class_weight("balanced", classes=np.arange(C.NUM_CLASSES), y=y)
    return dict(enumerate(cw))


def train(train_ds, val_ds, epochs=12, fine_tune_epochs=5, class_weight=None):
    import tensorflow as tf
    model, base = build_model()
    cbs = [tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
           tf.keras.callbacks.ReduceLROnPlateau(patience=2, factor=0.3)]
    hist1 = model.fit(train_ds, validation_data=val_ds, epochs=epochs,
                      class_weight=class_weight, callbacks=cbs)
    # Stage 2: unfreeze top of base and fine-tune at low LR
    base.trainable = True
    for layer in base.layers[:-30]:
        layer.trainable = False
    model.compile(optimizer=tf.keras.optimizers.Adam(1e-5),
                  loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    hist2 = model.fit(train_ds, validation_data=val_ds, epochs=fine_tune_epochs,
                      class_weight=class_weight, callbacks=cbs)
    os.makedirs(C.MODELS_DIR, exist_ok=True)
    model.save(C.CNN_MODEL_PATH)
    return model, (hist1, hist2)


def evaluate(model, test_ds):
    """Return (accuracy, confusion_matrix, classification_report_str)."""
    import tensorflow as tf
    from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
    y_true, y_pred = [], []
    for xb, yb in test_ds:
        p = model.predict(xb, verbose=0)
        y_pred.extend(p.argmax(1)); y_true.extend(yb.numpy())
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=range(C.NUM_CLASSES))
    rep = classification_report(y_true, y_pred, target_names=C.CATEGORIES)
    return acc, cm, rep


_model = None
def predict_image(image_path):
    """INTEGRATION INTERFACE (Part 5). Load saved model lazily, return category str."""
    global _model
    import tensorflow as tf
    if _model is None:
        _model = tf.keras.models.load_model(C.CNN_MODEL_PATH)
    img = tf.keras.utils.load_img(image_path, target_size=C.IMG_SIZE)
    arr = tf.keras.utils.img_to_array(img)[None, ...]
    idx = int(_model.predict(arr, verbose=0).argmax(1)[0])
    return C.IDX_TO_CAT[idx]
