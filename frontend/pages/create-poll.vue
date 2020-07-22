<template>
  <section class="section">
    <div class="content">
      <h1>Create a poll</h1>

      <b-field horizontal label="Question">
        <b-input placeholder="What if cat ruled the world" name="question" expanded></b-input>
      </b-field>

      <b-field horizontal label="Choice 1">
        <b-input placeholder="World revenge" name="question" expanded></b-input>
      </b-field>

      <b-field horizontal label="Choice 2">
        <b-input placeholder="Loud purr" name="question" expanded></b-input>
      </b-field>

      <b-button type="is-dark" @click="SubmitPoll()">Submit</b-button>
    </div>
  </section>
</template>

<script>
export default {
  methods: {
      SubmitPoll() {
          this.$router.push("/")
      }
  },
}
</script>