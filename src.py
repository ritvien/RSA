import random


def modular_exponentiation(base, exp, mod):
    '''
    Tính modulo của lũy thừa
    
    Parameters:
        base (int): cơ số
        exp (int): lũy thừa/số mũ
        mod (int): modulo
    
    Return:
            int: kết quả của phép tính modulo lũy thừa
    
    '''
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def miller_rabin_test(n, k=50): 
    '''
    Hàm kiểm tra số nguyên tố bằng thuật toán Miller-Rabin
    
    Parameters:
        n (int): Số cần kiểm tra tính nguyên tố
        k (int): Số lần lặp, thử lại (càng to càng chính xác)
    
    Return:
        bool: Kết quả có phải số nguyên tố không
    
    '''
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = modular_exponentiation(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = modular_exponentiation(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_large_prime(N):
    '''
    Hàm sinh số nguyên tố lớn hơn số N cho trước
    
    Parameters:
        N (int): số cho trước
    
    Return:
        int: Số nguyên tố lớn hơn N
    
    '''
    while True:
        result = random.randint(N+1, 2*N)
        if miller_rabin_test(result):
            return result


        



def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inv(a, m):
    '''
    Tính nghịch đảo modulo của a modulo m bằng thuật toán Euclide mở rộng
    
    Parameters:
        a (int): Số nguyên cần tìm nghịch đảo modulo
        m (int): Modulo
    
    Return:
        int: Nghịch đảo modulo của a modulo m
    
    '''
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def generate_rsa_keys(key_size=1024):
    '''
    Tạo cặp khóa RSA
    
    Parameters:
        key_size (int): Độ dài của khóa RSA
        
    Return:
        tuple:(int,int),tuple:(int,int) : Khóa công khai, khóa riêng
    
    '''
    p = generate_large_prime(2**(key_size//2))
    q = generate_large_prime(2**(key_size//2))
    n = p * q
    phi = (p - 1) * (q - 1)
    
    e = random.randint(2, phi - 1) 
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    
    d = mod_inv(e, phi)
    return (e, n), (d, n)

def encrypt(original_num, public_key):
    """
    Mã hóa một số nguyên bằng khóa công khai RSA

    Parameters:
        original_num (int): Số nguyên cần mã hóa
        public_key (tuple): Cặp khóa công khai RSA (e, n)

    Returns:
        int: Số nguyên đã được mã hóa
        
    """
    e, n = public_key
    return modular_exponentiation(original_num, e, n)

def decrypt(encoded_num, private_key):
    """
    Giải mã một số nguyên đã mã hóa bằng khóa riêng RSA

    Parameters:
        encoded_num (int): Số nguyên đã được mã hóa
        private_key (tuple): Cặp khóa riêng RSA (d, n)

    Returns:
        int: Số nguyên đã được giải mã

    """
    
    d, n = private_key
    return modular_exponentiation(encoded_num, d, n)
