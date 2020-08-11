<template>
  <PollResult v-bind:poll="poll"  />
</template>

<script>
import PollResult from '~/components/PollResult'

export default {
  name: 'PollResultPage',

  components: {
    PollResult,
  },
  data() {
    return {
      poll: {},
    }
  },
  async created() {
    const config = {
      headers: {
        Accept: 'application/json',
      },
    }
    try {
      const res = await this.$axios.get(`/vote/${this.$route.params.id}`, config)
      this.poll = res.data
    } catch (error) {
      console.log(error)
    }
  },
}
</script>

