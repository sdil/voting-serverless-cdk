<template>
  <div>
    <b-navbar>
      <template slot="brand">
        <b-navbar-item tag="router-link" :to="{ path: '/' }">
          <b>Voting Serverless App</b>
        </b-navbar-item>
      </template>

      <template slot="start">
        <!-- We cannot use nuxt-link here, it caues a Hydration issue
        use tag `tag="router-link" :to="{ path: '/' }` for linking here-->

        <b-navbar-item tag="router-link" :to="{ path: '/' }">Home</b-navbar-item>
        <b-navbar-item href="#">About</b-navbar-item>
        <b-navbar-item href="https://github.com/sdil/voting-serverless-cdk">Github Repo</b-navbar-item>
      </template>

      <template slot="end">
        <b-navbar-item tag="div">
          <div v-if="$auth.isAuthenticated">
            <button class="button is-primary" @click="$store.dispatch('auth/logout')">Logout</button>
          </div>
          <div v-else>
            <div class="buttons">
              <nuxt-link class="button is-primary" to="/register">
                <strong>Register</strong>
              </nuxt-link>
              <nuxt-link class="button is-light" to="/login">Log in</nuxt-link>
            </div>
          </div>
        </b-navbar-item>
      </template>
    </b-navbar>

    <div class="container column is-10">
      <nuxt />
    </div>
  </div>
</template>

<script>
export default {}
</script>
