<template>
  <section class="section">
    <div class="content">
      <h1>Create a poll</h1>

      <b-field horizontal label="Question">
        <b-input
          v-model="question"
          placeholder="What if cat ruled the world"
          name="question"
          expanded
        ></b-input>
      </b-field>

      <b-field horizontal label="Choice 1">
        <b-input v-model="choice1" placeholder="World revenge" name="question" expanded></b-input>
      </b-field>

      <b-field horizontal label="Choice 2">
        <b-input v-model="choice2" placeholder="Loud purr" name="question" expanded></b-input>
      </b-field>

      <b-button type="is-dark" @click="CreatePoll()">Submit</b-button>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    return {
      question: '',
      choice1: '',
      choice2: '',
      poll_id: '',
    }
  },
  methods: {
    CreatePoll() {
      const config = {
        headers: {
          Authorization: `Bearer ${this.$auth.accessToken}`,
          Accept: 'application/json'
        },
      }

      // use axios to POST data to API Server
      this.$axios
        .post(
          `/vote`,
          {
            question: this.question,
            choice1: this.choice1,
            choice2: this.choice2,
          },
          config
        )
        .then((res) => {
          console.log(res)
          this.poll_id = res.data.poll_id
        })
      this.$router.push({ name: 'index' })
    },
  },
}
</script>