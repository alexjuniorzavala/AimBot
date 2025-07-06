import os

# Criar estrutura de diretórios
def criar_estrutura_yolo():
    base_dir = "D:/Alex/Projetos Python/yolov5"
    dirs = [
        "data/images/train",
        "data/images/val",
        "data/labels/train",
        "data/labels/val"
    ]
    
    for dir_path in dirs:
        path = os.path.join(base_dir, dir_path)
        os.makedirs(path, exist_ok=True)
        print(f"Diretório criado: {path}")

# Criar arquivo data.yaml
def criar_data_yaml():
    yaml_content = """
train: data/images/train
val: data/images/val

# número de classes
nc: 1

# nomes das classes
names: ['target']
"""
    
    with open("D:/Alex/Projetos Python/yolov5/data/data.yaml", "w") as f:
        f.write(yaml_content)
    print("Arquivo data.yaml criado")

if __name__ == "__main__":
    criar_estrutura_yolo()
    criar_data_yaml() 