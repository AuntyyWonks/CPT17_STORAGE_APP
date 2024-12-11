import Amplify, { Auth } from 'aws-amplify';
import awsconfig from './aws-exports';


Amplify.configure({
  Auth: {
    region: 'eu-west-1', 
    userPoolId: 'eu-west-1_JMpYjGBfK',
    userPoolWebClientId: '6fjpsk21jp56kup72u8d3cgoau',
    mandatorySignIn: true,
  },
});

// Handle form submission
document.getElementById('loginForm').addEventListener('submit', async (e) => {
  e.preventDefault(); 

  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  try {
      const user = await Auth.signIn(username, password);
      console.log('User signed in successfully:', user);

      window.location.href = 'homeconsole.html'; 
  } catch (error) {
      console.error('Error signing in:', error);
      
      if (error.code === 'UserNotFoundException') {
          document.getElementById('error-message').textContent = 'User not found';
          window.location.href = 'index.html';
      } else if (error.code === 'NotAuthorizedException') {
          document.getElementById('error-message').textContent = 'Incorrect username or password';
      
      } else {
          document.getElementById('error-message').textContent = 'An error occurred: ' + error.message;
      }
  }
});
