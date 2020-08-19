import { CognitoRefreshToken } from 'amazon-cognito-identity-js';
import { Auth, loadingBar } from 'aws-amplify';

export const state = () => ({
    isAuthenticated: false,
    user: null
})

export const mutations = {
    set(state, user) {
        state.isAuthenticated = !!user;
        state.user = user;
    }
}

export const actions = {
    async load({ dispatch }) {
        await dispatch('fetchUser')
    },
    async fetchUser({commit, dispatch}) {
        // This will fetch the user details and store it in `user` state
        // This will fetch the user again after the token expires

        try {
            const user = await Auth.currentAuthenticatedUser()
            const expires = user.getSignInUserSession().getIdToken().payload.exp - Math.floor(new Date().getTime() / 1000)
            console.log(`Token expires in ${expires} seconds`)
            setTimeout(async () => {
                console.log('Renewing Token')
                await dispatch('fetchUser')
            }, expires * 1000)
            commit('set', user)
        } catch (err) {
            console.log("no user logged in")
            commit('user', null)
        }
    },
    async register(_, { email, password }) {
        const user = await Auth.signUp({
            username: email,
            password,
            attributes: {
                email: email
            }
        })
        return user
    },
    async confirmRegistration(_, { email, code }) {
        return await Auth.confirmSignUp(email, code);
    },

    async login({ dispatch }, { email, password }) {
        const user = await Auth.signIn(email, password)
        await dispatch('fetchUser')
        return user
    },

    async logout({ commit }) {
        await Auth.signOut()
        commit('set', null)
    }
}