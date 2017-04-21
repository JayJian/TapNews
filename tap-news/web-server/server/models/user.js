const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

//make sure email is unique
const UserSchema = new mongoose.Schema({
  email: {
    type: String,
    index: { unique:true }
  },
  password: String
});

//write a method to verify whether the password is correct
UserSchema.methods.comparePassword = function comparePassword(password, callback){
  bcrypt.compare(password, this.password, callback);
};

//pre is a key word, provided method
UserSchema.pre('save', function saveHook(next) {
  const user = this;

  // proceed further only if the password is modified or the user is new
  if (!user.isModified('password')) return next();


  return bcrypt.genSalt((saltError, salt) => {
    if (saltError) { return next(saltError); }

    return bcrypt.hash(user.password, salt, (hashError, hash) => {
      if (hashError) { return next(hashError); }

      // replace a password string with hash value
      user.password = hash;

      return next();
    });
  });
});

module.exports = mongoose.model('User', UserSchema);
