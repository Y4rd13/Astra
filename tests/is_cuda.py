import torch

print(torch.cuda.is_available())
print("cuda" if torch.cuda.is_available() else "cpu")