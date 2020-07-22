<template>
  <section class="section">
    <div class="columns is-mobile">
      <div class="content">
        <b-button tag="router-link" to="create-poll" type="is-link" icon-left="vote">Create a poll</b-button>

        <Poll key="1" id="1" question="What is that?" />

        <Poll key="2" id="2" question="Where is that?" />
      </div>
    </div>
  </section>
</template>

<script>
import Poll from '~/components/Poll'

export default {
  name: 'HomePage',

  components: {
    Poll
  },
  

}
</script>
