<template>
  <div class="content">
    <h1>Register</h1>
    <form v-if="step === steps.register">
      <b-field horizontal label="Email Address">
        <b-input v-model="registerForm.email" type="email" placeholder="user@example.com" />
      </b-field>
      <b-field horizontal label="Password">
        <b-input v-model="registerForm.password" type="password" placeholder="********" />
      </b-field>
      <b-button type="is-dark" @click="register">Register</b-button>
    </form>

    <form v-else>
      <b-field horizontal label="Email Address">
        <b-input v-model="confirmForm.email" type="email" placeholder="user@example.com" />
      </b-field>
      <b-field horizontal label="Code">
        <b-input v-model="confirmForm.code" placeholder="1234" />
      </b-field>
      <b-button type="is-dark" @click="confirm">Confirm</b-button>
    </form>

  </div>
</template>

<script>
const steps = {
  register: 'REGISTER',
  confirm: 'CONFIRM',
}

export default {
  data: () => ({
    steps: { ...steps },
    step: steps.register,
    registerForm: {
      email: '',
      password: '',
    },
    confirmForm: {
      email: '',
      code: '',
    },
  }),

  methods: {
    async register() {
      try {
        await this.$store.dispatch('auth/register', this.registerForm)
        this.confirmForm.email = this.registerForm.email;
        this.step = this.steps.confirm
      } catch (error) {
        console.log({ error })
      }
    },
    async confirm() {
        try {
            await this.$store.dispatch('auth/confirmRegistration', this.confirmForm)
            await this.$store.dispatch('auth/login', this.registerForm)
            this.$router.push('/')
        } catch (error) {
            console.log({ error })
        }
    }
  },
}
</script>