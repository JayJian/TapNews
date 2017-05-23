#!/bin/bash
service redis_6379 start
service mongod start

cd news-recommendation-service
python recommendation_service.py &
python click_log_processor.py &

cd ../backend-server
python service.py &

cd ../web-server/client
npm run build &

cd ../server
pm2 start npm -- start --watch

echo "=================================================="
read -p "PRESS [ENTER] TO TERMINATE PROCESSES." PRESSKEY

killall -r node
killall -r python
