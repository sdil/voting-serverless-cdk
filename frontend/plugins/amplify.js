import Vue from 'vue'
import Amplify, { Auth } from 'aws-amplify';

Amplify.configure({
    Auth: {

        // REQUIRED - Amazon Cognito Region
        region: process.env.webClientId,

        // OPTIONAL - Amazon Cognito User Pool ID
        userPoolId: process.env.userPoolId,

        // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
        userPoolWebClientId: process.env.webClientId,

        // OPTIONAL - Enforce user authentication prior to accessing AWS resources or not
        mandatorySignIn: false,

        // OPTIONAL - Manually set the authentication flow type. Default is 'USER_SRP_AUTH'
        authenticationFlowType: 'USER_PASSWORD_AUTH',

        // OPTIONAL - Manually set key value pairs that can be passed to Cognito Lambda Triggers
        clientMetadata: { myCustomKey: 'myCustomValue' },

    }
});

// You can get the current config object
const currentConfig = Auth.configure();
Vue.use(Auth)