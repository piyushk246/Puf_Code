import math

def row_col_decoder(a):
    b = math.log2(a)
    x = (b + a) / 2   
    y = a - x         
    print("Rounded x:", round(x))
    print("Rounded y:", round(y))
    # return  round(x),round(y) 

# Example usage
a = 32
x,y = row_col_decoder(a)
print(x,y)
