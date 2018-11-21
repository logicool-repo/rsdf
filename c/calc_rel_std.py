import numpy as np

def local_variation_coefficient(arr):
    c1 = np.mean(arr)
    c2 = np.mean(arr**2)
    c3 = (((c2 - c1**2)**0.5)/c1)
    return c3

def main():
    a = local_variation_coefficient(np.asarray([1,2,3,4,5,6,7,8,9],dtype=np.float32))
    print("Relative Standard Deviation = " + str(np.round(a,6)))

if __name__ == '__main__':

    main()
