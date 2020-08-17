<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <div v-if="$auth.isAuthenticated">
          <b-button tag="router-link" to="create-poll" type="is-link" icon-left="vote">Create a poll</b-button>
        </div>
        <div v-else>
          <strong>Please login to create your own poll</strong>
        </div>

        <div v-for="poll in polls">
          <Poll :key="poll.id" v-bind:poll="poll" />
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import Poll from '~/components/Poll'

export default {
  name: 'HomePage',

  components: {
    Poll,
  },

  data() {
    return {
      polls: [],
    }
  },

  async created() {
    const config = {
      headers: {
        Accept: 'application/json',
      },
    }
    try {
      const res = await this.$axios.get('/vote', config)
      this.polls = res.data
    } catch (error) {
      console.log(error)
    }
  },
}
</script>
