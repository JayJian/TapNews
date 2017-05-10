# TapNews
(Development use only)

(client) install create-react-app

(client) install materialize

(server) install express-generator

(server) install nodemon

(client) install lodash : debounce

(backend-server) sudo intstall python-jsonrpc : rpc server

(server) install jayson : rpc client

install MongoDB

(backend-server) install pymongo

(backend-server) install pika

(client) create client/src/Auth

(client) create client/src/Base

(client) create client/src/Login and client/src/SignUp

(client) install react-router@"<4.0.0" : version 4.0.0 has big change so that we use one version earlier

(client) we used configueration-styled router not component-styled router

(server) install cors

(server) install mongoose

(server) install bcrypt

(server) create schema and model for mongoose

(server) config mongoDB connection

(server) install passport

(server) install passport-local: a passport strategy

(server) install jsonwebtoken

(server) create passport local strategies for login and signup

(server) create auth-checker middleware to guard route on '/news'

(server) initialize passport and setup auth-checker in app.js

(server) create route middleware auth.js to handle logic of '/auth'

(py-utils) install requests

(py-utils) install redis

(news-pipline) create news monitor

(news-pipline) install newspaper

sudo apt-get install python-dev
sudo apt-get install libxml2-dev libxslt-dev -y
sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev -y
sudo pip install newspaper
curl https://raw.githubusercontent.com/codelucas/newspaper/master/download_corpora.py | python2.7
(news-pipline) create news scraper

(news-pipline) install NumPy, SciPy, scikit-learn, dateutil

(news-pipline) create news deduper

(backend-server) create rpc server util to handle pagination, modify NewsPanel.js @ client, news.js routes and rpc-client.js @ server to handle pagination.

(recommend-service) create recommend_service:

(client) NewsCard.js listen to click, restful post to node server
(server) add log transfer in news.js routes, call rpc-client logNewsClick
(backend-server) rpc-server call rpc-server-util and send log rpc request to rabbitmq
click log processor receive rabbitmq, handle time decay model by click
create a new rpc server: recommend-server at port 5050
create a new rpc client: recommend-client in py-util
recommend-client expose service for other user to get a user's preference model
install jupyter via dockerfile

sudo docker build . -t siyuanli/cs503_tensorflow_jupyter
sudo docker login
sudo docker push siyuanli/cs503_tensorflow_jupyter
run jupyter

docker run -it --rm -p 8888:8888 siyuanli/cs503_tensorflow_jupyter
upload tensorflow.ipynb, go through the tutorial to learn tensorflow

create news classifier service

install tensorflow and pandas
create news cnn model to setup convolution steps, one hot word processing, loss function, training process
create classifier trainer to setup vocabulary processor, estimator, fit, prediction and accuracy calculation
import all news training and testing data in labeled_news.csv
expose the news classifier service as a rpc server

create function to load trained model and vocabulary processor
install watchdog to monitor cnn model change. working as a hot starter, meaning that once new training model updated, this watchdog could update the current loaded trained model and vocabulary processor correspondingly. Notice that once model and vocabulary processor are trained with new data, the state(information) in the classifier object and the vocab_processor object are still using the outdated state. Hence, manual update needed
create a classifier service rpc client in py_utils

update news_scraper with classifier function before store a new news into database

To start either client or server by itself: npm start
In script section of client/package.json. Except npm start, all other command need to do it with run, for example: npm run build to build the react project.
All python file or folder should be named in _ style but NOT - style. Since the import not work with -
