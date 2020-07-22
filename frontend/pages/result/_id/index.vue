<template>
  <PollResult :id=$route.params.id question="sadfg"  />
</template>

<script>
import PollResult from '~/components/PollResult'

export default {
  name: 'PollResultPage',

  components: {
    PollResult
  },
  data() {
    return {
        radio: 'default'
    }
  }

}
</script>
