var bodyParser = require('body-parser');
var cors = require('cors');
var express = require('express');
var path = require('path');
var passport = require('passport');
var mongoose = require('mongoose');

var auth = require('./routes/auth');
var index = require('./routes/index');
var news = require('./routes/news');


var app = express();

var config = require('./config/config.json');
require('./models/main.js').connect(config.mongoDbUri);

// view engine setup
app.set('views', path.join(__dirname, '../client/build/'));
app.set('view engine', 'jade');
app.use('/static', express.static(path.join(__dirname, '../client/build/static/')));

//client and server run in differet port would occur the problem
// app.all("*", function(req,res,next){
//   res.header("Access-Control-Allow-Origin", "*");
//   res.header("Access-Control-Allow-Headers", "X-Requested-With");
//   next();
// });
//deal with the cross origin
app.use(cors());
app.use(bodyParser.json());

app.use(passport.initialize());
var localSignupStrategy = require('./passport/signup_passport');
var localLoginStrategy = require('./passport/login_passport');
passport.use('local-signup', localSignupStrategy);
passport.use('local-login', localLoginStrategy);

// pass the authenticaion checker middleware
const authCheckMiddleware = require('./middleware/auth_checker');
//once go through the check then you can direct to /news
app.use('/news', authCheckMiddleware);

app.use('/', index);
app.use('/auth',auth);
app.use('/news', news);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  var err = new Error('Not Found');
  err.status = 404;
  res.render('404 Not Found');
});


module.exports = app;
