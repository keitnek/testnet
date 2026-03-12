import random

def generate_number():
    """Tạo số ngẫu nhiên từ 01 đến 99"""
    return str(random.randint(1, 99)).zfill(2)
