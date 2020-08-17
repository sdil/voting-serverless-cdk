<template>
  <div class="content">
    <h1>Log In</h1>
    <form>
      <b-field horizontal label="Email Address">
        <b-input v-model="form.email" type="email" placeholder="user@example.com"/>
      </b-field>
      <b-field horizontal label="Password">
        <b-input v-model="form.password" type="password" placeholder="********"/>
      </b-field>
      <b-button type="is-dark" @click="login">Login</b-button>
    </form>
  </div>
</template>

<script>
export default {
  data: () => ({
    form: {
      email: '',
      password: ''
    }
  }),
  methods: {
    async login() {
      try {
        await this.$store.dispatch('auth/login', this.form)
        this.$router.push('/')
      } catch (error) {
        console.log({ error })
      }
    }
  }
}
</script>
