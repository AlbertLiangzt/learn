执行顺序
cat a.txt | python map_a.py > a.result
cat b.txt | python map_b.py > b.result

cat a.result b.result | python map_join.py | sort -k1,1 -k2,2 > join.result

cat join.result | python reduce.py > reduce.result
