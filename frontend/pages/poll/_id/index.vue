<template>
  <Poll v-bind:poll="poll" />
</template>

<script>
import Poll from '~/components/Poll'

export default {
  name: 'PollPage',

  components: {
    Poll,
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
