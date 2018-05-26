#! /bin/bash
 
declare -a doors
#申明一个数组， -a 表示数组
for((i=1; i <= 100; i++)); do
    doors[$i]=0
done
#这段是生成100个0， 可用echo $((doors[$i]))来查看，且注意必须使用doors[$i] 而不是i ，(())而不是()

for((i=1; i <= 100; i++)); do
    for((j=i; j <= 100; j += i)); do
	echo $i $j
	doors[$j]=$(( doors[j] ^ 1 ))
    done
done
#此段是核心，echo $i $j 分别表示第i次过们的时候，第j个门， doors[$j]表示当前门的状态
#这儿这个 doors[j] ^ 1 还不懂为什么能表示门的状态， ^ 这个到底是啥运算符？？？ 正则？感觉不像啊

for((i=1; i <= 100; i++)); do
    if [[ ${doors[$i]} -eq 0 ]]; then
	op="closed"
    else
	op="open"
    fi
    echo $i $op
done
#做得好看一点
