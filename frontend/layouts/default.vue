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
        <b-navbar-item tag="router-link" :to="{ path: '/' }">
          Home
        </b-navbar-item>
        <b-navbar-item href="#">API Doc</b-navbar-item>
        <b-navbar-dropdown label="Info">
          <b-navbar-item href="#">About</b-navbar-item>
          <b-navbar-item href="https://github.com/sdil/voting-serverless-cdk">Github Repository</b-navbar-item>
        </b-navbar-dropdown>
      </template>

      <template slot="end">
        <b-navbar-item tag="div">
          <div class="buttons">
            <a class="button is-primary">
              <strong>Sign up</strong>
            </a>
            <a class="button is-light">Log in</a>
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
export default {
  data () {
    return {
    }
  }
}
</script>
