//its a help class to provide some services
class Auth{
  //authenticate a user, save the token and email in localStorage
  static authenticateUser(token, email){
    localStorage.setItem('token', token);
    localStorage.setItem('email', email);
  }

  //method to check whether the user is authenticated
  static isUserAuthenticated(){
    return localStorage.getItem('token') !== null;
  }

  //deauthenticate a user by removing token and email from localStorage
  static deauthenticate(){
    localStorage.removeItem('token');
    localStorage.removeItem('email');
  }

  //get a token value
  static getToken(){
    return localStorage.getItem('token');
  }

  static getEmail(){
    return localStorage.getItem('email');
  }
}

export default Auth;
