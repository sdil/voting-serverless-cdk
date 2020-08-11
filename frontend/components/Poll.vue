<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <nuxt-link :to="'/poll/' + poll.id">
          <h2 class="is-medium">{{ poll.question }}</h2>
        </nuxt-link>

        <div class="field" v-for="(result, answer) in poll.result">
          <b-radio v-model="picked" v-bind:native-value="answer">{{ answer }}</b-radio>
        </div>

        <b-button type="is-dark" @click="SubmitVote()">Submit</b-button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    poll: {
      type: Object,
      required: true,
    },
  },
  methods: {
    SubmitVote() {
      // use axios to POST data to API Server
      this.$axios.post(`/vote/${this.$route.params.id}`, {
        poll: this.$route.params.id,
        answer: this.picked
      })
      this.$router.push({ name: 'result-id', params: { id: this.poll.id } })
    },
  },
  data() {
    return {
      picked: '',
    }
  },
}
</script>