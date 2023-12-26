#!/bin/bash

cd test
var=1
while [ $var -le 3 ]
do
    python learner_test.py train
    # python clear_gpu_cache.py 1
    echo $var
    var=$(( var + 1 ))
done
# python clear_gpu_cache.py 1
echo "Exit Status of the previous command is $?"    # 输出上一条命令的退出状态
