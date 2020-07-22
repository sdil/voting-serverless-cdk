<template>

  <Poll
    :id=$route.params.id
    question="sadfg"
  />

</template>

<script>
import Poll from '~/components/Poll'

export default {
  name: 'PollPage',

  components: {
    Poll
  },
  data() {
    return {
        radio: 'default'
    }
  }

}
</script>
