import torch
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ['0', '1']:
        print("[USAGE] python clear_gpu_cache.py <gpu_id>")
        exit(1)
    
    os.environ['CUDA_VISIBLE_DEVICES'] = sys.argv[1]
    torch.cuda.empty_cache()