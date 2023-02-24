import io
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
import json

#model building
model = models.densenet121(pretrained=True)
model.eval()

#imagenet
imagenet_class_index = json.load(open('./static/imagenet_class_index.json'))

def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)


def get_prediction(image_bytes):
    tensor = transform_image(image_bytes=image_bytes)
    outputs = model.forward(tensor)
    _, y_hat = outputs.max(1)
    predicted_idx = str(y_hat.item())
    return imagenet_class_index[predicted_idx]  

def get_result(image_file):
    image_bytes = image_file.read()
    print(image_bytes)
    class_id, class_name = get_prediction(image_bytes=image_bytes)
    return {class_id, class_name}