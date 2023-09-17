pids=`jupyter notebook list | grep "localhost" | awk {'print $1'} | sed 's/[^0-9]*//g' | awk '{print substr ($0, 0, 4)}'`
for pid in ${pids}; do
  jupyter notebook stop ${pid}
done
