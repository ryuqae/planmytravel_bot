# kill -9 `cat bot.pid`
nohup /home/jeongwoo/miniconda3/envs/telegram/bin/python /home/jeongwoo/workspace/6_CustomBot/main.py --MODEL gpt-4-1106-preview > main.log 2>&1 & echo $! > bot.pid