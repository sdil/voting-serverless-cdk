<template>
  <div>
    <b-navbar>
      <template slot="brand">
        <b-navbar-item>
          <nuxt-link to="/">
            <b>Voting Serverless App</b>
          </nuxt-link>
        </b-navbar-item>
      </template>
      <template slot="start">
        <b-navbar-item>
          <nuxt-link to="/">Home</nuxt-link>
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
