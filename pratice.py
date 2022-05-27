import os

path1 = r"C:\Users\오나성\Desktop\Warehouse_program\uploads\sample\smartstore\sample_smartstore.xlsx"

if "smartstore" in os.path.dirname(path1):
    print("true")
else:
    print("false")
